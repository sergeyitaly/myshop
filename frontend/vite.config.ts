// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import svgr from 'vite-plugin-svgr';
import reactRefresh from '@vitejs/plugin-react-refresh';
import path from 'path';

export default defineConfig({
  plugins: [
    svgr(),
    react(),
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
      },
      output: {
        entryFileNames: '[name].js', // Output format for JS files
        assetFileNames: 'assets/[name].[ext]', // Output format for other assets (e.g., CSS, images)
        chunkFileNames: '[name].js', // Output format for chunk files
      },
    },
  },

  server: {
    port: 5173, // Specify the port for the Vite development server
    proxy: {
      '/static': {
        target: 'http://localhost:8000', // Proxy requests to Django development server
        changeOrigin: true,
      },
    },
  },
});
