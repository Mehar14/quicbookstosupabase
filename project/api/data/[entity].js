const { createClient } = require("@supabase/supabase-js");

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
);

function stripPrefix(tableName) {
  return tableName.replace(/^qbo_/, "");
}

function toLabel(tableName) {
  return stripPrefix(tableName)
    .replace(/_/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

module.exports = async function handler(req, res) {
  if (req.method !== "GET") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { entity } = req.query; // e.g. "accounts"

  try {
    // Get all tables and find the one whose stripped name matches
    const { data: tables, error: tableError } = await supabase.rpc("get_public_tables");
    if (tableError) throw tableError;

    const match = (tables ?? []).find((r) => stripPrefix(r.table_name) === entity);
    if (!match) {
      return res.status(404).json({ error: `Unknown entity: "${entity}"` });
    }

    const realTable = match.table_name; // e.g. "qbo_accounts"

    // Get columns in order
    const { data: cols, error: colError } = await supabase.rpc("get_table_columns", { target_table: realTable });
    if (colError) throw colError;

    const columns = (cols ?? []).map((r) => r.column_name);

    // Fetch rows from the real table name
    const { data, error: dataError } = await supabase
      .from(realTable)
      .select("*")
      .order("id", { ascending: true });

    if (dataError) throw dataError;

    return res.status(200).json({
      label:   toLabel(realTable),
      table:   realTable,
      columns,
      rows:    data ?? [],
    });
  } catch (err) {
    console.error(`[/api/data/${entity}]`, err);
    return res.status(500).json({ error: err.message || "Internal server error" });
  }
};