import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import svgLoader from 'vite-plugin-svgr';
import { TanStackRouterVite } from '@tanstack/router-vite-plugin';

const cssFileName = 'index.min.css';

export default defineConfig({
  plugins: [
    react(), svgLoader(), TanStackRouterVite(),
  ],
  build: {
    //outDir: '../../static',
    manifest: 'manifest.json',
    rollupOptions: {
      input: ['/src/main.tsx', './index.html'],
      output: {
        entryFileNames: `assets/js/[name].min.js`, // Output path for JS files
        assetFileNames: `assets/css/${cssFileName}`, // Output path for CSS files
        chunkFileNames: `assets/js/[name]-[hash].js`, // Output path for chunk files
      },
    },
  },
});
