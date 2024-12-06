import pandas as pd

# Mock transaction data
data = {
    'transaction_id': [1, 2, 3, 4, 5, 6],
    'customer_id': ['C001', 'C002', 'C003', 'C001', 'C004', 'C002'],
    'amount': [150.0, 200.0, 450.0, 3000.0, 500.0, 50.0],
    'date': ['2024-12-05', '2024-12-05', '2024-12-05', '2024-12-05', '2024-12-05', '2024-12-05']
}

# Step 1: Create a DataFrame
df = pd.DataFrame(data)

# Step 2: Data Cleaning
# Remove missing values
df.dropna(inplace=True)

# Ensure correct data types
df['amount'] = df['amount'].astype(float)
df['date'] = pd.to_datetime(df['date'])

# Step 3: Generate Daily Sales Summary
daily_sales_summary = df.groupby('date')['amount'].sum().reset_index()

# Step 4: Identify Outliers using the IQR method
Q1 = df['amount'].quantile(0.25)  # First quartile
Q3 = df['amount'].quantile(0.75)  # Third quartile
IQR = Q3 - Q1  # Interquartile range

# Calculate bounds for outliers
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Identify outliers
outliers = df[(df['amount'] < lower_bound) | (df['amount'] > upper_bound)]

# Step 5: Save Results to an Excel File
with pd.ExcelWriter('transaction_data_summary.xlsx') as writer:
    df.to_excel(writer, sheet_name='Individual Transactions', index=False)
    daily_sales_summary.to_excel(writer, sheet_name='Daily Sales Summary', index=False)
    outliers.to_excel(writer, sheet_name='Outliers', index=False)

# Step 6: Display Results
print("Daily Sales Summary:")
print(daily_sales_summary)

print("\nOutliers:")
print(outliers)

print("\nExcel file 'transaction_data_summary.xlsx' has been generated with the results.")
