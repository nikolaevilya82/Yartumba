import { useState, useCallback, useEffect } from 'react';
import type { Product, CatalogFilters } from '../../core/types/catalog.types';
import type { FurnitureType } from '../../core/constants/product.constants';

interface CatalogState {
  products: Product[];
  filteredProducts: Product[];
  currentFilters: CatalogFilters;
  selectedType: FurnitureType | null;
  isLoaded: boolean;
  error: string | null;
}

const initialState: CatalogState = {
  products: [],
  filteredProducts: [],
  currentFilters: {
    furnitureType: null,
    priceMin: undefined,
    priceMax: undefined,
    searchQuery: '',
  },
  selectedType: null,
  isLoaded: false,
  error: null,
};

// Моковые данные
const mockProducts: Product[] = [
  {
    id: '123e4567-e89b-12d3-a456-426614174000',
    product_id: '123e4567-e89b-12d3-a456-426614174001',
    name: 'Стеллаж "Лес"',
    description: 'Книжная полка с 4 полками',
    base_price: 8500,
    image_url: 'https://placehold.co/400x300/e8e8e8/999999?text=Полка',
    furniture_type: 'bookshelf',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: '223e4567-e89b-12d3-a456-426614174000',
    product_id: '223e4567-e89b-12d3-a456-426614174001',
    name: 'Тумба "Уют"',
    description: 'Прикроватная тумба с ящиком',
    base_price: 5200,
    image_url: 'https://placehold.co/400x300/e8e8e8/999999?text=Тумба',
    furniture_type: 'nightstand',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: '323e4567-e89b-12d3-a456-426614174000',
    product_id: '323e4567-e89b-12d3-a456-426614174001',
    name: 'Комод "Семейный"',
    description: 'Комод с 4 ящиками',
    base_price: 12500,
    image_url: 'https://placehold.co/400x300/e8e8e8/999999?text=Комод',
    furniture_type: 'dresser',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
];

export function useCatalogStore() {
  const [state, setState] = useState<CatalogState>(initialState);

  const applyFilters = useCallback((currentState: CatalogState) => {
    let filtered = [...currentState.products];
    
    if (currentState.selectedType) {
      filtered = filtered.filter(p => p.furniture_type === currentState.selectedType);
    }
    
    if (currentState.currentFilters.priceMin !== undefined) {
      filtered = filtered.filter(p => p.base_price >= currentState.currentFilters.priceMin!);
    }
    if (currentState.currentFilters.priceMax !== undefined) {
      filtered = filtered.filter(p => p.base_price <= currentState.currentFilters.priceMax!);
    }
    
    if (currentState.currentFilters.searchQuery) {
      const query = currentState.currentFilters.searchQuery.toLowerCase();
      filtered = filtered.filter(p => 
        p.name.toLowerCase().includes(query) ||
        (p.description?.toLowerCase().includes(query) ?? false)
      );
    }
    
    return { ...currentState, filteredProducts: filtered };
  }, []);

  const setSelectedType = useCallback((type: FurnitureType | null) => {
    setState(prev => {
      const newState = { ...prev, selectedType: type, currentFilters: { ...prev.currentFilters, furnitureType: type } };
      return applyFilters(newState);
    });
  }, [applyFilters]);

  const setSearchQuery = useCallback((query: string) => {
    setState(prev => {
      const newState = { ...prev, currentFilters: { ...prev.currentFilters, searchQuery: query } };
      return applyFilters(newState);
    });
  }, [applyFilters]);

  const clearFilters = useCallback(() => {
    setState(prev => {
      const newState = {
        ...prev,
        selectedType: null,
        currentFilters: {
          furnitureType: null,
          priceMin: undefined,
          priceMax: undefined,
          searchQuery: '',
        },
      };
      return applyFilters(newState);
    });
  }, [applyFilters]);

  const loadProducts = useCallback(async () => {
    try {
      // TODO: Подключить к реальному API
      // const response = await catalogService.getProducts({ per_page: 100 });
      
      setState(prev => {
        const newState = {
          ...prev,
          products: mockProducts,
          isLoaded: true,
          error: null,
        };
        return applyFilters(newState);
      });
    } catch (err) {
      setState(prev => ({
        ...prev,
        error: (err as Error).message || 'Ошибка загрузки товаров',
        isLoaded: true,
      }));
    }
  }, [applyFilters]);

  const clear = useCallback(() => {
    setState(initialState);
  }, []);

  return {
    ...state,
    setSelectedType,
    setSearchQuery,
    clearFilters,
    loadProducts,
    clear,
  };
}
