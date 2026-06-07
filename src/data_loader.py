"""
Data Loader Module
Handles loading and initial exploration of Facebook data
"""

import pandas as pd
import numpy as np
from typing import Tuple


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load Facebook data from Excel file.
    
    Args:
        filepath: Path to Excel file
        
    Returns:
        DataFrame with loaded data
    """
    try:
        df = pd.read_excel(filepath, sheet_name='FacebookData')
        return df
    except Exception as e:
        raise ValueError(f"Error loading data: {str(e)}")


def get_data_overview(df: pd.DataFrame) -> dict:
    """
    Get overview statistics of the data.
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        Dictionary with overview information
    """
    overview = {
        'total_records': len(df),
        'total_columns': len(df.columns),
        'column_names': df.columns.tolist(),
        'data_types': df.dtypes.to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'duplicates': df.duplicated().sum(),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024
    }
    return overview


def get_statistical_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get descriptive statistics for numerical columns.
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        Statistical summary DataFrame
    """
    return df.describe().T


def validate_data(df: pd.DataFrame) -> Tuple[bool, list]:
    """
    Validate data integrity.
    
    Args:
        df: DataFrame to validate
        
    Returns:
        Tuple of (is_valid, list of issues)
    """
    issues = []
    
    # Check for required columns
    required_cols = ['UserID', 'Name', 'Age', 'City', 'PostsCount', 'Followers', 'EngagementRate']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        issues.append(f"Missing required columns: {missing_cols}")
    
    # Check Age range
    if 'Age' in df.columns:
        invalid_ages = df[(df['Age'] < 13) | (df['Age'] > 120)]
        if len(invalid_ages) > 0:
            issues.append(f"Found {len(invalid_ages)} records with invalid ages")
    
    # Check negative values
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if (df[col] < 0).any():
            issues.append(f"Column '{col}' contains negative values")
    
    return len(issues) == 0, issues


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess the data.
    
    Args:
        df: Raw DataFrame
        
    Returns:
        Cleaned DataFrame
    """
    df = df.copy()
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Handle missing values
    df = df.dropna()
    
    # Convert Age to integer
    if 'Age' in df.columns:
        df['Age'] = df['Age'].astype(int)
    
    # Convert numerical columns
    numeric_cols = ['PostsCount', 'Followers']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].astype(int)
    
    # Round engagement rate
    if 'EngagementRate' in df.columns:
        df['EngagementRate'] = df['EngagementRate'].round(2)
    
    return df


if __name__ == "__main__":
    # Test the module
    try:
        df = load_data('sample_facebook_data.xlsx')
        print("Data loaded successfully")
        print(f"Shape: {df.shape}")
        
        overview = get_data_overview(df)
        print(f"\nData Overview:")
        print(f"Records: {overview['total_records']}")
        print(f"Missing values: {sum(overview['missing_values'].values())}")
        
        valid, issues = validate_data(df)
        print(f"\nValidation: {'Passed' if valid else 'Failed'}")
        if issues:
            for issue in issues:
                print(f"- {issue}")
        
        df_clean = clean_data(df)
        print(f"\nAfter cleaning:")
        print(f"Shape: {df_clean.shape}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
