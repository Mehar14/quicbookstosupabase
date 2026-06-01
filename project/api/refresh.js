import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// ---------------------------------------------------------------------------
// Optional: if you have a QuickBooks sync Edge Function deployed in Supabase,
// set SUPABASE_SYNC_FUNCTION_NAME in your Vercel env vars to its function name
// and this endpoint will invoke it automatically on refresh.
// Leave it unset to skip the sync step (data will still reload from Supabase).
// ---------------------------------------------------------------------------
const SYNC_FUNCTION = process.env.SUPABASE_SYNC_FUNCTION_NAME;

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    if (SYNC_FUNCTION) {
      // Invoke the Supabase Edge Function that pulls fresh data from QuickBooks.
      const { error } = await supabase.functions.invoke(SYNC_FUNCTION);
      if (error) {
        console.warn("[/api/refresh] Sync function error:", error.message);
        // Return a soft error — the UI will show a warning toast but not crash.
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
}