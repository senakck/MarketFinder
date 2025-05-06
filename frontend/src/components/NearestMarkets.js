import React from 'react';

const NearestMarkets = ({ markets }) => {
  return (
    <div className="nearest-markets">
      <h3>En Yakın Marketler</h3>
      <div className="markets-list">
        {markets.map((market, index) => (
          <div key={index} className="market-item">
            <h4>{index + 1}. {market.name}</h4>
            <p className="market-address">{market.address}</p>
            <div className="market-details">
              <p><strong>Mesafe:</strong> {market.distance.toFixed(1)} km</p>
              <p><strong>Süre:</strong> {market.duration} dakika</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default NearestMarkets;
