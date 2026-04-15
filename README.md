# Taipei House Rental Price Predictor

A full-stack Machine Learning application designed to scrape, analyze, and predict rental prices in Taipei City. This project covers the entire data engineering pipeline: from automated web scraping and data cleaning to model training and deployment via FastAPI.

## Key Features

- **Data Acquisition**: Interactive CLI scraper targeting Taipei rental listings from great-home.com.tw
- **Data Cleaning & EDA**: Visual analysis using Pandas and Seaborn to identify market trends and price correlations
- **Machine Learning**: XGBoost gradient boosting model trained on district, size, rooms, halls, bathrooms, and age
- **Real-time API**: FastAPI-powered prediction service with Pydantic validation
- **Modern Web UI**: Responsive frontend built with Tailwind CSS and Fetch API
- **Containerization**: Docker support for consistent deployment

## Project Structure

```
house-price-predictor/
├── data/                    # Raw CSV and SQLite database files
├── models/                  # Trained XGBoost model and column encoder (.pkl)
├── src/
│   ├── __init__.py
│   ├── scraper.py           # HouseScraper class for web scraping
│   ├── database.py          # Database class for SQLite operations
│   └── utils.py             # Utility functions
├── static/
│   └── index.html           # Web UI (Tailwind CSS + Fetch API)
├── app.py                   # FastAPI application (prediction endpoint)
├── train_model.py           # Model training script
├── main.py                  # Interactive CLI for data collection
├── analysis.py              # EDA visualizations (district analysis, correlations)
├── Dockerfile               # Container configuration
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Installation & Setup

### Option 1: Docker (Recommended)

1. Build the image:
   ```bash
   docker build -t house-price-app .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 house-price-app
   ```

3. Access the UI at `http://localhost:8000`

### Option 2: Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the API:
   ```bash
   uvicorn app:app --reload
   ```

## Tech Stack

- **Language**: Python 3.12
- **ML & Data**: Scikit-learn, XGBoost, Pandas, NumPy, Seaborn, Matplotlib
- **API Framework**: FastAPI, Pydantic, Uvicorn
- **Frontend**: HTML5, Tailwind CSS, JavaScript (Fetch API)
- **Database**: SQLite
- **DevOps**: Docker

## License

This project is licensed under the MIT License.