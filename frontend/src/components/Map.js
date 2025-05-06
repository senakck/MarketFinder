import React, { useState, useEffect } from 'react';
import { GoogleMap, LoadScript, Marker, Circle } from '@react-google-maps/api';

const Map = ({ markers, onMarkerClick, onRadiusChange }) => {
  const [userLocation, setUserLocation] = useState(null);
  const [radius, setRadius] = useState(0); // Başlangıçta çember gösterme
  
  const mapStyles = {
    height: "70vh",
    width: "100%"
  };

  const defaultCenter = {
    lat: 39.9334, // Ankara'nın koordinatları
    lng: 32.8597
  };

  useEffect(() => {
    // Kullanıcının konumunu al
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const userPos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          };
          setUserLocation(userPos);
          // Konum alınır alınmaz radius değeriyle API'yi çağır
          onRadiusChange(userPos.lat, userPos.lng, radius * 1000);
        },
        (error) => {
          console.error('Konum alınamadı:', error);
        }
      );
    }
  }, []); // Sadece component mount olduğunda çalışsın

  // radius değiştiğinde API'yi çağır
  useEffect(() => {
    if (userLocation) {
      onRadiusChange(userLocation.lat, userLocation.lng, radius * 1000);
    }
  }, [radius, userLocation, onRadiusChange]);

  const handleRadiusChange = (e) => {
    const newRadius = parseInt(e.target.value, 10); // String'i integer'a çevir
    setRadius(newRadius);
    if (userLocation) {
      onRadiusChange(userLocation.lat, userLocation.lng, newRadius * 1000); // API için metreye çevir
    }
  };

  return (
    <div>
      <div className="radius-control">
        <label htmlFor="radius-input">Kaç km çevredeki marketleri görmek istersiniz?</label>
        <div className="radius-input-container">
          <input
            id="radius-input"
            type="range"
            min="1"
            max="10"
            value={radius}
            onChange={(e) => handleRadiusChange(e)}
          />
          <span className="radius-value">{radius} km</span>
        </div>
      </div>

      <LoadScript googleMapsApiKey="AIzaSyDep0OeyVVHnIBKRr_jJSJhFGs4RMdpUcQ">
        <GoogleMap
          mapContainerStyle={mapStyles}
          zoom={radius === 0 ? 13 : Math.max(16 - radius, 12)}
          center={userLocation || defaultCenter}
        >
          {userLocation && (
            <>
              <Marker
                position={userLocation}
                icon={{
                  url: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
                }}
              />
              {radius > 0 && (
                <Circle
                  center={userLocation}
                  radius={radius * 1000} // Circle için metreye çevir
                  options={{
                    fillColor: '#3B82F6',
                    fillOpacity: 0.1,
                    strokeColor: '#3B82F6',
                    strokeOpacity: 0.8,
                    strokeWeight: 2,
                  }}
                />
              )}
            </>
          )}

          {markers.map((marker, index) => (
            <Marker
              key={index}
              position={marker.location}
              onClick={() => onMarkerClick(marker)}
              icon={{
                url: marker.name === 'Migros' 
                  ? 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
                  : 'http://maps.google.com/mapfiles/ms/icons/yellow-dot.png'
              }}
            />
          ))}
        </GoogleMap>
      </LoadScript>
    </div>
  );
};

export default Map;
