import pandas as pd

class DataProcessor:
    """Handles data loading and basic preprocessing."""

    @staticmethod
    def load_data(uploaded_file):
        """Load CSV or Excel file into a pandas DataFrame."""
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(uploaded_file)
            else:
                raise ValueError("Unsupported file format. Please upload CSV or Excel.")
            return df
        except Exception as e:
            raise Exception(f"Error loading file: {str(e)}")

    @staticmethod
    def get_data_overview(df):
        """Return a dictionary with basic data overview details."""
        overview = {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "missing_values": df.isnull().sum(),
            "column_names": df.columns.tolist(),
            "data_types": df.dtypes.apply(str).to_dict(),
            "unique_values": df.nunique().to_dict(),
        }
        return overview
