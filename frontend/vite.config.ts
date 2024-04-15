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
        entryFileNames: 'assets/[name].js', // Output format for JS files
        assetFileNames: 'assets/[name].[ext]', // Output format for other assets (e.g., CSS, images)
        chunkFileNames: 'assets/[name].js', // Output format for chunk files
      },
      
    },
  },
});
