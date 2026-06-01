const { createClient } = require("@supabase/supabase-js");

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
);

const SYNC_FUNCTION = process.env.SUPABASE_SYNC_FUNCTION_NAME;

module.exports = async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    if (SYNC_FUNCTION) {
      const { error } = await supabase.functions.invoke(SYNC_FUNCTION);
      if (error) {
        return res.status(200).json({
          status: "error",
          message: `Sync encountered an issue: ${error.message}`,
        });
      }
    }

    return res.status(200).json({
      status: "ok",
      message: SYNC_FUNCTION
        ? "QuickBooks data synced and reloaded successfully."
        : "Data reloaded from Supabase.",
    });
  } catch (err) {
    console.error("[/api/refresh]", err);
    return res.status(500).json({ error: err.message || "Internal server error" });
  }
};