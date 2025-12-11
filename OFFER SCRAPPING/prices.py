import pandas as pd
import re

# Load the CSV
df = pd.read_csv('hotpoint_all_fridges.csv')

def clean_price(price_str):
    if pd.isna(price_str) or price_str == 'N/A':
        return 0.0
    # Remove anything that is not a digit or dot
    cleaned = re.sub(r'[^\d.]', '', price_str)
    try:
        return float(cleaned)
    except:
        return 0.0

# Apply cleaning
df['Current Price Num'] = df['Current Price'].apply(clean_price)
df['Original Price Num'] = df['Original Price'].apply(clean_price)

# Optional: discount
df['Discount Amount'] = df['Original Price Num'] - df['Current Price Num']
df['Discount Amount'] = df['Discount Amount'].apply(lambda x: x if x > 0 else 0)

# Save cleaned CSV
df.to_csv('hotpoint_all_fridges_clean.csv', index=False)

print("Clean CSV saved as 'hotpoint_all_fridges_clean.csv'")
