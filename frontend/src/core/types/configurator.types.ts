import type { FurnitureType } from '../constants/product.constants';
import type { MaterialType } from '../constants/configurator.constants';

// Опция выбора материала
export interface MaterialOption {
  id: number;
  name: string;
  type: MaterialType;
  color?: string;
  texture?: string;
  price_modifier: number;
  image?: string;
}

// Опция кромки
export interface EdgeOption {
  id: number;
  name: string;
  type: string;
  thickness: number;
  color?: string;
  price_modifier: number;
}

// Опция фурнитуры (направляющие)
export interface SlideGuideOption {
  id: number;
  name: string;
  type: string;
  extend_type: string;
  price_modifier: number;
}

// Опция фурнитуры (петли)
export interface HingeOption {
  id: number;
  name: string;
  type: string;
  opening_angle: number;
  price_modifier: number;
}

// Опция опор/ножек
export interface SupportOption {
  id: number;
  name: string;
  type: string;
  height: number;
  material?: string;
  price_modifier: number;
}

// Опция крепления (настенное)
export interface WallMountOption {
  id: number;
  name: string;
  type: string;
  max_weight: number;
  price_modifier: number;
}

// Полный набор опций для конфигуратора
export interface ConfiguratorOptions {
  materials: MaterialOption[];
  edges: EdgeOption[];
  slideGuides: SlideGuideOption[];
  hinges: HingeOption[];
  supports: SupportOption[];
  wallMounts: WallMountOption[];
}

// Конфигурация одной части изделия
export interface PartConfiguration {
  part_type: string;
  material_id?: number;
  edge_id?: number;
  width: number;
  height: number;
  thickness: number;
  quantity: number;
}

// Конфигурация товара
export interface FurnitureConfiguration {
  furniture_type: FurnitureType;
  width: number;
  height: number;
  depth: number;
  shelf_count?: number;
  drawer_count?: number;
  row_count?: number;
  has_back_panel?: boolean;
  has_door?: boolean;
  has_mirror?: boolean;
  leg_height?: number;
  parts: PartConfiguration[];
  // Выбранные материалы
  body_material_id?: number;
  shelf_material_id?: number;
  facade_material_id?: number;
  edge_material_id?: number;
  slide_guide_id?: number;
  hinge_id?: number;
  support_id?: number;
  wall_mount_id?: number;
}

// Результат расчёта конфигурации
export interface ConfigurationCalculation {
  total_price: number;
  material_cost: number;
  hardware_cost: number;
  labor_cost: number;
  dimensions: {
    width: number;
    height: number;
    depth: number;
  };
  parts_count: number;
  estimated_time?: number; // минуты
}

// Сохранённая конфигурация
export interface SavedConfiguration {
  id: number;
  name: string;
  furniture_type: FurnitureType;
  configuration: FurnitureConfiguration;
  total_price: number;
  created_at: string;
  updated_at: string;
}

// Тип конфигуратора
export type ConfiguratorMode = 'create' | 'edit' | 'view';
