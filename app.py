import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from groq import Groq  # 🌟 OpenAI hata kar Groq import kiya
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Data Analyst Pro", page_icon="📈", layout="wide")

st.title("📈 AI-Driven Automated Data Analytics Platform")
st.write("Upload a CSV or SQLite Database file. Automated preprocessing, charts, and insights powered by Llama-3 via Groq.")

# --- GROQ API SETUP ---
# 🌟 Apni Groq API Key yahan daalein (Jo bilkul free hai)
GROQ_API_KEY = st.secrets["GROQ_API_KEY"] 

if GROQ_API_KEY != "YOUR_GROQ_API_KEY_HERE":
    client = Groq(api_key=GROQ_API_KEY)
else:
    st.warning("⚠️ Please insert your Groq API Key in the code to unlock Free AI Insights.")

# --- STEP 1: FILE UPLOAD (CSV or DB) ---
uploaded_file = st.file_uploader("Upload your data file (.csv, .db, .sqlite)", type=["csv", "db", "sqlite"])

df = None

if uploaded_file is not None:
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
    
    if file_extension == ".csv":
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Loaded CSV file: {uploaded_file.name}")
        
    elif file_extension in [".db", ".sqlite"]:
        with open("temp_db.db", "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        conn = sqlite3.connect("temp_db.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        if tables:
            st.info(f"💾 Database contains {len(tables)} table(s).")
            selected_table = st.selectbox("Select a table to analyze:", tables)
            df = pd.read_sql_query(f"SELECT * FROM {selected_table}", conn)
            st.success(f"✅ Loaded table '{selected_table}' from database.")
        else:
            st.error("❌ The uploaded database file has no tables.")
        conn.close()

# --- PROCESSING & AI ENGINE ---
if df is not None:
    st.subheader("📋 Data Preview (First 5 Rows)")
    st.dataframe(df.head())

    # --- STEP 2: AUTOMATED DATA CLEANING ---
# === 🌟 IS UPGRADED CLEANING CODE SE APNA PURANA STEP 2 REPLACE KAREIN ===
    st.markdown("---")
    st.subheader("🛠️ Automated Data Preprocessing Status")
    
    # Standardize Missing Values: Agar data mein string waale 'nan', 'null', 'NA' ya khaali spaces hain, unhe real NaN mein badlein
    df.replace([r'^\s*$', 'null', 'nan', 'NA', 'NaN'], pd.NA, regex=True, inplace=True)
    
    missing_data = df.isnull().sum()
    columns_with_missing = missing_data[missing_data > 0]
    
    if not columns_with_missing.empty:
        st.write("🔍 Missing values detected. Cleaning in progress...")
        
        # Ek naya temporary dataframe bana kar clean kar rahe hain taaki inplace ka error na aaye
        for col in df.columns:
            if df[col].isnull().any():
                if df[col].dtype == "object" or df[col].dtype == "string":
                    # Text columns ke liye 'Unknown' se fill karein
                    df[col] = df[col].fillna("Unknown")
                else:
                    # Numeric columns ke liye Median se fill karein
                    median_value = df[col].median()
                    df[col] = df[col].fillna(median_value)
                    
        st.success("✅ All missing values handled successfully (Numeric -> Median, Text -> 'Unknown').")
    else:
        st.success("✅ No missing values found! The dataset is clean.")
        
    # Duplicates handling
    duplicate_count = df.duplicated().sum()
    if duplicate_count > 0:
        df = df.drop_duplicates()
        st.success(f"✅ Removed {duplicate_count} duplicate rows successfully.")
    # =======================================================================
   # === 🌟 IS PROFESSIONAL CHART LAYOUT SE APNA PURANA STEP 3 REPLACE KAREIN ===
    st.markdown("---")
    st.subheader("📊 Executive Data Insights Dashboard")
    st.write("Charts ko bada aur clear dekhne ke liye aap har chart ke top-right corner par 'Fullscreen' button use kar sakte hain.")

    columns = df.columns.tolist()

    # --- ROW 1: KEY PERFORMANCE INDICATORS (KPIs) ---
    st.markdown("### 📈 Quick Metrics")
    kpi1, kpi2, kpi3 = st.columns(3)
    
    # Auto-detect target count for metrics
    default_target = "Churn" if "Churn" in columns else columns[-1]
    total_records = len(df)
    
    with kpi1:
        st.metric(label="Total Analyzed Records", value=f"{total_records:,}")
    with kpi2:
        st.metric(label="Total Features (Columns)", value=len(columns))
    with kpi3:
        # Agar numeric column hai toh average automatic show karega
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if numeric_cols:
            st.metric(label=f"Avg {numeric_cols[0]}", value=f"{df[numeric_cols[0]].median():.2f}")
        else:
            st.metric(label="Dataset Status", value="Fully Cleaned")

    st.markdown("---")

    # --- ROW 2: CORE DISTRIBUTIONS (Bade Size ke Charts) ---
    st.markdown("### 🔄 Distribution & Category Analysis")
    col_left, col_right = st.columns(2)

    with col_left:
        target_col = st.selectbox("1. Select Main Categorical/Target Column (e.g., Churn)", columns, index=columns.index(default_target), key="chart_target")
        # Donut Chart for clean composition percentage
        fig_pie = px.pie(df, names=target_col, hole=0.4, title=f"Percentage Composition of {target_col}",
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_pie.update_layout(height=450, margin=dict(l=20, r=20, t=40, b=20)) # Width & clarity improve ki
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        bar_x = st.selectbox("2. Select Feature for Volume Count (Bar Chart)", columns, index=0 if len(columns)>0 else 0, key="chart_bar_x")
        fig_bar = px.histogram(df, x=bar_x, color=target_col, barmode="group", text_auto=True,
                               title=f"Volume Count of {bar_x} split by {target_col}",
                               color_discrete_sequence=px.colors.qualitative.Safe)
        fig_bar.update_layout(height=450, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # --- ROW 3: TRENDS & CORRELATIONS (Bade Size ke Charts) ---
   
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>📊 Interactive Business Intelligence Canvas</h2>", unsafe_allow_html=True)
    st.write("This grid updates dynamically based on your data columns, exactly like a Power BI or Tableau desktop canvas.")

    columns = df.columns.tolist()
    default_target = "Churn" if "Churn" in columns else columns[-1]

    # --- TOP ROW: KPI CARDS (Power BI Style Cards) ---
    st.markdown("### 🔑 Executive Summary KPIs")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    with kpi1:
        st.markdown(f"<div style='padding: 15px; border-radius: 5px; background-color: #00008B; border-left: 5px solid #1E3A8A;'><strong>Total Records</strong><br><span style='font-size: 24px; font-weight: bold;'>{len(df):,}</span></div>", unsafe_allow_html=True)
    with kpi2:
        st.markdown(f"<div style='padding: 15px; border-radius: 5px; background-color: #00008B; border-left: 5px solid #10B981;'><strong>Total Features</strong><br><span style='font-size: 24px; font-weight: bold;'>{len(columns)} Cols</span></div>", unsafe_allow_html=True)
    with kpi3:
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        val = f"{df[numeric_cols[0]].median():.1f}" if numeric_cols else "Clean"
        lbl = f"Median {numeric_cols[0]}" if numeric_cols else "Data Status"
        st.markdown(f"<div style='padding: 15px; border-radius: 5px; background-color: #00008B; border-left: 5px solid #F59E0B;'><strong>{lbl}</strong><br><span style='font-size: 24px; font-weight: bold;'>{val}</span></div>", unsafe_allow_html=True)
    with kpi4:
        st.markdown(f"<div style='padding: 15px; border-radius: 5px; background-color: #00008B; border-left: 5px solid #EF4444;'><strong>Missing Rows Fixed</strong><br><span style='font-size: 24px; font-weight: bold;'>{df.isnull().sum().sum()}</span></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- THE POWER BI CANVAS SETUP: 2X2 GRID SYSTEM ---
    # Global Controls for the entire canvas inside a clean sidebar layout or top row
    st.markdown("### 🛠️ Canvas Controls")
    ctrl1, ctrl2, ctrl3 = st.columns(3)
    with ctrl1:
        target_col = st.selectbox("🎯 Select Primary Target (Color Legend)", columns, index=columns.index(default_target))
    with ctrl2:
        cat_col = st.selectbox("🗂️ Select Category Axis (X-Axis for Bar/Box)", columns, index=0)
    with ctrl3:
        num_col = st.selectbox("🔢 Select Metric/Value Axis (Y-Axis for Line/Box)", numeric_cols if numeric_cols else columns, index=1 if len(numeric_cols)>1 else 0)

    st.markdown("---")

    # Creating the 2x2 Grid using Streamlit Columns
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    # --- CHART 1: DONUT COMPOSITION (Top Left) ---
    with row1_col1:
        st.markdown("#### 🍩 1. Target Proportion Analysis")
        fig_pie = px.pie(df, names=target_col, hole=0.5, 
                         color_discrete_sequence=px.colors.qualitative.Prism)
        fig_pie.update_layout(height=350, margin=dict(l=10, r=10, t=20, b=10), showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- CHART 2: GROUPED BAR CHART (Top Right) ---
    with row1_col2:
        st.markdown("#### 📊 2. Categorical Cross-Tabulation")
        fig_bar = px.histogram(df, x=cat_col, color=target_col, barmode="group", text_auto=True,
                               color_discrete_sequence=px.colors.qualitative.Safe)
        fig_bar.update_layout(height=350, margin=dict(l=10, r=10, t=20, b=10), xaxis_title=cat_col, yaxis_title="Count")
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- CHART 3: GRADIENT AREA / LINE TREND (Bottom Left) ---
    with row2_col1:
        st.markdown("#### 📈 3. Cumulative Continuous Trend")
        if numeric_cols:
            # Time or sequential column identification
            trend_x = numeric_cols[0]
            df_trend = df.groupby(trend_x)[num_col].mean().reset_index()
            
            fig_area = px.area(df_trend, x=trend_x, y=num_col, 
                               title=f"Average {num_col} over {trend_x}")
            fig_area.update_layout(height=350, margin=dict(l=10, r=10, t=20, b=10))
            st.plotly_chart(fig_area, use_container_width=True)
        else:
            st.info("Line trend requests numeric values.")

    # --- CHART 4: DISTRIBUTION BOX PLOT (Bottom Right) ---
    with row2_col2:
        st.markdown("#### 📦 4. Outlier & Range Spread Analysis")
        fig_box = px.box(df, x=cat_col, y=num_col, color=target_col,
                         color_discrete_sequence=px.colors.qualitative.Vivid)
        fig_box.update_layout(height=350, margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")
    # --- ROW 5: DETAILED DATA VIEW ---
    st.markdown("### 🔍 Drill-Down Data Sheet")
    st.dataframe(df, use_container_width=True)
   
    # =======================================================================

    # --- STEP 4: FREE AI INSIGHTS & FUTURE STRATEGIES ---
    st.markdown("---")
    st.subheader("🤖 Open-Source AI Business Executive Summary")
    
    if GROQ_API_KEY != "YOUR_GROQ_API_KEY_HERE":
        if st.button("🤖 Generate AI Executive Summary"):
            with st.spinner("Llama-3 is analyzing your dataset... Please wait."):
                try:
                    data_summary = f"""
                    Dataset Shape: {df.shape}
                    Columns available: {columns[:15]}
                    Numeric Data Description Summary:
                    {df.describe().to_string()}
                    Target Column ({target_col}) Distribution:
                    {df[target_col].value_counts().to_dict()}
                    """
                    
                    # 🌟 Groq API Call using Llama 3 
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",  # Current state-of-the-art free model on Groq
                        messages=[
                            {"role": "system", "content": "You are a Senior Strategic Business Data Analyst."},
                            {"role": "user", "content": f"Analyze this dataset summary and provide: 1. Data Explanation, 2. Business Revenue Impact, and 3. 3 Future Strategies for customer retention/growth.\n\nData Summary:\n{data_summary}"}
                        ]
                    )
                    
                    st.markdown(response.choices[0].message.content)
                    
                except Exception as e:
                    st.error(f"Groq AI failed to respond: {e}")
    else:
        st.info("💡 Top par apni Groq API Key daaliye fir 'Generate' button dabaiye.")