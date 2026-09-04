import React from 'react';
import '../../styles/components.css';

export const Filters = ({ filters, setFilters, onApply }) => {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFilters((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <div className="filters-container">
      <h3 className="filters-title">Filters</h3>
      
      <div className="filter-group">
        <label className="filter-label">Category</label>
        <select 
          name="category" 
          className="filter-select" 
          value={filters.category || ''} 
          onChange={handleChange}
        >
          <option value="">All Categories</option>
          <option value="Dresses">Dresses</option>
          <option value="Trousers">Trousers</option>
          <option value="Sneakers">Sneakers</option>
          <option value="Tops">Tops</option>
          <option value="Jackets">Jackets</option>
          <option value="Bags">Bags</option>
        </select>
      </div>

      <div className="filter-group">
        <label className="filter-label">Gender</label>
        <select 
          name="gender" 
          className="filter-select" 
          value={filters.gender || ''} 
          onChange={handleChange}
        >
          <option value="">All Genders</option>
          <option value="Women">Women</option>
          <option value="Men">Men</option>
          <option value="Unisex">Unisex</option>
        </select>
      </div>
    </div>
  );
};
