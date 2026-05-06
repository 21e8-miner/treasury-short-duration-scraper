import requests

# API URL for real-time treasury data
API_URL = "https://api.example.com/treasury-data"

def fetch_real_time_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()  # Assuming the API returns JSON data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

if __name__ == "__main__":
    data = fetch_real_time_data()
    if data:
        print("Real-time Treasury Data:")
        print(data)