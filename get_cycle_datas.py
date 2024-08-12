import csv
import requests
from lxml import html
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Define the XPaths
# Define the XPaths
xpaths = {
    'Price': '/html/body/div[2]/div[2]/div[3]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/text()',
    'Brand': '/html/body/div[2]/div[2]/div[3]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[3]/div[2]',
    'Year': '/html/body/div[2]/div[2]/div[3]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[5]/div[2]',
    'Type': '/html/body/div[2]/div[2]/div[3]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[6]/div[2]',
    'Km': '/html/body/div[2]/div[2]/div[3]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[7]/div[2]',
    'Gear': '/html/body/div[2]/div[2]/div[3]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[8]/div[2]',
    'Fuel Type': '/html/body/div[2]/div[2]/div[3]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[9]/div[2]',
    'Engine volume': '/html/body/div[2]/div[2]/div[3]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[10]/div[2]',
    'engine power': '/html/body/div[2]/div[2]/div[3]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[11]/div[2]',
}

# Check if the URLs file exists
try:
    with open('urls.txt', 'r') as f:
        urls = f.read().splitlines()
except FileNotFoundError:
    print("The 'urls.txt' file does not exist in the current directory.")
    exit(1)

# Check if the URLs file is empty
if not urls:
    print("The 'urls.txt' file is empty.")
    exit(1)

# Initialize a list to store the data
data = []

# For each URL
for url in urls:
    print(f"Processing URL: {url}")
    # Make a request to the URL
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to fetch the web page: {url}")
        continue
    # Parse the HTML content
    tree = html.fromstring(response.content)
    # Initialize a dictionary to store the data for this URL
    row = {}
    # For each XPath and if
    for key, xpath in xpaths.items():
        result = tree.xpath(xpath)
        if result:
            if xpath.endswith('/text()'):
                row[key] = result[0].strip()
            else:
                row[key] = result[0].text_content().strip()
        else:
            print(f"Failed to extract data using XPath: {xpath}")
            row[key] = None
    # Add the dictionary to the list
    data.append(row)

le = LabelEncoder()

# Write the data to a CSV file
with open('motors.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=xpaths.keys())
    writer.writeheader()
    writer.writerows(data)

df = pd.DataFrame(data)

# Apply LabelEncoder to the 'Gear' column
df['Gear'] = le.fit_transform(df['Gear'])
df['Fuel Type'] = le.fit_transform(df['Fuel Type'])
df['Type'] = le.fit_transform(df['Type'])
df['Brand'] = le.fit_transform(df['Brand'])

df['Price'] = df['Price'].str.replace(' TL', '').str.replace('.', '')
df['Km'] = df['Km'].str.replace(' km', '').str.replace('.', '')
df['Engine volume'] = df['Engine volume'].str.replace(' cm3', '')
df['engine power'] = df['engine power'].str.replace(' hp', '')

# Write the DataFrame to a CSV file
df.to_csv('motors.csv', index=False)