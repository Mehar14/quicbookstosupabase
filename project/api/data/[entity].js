const { createClient } = require("@supabase/supabase-js");

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
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
    const { data: tables, error: schemaError } = await supabase
      .from("information_schema.tables")
      .select("table_name")
      .eq("table_schema", "public")
      .eq("table_type", "BASE TABLE")
      .eq("table_name", entity)
      .single();

    if (schemaError || !tables) {
      return res.status(404).json({ error: `Unknown entity: "${entity}"` });
    }

    const { data: columnRows, error: colError } = await supabase
      .from("information_schema.columns")
      .select("column_name, ordinal_position")
      .eq("table_schema", "public")
      .eq("table_name", entity)
      .order("ordinal_position");

    if (colError) throw colError;

    const columns = (columnRows ?? []).map((r) => r.column_name);

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