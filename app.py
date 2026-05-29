import pandas as pd

print("⏳ Loading dataset directly from folder...")
df = pd.read_csv("data.csv", encoding="ISO-8859-1")
print(f"✅ Loaded {len(df)} rows.\n")

# 1. Create a dynamic "Total_Cost" column
df["Total_Cost"] = df["Quantity"].abs() * df["UnitPrice"]

# 2. Filter for Canceled Orders
cancelled_orders = df[df["InvoiceNo"].astype(str).str.startswith("C")]

# 3. Calculate total revenue lost from cancellations
total_lost = cancelled_orders["Total_Cost"].sum()
print(f"🚨 Total Revenue Lost from Cancellations: ${total_lost:,.2f}\n")

# 4. Find the top 5 most frequently cancelled items (Fixed order of operations)
top_cancelled_items = cancelled_orders.groupby("Description")["Quantity"].sum().abs()
print("📉 Top 5 Items with the most cancelled quantities:")
print(top_cancelled_items.nlargest(5))
