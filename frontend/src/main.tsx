import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.scss'
import { routeTree } from './routeTree.gen'
import { RouterProvider, createRouter } from '@tanstack/react-router'

const router = createRouter({ routeTree })

declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)

// This line is important for React Fast Refresh (HMR)
if (import.meta.hot) {
  import.meta.hot.accept();
}