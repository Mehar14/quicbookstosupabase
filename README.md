# QuickBooks → Supabase Data Pipeline

A full-stack data synchronization pipeline that extracts business data from QuickBooks Online Sandbox, stores it in Supabase PostgreSQL, and exposes the data through a web dashboard.

## Live Demo

🌐 **Vercel Deployment:** https://quicbookstosupabase.vercel.app/

📺 **Demo Video:** https://www.youtube.com/watch?v=M7j2DeOMzaE

[![Watch the demo](https://img.youtube.com/vi/M7j2DeOMzaE/maxresdefault.jpg)](https://www.youtube.com/watch?v=M7j2DeOMzaE)

---

## Features

* QuickBooks Online Sandbox Integration
* Automated Data Synchronization
* Supabase PostgreSQL Storage
* Web Dashboard for Data Exploration

### Supported QuickBooks Entities

* Account
* Bill
* CompanyInfo
* Customer
* Employee
* Estimate
* Invoice
* Item
* Payment
* Preferences
* ProfitAndLoss
* TaxAgency
* Vendor

---

## Architecture

```text
QuickBooks Online Sandbox
            │
            ▼
      Sync Pipeline
            │
            ▼
      Supabase PostgreSQL
            │
            ▼
       Flask Backend
            │
            ▼
       Web Dashboard
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd project
```

### 2. Configure Environment Variables

Create a `.env` file in the project root.

```bash
cp .env.example .env
```

Populate the file with the required credentials:

```env
# QuickBooks Configuration
QBO_CLIENT_ID=
QBO_CLIENT_SECRET=
QBO_REALM_ID=
QBO_REFRESH_TOKEN=

# Supabase Configuration
SUPABASE_URL=
SUPABASE__KEY=

```

### 3. Install Dependencies

```bash
.venv/bin/pip install -r requirements.txt
```

### 4. Start the Application

```bash
.venv/bin/python server.py
```

The application will start locally and connect to the configured Supabase database.

---

## How It Works

1. Select an entity from the sidebar (Account, Customer, Invoice, Vendor, etc.).
2. Data is loaded from the corresponding Supabase table.
3. Click **Refresh from QuickBooks** to trigger a fresh synchronization.
4. The pipeline retrieves the latest data from QuickBooks Online Sandbox.
5. Records are updated in Supabase.
6. Refresh the dashboard to view the latest data.

---

## Current Tech Stack

### Backend

* Python
* Flask

### Database

* Supabase PostgreSQL

### Data Source

* QuickBooks Online Sandbox API

### Deployment

* Vercel

---

## Future Work: AI-Powered Financial Analytics

The next phase of this project is building a Retrieval-Augmented Generation (RAG) system capable of answering questions about QuickBooks data using natural language.

### Planned Stack

* LangChain
* SQLCoder
* ChromaDB
* Supabase PostgreSQL
* Large Language Models (LLMs)

### Planned Architecture

```text
User Question
      │
      ▼
Natural Language Query
      │
      ▼
Text-to-SQL Agent
      │
      ▼
Generated SQL Query
      │
      ▼
Supabase Database
      │
      ▼
Context Retrieval
      │
      ▼
LLM Response
```

### Example Queries

* "Who are the top 10 customers by revenue?"
* "Show all unpaid invoices."
* "What was total revenue last month?"
* "Which vendors received the highest payments?"
* "Summarize company financial performance."

The goal is to transform QuickBooks data into a conversational analytics experience where users can retrieve insights without writing SQL.

---
