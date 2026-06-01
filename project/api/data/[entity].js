const { createClient } = require("@supabase/supabase-js");

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

function toLabel(tableName) {
  return tableName
    .replace(/_/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

module.exports = async function handler(req, res) {
  if (req.method !== "GET") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { entity } = req.query;

  try {
    // Validate table exists
    const { data: tables, error: tableError } = await supabase.rpc("get_public_tables");
    if (tableError) throw tableError;

    const exists = (tables ?? []).some((r) => r.table_name === entity);
    if (!exists) {
      return res.status(404).json({ error: `Unknown entity: "${entity}"` });
    }

    // Get columns in order
    const { data: cols, error: colError } = await supabase.rpc("get_table_columns", { target_table: entity });
    if (colError) throw colError;

    const columns = (cols ?? []).map((r) => r.column_name);

    // Fetch rows
    const { data, error: dataError } = await supabase
      .from(entity)
      .select("*")
      .order("id", { ascending: true });

    if (dataError) throw dataError;

    return res.status(200).json({
      label:   toLabel(entity),
      table:   entity,
      columns,
      rows:    data ?? [],
    });
  } catch (err) {
    console.error(`[/api/data/${entity}]`, err);
    return res.status(500).json({ error: err.message || "Internal server error" });
  }
};