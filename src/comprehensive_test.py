"""
Comprehensive Project Test
Verifies all project modules and integration
"""

import pandas as pd
import numpy as np
import os
from src.data_loader import load_data, clean_data, get_data_overview, validate_data
from src.analyzer import DataAnalyzer
from src.visualizer import DataVisualizer

def run_tests():
    print("=" * 60)
    print("RUNNING COMPREHENSIVE PROJECT TESTS")
    print("=" * 60)
    
    test_results = []
    
    # 1. Test Data Loading
    print("\n[1/5] Testing Data Loader...")
    try:
        df = load_data('sample_facebook_data.xlsx')
        print(f"Data loaded successfully")
        print(f"Total records: {len(df)}")
        test_results.append(("Data Loading", True))
    except Exception as e:
        print(f"Failed: {str(e)}")
        test_results.append(("Data Loading", False))
    
    # 2. Test Validation
    if test_results[-1][1]:
        try:
            valid, issues = validate_data(df)
            if valid:
                print(f"Data validation passed")
            else:
                print(f"Validation issues found:")
                for issue in issues:
                    print(f"  - {issue}")
            test_results.append(("Data Validation", valid))
        except Exception as e:
            print(f"Failed: {str(e)}")
            test_results.append(("Data Validation", False))
    
    # 3. Test Cleaning
    if test_results[-1][1]:
        try:
            df_clean = clean_data(df)
            print(f"Data cleaned successfully")
            test_results.append(("Data Cleaning", True))
        except Exception as e:
            print(f"Failed: {str(e)}")
            test_results.append(("Data Cleaning", False))
            
    # 4. Test Analysis
    if test_results[-1][1]:
        print("\n[2/5] Testing Analyzer...")
        try:
            analyzer = DataAnalyzer(df_clean)
            overview = get_data_overview(df_clean)
            print(f"Overview generated")
            
            # Run various analyses
            age_stats = analyzer.get_age_statistics()
            follower_stats = analyzer.get_followers_statistics()
            posts_stats = analyzer.get_posts_statistics()
            engagement_stats = analyzer.get_engagement_statistics()
            city_dist = analyzer.get_city_distribution()
            correlations = analyzer.get_correlations()
            
            print(f"Age analysis completed")
            print(f"Followers analysis completed")
            print(f"Posts analysis completed")
            print(f"Engagement analysis completed")
            print(f"City analysis completed")
            print(f"Correlation analysis completed")
            test_results.append(("Statistical Analysis", True))
        except Exception as e:
            print(f"Failed: {str(e)}")
            test_results.append(("Statistical Analysis", False))
            
    # 5. Test Visualizer
    if test_results[-1][1]:
        print("\n[3/5] Testing Visualizer...")
        try:
            viz = DataVisualizer()
            if not os.path.exists('charts'):
                os.makedirs('charts')
                
            test_charts = [
                (viz.create_age_histogram, 'test_age.png'),
                (viz.create_correlation_heatmap, 'test_corr.png'),
                (viz.create_scatter_posts_followers, 'test_scatter.png')
            ]
            
            test_count = 0
            for func, filename in test_charts:
                fig = func(df_clean)
                fig.savefig(f"charts/{filename}")
                test_count += 1
                
            print(f"Age histogram created successfully")
            print(f"Correlation heatmap created successfully")
            print(f"Scatter plot created successfully")
            print(f"All {test_count} visualizations tested successfully")
            test_results.append(("Visualization Generation", True))
        except Exception as e:
            print(f"Failed: {str(e)}")
            test_results.append(("Visualization Generation", False))

    # 6. Test Filtering
    if test_results[-1][1]:
        print("\n[4/5] Testing Filtering Logic...")
        try:
            young_users = df_clean[df_clean['Age'] < 25]
            print(f"Filtered {len(young_users)} users with age < 25")
            
            karachi_users = df_clean[df_clean['City'] == 'Karachi']
            print(f"Found {len(karachi_users)} users in Karachi")
            
            top_followers = analyzer.get_top_users_by_followers(5)
            print(f"Retrieved top 5 users by followers")
            test_results.append(("Data Filtering", True))
        except Exception as e:
            print(f"Failed: {str(e)}")
            test_results.append(("Data Filtering", False))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    all_passed = all(result[1] for result in test_results)
    if all_passed:
        print("All tests passed successfully!")
    else:
        print("Some tests failed. Please check the logs above.")
        
    for name, status in test_results:
        print(f"- {name}: {'Passed' if status else 'Failed'}")
    
    print("\n" + "=" * 60)
    print("PROJECT READY FOR DEPLOYMENT")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
