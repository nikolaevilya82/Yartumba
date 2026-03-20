import type { FurnitureType, PartType } from '../constants/product.constants';

// Базовый интерфейс товара
export interface Product {
  id: number;
  name: string;
  description?: string;
  price: number;
  image?: string;
  category_id: number;
  article?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

// Базовый интерфейс мебели
export interface Furniture {
  id: number;
  product_id: number;
  width: number;
  height: number;
  depth: number;
  material_id?: number;
  created_at: string;
  updated_at: string;
}

// Книжная полка
export interface Bookshelf extends Furniture {
  shelf_count: number;
  has_back_panel: boolean;
  max_weight_per_shelf: number;
}

// Прикроватная тумба
export interface Nightstand extends Furniture {
  drawer_count: number;
  has_door: boolean;
  leg_height?: number;
}

// Комод
export interface Dresser extends Furniture {
  drawer_count: number;
  row_count: number;
  has_mirror: boolean;
}

// Деталь мебели (bookshelf_part, nightstand_part, dresser_part)
export interface FurniturePart {
  id: number;
  furniture_id: number;
  furniture_type: FurnitureType;
  part_type: PartType;
  sheet_material_id?: number;
  edge_material_id?: number;
  width: number;
  height: number;
  thickness: number;
  quantity: number;
  created_at: string;
  updated_at: string;
}

// Тип товара для универсальных функций
export type AnyFurniture = Bookshelf | Nightstand | Dresser;
export type AnyFurniturePart = FurniturePart;

// Тип для отображения в каталоге
export interface FurnitureCatalogItem {
  id: number;
  type: FurnitureType;
  name: string;
  price: number;
  image?: string;
  width: number;
  height: number;
  depth: number;
}

// Связь с продуктом
export interface FurnitureWithProduct extends Furniture {
  product: Product;
}
