from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class MarketScraper:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument("--headless")
        
    def scrape_markets(self, urls):
        driver = None
        products = []
        
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
            
            for url in urls:
                print(f"Sayfa işleniyor: {url}")
                products.extend(self._scrape_page(driver, url))
                    
        except Exception as e:
            print(f"Genel hata: {e}")
            return {"error": str(e)}
        finally:
            if driver:
                driver.quit()
                
        return products
    
    def _scrape_page(self, driver, url):
        page_products = []
        
        try:
            driver.get(url)
            WebDriverWait(driver, 20).until(lambda d: d.execute_script('return document.readyState') == 'complete')
            
            if 'a101' in url:
                products = self._scrape_a101_products(driver)
            else:
                products = self._scrape_migros_products(driver)
                
            page_products.extend(products)
            
        except Exception as e:
            print(f"Sayfa işleme hatası: {e}")
            
        return page_products
    
    def _scrape_a101_products(self, driver):
        products = []
        
        try:
            WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.w-full.border')))
            items = driver.find_elements(By.CSS_SELECTOR, '.w-full.border')
            
            for item in items:
                try:
                    name = item.find_element(By.CSS_SELECTOR, '.mobile\\:text-xs.tablet\\:text-xs').text.strip()
                    url = item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                    try:
                        price = item.find_element(By.CSS_SELECTOR, '.text-md.absolute.bottom-0').text.strip()
                    except:
                        price = "Fiyat bulunamadı"
                        
                    products.append({
                        "name": name,
                        "price": price,
                        "url": url,
                        "market": "A101"
                    })
                    
                except Exception as e:
                    print(f"Ürün işleme hatası (A101): {e}")
                    
        except Exception as e:
            print(f"A101 ürünleri çekilemedi: {e}")
            
        return products
    
    def _scrape_migros_products(self, driver):
        products = []
        
        try:
            WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'sm-list-page-item')))
            items = driver.find_elements(By.CSS_SELECTOR, 'sm-list-page-item')
            
            for item in items:
                try:
                    name = item.find_element(By.CSS_SELECTOR, '.product-name').text.strip()
                    url = item.find_element(By.CSS_SELECTOR, '.product-name').get_attribute('href')
                    try:
                        price = item.find_element(By.CSS_SELECTOR, '.price.subtitle-1 span').text.strip()
                    except:
                        price = "Fiyat bulunamadı"
                        
                    products.append({
                        "name": name,
                        "price": price,
                        "url": url,
                        "market": "Migros"
                    })
                    
                except Exception as e:
                    print(f"Ürün işleme hatası (Migros): {e}")
                    
        except Exception as e:
            print(f"Migros ürünleri çekilemedi: {e}")
            
        return products
