import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import svgr from 'vite-plugin-svgr';
import reactRefresh from '@vitejs/plugin-react-refresh';
import path from 'path';
import { PreRenderedAsset } from "rollup";
import commonjs from 'vite-plugin-commonjs';
import dotenv from 'dotenv';
import { resolve } from 'path';

dotenv.config({ path: resolve(__dirname, '.env') });

const assetDir = "assets";
const entryFileNames = `${assetDir}/[name].js`;
const chunkFileNames = `${assetDir}/[name].js`;

const assets = [
  { output: `${assetDir}/img/[name].[ext]`, regex: /\.(png|jpe?g|gif|svg|webp|avif|jpg)$/ },
  { output: `${assetDir}/css/[name].[ext]`, regex: /\.css$/ },
  { output: `${assetDir}/js/[name].[ext]`, regex: /\.js$/ },
  { output: `${assetDir}/[name][ext]`, regex: /\.xml$/ }
];

function processAssetFileNames(info: PreRenderedAsset): string {
  const name = info.name as string;
  const result = assets.find(a => a.regex.test(name));
  return result ? result.output : `${assetDir}/[name].[ext]`;
}

export default defineConfig({
  plugins: [
    svgr(),
    react(),
    reactRefresh(),
    commonjs()
  ],
  resolve: {
    alias: {
      '@mui/icons-material': '@mui/icons-material/esm',
    },
  },
  define: {
    'process.env': {
      VITE_LOCAL_API_BASE_URL: process.env.VITE_LOCAL_API_BASE_URL,
      VITE_API_BASE_URL: process.env.VITE_API_BASE_URL,
    },
  },
  build: {
    modulePreload: { polyfill: false },
    outDir: path.resolve(__dirname, '../dist'),
    manifest: 'manifest.json',
    emptyOutDir: true,
    chunkSizeWarningLimit: 1000, // Increase the limit to 1000 kB
    rollupOptions: {
      input: { main: path.resolve(__dirname, 'src/main.tsx') },
      output: {
        entryFileNames,
        assetFileNames: processAssetFileNames,
        chunkFileNames,
        manualChunks(id) {
          // Example: Manually group React and ReactDOM into a vendor chunk
          if (id.includes('node_modules/react') || id.includes('node_modules/react-dom')) {
            return 'vendor';
          }
        },
      },
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/static': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
});
