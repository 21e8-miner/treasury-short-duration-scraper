# Treasury Short Duration Scraper

This repository provides a real-time scraping and visualization tool for treasury-related data with a focus on short-duration financial instruments. Utilizing a combination of Python for backend data-fetching and Chart.js for frontend visualization, it enables users to access, monitor, and analyze treasury market trends dynamically.

## Features

- **Real-Time Data Fetching**: Retrieves live treasury data via API calls.
- **Interactive Dashboard**: Visualizes real-time data using Chart.js on the web.
- **Python-Powered Engine**: Backend built with Flask and real-time processing capabilities.
- **Customizable and Extendable**: Designed for adding more features or adapting to additional treasury data sources.

## How It Works

1. **Backend (Python)**: Fetches real-time data from an external API.
2. **Flask API**: Serves fetched data to the frontend.
3. **Frontend (HTML + JavaScript)**: Displays the data in an interactive, auto-refreshing dashboard.

### Running the Application

1. Clone this repository:
   ```bash
   git clone https://github.com/21e8-miner/treasury-short-duration-scraper.git
   ```

2. Navigate into the directory:
   ```bash
   cd treasury-short-duration-scraper
   ```

3. Install dependencies (use a virtual environment if needed):
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask server:
   ```bash
   python app.py
   ```

5. Open a browser and navigate to `http://127.0.0.1:5000` to view the dashboard.

### File Structure

- `real_time_data_fetcher.py`: Backend script for data fetching.
- `app.py`: Flask API for serving data.
- `templates/index.html`: Interactive dashboard for data visualization.

## Future Improvements

- Add support for multiple treasury instruments.
- Integrate a reliable database for historical data storage.
- Enhance user interface with advanced visualizations.

---
Feel free to contribute or suggest improvements for this project!