import os
import requests
import json
import time
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

API_KEY = os.getenv("REACT_APP_GOOGLE_MAPS_API_KEY")  # Ortam değişkeninden API anahtarını al

def fetch_places(query):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={API_KEY}"
    all_results = []
    while url:
        try:
            response = requests.get(url)
            response.raise_for_status()  # HTTP hatalarını yakala
            data = response.json()
            all_results.extend(data.get('results', []))
            url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?pagetoken={data.get('next_page_token')}&key={API_KEY}" if 'next_page_token' in data else None
            time.sleep(2)  # API'nin `next_page_token`'ı işleyebilmesi için bekleyin
        except requests.exceptions.RequestException as e:
            print(f"Hata oluştu: {e}")
            break
    return all_results

def main():
    try:
        migros_locations = fetch_places("Migros Ankara")
        a101_locations = fetch_places("A101 Ankara")

        all_locations = {
            "Migros": migros_locations,
            "A101": a101_locations
        }

        # Gelen sonuçları kaydetme
        try:
            with open("marketler.json", "w", encoding="utf-8") as file:
                json.dump(all_locations, file, ensure_ascii=False, indent=4)
            print("Market konumları kaydedildi!")
        except Exception as e:
            print(f"Dosya kaydedilirken hata oluştu: {e}")
    except Exception as e:
        print(f"Genel hata: {e}")

if __name__ == "__main__":
    main()


    