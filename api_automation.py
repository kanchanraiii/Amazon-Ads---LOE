import requests
import json

# API Credentials (Example placeholders)
SELLER_ID = "YOUR_SELLER_ID"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"

# Function to update listing
def update_amazon_listing(asin, updated_description):
    url = f"https://sellingpartnerapi.amazon.com/listings/v2021-08-01/items/{SELLER_ID}"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "productType": "PRODUCT",
        "attributes": {
            "item_name": "Updated Product Title",
            "item_description": updated_description
        }
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        print(f"Successfully updated {asin}")
    else:
        print(f"Failed to update {asin}: {response.text}")

# Read optimized data
df = pd.read_csv("optimized_products.csv")

# Loop through products and update listings
for index, row in df.iterrows():
    update_amazon_listing(row["ASIN"], row["Optimized_Description"])
