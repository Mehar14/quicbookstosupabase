import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

function toLabel(tableName) {
  return tableName
    .replace(/_/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

export default async function handler(req, res) {
  if (req.method !== "GET") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    // Auto-discover all tables in the public schema
    const { data: tables, error } = await supabase
      .from("information_schema.tables")
      .select("table_name")
      .eq("table_schema", "public")
      .eq("table_type", "BASE TABLE")
      .order("table_name");

    if (error) throw error;

    // Fetch row count for each table in parallel
    const entities = await Promise.all(
      (tables ?? []).map(async ({ table_name }) => {
        const { count } = await supabase
          .from(table_name)
          .select("*", { count: "exact", head: true });

        return {
          name:  table_name,
          label: toLabel(table_name),
          table: table_name,
          count: count ?? 0,
        };
      })
    );

    return res.status(200).json({ entities });
  } catch (err) {
    console.error("[/api/entities]", err);
    return res.status(500).json({ error: err.message || "Internal server error" });
  }
}