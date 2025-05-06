import React, { useState, useEffect } from 'react';
import { GoogleMap, LoadScript, Marker, Circle } from '@react-google-maps/api';

const Map = ({ markers, onMarkerClick, onRadiusChange }) => {
  const [userLocation, setUserLocation] = useState(null);
  const [radius, setRadius] = useState(5000); // 5km varsayılan
  
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
          onRadiusChange(userPos.lat, userPos.lng, radius);
        },
        (error) => {
          console.error('Konum alınamadı:', error);
        }
      );
    }
  }, []);

  const handleRadiusChange = (e) => {
    const newRadius = parseInt(e.target.value);
    setRadius(newRadius);
    if (userLocation) {
      onRadiusChange(userLocation.lat, userLocation.lng, newRadius);
    }
  };

  return (
    <div>
      <div className="radius-control">
        <label>Arama yarıçapı: {radius/1000} km</label>
        <input
          type="range"
          min="1000"
          max="10000"
          step="1000"
          value={radius}
          onChange={handleRadiusChange}
        />
      </div>

      <LoadScript googleMapsApiKey="AIzaSyDep0OeyVVHnIBKRr_jJSJhFGs4RMdpUcQ">
        <GoogleMap
          mapContainerStyle={mapStyles}
          zoom={13}
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
              <Circle
                center={userLocation}
                radius={radius}
                options={{
                  fillColor: '#3B82F6',
                  fillOpacity: 0.1,
                  strokeColor: '#3B82F6',
                  strokeOpacity: 0.8,
                  strokeWeight: 2,
                }}
              />
            </>
          )}

          {markers.map((marker, index) => (
            <Marker
              key={index}
              position={marker.position}
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
