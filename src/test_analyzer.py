"""
Test Analyzer Script
Verifies the functionality of the DataAnalyzer class
"""

import pandas as pd
from src.data_loader import load_data, clean_data
from src.analyzer import DataAnalyzer

def test_analyzer():
    try:
        # Load data
        print("Loading data...")
        df = load_data('sample_facebook_data.xlsx')
        df = clean_data(df)
        
        # Initialize analyzer
        analyzer = DataAnalyzer(df)
        
        print("-" * 50)
        print("TESTING ANALYZER MODULE")
        print("-" * 50)
        
        print("\nAGE STATISTICS:")
        for key, val in analyzer.get_age_statistics().items():
            print(f"  {key}: {val}")
        
        print("\nFOLLOWERS STATISTICS:")
        for key, val in analyzer.get_followers_statistics().items():
            print(f"  {key}: {val}")
        
        print("\nPOSTS STATISTICS:")
        for key, val in analyzer.get_posts_statistics().items():
            print(f"  {key}: {val}")
        
        print("\nENGAGEMENT STATISTICS:")
        for key, val in analyzer.get_engagement_statistics().items():
            print(f"  {key}: {val}")
        
        print("\nTOP 5 CITIES:")
        print(analyzer.get_top_cities(5))
        
        print("\nAnalysis complete!")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_analyzer()
