"""CSV parsing service."""
import pandas as pd
from typing import List, Dict, Any


def parse_csv(filepath: str) -> List[Dict[str, Any]]:
    """
    Parse CSV or Excel file and extract student data.
    
    Expected columns: Student Id, Name, Course, Marks
    (Column names are case-insensitive and whitespace-tolerant)
    
    Args:
        filepath: Path to CSV or Excel file
        
    Returns:
        List of dictionaries with student data
        
    Raises:
        ValueError: If required columns are missing
    """
    try:
        # Try reading as Excel first, then CSV
        if filepath.endswith('.xlsx') or filepath.endswith('.xls'):
            df = pd.read_excel(filepath)
        else:
            df = pd.read_csv(filepath)

        # Normalize column names (strip whitespace)
        df.columns = df.columns.str.strip()
        
        required_cols = ['Student Id', 'Name', 'Course', 'Marks']
        
        # Create mapping from lowercase to original column names
        df_cols_lower = {col.lower(): col for col in df.columns}
        
        # Check for missing columns and build rename mapping
        rename_map = {}
        for required_col in required_cols:
            required_col_lower = required_col.lower()
            if required_col_lower not in df_cols_lower:
                raise ValueError(f"Missing required column: {required_col}")
            # Map original column name to standardized name
            original_col = df_cols_lower[required_col_lower]
            rename_map[original_col] = required_col
        
        # Rename columns to match required format
        df = df.rename(columns=rename_map)

        # Clean and validate data
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Failed to find column: {col}")
        
        df['Student Id'] = df['Student Id'].astype(str).str.strip()
        df['Name'] = df['Name'].astype(str).str.strip()
        df['Course'] = df['Course'].astype(str).str.strip()
        df['Marks'] = pd.to_numeric(df['Marks'], errors='coerce')

        # Remove rows with invalid marks
        df = df.dropna(subset=['Marks'])

        # Convert to list of dicts
        records = df[['Student Id', 'Name', 'Course', 'Marks']].to_dict('records')
        
        if not records:
            raise ValueError("No valid student records found in file")

        return records

    except Exception as e:
        raise ValueError(f"Error parsing file: {str(e)}")


def validate_marks(marks: float, min_val: float = 0, max_val: float = 100) -> bool:
    """Validate that marks are within acceptable range."""
    return min_val <= marks <= max_val
