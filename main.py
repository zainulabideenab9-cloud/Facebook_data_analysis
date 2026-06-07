"""
Facebook Data Analysis Dashboard
Streamlit application for interactive data analysis and visualization
"""

import streamlit as st
import pandas as pd
import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_loader import load_data, clean_data, get_data_overview, get_statistical_summary, validate_data
from src.analyzer import DataAnalyzer
from src.visualizer import DataVisualizer


# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Facebook Data Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM STYLING (Theme-Aware) ====================
st.markdown("""
    <style>
    /* Theme-Aware Variables and Global Styles */
    :root {
        --fb-blue: #1877F2;
    }
    
    /* Navigation Bar Branding */
    .nav-logo {
        color: var(--fb-blue);
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        padding-bottom: 10px;
    }
    
    /* Professional Navbar Buttons */
    div.stButton > button {
        background-color: transparent;
        color: inherit;
        border: 1px solid transparent;
        padding: 8px 16px;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.2s ease;
        border-radius: 4px;
        width: 100%;
    }
    
    div.stButton > button:hover {
        background-color: rgba(128, 128, 128, 0.1);
        border-color: var(--fb-blue);
        color: var(--fb-blue);
    }
    
    div.stButton > button:focus:not(:active) {
        color: var(--fb-blue);
        background-color: rgba(24, 119, 242, 0.1);
    }

    /* Metric Box Styling */
    .metric-box {
        background-color: rgba(128, 128, 128, 0.05);
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid var(--fb-blue);
        margin-bottom: 15px;
    }

    /* Hide redundant sidebar navigation elements */
    [data-testid="stSidebarNav"] {
        display: none;
    }
    
    /* Main Content Spacing */
    .main .block-container {
        padding-top: 1.5rem;
    }

    /* Horizontal line styling */
    hr {
        margin: 1rem 0 !important;
        opacity: 0.2;
    }
    </style>
    """, unsafe_allow_html=True)


# ==================== SESSION STATE ====================
if 'df' not in st.session_state:
    st.session_state.df = None
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = None
if 'visualizer' not in st.session_state:
    st.session_state.visualizer = DataVisualizer()
if 'page' not in st.session_state:
    st.session_state.page = "Home"


# ==================== TOP NAVIGATION BAR ====================
# Using columns to create a modern responsive header
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, nav_col6 = st.columns([2.5, 1, 1, 1, 1, 1])

with nav_col1:
    st.markdown('<div class="nav-logo">Facebook Analytics</div>', unsafe_allow_html=True)

def set_page(name):
    st.session_state.page = name

with nav_col2:
    if st.button("Home", key="nav_home"):
        set_page("Home")
with nav_col3:
    if st.button("Overview", key="nav_overview"):
        set_page("Overview")
with nav_col4:
    if st.button("Analysis", key="nav_analysis"):
        set_page("Analysis")
with nav_col5:
    if st.button("Charts", key="nav_viz"):
        set_page("Visualizations")
with nav_col6:
    if st.button("Insights", key="nav_insights"):
        set_page("Detailed Insights")

st.markdown("---")

# ==================== SIDEBAR ====================
st.sidebar.title("Data Control")

# Data loading section
st.sidebar.header("Data Ingestion")
uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=['xlsx', 'xls'])

if uploaded_file is not None:
    try:
        with open('temp_data.xlsx', 'wb') as f:
            f.write(uploaded_file.getvalue())
        
        st.session_state.df = load_data('temp_data.xlsx')
        st.session_state.df = clean_data(st.session_state.df)
        st.session_state.analyzer = DataAnalyzer(st.session_state.df)
        st.sidebar.success("Data loaded successfully")
    except Exception as e:
        st.sidebar.error(f"Error loading file: {str(e)}")
else:
    if st.sidebar.button("Load Sample Data"):
        try:
            st.session_state.df = load_data('sample_facebook_data.xlsx')
            st.session_state.df = clean_data(st.session_state.df)
            st.session_state.analyzer = DataAnalyzer(st.session_state.df)
            st.sidebar.success("Sample data loaded")
        except Exception as e:
            st.sidebar.error(f"Error: {str(e)}")


# ==================== MAIN CONTENT ====================
def render_home():
    """Render home page"""
    st.title("Facebook Data Analysis Dashboard")
    st.markdown("""
    This project provides a comprehensive analytical framework for exploring Facebook demographic and engagement data. 
    By utilizing advanced statistical modeling and high-fidelity visualizations, the dashboard transforms raw user 
    datasets into actionable behavioral intelligence.
    """)
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### Core Purpose
        Analyze Facebook user data to derive actionable insights about:
        - User demographics and age distributions
        - Engagement patterns and content reach
        - Geographic distribution across major hubs
        """)
    
    with col2:
        st.markdown("""
        ### Technical Stack
        - **Pandas & NumPy** - Data manipulation and vectorized operations
        - **Matplotlib** - Professional static visualizations
        - **Streamlit** - Modern reactive web interface
        - **Python** - Core programming logic
        """)
    
    with col3:
        st.markdown("""
        ### System Features
        - Automated data ingestion and validation
        - Multi-dimensional statistical analysis
        - High-fidelity correlation heatmaps
        - Interactive filtering and data export
        """)
    
    st.markdown("---")
    
    if st.session_state.df is not None:
        st.info("Data is loaded. Use the navigation above to explore the analysis.")
    else:
        st.warning("Please load the dataset using the sidebar to begin analysis.")


def render_overview():
    """Render data overview page"""
    if st.session_state.df is None:
        st.warning("Please load data first")
        return
    
    st.title("Data Overview")
    st.markdown("Initial snapshot and validation metrics of the current dataset.")
    st.markdown("---")
    
    df = st.session_state.df
    
    # Data summary
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        st.metric("Total Columns", len(df.columns))
    with col3:
        st.metric("Unique Cities", df['City'].nunique())
    with col4:
        st.metric("Missing Values", df.isnull().sum().sum())
    
    st.markdown("---")
    
    # Validation
    st.subheader("Data Integrity Validation")
    valid, issues = validate_data(df)
    
    if valid:
        st.success("System-wide data validation passed successfully.")
    else:
        st.warning("Data validation issues identified:")
        for issue in issues:
            st.write(f"- {issue}")
    
    st.markdown("---")
    
    # Display data
    st.subheader("Dataset Preview")
    col1, col2 = st.columns(2)
    
    with col1:
        num_rows = st.slider("Rows to display:", 5, len(df), 15)
    with col2:
        if st.checkbox("Show all schema columns"):
            st.dataframe(df.head(num_rows), use_container_width=True)
        else:
            st.dataframe(df[['Name', 'Age', 'City', 'Followers', 'PostsCount', 'EngagementRate']].head(num_rows), use_container_width=True)
    
    st.markdown("---")
    
    # Statistical summary
    st.subheader("Variable Distribution Summary")
    st.dataframe(get_statistical_summary(df), use_container_width=True)


def render_analysis():
    """Render detailed analysis page"""
    if st.session_state.analyzer is None:
        st.warning("Please load data first")
        return
    
    st.title("Statistical Analysis")
    st.markdown("Deep-dive metrics across all core behavioral dimensions.")
    st.markdown("---")
    
    analyzer = st.session_state.analyzer
    
    # Tabs for different analyses
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Age", "Followers", "Posts", "Engagement", "Correlations"])
    
    # Age Analysis
    with tab1:
        st.subheader("Demographic Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        age_stats = analyzer.get_age_statistics()
        
        with col1:
            st.metric("Mean Age", f"{age_stats['mean']} years")
        with col2:
            st.metric("Median Age", f"{age_stats['median']} years")
        with col3:
            st.metric("Minimum Age", f"{age_stats['min']} years")
        with col4:
            st.metric("Maximum Age", f"{age_stats['max']} years")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Standard Deviation", f"{age_stats['std_dev']} years")
        with col2:
            st.metric("Interquartile Range", f"{age_stats['q75'] - age_stats['q25']} years")
    
    # Followers Analysis
    with tab2:
        st.subheader("Network Reach Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        followers_stats = analyzer.get_followers_statistics()
        
        with col1:
            st.metric("Average Followers", f"{followers_stats['mean']:.0f}")
        with col2:
            st.metric("Median Followers", f"{followers_stats['median']:.0f}")
        with col3:
            st.metric("Peak Reach", f"{followers_stats['max']:.0f}")
        with col4:
            st.metric("Minimum Reach", f"{followers_stats['min']:.0f}")
        
        st.markdown("---")
        st.subheader("Top Performers by Network Size")
        top_users = analyzer.get_top_users_by_followers(10)
        st.dataframe(top_users, use_container_width=True)
    
    # Posts Analysis
    with tab3:
        st.subheader("Content Output Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        posts_stats = analyzer.get_posts_statistics()
        
        with col1:
            st.metric("Average Output", f"{posts_stats['mean']:.1f} posts")
        with col2:
            st.metric("Aggregate Output", f"{posts_stats['total_posts']} posts")
        with col3:
            st.metric("Maximum Output", f"{posts_stats['max']} posts")
        with col4:
            st.metric("Minimum Output", f"{posts_stats['min']} posts")
        
        st.markdown("---")
        st.subheader("Most Active Content Creators")
        top_posters = analyzer.get_top_posters(10)
        st.dataframe(top_posters, use_container_width=True)
    
    # Engagement Analysis
    with tab4:
        st.subheader("Interaction Efficiency Analysis")
        col1, col2, col3 = st.columns(3)
        
        engagement_stats = analyzer.get_engagement_statistics()
        
        with col1:
            st.metric("Mean Engagement", f"{engagement_stats['mean']:.2f}%")
        with col2:
            st.metric("Maximum Engagement", f"{engagement_stats['max']:.2f}%")
        with col3:
            st.metric("Median Engagement", f"{engagement_stats['median']:.2f}%")
        
        st.markdown("---")
        
        # High engagement users
        threshold = st.slider("Filter by Engagement Threshold (%)", 0.0, 10.0, 7.0, 0.5)
        st.subheader(f"High-Performing Users (Engagement >= {threshold}%)")
        high_eng = analyzer.get_high_engagement_users(threshold, 10)
        st.dataframe(high_eng, use_container_width=True)
    
    # Correlations
    with tab5:
        st.subheader("Inter-Variable Correlation Matrix")
        
        corr_insights = analyzer.get_correlation_insights()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Age vs Network Size", f"{corr_insights['age_vs_followers']:.3f}")
        with col2:
            st.metric("Age vs Efficiency", f"{corr_insights['age_vs_engagement']:.3f}")
        with col3:
            st.metric("Activity vs Network Size", f"{corr_insights['posts_vs_followers']:.3f}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Activity vs Efficiency", f"{corr_insights['posts_vs_engagement']:.3f}")
        with col2:
            st.metric("Network Size vs Efficiency", f"{corr_insights['followers_vs_engagement']:.3f}")


def render_visualizations():
    """Render visualization page"""
    if st.session_state.analyzer is None:
        st.warning("Please load data first")
        return
    
    st.title("Analytical Visualizations")
    st.markdown("Graphical interpretation of the dataset dimensions and statistical relationships.")
    st.markdown("---")
    
    df = st.session_state.df
    viz = st.session_state.visualizer
    
    # Visualization selection
    col1, col2 = st.columns(2)
    
    with col1:
        viz_type = st.selectbox(
            "Select Graphical Component:",
            ["Age Distribution", "Followers Distribution", "Posts Distribution", 
             "Engagement Rate", "Posts vs Followers", "Correlation Matrix",
             "Age Group Analysis", "Box Plots", "Top Cities"]
        )
    
    if viz_type == "Age Distribution":
        st.subheader("User Age Distribution Frequency")
        fig = viz.create_age_histogram(df)
        st.pyplot(fig)
    
    elif viz_type == "Followers Distribution":
        st.subheader("Network Reach Distribution Frequency")
        fig = viz.create_followers_histogram(df)
        st.pyplot(fig)
    
    elif viz_type == "Posts Distribution":
        st.subheader("Content Output Distribution Frequency")
        fig = viz.create_posts_histogram(df)
        st.pyplot(fig)
    
    elif viz_type == "Engagement Rate":
        st.subheader("Efficiency Distribution Frequency")
        fig = viz.create_engagement_histogram(df)
        st.pyplot(fig)
    
    elif viz_type == "Posts vs Followers":
        st.subheader("Relationship Analysis: Activity vs Reach")
        fig = viz.create_scatter_posts_followers(df)
        st.pyplot(fig)
    
    elif viz_type == "Correlation Matrix":
        st.subheader("Statistical Dependence Heatmap")
        fig = viz.create_correlation_heatmap(df)
        st.pyplot(fig)
    
    elif viz_type == "Age Group Analysis":
        st.subheader("Demographic Performance Comparison")
        fig = viz.create_age_group_comparison(df)
        st.pyplot(fig)
    
    elif viz_type == "Box Plots":
        st.subheader("Statistical Moment Distributions")
        fig = viz.create_box_plots(df)
        st.pyplot(fig)
    
    elif viz_type == "Top Cities":
        st.subheader("Geographical Concentration hubs")
        top_n = st.slider("Select Top N Cities:", 5, 15, 10)
        fig = viz.create_top_cities_bar(df, top_n)
        st.pyplot(fig)


def render_detailed_insights():
    """Render detailed insights page"""
    if st.session_state.analyzer is None:
        st.warning("Please load data first")
        return
    
    st.title("Granular Insights")
    st.markdown("Aggregated metrics and interactive filtering for targeted data exploration.")
    st.markdown("---")
    
    analyzer = st.session_state.analyzer
    df = st.session_state.df
    
    # City Analysis
    st.subheader("Geographical Performance Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Urban Distribution")
        city_dist = analyzer.get_city_distribution()
        st.dataframe(city_dist, use_container_width=True)
    
    with col2:
        st.markdown("#### Regional Statistics")
        city_stats = analyzer.get_city_statistics()
        st.dataframe(city_stats, use_container_width=True)
    
    st.markdown("---")
    
    # Age Group Analysis
    st.subheader("Demographic Segment Analysis")
    age_group_analysis = analyzer.get_age_group_analysis()
    st.dataframe(age_group_analysis, use_container_width=True)
    
    st.markdown("---")
    
    # Filters
    st.subheader("Dynamic Multi-Parameter Filters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_cities = st.multiselect(
            "Target Metropolitan Areas:",
            df['City'].unique(),
            default=df['City'].unique()[:3]
        )
    
    with col2:
        age_range = st.slider(
            "Demographic Range Selection:",
            int(df['Age'].min()), int(df['Age'].max()), 
            (int(df['Age'].min()), int(df['Age'].max()))
        )
    
    with col3:
        min_followers = st.number_input(
            "Minimum Network Reach Threshold:",
            min_value=int(df['Followers'].min()),
            max_value=int(df['Followers'].max()),
            value=int(df['Followers'].min())
        )
    
    # Apply filters
    filtered_df = df[
        (df['City'].isin(selected_cities)) &
        (df['Age'] >= age_range[0]) &
        (df['Age'] <= age_range[1]) &
        (df['Followers'] >= min_followers)
    ]
    
    st.markdown("---")
    st.subheader(f"Refined Results Segment ({len(filtered_df)} records)")
    st.dataframe(filtered_df, use_container_width=True)
    
    st.markdown("---")
    
    # Download option
    st.subheader("Data Export")
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Export Filtered Segment as CSV",
        data=csv,
        file_name="facebook_data_analysis_export.csv",
        mime="text/csv"
    )


# ==================== ROUTE PAGES ====================
if st.session_state.page == "Home":
    render_home()
elif st.session_state.page == "Overview":
    render_overview()
elif st.session_state.page == "Analysis":
    render_analysis()
elif st.session_state.page == "Visualizations":
    render_visualizations()
elif st.session_state.page == "Detailed Insights":
    render_detailed_insights()


# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px; font-size: 0.9rem;'>
    <p>Facebook Data Analysis Framework v1.2</p>
    <p>Developed with Streamlit | Powered by the Python Scientific Stack</p>
    </div>
    """, unsafe_allow_html=True)
