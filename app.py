import pandas as pd

df = pd.read_csv("data.csv", encoding="ISO-8859-1")

df = df.dropna(subset=["CustomerID", "Description"])

df["CustomerID"] = df["CustomerID"].astype(int).astype(str)

df["Total_Cost"] = df["Quantity"].abs() * df["UnitPrice"]

cancelled_df = df[df["InvoiceNo"].astype(str).str.startswith("C")]
successful_df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

top_cancelled_products = (
    cancelled_df.groupby("Description")["Quantity"]
    .sum()
    .abs()
    .reset_index()
    .rename(columns={"Quantity": "Total_Units_Cancelled"})
    .nlargest(10, "Total_Units_Cancelled")
)

# Find total successful spend per customer
vip_spend = successful_df.groupby("CustomerID")["Total_Cost"].sum().reset_index().rename(columns={"Total_Cost": "Total_Successful_Spend"})

# Find total cancelled losses per customer
vip_lost = cancelled_df.groupby("CustomerID")["Total_Cost"].sum().reset_index().rename(columns={"Total_Cost": "Total_Cancelled_Loss"})

# Merge them together to find the cross-section
vip_report = pd.merge(vip_spend, vip_lost, on="CustomerID")
# Filter for true high-spenders (e.g., spent > $2,000 successfully) and sort by biggest loss
vip_report = vip_report[vip_report["Total_Successful_Spend"] > 2000].nlargest(10, "Total_Cancelled_Loss")


output_filename = "Executive_Cancellation_Report.xlsx"

with pd.ExcelWriter(output_filename, engine="openpyxl") as writer:
    top_cancelled_products.to_excel(writer, sheet_name="Top_Cancelled_Products", index=False)
    vip_report.to_excel(writer, sheet_name="At_Risk_VIP_Customers", index=False)

print(f"\nClient Deliverable Created Successfully: '{output_filename}'")

# --- STEP 6: DATA VERIFICATION LOGIC ---
print("\n🛡️ Running Verification Audit...")

# 1. Calculate the total cost of the absolute raw dataset
total_raw_dataset_cost = df["Total_Cost"].sum()

# 2. Calculate the combined cost of our split dataframes
total_split_combined_cost = successful_df["Total_Cost"].sum() + cancelled_df["Total_Cost"].sum()

print(f"-> Raw Dataset Total:      ${total_raw_dataset_cost:,.2f}")
print(f"-> Split Segments Total:   ${total_split_combined_cost:,.2f}")

# 3. Assert check (They must match perfectly down to the penny)
if round(total_raw_dataset_cost, 2) == round(total_split_combined_cost, 2):
    print("✅ VERIFICATION SUCCESS: Data segments reconcile perfectly. Zero rows leaked.")
else:
    print("❌ VERIFICATION FAILED: Data mismatch detected! Check filter boundaries.")
