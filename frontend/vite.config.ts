// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import svgr from 'vite-plugin-svgr';
import reactRefresh from '@vitejs/plugin-react-refresh';
import path from 'path';
import {PreRenderedAsset} from "rollup";

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
      regex: /\.(png|jpe?g|gif|svg|webp|avif)$/
  },
  {
      regex: /\.css$/,
      output: `${assetDir}/css/[name].[ext]`
  },
  {
      output: `${assetDir}/[name].[ext]`,
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
    emptyOutDir: true, //delete everything in ..dist folder before build
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, 'src/main.tsx'), // Entry point for the application
      },
      output: {
        entryFileNames: entryFileNames,
        assetFileNames: processAssetFileNames,
        chunkFileNames: chunkFileNames
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
