import requests
import json
from json import JSONDecodeError
from collections import defaultdict
from datetime import datetime

API_KEY = '<YOUR_API_KEY>'
STEAM_ID = '<YOUR_STEAM_ID>'
def fetch_owned_games(steam_id):
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={API_KEY}&steamid={steam_id}&include_appinfo=1&format=json"
    response = requests.get(url)

    try:
        data = json.loads(response.text)
    except JSONDecodeError:
        print("Error: Unable to parse the API response. Please check your API key and Steam ID.")
        return []

    return data['response']['games']

def list_owned_games(games):
    for game in games:
        if 'price' in game:
            print(f"{game['name']} - ${game['price']:.2f}")
        else:
            print(game['name'])

def fetch_price(app_id):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    response = requests.get(url)
    try:
        data = json.loads(response.text)
    except JSONDecodeError:
        return None

    if data and data.get(str(app_id), {}).get('success'):
        try:
            return data[str(app_id)]['data']['price_overview']['final'] / 100
        except KeyError:
            print(f"Error: Unable to fetch price for app ID {app_id}. Price overview data is missing.")
            return None
    else:
        print(f"Error: Unable to fetch data for app ID {app_id}.")
        return None



def fetch_owned_games_with_prices(steam_id):
    games = fetch_owned_games(steam_id)
    for game in games:
        price = fetch_price(game['appid'])
        if price is not None:
            game['price'] = price
    return games


def main():
    games = fetch_owned_games_with_prices(STEAM_ID)
    num_games_with_price = len([game for game in games if 'price' in game])
    num_games_without_price = len(games) - num_games_with_price
    total_price = sum(game['price'] for game in games if 'price' in game)

    while True:
        print("\nOptions:")
        print("1. Display list of owned games")
        print(f"2. Show total price of owned games ({num_games_with_price} games with prices, {num_games_without_price} games without prices)")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ")
        if choice == '1':
            list_owned_games(games)
        elif choice == '2':
            print(f"Total price of owned games: ${total_price:.2f}")
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()