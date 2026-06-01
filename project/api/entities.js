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

  try {
    const { data: tables, error } = await supabase.rpc("get_public_tables");

    if (error) throw error;

    const entities = await Promise.all(
      (tables ?? []).map(async ({ table_name }) => {
        const { count } = await supabase
          .from(table_name)
          .select("*", { count: "exact", head: true });

        return {
          name:  stripPrefix(table_name), // "accounts" not "qbo_accounts"
          label: toLabel(table_name),      // "Accounts"
          table: table_name,               // "qbo_accounts" — actual Supabase table
          count: count ?? 0,
        };
      })
    );

    return res.status(200).json({ entities });
  } catch (err) {
    console.error("[/api/entities]", err);
    return res.status(500).json({ error: err.message || "Internal server error" });
  }
};