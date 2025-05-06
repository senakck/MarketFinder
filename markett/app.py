from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import csv
import time

# Tarayıcı ayarları
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--headless")  # Headless modu etkinleştir

all_products = []

urls = [
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

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    for url in urls:
        print(f"Sayfa işleniyor: {url}")
        driver.get(url)

        WebDriverWait(driver, 20).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        try:
            if 'a101' in url:
                WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.w-full.border')))
                products = driver.find_elements(By.CSS_SELECTOR, '.w-full.border')
            else:
                WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'sm-list-page-item')))
                products = driver.find_elements(By.CSS_SELECTOR, 'sm-list-page-item')

            for product in products:
                try:
                    if 'a101' in url:
                        name = product.find_element(By.CSS_SELECTOR, '.mobile\\:text-xs.tablet\\:text-xs').text.strip()
                        product_url = product.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                        try:
                            price = product.find_element(By.CSS_SELECTOR, '.text-md.absolute.bottom-0').text.strip()
                        except:
                            price = "Fiyat bulunamadı"
                    else:
                        name = product.find_element(By.CSS_SELECTOR, '.product-name').text.strip()
                        product_url = product.find_element(By.CSS_SELECTOR, '.product-name').get_attribute('href')
                        try:
                            price = product.find_element(By.CSS_SELECTOR, '.price.subtitle-1 span').text.strip()
                        except:
                            price = "Fiyat bulunamadı"

                    product_data = {
                        'name': name,
                        'url': product_url,
                        'price': price,
                        'market': 'Migros' if 'migros' in url else 'A101'  # Market bilgisini ekle
                    }
                    all_products.append(product_data)
                    print(f"Ürün: {name}, Market: {product_data['market']}, Fiyat: {price}, URL: {product_url}")
                except Exception as e:
                    print(f"Ürün işlenirken hata: {e}")
        except Exception as e:
            print(f"Ürünler yüklenirken hata: {e}")

        # İstekler arasında bekleme süresi ekleyin
        time.sleep(5)

    if all_products:
        try:
            with open('urunler.json', 'w', encoding='utf-8') as json_file:
                json.dump(all_products, json_file, ensure_ascii=False, indent=4)

            with open('urunler.csv', 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['Ürün Adı', 'Fiyat', 'URL', 'Market'])
                for product in all_products:
                    writer.writerow([product['name'], product['price'], product['url'], product['market']])
            print("Tüm ürünler başarıyla JSON ve CSV dosyalarına kaydedildi.")
        except Exception as e:
            print(f"Dosya kaydedilirken hata: {e}")
    else:
        print("Ürün listesi boş, JSON ve CSV dosyasına yazılmadı.")

except Exception as e:
    print(f"Genel hata: {e}")

finally:
    if 'driver' in locals():
        driver.quit()