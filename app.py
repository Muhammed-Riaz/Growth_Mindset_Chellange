import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 🎯 Set Page Title
st.set_page_config(page_title="Dynamic Data Visualization", layout="wide")

# 🔹 Sidebar - User Info Input
st.sidebar.title("📌 User Information")
user_name = st.sidebar.text_input("Enter your name:")
user_age = st.sidebar.number_input("Enter your age:", min_value=1, max_value=100)
st.sidebar.write(f"👤 Hello, **{user_name}**! Let's analyze some data. 🚀")

# 📂 File Upload Section
st.title("📊 Data Visualization Dashboard")
st.write("Upload a CSV file to analyze its contents.")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    # Load Data
    df = pd.read_csv(uploaded_file)

    # Convert date column if available
    date_col = None
    for col in df.columns:
        if "date" in col.lower() or "time" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")
            date_col = col
            break

    # Show Data
    st.subheader("📋 Data Table")
    st.dataframe(df)

    # Show basic stats
    st.subheader("📊 Basic Statistics")
    st.write(df.describe())

    # 🔥 Auto-Detect Numeric Columns
    numeric_df = df.select_dtypes(include=[np.number])
    numeric_cols = numeric_df.columns

    if len(numeric_cols) > 0:
        selected_col = st.selectbox("📌 Select a column for analysis", numeric_cols)

        # 📊 Box Plot (to check distribution)
        st.subheader(f"📦 Distribution of {selected_col}")
        fig, ax = plt.subplots()
        sns.boxplot(y=df[selected_col], ax=ax)
        ax.set_ylabel(selected_col)
        st.pyplot(fig)

        # 📈 Line Plot (if a date column exists)
        if date_col:
            st.subheader(f"📈 Trend of {selected_col} Over Time")
            df_sorted = df.dropna(subset=[date_col, selected_col]).sort_values(date_col)
            fig, ax = plt.subplots()
            ax.plot(df_sorted[date_col], df_sorted[selected_col], marker='o', linestyle='-', color='b')
            ax.set_xlabel(date_col)
            ax.set_ylabel(selected_col)
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.subheader(f"📉 Line Plot of {selected_col}")
            fig, ax = plt.subplots()
            ax.plot(df[selected_col], marker='o', linestyle='-', color='g')
            ax.set_ylabel(selected_col)
            st.pyplot(fig)
    else:
        st.warning("⚠️ No numeric columns found for visualization!")
else:
    st.warning("📂 Please upload a CSV file to continue.")
