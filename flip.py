import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_flipkart_products(query, page_length=4, output_csv="flipkart_product_data.csv"):
    """
    Scrapes Flipkart search results for a given query and number of pages using only Selenium.
    
    Args:
        query (str): Search query (e.g., "laptop").
        page_length (int): Number of pages to scrape.
        output_csv (str): CSV file to save the results.
    
    Returns:
        pd.DataFrame: DataFrame containing the scraped product data.
    """
    product_data = []
    driver = webdriver.Chrome()  # Adjust path if needed

    base_url = ("https://www.flipkart.com/search?q={query}"
                "&otracker=search&otracker1=search&marketplace=FLIPKART"
                "&as-show=on&as=off&page={page}")

    for page in range(1, page_length + 1):
        url = base_url.format(query=query, page=page)
        driver.get(url)
        
        # Wait until product elements are loaded
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "_75nlfW"))
            )
        except Exception as e:
            print(f"Error on page {page}: {e}")
            continue

        # Additional pause to allow dynamic content to load
        time.sleep(2)
        products = driver.find_elements(By.CLASS_NAME, "_75nlfW")
        print(f"Page {page}: Found {len(products)} products.")
        
        for product in products:
            d = {}
            # Extract title (from class "KzDlHZ"), truncate to 22 characters
            try:
                title_elem = product.find_element(By.CLASS_NAME, "KzDlHZ")
                d["title"] = title_elem.text.strip()[:29]
            except Exception:
                d["title"] = "N/A"
            
            # Extract link (from class "CGtC98")
            try:
                link_elem = product.find_element(By.CLASS_NAME, "CGtC98")
                href = link_elem.get_attribute("href")
                d["link"] = f"{href}" if href else "N/A"
            except Exception:
                d["link"] = "N/A"
            
            # Extract price (from class "Nx9bqj" or combined class "Nx9bqj _4b5DiR")
            try:
                price_elem = product.find_element(By.CSS_SELECTOR, "div._30jeq3")
                d["price"] = price_elem.text.strip()
            except Exception:
                d["price"] = "N/A"
            
            # Extract offer (discount) from class "UkUFwK"
            try:
                offer_elem = product.find_element(By.CLASS_NAME, "UkUFwK")
                d["offer"] = offer_elem.text.strip()
            except Exception:
                d["offer"] = "N/A"
            
            # Extract rating from class "XQDdHH"
            try:
                rating_elem = product.find_element(By.CLASS_NAME, "XQDdHH")
                d["rating"] = rating_elem.text.strip()
            except Exception:
                d["rating"] = "N/A"
            
            product_data.append(d)
        time.sleep(1)

    driver.quit()
    
    # Convert the list of dictionaries into a DataFrame and save as CSV
    df = pd.DataFrame(product_data)
    df.to_csv(output_csv, index=False)
    print(f"Data saved successfully to {output_csv}.")
    return df

# Example usage:
if __name__ == "__main__":
    scrape_flipkart_products("laptop", page_length=4)






