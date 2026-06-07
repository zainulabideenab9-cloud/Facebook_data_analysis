"""
Visualizer Module
Creates matplotlib visualizations for Facebook data analysis
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import Tuple
import io


class DataVisualizer:
    """Class for creating visualizations"""
    
    def __init__(self):
        """Initialize visualizer with matplotlib settings"""
        plt.style.use('seaborn-v0_8-darkgrid')
        self.colors = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'success': '#2ca02c',
            'danger': '#d62728',
            'warning': '#ff9896',
            'info': '#17becf'
        }
    
    def create_age_histogram(self, df: pd.DataFrame, bins: int = 15) -> plt.Figure:
        """Create age distribution histogram"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.hist(df['Age'], bins=bins, color=self.colors['primary'], edgecolor='black', alpha=0.7)
        ax.axvline(df['Age'].mean(), color=self.colors['danger'], linestyle='--', linewidth=2, label=f'Mean: {df["Age"].mean():.1f}')
        ax.axvline(df['Age'].median(), color=self.colors['success'], linestyle='--', linewidth=2, label=f'Median: {df["Age"].median():.1f}')
        
        ax.set_xlabel('Age (years)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Users', fontsize=12, fontweight='bold')
        ax.set_title('Age Distribution of Facebook Users', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_followers_histogram(self, df: pd.DataFrame, bins: int = 20) -> plt.Figure:
        """Create followers distribution histogram"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.hist(df['Followers'], bins=bins, color=self.colors['secondary'], edgecolor='black', alpha=0.7)
        ax.axvline(df['Followers'].mean(), color=self.colors['danger'], linestyle='--', linewidth=2, label=f'Mean: {df["Followers"].mean():.0f}')
        ax.axvline(df['Followers'].median(), color=self.colors['success'], linestyle='--', linewidth=2, label=f'Median: {df["Followers"].median():.0f}')
        
        ax.set_xlabel('Number of Followers', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Users', fontsize=12, fontweight='bold')
        ax.set_title('Followers Distribution', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_top_cities_bar(self, df: pd.DataFrame, top_n: int = 10) -> plt.Figure:
        """Create top cities bar chart"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        city_counts = df['City'].value_counts().head(top_n)
        colors_list = [self.colors['primary']] * (top_n - 1) + [self.colors['danger']]
        
        bars = ax.bar(range(len(city_counts)), city_counts.values, color=colors_list, edgecolor='black', alpha=0.8)
        
        # Add value labels on bars
        for i, (bar, val) in enumerate(zip(bars, city_counts.values)):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, 
                   str(int(val)), ha='center', va='bottom', fontweight='bold')
        
        ax.set_xticks(range(len(city_counts)))
        ax.set_xticklabels(city_counts.index, rotation=45, ha='right')
        ax.set_ylabel('Number of Users', fontsize=12, fontweight='bold')
        ax.set_title(f'Top {top_n} Cities by User Count', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return fig
    
    def create_scatter_posts_followers(self, df: pd.DataFrame) -> plt.Figure:
        """Create scatter plot of posts vs followers"""
        fig, ax = plt.subplots(figsize=(10, 7))
        
        scatter = ax.scatter(df['PostsCount'], df['Followers'], 
                            c=df['EngagementRate'], cmap='viridis', 
                            s=100, alpha=0.6, edgecolors='black', linewidth=0.5)
        
        ax.set_xlabel('Number of Posts', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Followers', fontsize=12, fontweight='bold')
        ax.set_title('Posts vs Followers (colored by Engagement Rate)', fontsize=14, fontweight='bold')
        
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Engagement Rate (%)', fontsize=11, fontweight='bold')
        
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig
    
    def create_engagement_histogram(self, df: pd.DataFrame, bins: int = 20) -> plt.Figure:
        """Create engagement rate distribution"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.hist(df['EngagementRate'], bins=bins, color=self.colors['info'], edgecolor='black', alpha=0.7)
        ax.axvline(df['EngagementRate'].mean(), color=self.colors['danger'], linestyle='--', linewidth=2, label=f'Mean: {df["EngagementRate"].mean():.2f}%')
        
        ax.set_xlabel('Engagement Rate (%)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Users', fontsize=12, fontweight='bold')
        ax.set_title('Engagement Rate Distribution', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_posts_histogram(self, df: pd.DataFrame, bins: int = 20) -> plt.Figure:
        """Create posts distribution histogram"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.hist(df['PostsCount'], bins=bins, color=self.colors['success'], edgecolor='black', alpha=0.7)
        ax.axvline(df['PostsCount'].mean(), color=self.colors['danger'], linestyle='--', linewidth=2, label=f'Mean: {df["PostsCount"].mean():.1f}')
        
        ax.set_xlabel('Number of Posts', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Users', fontsize=12, fontweight='bold')
        ax.set_title('Posts Distribution', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_correlation_heatmap(self, df: pd.DataFrame) -> plt.Figure:
        """Create correlation matrix heatmap"""
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Calculate correlation
        numeric_cols = ['Age', 'PostsCount', 'Followers', 'EngagementRate']
        corr_matrix = df[numeric_cols].corr()
        
        # Create heatmap
        im = ax.imshow(corr_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
        
        # Set ticks and labels
        ax.set_xticks(range(len(numeric_cols)))
        ax.set_yticks(range(len(numeric_cols)))
        ax.set_xticklabels(numeric_cols, rotation=45, ha='right')
        ax.set_yticklabels(numeric_cols)
        
        # Add correlation values
        for i in range(len(numeric_cols)):
            for j in range(len(numeric_cols)):
                text = ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                             ha="center", va="center", color="black", fontweight='bold')
        
        ax.set_title('Correlation Matrix Heatmap', fontsize=14, fontweight='bold')
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Correlation Coefficient', fontsize=11, fontweight='bold')
        
        plt.tight_layout()
        return fig
    
    def create_age_group_comparison(self, df: pd.DataFrame) -> plt.Figure:
        """Create comparison chart by age groups"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Create age groups
        bins = [18, 25, 35, 45, 55, 65]
        labels = ['18-24', '25-34', '35-44', '45-54', '55-64']
        df_temp = df.copy()
        df_temp['AgeGroup'] = pd.cut(df_temp['Age'], bins=bins, labels=labels, right=False)
        
        # 1. Average Followers by Age Group
        age_followers = df_temp.groupby('AgeGroup')['Followers'].mean()
        axes[0, 0].bar(age_followers.index, age_followers.values, color=self.colors['primary'], edgecolor='black', alpha=0.7)
        axes[0, 0].set_title('Avg Followers by Age Group', fontweight='bold')
        axes[0, 0].set_ylabel('Average Followers')
        axes[0, 0].grid(True, alpha=0.3, axis='y')
        
        # 2. Average Posts by Age Group
        age_posts = df_temp.groupby('AgeGroup')['PostsCount'].mean()
        axes[0, 1].bar(age_posts.index, age_posts.values, color=self.colors['secondary'], edgecolor='black', alpha=0.7)
        axes[0, 1].set_title('Avg Posts by Age Group', fontweight='bold')
        axes[0, 1].set_ylabel('Average Posts')
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        # 3. Average Engagement by Age Group
        age_engagement = df_temp.groupby('AgeGroup')['EngagementRate'].mean()
        axes[1, 0].bar(age_engagement.index, age_engagement.values, color=self.colors['info'], edgecolor='black', alpha=0.7)
        axes[1, 0].set_title('Avg Engagement Rate by Age Group', fontweight='bold')
        axes[1, 0].set_ylabel('Engagement Rate (%)')
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # 4. User Count by Age Group
        age_count = df_temp['AgeGroup'].value_counts().sort_index()
        axes[1, 1].bar(age_count.index, age_count.values, color=self.colors['success'], edgecolor='black', alpha=0.7)
        axes[1, 1].set_title('User Count by Age Group', fontweight='bold')
        axes[1, 1].set_ylabel('Number of Users')
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return fig
    
    def create_box_plots(self, df: pd.DataFrame) -> plt.Figure:
        """Create box plots for numerical features"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Age
        axes[0, 0].boxplot([df['Age']], labels=['Age'], patch_artist=True,
                          boxprops=dict(facecolor=self.colors['primary'], alpha=0.7))
        axes[0, 0].set_title('Age Distribution', fontweight='bold')
        axes[0, 0].set_ylabel('Age (years)')
        axes[0, 0].grid(True, alpha=0.3, axis='y')
        
        # Followers
        axes[0, 1].boxplot([df['Followers']], labels=['Followers'], patch_artist=True,
                          boxprops=dict(facecolor=self.colors['secondary'], alpha=0.7))
        axes[0, 1].set_title('Followers Distribution', fontweight='bold')
        axes[0, 1].set_ylabel('Followers')
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        # Posts
        axes[1, 0].boxplot([df['PostsCount']], labels=['Posts'], patch_artist=True,
                          boxprops=dict(facecolor=self.colors['success'], alpha=0.7))
        axes[1, 0].set_title('Posts Distribution', fontweight='bold')
        axes[1, 0].set_ylabel('Number of Posts')
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # Engagement
        axes[1, 1].boxplot([df['EngagementRate']], labels=['Engagement'], patch_artist=True,
                          boxprops=dict(facecolor=self.colors['info'], alpha=0.7))
        axes[1, 1].set_title('Engagement Rate Distribution', fontweight='bold')
        axes[1, 1].set_ylabel('Engagement Rate (%)')
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return fig


if __name__ == "__main__":
    try:
        import sys
        sys.path.insert(0, '.')
        
        from src.data_loader import load_data, clean_data
        
        df = load_data('sample_facebook_data.xlsx')
        df = clean_data(df)
        
        viz = DataVisualizer()
        
        print("Creating visualizations...")
        
        fig1 = viz.create_age_histogram(df)
        fig1.savefig('charts/age_distribution.png', dpi=150, bbox_inches='tight')
        print("Age histogram saved")
        
        fig2 = viz.create_followers_histogram(df)
        fig2.savefig('charts/followers_distribution.png', dpi=150, bbox_inches='tight')
        print("Followers histogram saved")
        
        fig3 = viz.create_top_cities_bar(df)
        fig3.savefig('charts/top_cities.png', dpi=150, bbox_inches='tight')
        print("Top cities chart saved")
        
        fig4 = viz.create_scatter_posts_followers(df)
        fig4.savefig('charts/posts_vs_followers.png', dpi=150, bbox_inches='tight')
        print("Scatter plot saved")
        
        fig5 = viz.create_engagement_histogram(df)
        fig5.savefig('charts/engagement_distribution.png', dpi=150, bbox_inches='tight')
        print("Engagement histogram saved")
        
        fig6 = viz.create_correlation_heatmap(df)
        fig6.savefig('charts/correlation_heatmap.png', dpi=150, bbox_inches='tight')
        print("Correlation heatmap saved")
        
        print("\nAll visualizations created successfully!")
        
    except Exception as e:
        import traceback
        print(f"Error: {str(e)}")
        traceback.print_exc()
