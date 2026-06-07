import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Sample data generation
num_records = 250

# Muslim names lists
first_names = [
    'Mohammed', 'Ahmed', 'Ali', 'Omar', 'Hassan', 'Hussein', 'Hamza', 'Bilal', 
    'Zaid', 'Mustafa', 'Ibrahim', 'Yusuf', 'Sulaiman', 'Yahya', 'Idris',
    'Fatima', 'Aisha', 'Zainab', 'Maryam', 'Khadija', 'Sara', 'Hafsa', 
    'Layla', 'Noura', 'Sana', 'Amira', 'Farah', 'Zahra', 'Hana', 'Rania'
]

last_names = [
    'Khan', 'Ahmed', 'Ali', 'Malik', 'Sheikh', 'Syed', 'Hussain', 'Shah', 
    'Qureshi', 'Abbas', 'Siddiqui', 'Farooq', 'Zaman', 'Mirza', 'Lodhi',
    'Hashmi', 'Baig', 'Chaudhry', 'Ansari', 'Ghani', 'Iqbal', 'Raza'
]

def generate_muslim_name():
    return f"{random.choice(first_names)} {random.choice(last_names)}"

# City names
cities = ['Karachi', 'Lahore', 'Islamabad', 'Faisalabad', 'Rawalpindi', 
          'Multan', 'Hyderabad', 'Peshawar', 'Quetta', 'Gujranwala',
          'Sialkot', 'Jhang', 'Sargodha', 'Bahawalpur', 'Rahim Yar Khan']

# Generate data
data = {
    'UserID': range(1001, 1001 + num_records),
    'Name': [generate_muslim_name() for _ in range(num_records)],
    'Age': np.random.randint(18, 65, num_records),
    'City': np.random.choice(cities, num_records),
    'PostsCount': np.random.randint(1, 500, num_records),
    'Followers': np.random.randint(50, 50000, num_records),
    'EngagementRate': np.random.uniform(0.5, 10.0, num_records),
    'JoinDate': [datetime.now() - timedelta(days=random.randint(30, 1000)) for _ in range(num_records)]
}

# Create DataFrame
df = pd.DataFrame(data)

# Round engagement rate to 2 decimals
df['EngagementRate'] = df['EngagementRate'].round(2)

# Format join date to string
df['JoinDate'] = df['JoinDate'].dt.strftime('%Y-%m-%d')

# Save to Excel
output_path = 'sample_facebook_data.xlsx'
df.to_excel(output_path, index=False, sheet_name='FacebookData')

print(f"Sample data created successfully!")
print(f"File: {output_path}")
print(f"Records: {len(df)}")
print(f"\nFirst 5 rows:")
print(df.head())
