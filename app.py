import streamlit as st
import pandas as pd
from utils.data_processor import DataProcessor
from utils.visualizer import Visualizer
from utils.llm_handler import LLMHandler

# ----------------------------------------------------
# 🔧 Streamlit Page Configuration
# ----------------------------------------------------
st.set_page_config(
    page_title="InsightLLM - Business Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------
# 🎨 Custom CSS Styling
# ----------------------------------------------------
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 🚀 Main App Function
# ----------------------------------------------------
def main():
    st.markdown('<div class="main-header">📊 InsightLLM</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Natural Language Business Analytics Generator</div>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("📁 Upload Data")
        uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=['csv', 'xlsx'])

    # ----------------------------------------------------
    # 🧮 Main Content
    # ----------------------------------------------------
    if uploaded_file is not None:
        processor = DataProcessor()
        df = processor.load_data(uploaded_file)
        # --- Convert date columns to datetime ---
        for col in df.columns:
            if "date" in col.lower():
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce', dayfirst=True)
                except Exception:
                    pass

        stats = processor.get_data_overview(df)

        st.success(f"✅ Data Loaded Successfully — {uploaded_file.name}")
        st.write("### Preview of Uploaded Data")
        st.dataframe(df.head(), use_container_width=True)

        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Overview",
            "📈 Visualizations",
            "🤖 AI Insights",
            "💬 Ask Questions"
        ])

        # ------------------ Tab 1: Overview ------------------
        with tab1:
            st.header("Dataset Overview")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Rows", stats["rows"])
            with col2:
                st.metric("Columns", stats["columns"])
            with col3:
                st.metric("Total Missing Values", stats["missing_values"].sum())
            st.divider()
            st.write("### Column Information")
            col_df = pd.DataFrame({
                "Column Name": stats["column_names"],
                "Data Type": [stats["data_types"][col] for col in stats["column_names"]],
                "Missing": [stats["missing_values"][col] for col in stats["column_names"]],
                "Unique Values": [stats["unique_values"][col] for col in stats["column_names"]]
            })
            st.write(col_df)

        # ------------------ Tab 2: Visualization ------------------
        with tab2:
            st.header("Auto-Generated Visualizations")
            viz = Visualizer(df)
            charts = viz.auto_generate_charts()
            for chart in charts:
                st.plotly_chart(chart, use_container_width=True)
                st.divider()

            st.subheader("Custom Visualization")
            plot_cols = df.select_dtypes(include=['number', 'datetime64[ns]']).columns.tolist()
            if len(plot_cols) >= 2:
                x_axis = st.selectbox("X-axis", plot_cols)
                y_axis = st.selectbox("Y-axis", plot_cols, index=1)
                color_candidates = df.columns.tolist()
                color_by = st.selectbox("Color by (optional)", ["None"] + color_candidates)
                fig = viz.create_scatter_plot(x_axis, y_axis, color_col=None if color_by == "None" else color_by)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Unable to generate plot for the selected columns.")
            else:
                st.warning("Not enough numeric or datetime columns to generate a custom scatter plot.")

        # ------------------ Tab 3: AI Insights ------------------
        with tab3:
            st.header("AI-Generated Insights")
            llm = LLMHandler()
            with st.spinner("Generating insights..."):
                insights = llm.generate_insights(df)
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.write(insights)
            st.markdown('</div>', unsafe_allow_html=True)

        # ------------------ Tab 4: Ask Questions ------------------
        with tab4:
            st.header("Ask Questions in Natural Language")
            llm = LLMHandler()
            question = st.text_input("Ask your question about the dataset:")
            if st.button("🔍 Get Answer") and question:
                with st.spinner("Processing your question..."):
                    answer = llm.answer_question(df, question)
                st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                st.write(answer)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        # ------------------ Default Welcome Screen ------------------
        st.info("👈 Upload a dataset to begin exploring with InsightLLM")
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("### 📊 Auto-Visualizations")
            st.write("Automatically generate charts based on your dataset.")
        with col2:
            st.markdown("### 🤖 AI Insights")
            st.write("Get intelligent insights and pattern detection.")
        with col3:
            st.markdown("### 💬 Natural Language")
            st.write("Ask data questions in plain English.")

# ----------------------------------------------------
# ▶️ Run Streamlit App
# ----------------------------------------------------
if __name__ == "__main__":
    main()
