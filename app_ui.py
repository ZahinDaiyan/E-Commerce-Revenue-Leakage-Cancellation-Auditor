import pandas as pd
import streamlit as st
import io

st.set_page_config(page_title="E-commerce Audit Tool", layout="wide")
st.title("📈 Automated Revenue & Cancellation Auditor")
st.write("Upload your raw transaction CSV file to instantly generate an executive financial report.")

# 1. File Uploader UI
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    with st.spinner("Processing massive dataset..."):
        # 2. Read the uploaded file
        df = pd.read_csv(uploaded_file, encoding="ISO-8859-1")
        
        # 3. Run your exact Pandas engine
        df["Total_Cost"] = df["Quantity"].abs() * df["UnitPrice"]
        cancelled_df = df[df["InvoiceNo"].astype(str).str.startswith("C")]
        successful_df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]
        
        # Calculations
        total_lost = cancelled_df["Total_Cost"].sum()
        
        # Tab 1 Data
        top_cancelled = (
            cancelled_df.groupby("Description")["Quantity"]
            .sum().abs().reset_index()
            .rename(columns={"Quantity": "Units_Cancelled"})
            .nlargest(10, "Units_Cancelled")
        )
        
        # --- Display Results in UI ---
        st.success("Analysis Complete!")
        
        # Metric KPI blocks
        col1, col2 = st.columns(2)
        col1.metric("Total Rows Processed", f"{len(df):,}")
        col2.metric("Total Revenue Lost", f"${total_lost:,.2f}", delta_color="inverse")
        
        # Display Data Table
        st.subheader("📉 Top 10 Most Cancelled Products")
        st.dataframe(top_cancelled, use_container_width=True)
        
        # 4. Memory buffer to download the Excel file directly from the browser
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            top_cancelled.to_excel(writer, sheet_name="Top_Cancelled", index=False)
            
        st.download_button(
            label="📥 Download Executive Excel Report",
            data=buffer.getvalue(),
            file_name="Executive_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )