
# Facebook Data Analysis Application

An analytical system designed for processing and visualizing large scale Facebook demographic and engagement data.

## Problem Statement

Manual analysis of social media datasets is inherently inefficient and prone to human error. Digital marketing professionals and demographic researchers often face challenges in:
- Extracting meaningful trends from raw Excel datasets.
- Maintaining data integrity during manual cleaning processes.
- Visualizing complex correlations between user activity and network reach.
- Accessing real-time, interactive insights without deep technical expertise in data science.

## Proposed Solution

The Facebook Data Analysis Framework provides an automated, end-to-end pipeline that transforms raw social media data into actionable intelligence. By utilizing a modular Python architecture, the system ensures:
- **Automated Ingestion**: Seamless handling of Excel-based data sources.
- **Strict Validation**: Programmatic checks to ensure data accuracy and structural integrity.
- **Multidimensional Analysis**: Vectorized statistical computations for demographics and engagement.
- **High-Fidelity Visualization**: Publication-quality graphical representations.
- **Interactive Interface**: A reactive dashboard for user-driven data exploration.

## Modules in this Project

### 1. Data Loader Module (`src/data_loader.py`)
The gateway for all incoming data. It handles the initial extraction from Excel workbooks, validates the presence of required schema attributes (UserID, Name, Age, etc.), and performs sanitization tasks such as removing duplicates and normalizing data types.

### 2. Data Analyzer Module (`src/analyzer.py`)
The computational core of the system. It uses the pandas and NumPy libraries to perform high-speed statistical calculations. This module is responsible for computing demographic distributions, city-wise metrics, and complex Pearson correlation matrices between variables like post count and engagement rates.

### 3. Data Visualizer Module (`src/visualizer.py`)
The visualization engine responsible for rendering data into intuitive charts. It produces various plot types including age distribution histograms, scatter plots for engagement analysis, and heatmaps for identifying statistical dependencies between metrics.

### 4. Main Interface (`main.py`)
The orchestration layer built with Streamlit. It integrates all the backend modules into a cohesive web application, providing users with interactive filters, data previews, and real-time visualization updates.

## How to Run the Project

Follow these steps to deploy the application in a local environment:

### Prerequisites
- Python 3.8 or higher installed.
- Pip package manager.

### Execution Steps
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   streamlit run main.py
   ```
   The dashboard will automatically open in your default browser at http://localhost:8501.

3. **Refresh Sample Data**:
   If you wish to reset or generate a new synthetic dataset:
   ```bash
   python generate_sample_data.py
   ```

## Conclusion

The Facebook Data Analysis Framework demonstrates a robust approach to social media analytics through modular engineering. By separating data ingestion, analysis, and visualization into autonomous components, the system achieves high reliability and maintainability. This project can serve as a comprehensive tool for understanding demographic patterns and engagement dynamics within social networks.

---
