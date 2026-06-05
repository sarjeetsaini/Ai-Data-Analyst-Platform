# 📈 AI-Driven Automated Data Analytics Platform

An enterprise-grade, high-fidelity Business Intelligence (BI) canvas built with Python, Streamlit, and Plotly. The platform ingests multi-format datasets (CSV, Excel, SQLite), automatically executes a robust data-cleaning pipeline, and delivers a dynamic 2x2 Power BI-style interactive dashboard combined with strategic executive summaries powered by open-source LLMs (Meta Llama-3 via Groq).

---

# Key Features

* **Multi-Format Data Ingestion:** Seamlessly reads `.csv`, Multi-sheet `.xlsx`/`.xls` (with dynamic sheet selectors), and `.db`/`.sqlite` relational databases.

* **Automated Data Cleaning Pipeline:** Programmatically standardizes structural anomalies, handles text-based/whitespace nulls (`NaN`, `null`, spaces), imputes missing fields (Numeric via Median, Categorical via 'Unknown'), and drops duplicate records.

* **Power BI-Style 2x2 Interactive Canvas:** Implements a consolidated 4-visual matrix grid layout with global cross-filtering controllers for high-density, single-frame data exploration.

* **Groq AI Core Integration:** Leverages open-source `Llama-3.3-70b` to generate real-time executive business observations, revenue risk mitigation plans, and future growth strategies without vendor lock-in or high API latency.

* **Premium Dark UI Theme:** Engineered with a corporate glassmorphic aesthetic using a custom cyber-executive midnight-blue palette.

