# house-price-predictor
# Main entry point for the application

from src.scraper import Scraper
from src.database import Database
from src.utils import some_utility_function

def main():
    # Initialize components
    scraper = Scraper()
    database = Database()

    # Example usage
    # scraper.scrape_data()
    # database.save_data(data)

    print("House Price Predictor is running!")

if __name__ == "__main__":
    main()