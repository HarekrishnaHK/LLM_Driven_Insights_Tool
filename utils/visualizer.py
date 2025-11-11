import plotly.express as px
import streamlit as st

class Visualizer:
    """Handles automatic and custom data visualizations."""

    def __init__(self, df):
        self.df = df

    def auto_generate_charts(self):
        charts = []
        try:
            num_cols = self.df.select_dtypes(include=['int64', 'float64']).columns
            for col in num_cols[:3]:
                fig = px.histogram(self.df, x=col, title=f"Distribution of {col}")
                charts.append(fig)
            cat_cols = self.df.select_dtypes(include=['object']).columns
            for col in cat_cols[:2]:
                value_counts = self.df[col].value_counts().reset_index()
                value_counts.columns = [col, 'Count']
                fig = px.bar(value_counts, x=col, y='Count', title=f"Count of {col}")
                charts.append(fig)
        except Exception as e:
            st.error(f"Error generating charts: {str(e)}")
        return charts

    def create_scatter_plot(self, x_col, y_col, color_col=None):
        try:
            fig = px.scatter(
                self.df,
                x=x_col,
                y=y_col,
                color=color_col if color_col and color_col != "None" else None,
                title=f"{x_col} vs {y_col}"
            )
            return fig
        except Exception as e:
            st.error(f"Error creating scatter plot: {str(e)}")
            return None
