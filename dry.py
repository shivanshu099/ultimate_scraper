import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_amazon_products(query, page_length=4, output_csv="amazon_product_data.csv"):
    """
    Scrapes Amazon India search results for a given query across a specified number of pages.
    
    Args:
        query (str): Search query (e.g., "laptop").
        page_length (int): Number of pages to scrape.
        output_csv (str): File path for saving the output CSV.
        
    Returns:
        pd.DataFrame: DataFrame containing the scraped product data.
    """
    # Initialize Selenium WebDriver
    driver = webdriver.Chrome()  # Adjust path if needed
    product_data = []
    base_url = "https://www.amazon.in/s?k={query}&page={page}"

    for page in range(1, page_length + 1):
        url = base_url.format(query=query, page=page)
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".s-main-slot")))
        except Exception as e:
            print(f"Timeout or error waiting for page {page}: {e}")
        time.sleep(5)  # Additional wait for dynamic content

        # Locate product cards using an XPath that filters items with a valid data-asin attribute
        product_cards = driver.find_elements(By.XPATH, "//div[contains(@class, 's-result-item') and @data-asin]")
        print(f"Page {page}: Found {len(product_cards)} products.")

        for card in product_cards:
            d = {}
            # Title extraction (truncate to first 29 characters)
            try:
                title_elem = card.find_element(By.TAG_NAME, "h2")
                title = title_elem.text.strip()
                d["title"] = title[:29]
            except Exception:
                d["title"] = "N/A"

            # Link extraction: Get the href attribute from the first anchor with class 'a-link-normal'
            try:
                link_elem = card.find_element(By.CSS_SELECTOR, "a.a-link-normal")
                href = link_elem.get_attribute("href")
                d["link"] = href if href.startswith("http") else "https://www.amazon.in" + href
            except Exception:
                d["link"] = "N/A"

            # Price extraction: Use the whole price part from the element with class 'a-price-whole'
            try:
                price_elem = card.find_element(By.CSS_SELECTOR, "span.a-price-whole")
                d["price"] = price_elem.text.strip()
            except Exception:
                d["price"] = "N/A"

            # Offer extraction: Look for any text containing 'off' (e.g., "(31% off)")
            try:
                offer_elem = card.find_element(By.XPATH, ".//*[contains(text(), 'off')]")
                match = re.search(r'\(?(\d+% off)\)?', offer_elem.text)
                d["offer"] = match.group(1) if match else offer_elem.text.strip()
            except Exception:
                d["offer"] = "N/A"

            # Rating extraction: Usually found in an element with class 'a-icon-alt'
            try:
                rating_elem = card.find_element(By.CSS_SELECTOR, "span.a-icon-alt")
                d["rating"] = rating_elem.text.strip()
            except Exception:
                d["rating"] = "N/A"

            product_data.append(d)
        time.sleep(1)

    driver.quit()

    # Convert collected data to a DataFrame and save to CSV
    df = pd.DataFrame(product_data)
    df.to_csv(output_csv, index=False)
    print(f"Data saved successfully to {output_csv}.")
    return df

# Example usage:
if __name__ == "__main__":
    df = scrape_amazon_products("laptop", 4)











