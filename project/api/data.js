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

  if (!entity) {
    return res.status(400).json({ error: "Missing entity query parameter" });
  }

  try {
    // Step 1: get all tables
    const { data: tables, error: tableError } = await supabase.rpc("get_public_tables");
    if (tableError) throw tableError;

    // Step 2: find matching table by stripped name
    const match = (tables ?? []).find((r) => stripPrefix(r.table_name) === entity);
    if (!match) {
      return res.status(404).json({ error: `Unknown entity: "${entity}"` });
    }

    const realTable = match.table_name;

    // Step 3: get columns and primary key in parallel
    const [colsRes, pkRes] = await Promise.all([
      supabase.rpc("get_table_columns", { target_table: realTable }),
      supabase.rpc("get_table_primary_key", { target_table: realTable }),
    ]);

    if (colsRes.error) throw colsRes.error;
    if (pkRes.error) throw pkRes.error;

    const columns  = (colsRes.data ?? []).map((r) => r.column_name);
    const orderCol = pkRes.data || columns[0]; // fall back to first column if no PK
    console.log("[data] ordering by primary key:", orderCol);

    // Step 4: fetch rows ordered by primary key
    const { data, error: dataError } = await supabase
      .from(realTable)
      .select("*")
      .order(orderCol, { ascending: true });

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