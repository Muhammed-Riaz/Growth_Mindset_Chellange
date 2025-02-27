import streamlit as st 
import pandas as pd 
import os
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide")

st.title("Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

upload_files = st.file_uploader("📂 Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if upload_files:
    for file in upload_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # ✅ Read File Based on Extension
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file, engine="openpyxl")
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

        # ✅ Display File Info
        st.write(f"### 📂 File: **{file.name}**")

        # ✅ Show Data Preview
        st.write("🔍 **Preview of the Data:**")
        st.dataframe(df.head())

        st.subheader("🧹 Data Cleaning Options")

        col1, col2, col3 = st.columns(3)

        # ✅ Remove Duplicates
        with col1:
            if st.button(f"🗑 Remove Duplicates ({file.name})"):
                df.drop_duplicates(inplace=True)
                st.success("✅ Duplicates removed!")

        # ✅ Fill Missing Values
        with col2:
            if st.button(f"⚡ Fill Missing Values ({file.name})"):
                numeric_cols = df.select_dtypes(include=["number"]).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.success("✅ Missing values filled!")

        # ✅ Erase All Data
        with col3:
            if st.button(f"🚨 Erase All Data ({file.name})"):
                df = pd.DataFrame(columns=df.columns)  # Keep column headers but remove all data
                st.warning("⚠️ All data erased! Only headers remain.")

        # ✅ Column Selection for Export
        st.subheader("🔄 Select Columns to Keep")
        columns_selected = st.multiselect(f"📌 Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns_selected]

        # ✅ Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"📈 Show Visualization ({file.name})"):
            chart_type = st.selectbox("📌 Choose a chart type:", ["Bar Chart", "Line Chart", "Scatter Plot"])

            numeric_cols = df.select_dtypes(include="number").columns
            if len(numeric_cols) < 1:
                st.warning("⚠️ No numeric columns available for visualization!")
            else:
                selected_x = st.selectbox("📌 Select X-axis:", numeric_cols)
                selected_y = st.selectbox("📌 Select Y-axis:", numeric_cols)

                fig, ax = plt.subplots(figsize=(8, 4))

                if chart_type == "Bar Chart":
                    df[selected_y].value_counts().plot(kind="bar", ax=ax, color="skyblue")
                    ax.set_ylabel(selected_y)
                    ax.set_title(f"Bar Chart of {selected_y}")

                elif chart_type == "Line Chart":
                    df.plot(x=selected_x, y=selected_y, kind="line", marker="o", linestyle="-", ax=ax, color="blue")
                    ax.set_ylabel(selected_y)
                    ax.set_title(f"Line Chart of {selected_y} over {selected_x}")

                elif chart_type == "Scatter Plot":
                    df.plot(x=selected_x, y=selected_y, kind="scatter", ax=ax, color="red")
                    ax.set_xlabel(selected_x)
                    ax.set_ylabel(selected_y)
                    ax.set_title(f"Scatter Plot of {selected_y} vs {selected_x}")

                st.pyplot(fig)

        # ✅ Convert & Download Section
        st.subheader("📥 Convert & Download")
        conversion_type = st.radio(f"🔄 Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"📤 Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False, engine="openpyxl")
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            # ✅ Download Button
            st.download_button(
                label=f"📥 Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("✅ All files processed successfully!")

