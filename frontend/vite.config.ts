import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import svgr from 'vite-plugin-svgr';
import reactRefresh from '@vitejs/plugin-react-refresh';
import path from 'path';
import commonjs from 'vite-plugin-commonjs';
import dotenv from 'dotenv';
import { resolve } from 'path';

dotenv.config({ path: resolve(__dirname, '.env') });

const assetDir = "assets";
const entryFileNames = `${assetDir}/[name].[hash].js`; // Adjusted entryFileNames pattern
const chunkFileNames = `${assetDir}/[name].[hash].js`; // Adjusted chunkFileNames pattern

const assets = [
  { output: `${assetDir}/img/[name].[hash].[ext]`, regex: /\.(png|jpe?g|gif|svg|webp|avif)$/ },
  { output: `${assetDir}/css/[name].[hash].css`, regex: /\.css$/ },
  { output: `${assetDir}/js/[name].[hash].js`, regex: /\.js$/ },
  { output: `${assetDir}/[name].[hash].[ext]`, regex: /\.xml$/ }
];

function processAssetFileNames(info) {
  const name = info.name;
  const result = assets.find(a => a.regex.test(name));
  return result ? result.output : `${assetDir}/[name].[hash].[ext]`;
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
      VITE_LOCAL_API_BASE_URL: JSON.stringify(process.env.VITE_LOCAL_API_BASE_URL),
      VITE_API_BASE_URL: JSON.stringify(process.env.VITE_API_BASE_URL),
    }
  },
  build: {
    chunkSizeWarningLimit: 1000,
    target: 'es2015',
    outDir: path.resolve(__dirname, '../dist'),
    manifest: true, // Generate manifest automatically
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, 'src/main.tsx')
      },
      output: {
        entryFileNames,
        assetFileNames: processAssetFileNames,
        chunkFileNames,
        format: 'cjs' // Ensure output is in CommonJS format
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
