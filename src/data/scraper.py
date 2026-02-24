from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import random
import os


def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    return driver


def scrape_domain_sold(num_pages=3):
    driver = get_driver()
    properties = []

    for page in range(1, num_pages + 1):
        url = f"https://www.domain.com.au/sold-listings/sydney-region-nsw/?page={page}"
        print(f"Scraping page {page}...")

        try:
            driver.get(url)
            time.sleep(random.uniform(3, 5))

            # Find listings
            listings = driver.find_elements(
                By.CSS_SELECTOR,
                "[data-testid='listing-card-wrapper-premiumplus'], [data-testid='listing-card-wrapper-standard']",
            )
            print(f"Found {len(listings)} listings on page {page}")

            for listing in listings:
                try:
                    # Price
                    try:
                        price = listing.find_element(
                            By.CSS_SELECTOR, "[data-testid='listing-card-price']"
                        ).text.strip()
                    except:
                        price = None

                    # Suburb
                    try:
                        suburb = listing.find_element(
                            By.CSS_SELECTOR, "[data-testid='address-line2']"
                        ).text.strip()
                    except:
                        suburb = None

                    # Features
                    try:
                        features = listing.find_elements(
                            By.CSS_SELECTOR,
                            "[data-testid='property-features-text-container']",
                        )
                        beds = features[0].text.strip() if len(features) > 0 else None
                        baths = features[1].text.strip() if len(features) > 1 else None
                        parking = (
                            features[2].text.strip() if len(features) > 2 else None
                        )
                    except:
                        beds = baths = parking = None

                    # Property type
                    try:
                        property_type = listing.find_element(
                            By.CSS_SELECTOR,
                            "span[class*='property-type'], [data-testid='listing-card-property-type'], span[class*='PropertyType']",
                        ).text.strip()
                    except:
                        try:
                            property_type = listing.find_element(
                                By.XPATH,
                                ".//span[contains(@class, 'type') or contains(@class, 'Type')]",
                            ).text.strip()
                        except:
                            property_type = "House"  # default fallback

                    properties.append(
                        {
                            "suburb": suburb,
                            "price": price,
                            "bedrooms": beds,
                            "bathrooms": baths,
                            "parking": parking,
                            "property_type": property_type,
                        }
                    )

                except Exception as e:
                    print(f"Error parsing listing: {e}")
                    continue

        except Exception as e:
            print(f"Error on page {page}: {e}")
            continue

        time.sleep(random.uniform(2, 4))

    driver.quit()
    return pd.DataFrame(properties)


if __name__ == "__main__":
    print("Starting Domain.com.au scraper...")
    df = scrape_domain_sold(num_pages=3)

    print(f"\nCollected {len(df)} properties")
    print(df.head())

    os.makedirs("data/validation", exist_ok=True)
    df.to_csv("data/validation/real_world_validation.csv", index=False)
    print("Saved to data/validation/real_world_validation.csv")
