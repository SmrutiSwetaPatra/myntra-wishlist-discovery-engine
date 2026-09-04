import React, { useState } from 'react';
import '../../styles/components.css';

export const ImageGallery = ({ images = [] }) => {
  const [activeIndex, setActiveIndex] = useState(0);

  if (!images || images.length === 0) {
    return <div className="image-gallery-placeholder">No Image Available</div>;
  }

  return (
    <div className="image-gallery">
      <div className="main-image-container">
        <img 
          src={images[activeIndex]} 
          alt={`Product view ${activeIndex + 1}`} 
          className="main-image"
        />
      </div>
      
      {images.length > 1 && (
        <div className="thumbnail-container">
          {images.map((img, index) => (
            <button 
              key={index}
              className={`thumbnail-button ${activeIndex === index ? 'active' : ''}`}
              onClick={() => setActiveIndex(index)}
            >
              <img src={img} alt={`Thumbnail ${index + 1}`} className="thumbnail-image" />
            </button>
          ))}
        </div>
      )}
    </div>
  );
};
