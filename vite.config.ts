import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import svgr from 'vite-plugin-svgr' 

const cssFileName = 'index.min.css'


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), svgr()], 

  publicDir: './public',
  build: {
    manifest: "manifest.json",
    rollupOptions: {
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