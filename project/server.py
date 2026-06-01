from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from database.supabase_client import get_supabase_client
from sync.registry import ENTITY_SYNC_CONFIGS
from sync.service import run_full_sync

WEB_DIR = Path(__file__).parent / "web"

ENTITY_LABELS = {
    "accounts": "Account",
    "bills": "Bill",
    "company_info": "Company Info",
    "customers": "Customer",
    "employees": "Employee",
    "estimates": "Estimate",
    "invoices": "Invoice",
    "items": "Item",
    "payments": "Payment",
    "preferences": "Preferences",
    "profit_and_loss": "Profit & Loss",
    "tax_agencies": "Tax Agency",
    "vendors": "Vendor",
}

HIDDEN_COLUMNS = {"raw_data", "synced_at"}


def get_entity_config(name: str):
    for config in ENTITY_SYNC_CONFIGS:
        if config.name == name:
            return config
    return None


app = Flask(__name__)


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/entities")
def list_entities():
    entities = []
    supabase_client = get_supabase_client()

    for config in ENTITY_SYNC_CONFIGS:
        count = 0
        try:
            response = (
                supabase_client.table(config.table)
                .select("*", count="exact")
                .limit(1)
                .execute()
            )
            count = response.count or 0
        except Exception:
            count = 0

        entities.append({
            "name": config.name,
            "label": ENTITY_LABELS.get(config.name, config.name),
            "table": config.table,
            "count": count,
        })

    return jsonify({"entities": entities})


@app.get("/api/data/<entity_name>")
def get_entity_data(entity_name):
    config = get_entity_config(entity_name)
    if not config:
        return jsonify({"error": f"Unknown entity: {entity_name}"}), 404

    limit = min(int(request.args.get("limit", 500)), 1000)
    supabase_client = get_supabase_client()

    order_column = (
        "generated_at"
        if config.conflict_column == "report_key"
        else "qbo_updated_at"
    )

    try:
        response = (
            supabase_client.table(config.table)
            .select("*")
            .order(order_column, desc=True)
            .limit(limit)
            .execute()
        )
    except Exception:
        response = (
            supabase_client.table(config.table)
            .select("*")
            .limit(limit)
            .execute()
        )

    rows = response.data or []
    columns = []
    if rows:
        columns = [
            column
            for column in rows[0].keys()
            if column not in HIDDEN_COLUMNS
        ]

    return jsonify({
        "entity": entity_name,
        "label": ENTITY_LABELS.get(entity_name, entity_name),
        "table": config.table,
        "columns": columns,
        "rows": rows,
        "count": len(rows),
    })


@app.post("/api/refresh")
def refresh_data():
    try:
        results = run_full_sync()
        errors = [item for item in results if item["status"] == "error"]
        return jsonify({
            "status": "ok" if not errors else "partial",
            "results": results,
            "message": "Data refreshed from QuickBooks to Supabase.",
        })
    except Exception as error:
        return jsonify({
            "status": "error",
            "message": str(error),
        }), 500


# Local development only — on Vercel, static files are served from public/
@app.get("/")
def index():
    return send_from_directory(WEB_DIR, "index.html")


@app.get("/<path:filename>")
def static_files(filename):
    if filename.startswith("api/"):
        return jsonify({"error": "Not found"}), 404

    if (WEB_DIR / filename).exists():
        return send_from_directory(WEB_DIR, filename)
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
