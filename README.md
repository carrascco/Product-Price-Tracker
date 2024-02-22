# Price Tracker

This project tracks the price of a specific product and sends an email notification if the price changes. It utilizes web scraping techniques to extract price information from a designated URL and compares it with the previously stored price. If a change is detected, it sends an email notification to the specified recipient.

## Features

- Scrapes the price of a product from a specified URL.
- Compares the current price with the previous price.
- Sends an email notification if the price changes.

## Setup

1. **Clone the Repository**: 
    ```bash
    git clone https://github.com/carrascco/Product-Price-Updates-Notifier
    cd Product-Price-Update-Notifier
    ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
    

4. **Configuration**:
    - Create a `cd.yaml` file for GitHub Actions configuration.
    - Add your Gmail credentials and receiver email address as secrets in your GitHub repository settings or as environment variables, if you run it locally.
    
5. **Run the Script Manually**:
    ```bash
    python main.py
    ```

## GitHub Actions

This project is configured to run periodically using GitHub Actions. It runs the script automatically at 6 AM every day.

## File Structure

- `main.py`: Python script to track price and send email notifications.
- `cd.yaml`: GitHub Actions workflow configuration file.
- `precio`: File to store the previously tracked price.
- `README.md`: Documentation file.

