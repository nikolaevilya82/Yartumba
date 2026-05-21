import { createContext, useContext } from 'react';
import * as cart from './cart';
import * as configurator from './configurator';
import * as catalog from './catalog';
import * as ui from './ui';

export const rootStore = {
  ...cart,
  ...configurator,
  ...catalog,
  ...ui,
};

export type RootStore = typeof rootStore;

const StoreContext = createContext<RootStore>(rootStore);

export const StoreProvider = StoreContext.Provider;

export const useStore = () => useContext(StoreContext);

// Удобные хуки
export const useCartStore = () => useStore().cartStore;
export const useCartActions = () => useStore().cartActions;
export const useCartLoading = () => useStore().cartLoadingStore;
export const useCartPromocode = () => useStore().cartPromocodeStore;

export const useConfiguratorData = () => useStore().configuratorDataStore;
export const useConfiguratorCalculation = () => useStore().configuratorCalculationStore;
export const useConfiguratorHistory = () => useStore().configuratorHistoryStore;
export const useConfiguratorUI = () => useStore().configuratorUIStore;

export const useCatalog = () => useStore().catalogStore;
export const useCatalogLoading = () => useStore().catalogLoadingStore;

export const useModal = () => useStore().modalStore;
export const useNotification = () => useStore().notificationStore;
export const useLoading = () => useStore().loadingStore;
export const useTheme = () => useStore().themeStore;
export const useLanguage = () => useStore().languageStore;
export const useSidebar = () => useStore().sidebarStore;
