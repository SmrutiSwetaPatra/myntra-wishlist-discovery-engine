import React, { useEffect, useState } from 'react';
import { Search, SlidersHorizontal } from 'lucide-react';
import { productService } from '../services/productService';
import { wishlistService } from '../services/wishlistService';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorState } from '../components/common/ErrorState';
import { ProductCard } from '../components/common/ProductCard';
import { Filters } from '../components/common/Filters';
import { Button } from '../components/common/Button';

export const Discover = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const [search, setSearch] = useState('');
  const [filters, setFilters] = useState({});
  const [showFilters, setShowFilters] = useState(false);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      setError(null);
      const params = { q: search, ...filters };
      const response = await productService.getProducts(params);
      setProducts(response.items || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Only fetch automatically on mount or if search is empty
    fetchProducts();
  }, [filters]);

  const handleSearch = (e) => {
    e.preventDefault();
    fetchProducts();
  };

  if (loading && products.length === 0) return <LoadingSpinner fullScreen />;
  if (error && products.length === 0) return <ErrorState message={error} onRetry={fetchProducts} />;

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Discover</h1>
        <p className="page-subtitle">Find new products to add to your wishlist.</p>
      </div>

      <div style={{ display: 'flex', gap: '16px', marginBottom: '24px' }}>
        <form onSubmit={handleSearch} style={{ flex: 1, display: 'flex', gap: '8px' }}>
          <div style={{ position: 'relative', flex: 1 }}>
            <Search size={20} style={{ position: 'absolute', left: '12px', top: '10px', color: 'var(--color-text-muted)' }} />
            <input 
              type="text" 
              placeholder="Search products..." 
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              style={{ width: '100%', padding: '10px 12px 10px 40px', borderRadius: 'var(--radius-md)', border: '1px solid var(--color-border)', outline: 'none' }}
            />
          </div>
          <Button type="submit" variant="primary">Search</Button>
        </form>
        <Button variant="secondary" onClick={() => setShowFilters(!showFilters)}>
          <SlidersHorizontal size={20} />
          Filters
        </Button>
      </div>

      <div style={{ display: 'flex', gap: '24px', alignItems: 'flex-start' }}>
        {showFilters && (
          <div style={{ width: '250px', flexShrink: 0 }}>
            <Filters filters={filters} setFilters={setFilters} />
          </div>
        )}

        <div style={{ flex: 1 }}>
          {loading ? (
            <LoadingSpinner />
          ) : products.length > 0 ? (
            <div className={`grid ${showFilters ? 'grid-cols-3' : 'grid-cols-4'}`}>
              {products.map(product => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          ) : (
            <div className="card" style={{ padding: '40px', textAlign: 'center' }}>
              <p className="text-muted">No products found.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
