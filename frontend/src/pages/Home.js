import React, { useState, useEffect } from 'react';
import Map from '../components/Map';
import NearestMarkets from '../components/NearestMarkets';
import ProductList from '../components/ProductList';

const Home = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [nearestMarkets, setNearestMarkets] = useState([]);

  const fetchProducts = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/products');
      const data = await response.json();
      setProducts(data);
    } catch (err) {
      setError('Ürünler yüklenirken bir hata oluştu');
    }
  };

  const fetchNearbyMarkets = async (lat, lng, radius) => {
    try {
      const response = await fetch(
        `http://localhost:5000/api/markets/nearby?lat=${lat}&lng=${lng}&radius=${radius}`
      );
      const data = await response.json();
      if (data.error) {
        setError(data.error);
      } else {
        setNearestMarkets(data);
      }
    } catch (err) {
      setError('Yakındaki marketler bulunamadı');
    }
  };

  const scrapeProducts = async () => {
    setLoading(true);
    setError(null);
    try {
      await fetch('http://localhost:5000/api/scrape');
      await fetchProducts();
    } catch (err) {
      setError('Ürünler çekilirken bir hata oluştu');
    } finally {
      setLoading(false);
    }
  };

  const handleMarkerClick = (marker) => {
    // Marketın ürünlerini filtrele
    setSearchQuery(marker.name);
  };

  const handleRadiusChange = (lat, lng, radius) => {
    fetchNearbyMarkets(lat, lng, radius);
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  return (
    <div className="home">
      <h1>Ürün Fiyat Karşılaştırma</h1>
      
      <div className="search-container">
        <input
          type="text"
          placeholder="Ürün adı girin..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button onClick={() => setSearchQuery('')}>Temizle</button>
      </div>

      <div className="main-content">
        <div className="map-container">
          <Map 
            markers={nearestMarkets} 
            onMarkerClick={handleMarkerClick}
            onRadiusChange={handleRadiusChange}
          />
        </div>
        
        <div className="markets-container">
          <NearestMarkets markets={nearestMarkets} />
        </div>
      </div>

      {error && <div className="error">{error}</div>}
      
      <button 
        className="update-button"
        onClick={scrapeProducts}
        disabled={loading}
      >
        {loading ? 'Ürünler Çekiliyor...' : 'Ürünleri Güncelle'}
      </button>
      
      <ProductList products={products.filter(product => 
        searchQuery ? product.name.toLowerCase().includes(searchQuery.toLowerCase()) : true
      )} />
    </div>
  );
};

export default Home;
