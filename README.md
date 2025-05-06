# MarketFinder

Market ürünlerini karşılaştırmanıza ve en uygun fiyatlı ürünleri bulmanıza yardımcı olan bir web uygulaması.

## Özellikler

- A101 ve Migros marketlerinden otomatik ürün fiyatı çekme
- Ürünleri kategorilere göre listeleme
- Fiyat karşılaştırma
- Modern ve kullanıcı dostu arayüz

## Kurulum

### Backend (Python Flask)

1. Python 3.8 veya üstü sürümü yükleyin
2. Backend klasörüne gidin:
   ```bash
   cd backend
   ```
3. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
4. Sunucuyu başlatın:
   ```bash
   python app.py
   ```

### Frontend (React)

1. Node.js 14 veya üstü sürümü yükleyin
2. Frontend klasörüne gidin:
   ```bash
   cd frontend
   ```
3. Bağımlılıkları yükleyin:
   ```bash
   npm install
   ```
4. Geliştirme sunucusunu başlatın:
   ```bash
   npm start
   ```

## Kullanım

1. Web tarayıcınızda `http://localhost:3000` adresine gidin
2. "Ürünleri Güncelle" butonuna tıklayarak en güncel fiyatları çekin
3. Ürünleri inceleyin ve karşılaştırın

## Teknolojiler

- Backend:
  - Python
  - Flask
  - Selenium
  - BeautifulSoup4

- Frontend:
  - React
  - CSS3
  - HTML5

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.
