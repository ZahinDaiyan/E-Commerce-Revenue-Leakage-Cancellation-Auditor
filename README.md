# E-Commerce Revenue Leakage & Cancellation Auditor 🚀

A high-performance data processing pipeline and automated web application built in Python to isolate financial losses from transactional cancellations. This system smoothly ingests, processes, and reconciles large-scale transactional data (**540,000+ records**) in seconds, converting raw operational chaos into multi-tab, executive-ready Excel reports.

🔗 **Live Web Application:** [Explore the Live Demo Dashboard](https://e-commerce-revenue-leakage-cancellation-auditor-ny32uggwzbybdt.streamlit.app/)

---

## 💼 The Business Challenge
Manual reconciliation of fragmented sales data is a classic corporate bottleneck. Standard office applications like Excel frequently choke or crash when handling datasets exceeding 100,000 rows. This tool was built to provide an instant, bulletproof data-cleaning and auditing asset that answers critical business questions:
1. **Financial Impact:** Exactly how much revenue is lost to cancellations?
2. **Inventory Quality:** Which products are generating the highest frequency of returns?
3. **Customer Retention:** Who are our highest-spending VIP clients experiencing the most friction?

---

## 🛠️ System Architecture & Pipeline Performance

The application is engineered defensively to handle raw upstream data drifts and ensure flawless mathematical outputs.

### 1. Robust Ingestion & Data Transformation
* **Encoding Fault Tolerance:** Uses `ISO-8859-1` encoding strings to gracefully parse varied international currencies and specific retail special characters without dropping connections.
* **Type-Safe Casting:** Standardizes floating-point tracking anomalies by formatting and dynamically casting key indices (such as converting stringified fractions into unified `int` and `str` states).

### 2. Idempotency & Data Reconciliation
To ensure absolute accuracy before file generation, the processing engine runs a strict structural audit check down to the penny. The total raw dataset volume must match the exact sum of the segregated splits:

$$\text{Total Original Dataset Cost} = \text{Successful Orders Cost} + \text{Cancelled Orders Cost}$$

```python
# Validation engine executing inside the automated pipeline
total_raw_dataset_cost = df["Total_Cost"].sum()
total_split_combined_cost = successful_df["Total_Cost"].sum() + cancelled_df["Total_Cost"].sum()

if round(total_raw_dataset_cost, 2) == round(total_split_combined_cost, 2):
    print("✅ VERIFICATION SUCCESS: Data segments reconcile perfectly. Zero rows leaked.")
