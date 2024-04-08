import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import svgr from "vite-plugin-svgr";
import { TanStackRouterVite } from '@tanstack/router-vite-plugin';


const cssFileName = 'index.min.css'


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), svgr(), TanStackRouterVite(),], 
  build: {
    manifest: 'manifest.json',
    rollupOptions: {
      input: ['/src/main.tsx', './index.html'],
      output: {
        assetFileNames: (file) => {
          return `assets/css/${cssFileName}`
        },
        entryFileNames: (file) => {
          return `assets/js/[name].min.js`
        }
      }
    }
  }

})