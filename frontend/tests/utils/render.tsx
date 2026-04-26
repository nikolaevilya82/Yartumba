import { render, type RenderOptions } from '@testing-library/react'
import type { ReactElement } from 'react'

// Импорт провайдеров если нужны (Router, ThemeProvider, etc.)
// import { BrowserRouter } from 'react-router-dom'
// import { ThemeProvider } from '...'

interface AllTheProvidersProps extends RenderOptions {
  // providers props
}

function AllTheProviders({ children }: { children: ReactElement }) {
  // Wrap with providers
  return <>{children}</>
}

const customRender = (
  ui: ReactElement,
  options?: AllTheProvidersProps
) => render(ui, {
  wrapper: AllTheProviders,
  ...options,
})

// Re-export everything
export * from '@testing-library/react'

// Override the default render
export { customRender as render }
