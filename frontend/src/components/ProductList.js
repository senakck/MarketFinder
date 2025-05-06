import React from 'react';

const ProductList = ({ products }) => {
  return (
    <div className="product-list">
      <h2>Ürünler</h2>
      <div className="products-grid">
        {products.map((product, index) => (
          <div key={index} className="product-card">
            <h3>{product.name}</h3>
            <p className="price">{product.price}</p>
            <p className="market">{product.market}</p>
            <a href={product.url} target="_blank" rel="noopener noreferrer">
              Ürüne Git
            </a>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProductList;
