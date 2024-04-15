import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import svgr from 'vite-plugin-svgr';
import { TanStackRouterVite } from '@tanstack/router-vite-plugin';
import reactRefresh from '@vitejs/plugin-react-refresh';
import path from 'path';

export default defineConfig({
  plugins: [
    svgr(),
    react(),
    TanStackRouterVite(),
    reactRefresh(),
  
  ],
  
  build: {
    modulePreload: {
      polyfill: false,
    },
    outDir: path.resolve(__dirname, '../dist'), // Output directory resolved to myshop/dist
    manifest: 'manifest.json',
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, 'src/main.tsx'), // Entry point for the application
        index: './index.html', // Index HTML file
      },
      output: {
        entryFileNames: '[name].js', // Output format for JS files
        assetFileNames: (assetInfo) => {
          // Determine if the asset is a CSS file
          const isCss = assetInfo.name.endsWith('.css');

          // Output CSS files directly to 'dist' folder
          return isCss ? `[name].[ext]` : `assets/[name].[ext]`;
        },
        chunkFileNames: '[name].js', // Output format for chunk files
      },
      
    },
  },
});
