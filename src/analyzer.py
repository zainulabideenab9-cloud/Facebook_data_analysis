"""
Data Analyzer Module
Performs statistical analysis on Facebook data
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


class DataAnalyzer:
    """Class for analyzing Facebook user data"""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize analyzer with DataFrame"""
        self.df = df.copy()
    
    # ===================== AGE ANALYSIS =====================
    def get_age_statistics(self) -> Dict:
        """Get age-related statistics"""
        return {
            'mean': round(self.df['Age'].mean(), 2),
            'median': round(self.df['Age'].median(), 2),
            'std_dev': round(self.df['Age'].std(), 2),
            'min': int(self.df['Age'].min()),
            'max': int(self.df['Age'].max()),
            'q25': int(self.df['Age'].quantile(0.25)),
            'q75': int(self.df['Age'].quantile(0.75))
        }
    
    def get_age_distribution(self, bins: int = 10) -> Dict:
        """Get age distribution in bins"""
        hist, bin_edges = np.histogram(self.df['Age'], bins=bins)
        return {
            'counts': hist.tolist(),
            'bin_edges': bin_edges.tolist(),
            'bins': bins
        }
    
    # ===================== FOLLOWERS ANALYSIS =====================
    def get_followers_statistics(self) -> Dict:
        """Get followers-related statistics"""
        return {
            'mean': round(self.df['Followers'].mean(), 2),
            'median': round(self.df['Followers'].median(), 2),
            'std_dev': round(self.df['Followers'].std(), 2),
            'min': int(self.df['Followers'].min()),
            'max': int(self.df['Followers'].max()),
            'q25': int(self.df['Followers'].quantile(0.25)),
            'q75': int(self.df['Followers'].quantile(0.75))
        }
    
    def get_top_users_by_followers(self, n: int = 10) -> pd.DataFrame:
        """Get top N users by follower count"""
        return self.df.nlargest(n, 'Followers')[['Name', 'Followers', 'PostsCount', 'EngagementRate']]
    
    # ===================== POSTS ANALYSIS =====================
    def get_posts_statistics(self) -> Dict:
        """Get posts-related statistics"""
        return {
            'mean': round(self.df['PostsCount'].mean(), 2),
            'median': round(self.df['PostsCount'].median(), 2),
            'std_dev': round(self.df['PostsCount'].std(), 2),
            'min': int(self.df['PostsCount'].min()),
            'max': int(self.df['PostsCount'].max()),
            'total_posts': int(self.df['PostsCount'].sum())
        }
    
    def get_top_posters(self, n: int = 10) -> pd.DataFrame:
        """Get top N users by post count"""
        return self.df.nlargest(n, 'PostsCount')[['Name', 'PostsCount', 'Followers', 'EngagementRate']]
    
    # ===================== ENGAGEMENT ANALYSIS =====================
    def get_engagement_statistics(self) -> Dict:
        """Get engagement rate statistics"""
        return {
            'mean': round(self.df['EngagementRate'].mean(), 2),
            'median': round(self.df['EngagementRate'].median(), 2),
            'std_dev': round(self.df['EngagementRate'].std(), 2),
            'min': round(self.df['EngagementRate'].min(), 2),
            'max': round(self.df['EngagementRate'].max(), 2)
        }
    
    def get_high_engagement_users(self, threshold: float = 7.0, n: int = 10) -> pd.DataFrame:
        """Get users with high engagement rates"""
        high_eng = self.df[self.df['EngagementRate'] >= threshold].nlargest(n, 'EngagementRate')
        return high_eng[['Name', 'EngagementRate', 'Followers', 'PostsCount']]
    
    # ===================== CITY ANALYSIS =====================
    def get_city_distribution(self) -> pd.DataFrame:
        """Get user count by city"""
        city_dist = self.df['City'].value_counts().reset_index()
        city_dist.columns = ['City', 'UserCount']
        return city_dist
    
    def get_top_cities(self, n: int = 10) -> pd.DataFrame:
        """Get top N cities by user count"""
        return self.df['City'].value_counts().head(n)
    
    def get_city_statistics(self) -> Dict:
        """Get statistics by city"""
        city_stats = self.df.groupby('City').agg({
            'UserID': 'count',
            'Followers': ['mean', 'median', 'max'],
            'EngagementRate': ['mean', 'max'],
            'PostsCount': 'mean'
        }).round(2)
        
        city_stats.columns = ['UserCount', 'AvgFollowers', 'MedianFollowers', 'MaxFollowers',
                             'AvgEngagement', 'MaxEngagement', 'AvgPosts']
        return city_stats.sort_values('UserCount', ascending=False)
    
    # ===================== CORRELATION ANALYSIS =====================
    def get_correlations(self) -> pd.DataFrame:
        """Calculate correlation between numerical variables"""
        numeric_df = self.df[['Age', 'PostsCount', 'Followers', 'EngagementRate']]
        return numeric_df.corr().round(3)
    
    def get_correlation_insights(self) -> Dict:
        """Get key correlation insights"""
        corr = self.get_correlations()
        
        return {
            'age_vs_followers': round(corr.loc['Age', 'Followers'], 3),
            'age_vs_engagement': round(corr.loc['Age', 'EngagementRate'], 3),
            'posts_vs_followers': round(corr.loc['PostsCount', 'Followers'], 3),
            'posts_vs_engagement': round(corr.loc['PostsCount', 'EngagementRate'], 3),
            'followers_vs_engagement': round(corr.loc['Followers', 'EngagementRate'], 3)
        }
    
    # ===================== AGE GROUP ANALYSIS =====================
    def get_age_group_analysis(self) -> pd.DataFrame:
        """Analyze metrics by age groups"""
        bins = [18, 25, 35, 45, 55, 65]
        labels = ['18-24', '25-34', '35-44', '45-54', '55-64']
        
        self.df['AgeGroup'] = pd.cut(self.df['Age'], bins=bins, labels=labels, right=False)
        
        age_group_stats = self.df.groupby('AgeGroup').agg({
            'UserID': 'count',
            'Followers': ['mean', 'median'],
            'PostsCount': 'mean',
            'EngagementRate': 'mean'
        }).round(2)
        
        age_group_stats.columns = ['UserCount', 'AvgFollowers', 'MedianFollowers', 
                                   'AvgPosts', 'AvgEngagement']
        return age_group_stats
    
    # ===================== COMPREHENSIVE SUMMARY =====================
    def get_overall_summary(self) -> Dict:
        """Get comprehensive summary of analysis"""
        return {
            'total_users': len(self.df),
            'age_stats': self.get_age_statistics(),
            'followers_stats': self.get_followers_statistics(),
            'posts_stats': self.get_posts_statistics(),
            'engagement_stats': self.get_engagement_statistics(),
            'total_cities': self.df['City'].nunique(),
            'top_cities': self.get_top_cities(5).to_dict(),
            'correlations': self.get_correlation_insights()
        }


if __name__ == "__main__":
    # Test the analyzer
    try:
        from .data_loader import load_data, clean_data
        
        df = load_data('sample_facebook_data.xlsx')
        df = clean_data(df)
        
        analyzer = DataAnalyzer(df)
        
        print("=" * 50)
        print("FACEBOOK DATA ANALYSIS SUMMARY")
        print("=" * 50)
        
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
        
        print("\nCORRELATIONS:")
        print(analyzer.get_correlations())
        
        print("\nAnalysis complete!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
