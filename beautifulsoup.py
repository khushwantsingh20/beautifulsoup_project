import requests
from bs4 import BeautifulSoup
import csv

# Function to extract product links from the category page
def get_product_links(category_url):
    response = requests.get(category_url)
    if response.status_code != 200:
        print(f"Failed to retrieve category page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    product_links = []

    # Adjust the selector to find product links
    product_containers = soup.find_all('a', class_='product-grid-item__link')  # Update this selector as needed
    if not product_containers:
        print("No product links found.")

    for link in product_containers:
        href = link.get('href')
        if href:
            product_links.append(---URL---)  # Adjust base URL if needed

    print(f"Found {len(product_links)} product links.")
    return product_links

# Function to extract product details from each product page
def extract_product_details(product_url):
    response = requests.get(product_url)
    if response.status_code != 200:
        print(f"Failed to retrieve product page {product_url}. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract product title
    title_tag = soup.find('h1', class_='productView-title')  # Update class as needed
    title = title_tag.get_text(strip=True) if title_tag else 'N/A'

    # Extract image URL
    img_tag = soup.find('img', id='product-featured-image-37518145126698')  # Update ID or use another selector
    image_url = img_tag['src'] if img_tag else 'N/A'

    # Extract price
    price_tag = soup.find('span', class_='price-item--sale')  # Update class as needed
    price = price_tag.get_text(strip=True) if price_tag else 'N/A'

    # Extract description
    desc_tag = soup.find('p')  # Update to a more specific selector if needed
    description = desc_tag.get_text(strip=True) if desc_tag else 'N/A'

    # Extract variant options
    variants = []
    select_element = soup.find('select', class_='select__select')  # Update class as needed
    if select_element:
        options = [option.get_text(strip=True) for option in select_element.find_all('option')]
        variants = options

    # Extract category (static as per your requirement)
    category = '--category--'  # Update if needed

    return {
        'Title': title,
        'Image URL': image_url,
        'Price': price,
        'Description': description,
        'Variants': ', '.join(variants),
        'Category': category
    }

# Main function to scrape the data and save to CSV
def main():
    base_url = '----url------'  # Replace with actual category URL
    product_links = get_product_links(base_url)
    products = []

    for link in product_links:
        product = extract_product_details(link)
        if product:
            products.append(product)

    # Check if products were collected
    if not products:
        print("No products were collected. Please check the scraping logic.")
        return

    # Write to CSV
    with open('products.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Image URL', 'Price', 'Description', 'Variants', 'Category']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for product in products:
            writer.writerow(product)

    print("Data successfully saved to 'products.csv'")

# Run the script
if __name__ == "__main__":
    main()


