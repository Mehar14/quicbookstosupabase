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

  const { entity } = req.query;
  console.log("[data] entity:", entity);

  if (!entity) {
    return res.status(400).json({ error: "Missing entity query parameter" });
  }

  try {
    // Step 1: get all tables
    const { data: tables, error: tableError } = await supabase.rpc("get_public_tables");
    console.log("[data] tables:", JSON.stringify(tables), "error:", tableError);
    if (tableError) throw tableError;

    // Step 2: find matching table by stripped name
    const match = (tables ?? []).find((r) => stripPrefix(r.table_name) === entity);
    console.log("[data] match:", match);
    if (!match) {
      return res.status(404).json({ error: `Unknown entity: "${entity}"` });
    }

    const realTable = match.table_name;

    // Step 3: get columns
    const { data: cols, error: colError } = await supabase.rpc("get_table_columns", { target_table: realTable });
    console.log("[data] columns:", JSON.stringify(cols), "error:", colError);
    if (colError) throw colError;

    const columns = (cols ?? []).map((r) => r.column_name);

    // Step 4: fetch rows
    const { data, error: dataError } = await supabase
      .from(realTable)
      .select("*")
      .order("qbo_id", { ascending: true });
    console.log("[data] rows:", data?.length ?? 0, "error:", dataError);
    if (dataError) throw dataError;

    return res.status(200).json({
      label:   toLabel(realTable),
      table:   realTable,
      columns,
      rows:    data ?? [],
    });
  } catch (err) {
    console.error("[/api/data] CAUGHT ERROR:", err.message);
    return res.status(500).json({ error: err.message || "Internal server error" });
  }
};