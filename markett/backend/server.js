const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config({ path: '../.env' });

const app = express();

// CORS yapılandırması
app.use(cors({
    origin: 'http://localhost:3000',
    methods: ['GET', 'POST'],
    credentials: true
}));

app.use(express.json());

const API_KEY = process.env.REACT_APP_GOOGLE_MAPS_API_KEY;

// Test endpoint'i
app.get('/', (req, res) => {
    res.json({ message: 'Backend sunucusu çalışıyor!' });
});

// API durumunu kontrol et
app.get('/api/status', (req, res) => {
    res.json({ 
        status: 'OK',
        apiKey: API_KEY ? 'Mevcut' : 'Eksik',
        apiKeyLength: API_KEY?.length || 0
    });
});

app.get('/api/places', async (req, res) => {
    try {
        const { latitude, longitude, keyword } = req.query;
        
        if (!latitude || !longitude || !keyword) {
            return res.status(400).json({
                error: 'Eksik parametreler',
                required: { latitude, longitude, keyword },
                received: req.query
            });
        }

        if (!API_KEY) {
            return res.status(400).json({
                error: 'API anahtarı bulunamadı',
                details: 'Lütfen .env dosyasını kontrol edin'
            });
        }

        console.log('Gelen istek:', {
            latitude,
            longitude,
            keyword,
            timestamp: new Date().toISOString()
        });

        const radius = 20000; // 20 km
        const url = `https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=${latitude},${longitude}&radius=${radius}&keyword=${encodeURIComponent(keyword)}&type=store&key=${API_KEY}`;
        
        console.log('Google Places API isteği yapılıyor...');
        const response = await axios.get(url);
        
        console.log('API Yanıtı:', {
            status: response.data.status,
            resultsCount: response.data.results?.length || 0,
            errorMessage: response.data.error_message
        });

        if (response.data.status === 'REQUEST_DENIED') {
            return res.status(400).json({
                error: 'API isteği reddedildi',
                details: response.data.error_message,
                apiKeyLength: API_KEY.length
            });
        }

        if (response.data.status === 'ZERO_RESULTS') {
            return res.json({
                status: 'OK',
                results: []
            });
        }

        res.json(response.data);
    } catch (error) {
        console.error('Hata detayları:', {
            message: error.message,
            response: error.response?.data,
            stack: error.stack
        });

        res.status(500).json({
            error: 'Market bilgileri alınamadı',
            details: error.response?.data || error.message
        });
    }
});

const PORT = process.env.PORT || 3001;

// Sunucuyu başlat
app.listen(PORT, () => {
    console.log(`
    🚀 Server başlatıldı:
    - Port: ${PORT}
    - Ortam: ${process.env.NODE_ENV || 'development'}
    - API Key Durumu: ${API_KEY ? 'Mevcut' : 'Eksik'}
    - API Key Uzunluğu: ${API_KEY?.length || 0}
    `);
}); 