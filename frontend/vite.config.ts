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

type AssetOutputEntry = {
  output: string,
  regex: RegExp
}

export const assetDir = "assets";
export const entryFileNames = `${assetDir}/[name].js`;
export const chunkFileNames = `${assetDir}/[name].js`

const assets: AssetOutputEntry[] = [
  {
    output: `${assetDir}/img/[name].[ext]`,
    regex: /\.(png|jpe?g|gif|svg|webp|avif|jpg)$/
  },
  {
    regex: /\.css$/,
    output: `${assetDir}/css/[name].[ext]`
  },
  {
    output: `${assetDir}/js/[name].[ext]`,
    regex: /\.js$/
  },
  {
    output: `${assetDir}/[name][ext]`,
    regex: /\.xml$/
  }
];

export function processAssetFileNames(info: PreRenderedAsset): string {
  if (info && info.name) {
    const name = info.name as string;
    const result = assets.find(a => a.regex.test(name));
    if (result) {
      return result.output;
    }
  }
  // default since we don't have an entry
  return `${assetDir}/[name].[ext]`
}

// Define the base API URL based on the environment
const apiBaseUrl = process.env.NODE_ENV === 'production' ? 'https://vercel.com' : 'http://localhost:8000';

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
    'process.env': process.env,
  },
  build: {
    modulePreload: {
      polyfill: false,
    },
    outDir: path.resolve(__dirname, '../dist'),
    manifest: 'manifest.json',
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, 'src/main.tsx'),
      },
      output: {
        entryFileNames: entryFileNames,
        assetFileNames: processAssetFileNames,
        chunkFileNames: chunkFileNames
      },
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/static': {
        target: apiBaseUrl,
        changeOrigin: true,
      },
    },
  },
});
