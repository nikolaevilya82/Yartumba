/**
 * Глобальная настройка тестов
 */
import '@testing-library/jest-dom'

// Очистка моков после каждого теста
afterEach(() => {
  // MSW моки
  // import { server } from './mocks/server'
  // server.resetHandlers()
})

// Очистка после всех тестов
afterAll(() => {
  // import { server } from './mocks/server'
  // server.close()
})

// Моки window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
})
