from flask import Blueprint, jsonify, request
from ..scraping.scraper import MarketScraper
import googlemaps
import os

api = Blueprint('api', __name__)

# Google Maps API anahtarı
GOOGLE_MAPS_API_KEY = 'AIzaSyDep0OeyVVHnIBKRr_jJSJhFGs4RMdpUcQ'
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

# Market URLs
URLS = [
    # Sebze Meyve
    'https://www.migros.com.tr/meyve-sebze-c-2?sayfa=1&sirala=onerilenler',
    'https://www.migros.com.tr/meyve-sebze-c-2?sayfa=2&sirala=onerilenler',
    'https://www.a101.com.tr/kapida/meyve-sebze/meyve',

    # İçecek 
    'https://www.migros.com.tr/icecek-c-6',
    'https://www.migros.com.tr/icecek-c-6?sayfa=2&sirala=onerilenler',
    'https://www.a101.com.tr/kapida/icecek/gazli-icecekler',

    # Temizlik
    'https://www.migros.com.tr/deterjan-temizlik-c-7',
    'https://www.migros.com.tr/deterjan-temizlik-c-7?sayfa=2&sirala=onerilenler',
    'https://www.a101.com.tr/kapida/temizlik-urunleri/bulasik',

    # Et
    'https://www.migros.com.tr/et-tavuk-balik-c-3',
    'https://www.migros.com.tr/et-tavuk-balik-c-3?sayfa=2&sirala=onerilenler',
    'https://www.a101.com.tr/kapida/et-balik-tavuk/kirmizi-et',

    # Süt Ürünleri
    'https://www.a101.com.tr/kapida/sut-urunleri-kahvaltilik/sut',
    'https://www.migros.com.tr/sut-kahvaltilik-c-4'
]

# Ürün verileri
products = []
scraper = MarketScraper()

@api.route('/products', methods=['GET'])
def get_products():
    """Tüm ürünleri getir"""
    search_query = request.args.get('q', '').lower()
    if search_query:
        filtered_products = [p for p in products if search_query in p['name'].lower()]
        return jsonify(filtered_products)
    return jsonify(products)

def get_nearby_stores(lat, lng, radius=5000):
    """Belirtilen konumun çevresindeki Migros ve A101 mağazalarını bul"""
    stores = []
    
    # Migros mağazalarını ara
    migros_result = gmaps.places_nearby(
        location=(lat, lng),
        radius=radius,
        keyword='Migros',
        type='store'
    )
    
    # A101 mağazalarını ara
    a101_result = gmaps.places_nearby(
        location=(lat, lng),
        radius=radius,
        keyword='A101',
        type='store'
    )
    
    # Sonuçları işle
    for store in migros_result.get('results', []) + a101_result.get('results', []):
        # Mesafe matrisini hesapla
        distance_result = gmaps.distance_matrix(
            origins=f"{lat},{lng}",
            destinations=f"{store['geometry']['location']['lat']},{store['geometry']['location']['lng']}",
            mode="driving"
        )
        
        # İlk rotayı al
        route = distance_result['rows'][0]['elements'][0]
        
        stores.append({
            'name': 'Migros' if 'Migros' in store['name'] else 'A101',
            'address': store['vicinity'],
            'location': {
                'lat': store['geometry']['location']['lat'],
                'lng': store['geometry']['location']['lng']
            },
            'distance': route['distance']['value'] / 1000,  # km cinsinden
            'duration': route['duration']['value'] // 60    # dakika cinsinden
        })
    
    return stores

@api.route('/markets/nearby', methods=['GET'])
def get_nearby_markets():
    """Yakındaki marketleri getir"""
    try:
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
        radius = int(request.args.get('radius', 5000))  
        
        stores = get_nearby_stores(lat, lng, radius)
        return jsonify(stores)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api.route('/scrape', methods=['GET'])
def scrape_products():
    """Ürünleri marketlerden çek"""
    global products
    products = []  # Reset products list
    
    try:
        products = scraper.scrape_markets(URLS)
        return jsonify({
            "message": "Scraping completed",
            "product_count": len(products)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
