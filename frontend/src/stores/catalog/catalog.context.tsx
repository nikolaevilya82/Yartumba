import React, { createContext, useContext, ReactNode } from 'react';
import { useCatalogStore as useCatalogStoreLogic } from './catalog.store';

interface CatalogContextType {
  products: any[];
  filteredProducts: any[];
  currentFilters: any;
  selectedType: string | null;
  isLoaded: boolean;
  error: string | null;
  setSelectedType: (type: string | null) => void;
  setSearchQuery: (query: string) => void;
  clearFilters: () => void;
  loadProducts: () => Promise<void>;
  clear: () => void;
}

const CatalogContext = createContext<CatalogContextType | undefined>(undefined);

export function CatalogProvider({ children }: { children: ReactNode }) {
  const store = useCatalogStoreLogic();
  
  return (
    <CatalogContext.Provider value={store}>
      {children}
    </CatalogContext.Provider>
  );
}

export function useCatalog() {
  const context = useContext(CatalogContext);
  if (context === undefined) {
    throw new Error('useCatalog must be used within a CatalogProvider');
  }
  return context;
}
