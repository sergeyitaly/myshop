// vite.config.ts
import { defineConfig } from "file:///Volumes/WINDOC/TeamChalange/KOLORIT/myshop/frontend/node_modules/vite/dist/node/index.js";
import react from "file:///Volumes/WINDOC/TeamChalange/KOLORIT/myshop/frontend/node_modules/@vitejs/plugin-react/dist/index.mjs";
import svgr from "file:///Volumes/WINDOC/TeamChalange/KOLORIT/myshop/frontend/node_modules/vite-plugin-svgr/dist/index.js";
import reactRefresh from "file:///Volumes/WINDOC/TeamChalange/KOLORIT/myshop/frontend/node_modules/@vitejs/plugin-react-refresh/index.js";
import path from "path";
import commonjs from "file:///Volumes/WINDOC/TeamChalange/KOLORIT/myshop/frontend/node_modules/vite-plugin-commonjs/dist/index.mjs";
import dotenv from "file:///Volumes/WINDOC/TeamChalange/KOLORIT/myshop/frontend/node_modules/dotenv/lib/main.js";
import { resolve } from "path";
var __vite_injected_original_dirname = "/Volumes/WINDOC/TeamChalange/KOLORIT/myshop/frontend";
dotenv.config({ path: resolve(__vite_injected_original_dirname, ".env") });
var assetDir = "assets";
var entryFileNames = `${assetDir}/[name].js`;
var chunkFileNames = `${assetDir}/[name].js`;
var assets = [
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
function processAssetFileNames(info) {
  if (info && info.name) {
    const name = info.name;
    const result = assets.find((a) => a.regex.test(name));
    if (result) {
      return result.output;
    }
  }
  return `${assetDir}/[name].[ext]`;
}
var vite_config_default = defineConfig({
  plugins: [
    svgr(),
    react(),
    reactRefresh(),
    commonjs()
  ],
  resolve: {
    alias: {
      "@mui/icons-material": "@mui/icons-material/esm"
    }
  },
  define: {
    "process.env": process.env
  },
  build: {
    modulePreload: {
      polyfill: false
    },
    //  outDir: path.resolve(__dirname, 'static'), // Output directory resolved to myshop/frontend/static
    outDir: path.resolve(__vite_injected_original_dirname, "../dist"),
    manifest: "manifest.json",
    emptyOutDir: true,
    //delete everything in ..dist folder before build
    rollupOptions: {
      external: [".env"],
      input: {
        main: path.resolve(__vite_injected_original_dirname, "src/main.tsx")
        // Entry point for the application
      },
      output: {
        entryFileNames,
        assetFileNames: processAssetFileNames,
        chunkFileNames
      }
    }
  },
  server: {
    port: 5173,
    // Specify the port for the Vite development server
    proxy: {
      "/static": {
        target: "http://localhost:8000",
        // Proxy requests to Django development server
        changeOrigin: true
      }
    }
  }
});
export {
  assetDir,
  chunkFileNames,
  vite_config_default as default,
  entryFileNames,
  processAssetFileNames
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcudHMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCIvVm9sdW1lcy9XSU5ET0MvVGVhbUNoYWxhbmdlL0tPTE9SSVQvbXlzaG9wL2Zyb250ZW5kXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ZpbGVuYW1lID0gXCIvVm9sdW1lcy9XSU5ET0MvVGVhbUNoYWxhbmdlL0tPTE9SSVQvbXlzaG9wL2Zyb250ZW5kL3ZpdGUuY29uZmlnLnRzXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ltcG9ydF9tZXRhX3VybCA9IFwiZmlsZTovLy9Wb2x1bWVzL1dJTkRPQy9UZWFtQ2hhbGFuZ2UvS09MT1JJVC9teXNob3AvZnJvbnRlbmQvdml0ZS5jb25maWcudHNcIjtpbXBvcnQgeyBkZWZpbmVDb25maWcgfSBmcm9tICd2aXRlJztcbmltcG9ydCByZWFjdCBmcm9tICdAdml0ZWpzL3BsdWdpbi1yZWFjdCc7XG5pbXBvcnQgc3ZnciBmcm9tICd2aXRlLXBsdWdpbi1zdmdyJztcbmltcG9ydCByZWFjdFJlZnJlc2ggZnJvbSAnQHZpdGVqcy9wbHVnaW4tcmVhY3QtcmVmcmVzaCc7XG5pbXBvcnQgcGF0aCBmcm9tICdwYXRoJztcbmltcG9ydCB7IFByZVJlbmRlcmVkQXNzZXQgfSBmcm9tIFwicm9sbHVwXCI7XG5pbXBvcnQgY29tbW9uanMgZnJvbSAndml0ZS1wbHVnaW4tY29tbW9uanMnO1xuXG5pbXBvcnQgZG90ZW52IGZyb20gJ2RvdGVudic7XG5pbXBvcnQgeyByZXNvbHZlIH0gZnJvbSAncGF0aCc7XG5cbmRvdGVudi5jb25maWcoeyBwYXRoOiByZXNvbHZlKF9fZGlybmFtZSwgJy5lbnYnKSB9KTtcblxudHlwZSBBc3NldE91dHB1dEVudHJ5ID0ge1xuICBvdXRwdXQ6IHN0cmluZyxcbiAgcmVnZXg6IFJlZ0V4cFxufVxuXG5leHBvcnQgY29uc3QgYXNzZXREaXIgPSBcImFzc2V0c1wiO1xuZXhwb3J0IGNvbnN0IGVudHJ5RmlsZU5hbWVzID0gYCR7YXNzZXREaXJ9L1tuYW1lXS5qc2A7XG5leHBvcnQgY29uc3QgY2h1bmtGaWxlTmFtZXMgPSBgJHthc3NldERpcn0vW25hbWVdLmpzYFxuXG5jb25zdCBhc3NldHM6IEFzc2V0T3V0cHV0RW50cnlbXSA9IFtcbiAge1xuICAgIG91dHB1dDogYCR7YXNzZXREaXJ9L2ltZy9bbmFtZV0uW2V4dF1gLFxuICAgIHJlZ2V4OiAvXFwuKHBuZ3xqcGU/Z3xnaWZ8c3ZnfHdlYnB8YXZpZnxqcGcpJC9cbiAgfSxcbiAge1xuICAgIHJlZ2V4OiAvXFwuY3NzJC8sXG4gICAgb3V0cHV0OiBgJHthc3NldERpcn0vY3NzL1tuYW1lXS5bZXh0XWBcbiAgfSxcbiAge1xuICAgIG91dHB1dDogYCR7YXNzZXREaXJ9L2pzL1tuYW1lXS5bZXh0XWAsXG4gICAgcmVnZXg6IC9cXC5qcyQvXG4gIH0sXG4gIHtcbiAgICBvdXRwdXQ6IGAke2Fzc2V0RGlyfS9bbmFtZV1bZXh0XWAsXG4gICAgcmVnZXg6IC9cXC54bWwkL1xuICB9XG5dO1xuXG5leHBvcnQgZnVuY3Rpb24gcHJvY2Vzc0Fzc2V0RmlsZU5hbWVzKGluZm86IFByZVJlbmRlcmVkQXNzZXQpOiBzdHJpbmcge1xuICBpZiAoaW5mbyAmJiBpbmZvLm5hbWUpIHtcbiAgICBjb25zdCBuYW1lID0gaW5mby5uYW1lIGFzIHN0cmluZztcbiAgICBjb25zdCByZXN1bHQgPSBhc3NldHMuZmluZChhID0+IGEucmVnZXgudGVzdChuYW1lKSk7XG4gICAgaWYgKHJlc3VsdCkge1xuICAgICAgcmV0dXJuIHJlc3VsdC5vdXRwdXQ7XG4gICAgfVxuICB9XG4gIC8vIGRlZmF1bHQgc2luY2Ugd2UgZG9uJ3QgaGF2ZSBhbiBlbnRyeVxuICByZXR1cm4gYCR7YXNzZXREaXJ9L1tuYW1lXS5bZXh0XWBcbn1cblxuZXhwb3J0IGRlZmF1bHQgZGVmaW5lQ29uZmlnKHtcbiAgcGx1Z2luczogW1xuICAgIHN2Z3IoKSxcbiAgICByZWFjdCgpLFxuICAgIHJlYWN0UmVmcmVzaCgpLFxuICAgIGNvbW1vbmpzKClcbiAgXSxcbiAgcmVzb2x2ZToge1xuICAgIGFsaWFzOiB7XG4gICAgICAnQG11aS9pY29ucy1tYXRlcmlhbCc6ICdAbXVpL2ljb25zLW1hdGVyaWFsL2VzbScsXG4gICAgfSxcbiAgfSxcbiAgZGVmaW5lOiB7XG4gICAgJ3Byb2Nlc3MuZW52JzogcHJvY2Vzcy5lbnYsXG4gIH0sXG4gIGJ1aWxkOiB7XG4gICAgbW9kdWxlUHJlbG9hZDoge1xuICAgICAgcG9seWZpbGw6IGZhbHNlLFxuICAgIH0sXG5cbiAgICAvLyAgb3V0RGlyOiBwYXRoLnJlc29sdmUoX19kaXJuYW1lLCAnc3RhdGljJyksIC8vIE91dHB1dCBkaXJlY3RvcnkgcmVzb2x2ZWQgdG8gbXlzaG9wL2Zyb250ZW5kL3N0YXRpY1xuICAgIG91dERpcjogcGF0aC5yZXNvbHZlKF9fZGlybmFtZSwgJy4uL2Rpc3QnKSxcbiAgICBtYW5pZmVzdDogJ21hbmlmZXN0Lmpzb24nLFxuICAgIGVtcHR5T3V0RGlyOiB0cnVlLCAvL2RlbGV0ZSBldmVyeXRoaW5nIGluIC4uZGlzdCBmb2xkZXIgYmVmb3JlIGJ1aWxkXG4gICAgcm9sbHVwT3B0aW9uczoge1xuICAgICAgZXh0ZXJuYWw6IFsnLmVudiddLFxuICAgICAgaW5wdXQ6IHtcbiAgICAgICAgbWFpbjogcGF0aC5yZXNvbHZlKF9fZGlybmFtZSwgJ3NyYy9tYWluLnRzeCcpLCAvLyBFbnRyeSBwb2ludCBmb3IgdGhlIGFwcGxpY2F0aW9uXG4gICAgICB9LFxuICAgICAgb3V0cHV0OiB7XG4gICAgICAgIGVudHJ5RmlsZU5hbWVzOiBlbnRyeUZpbGVOYW1lcyxcbiAgICAgICAgYXNzZXRGaWxlTmFtZXM6IHByb2Nlc3NBc3NldEZpbGVOYW1lcyxcbiAgICAgICAgY2h1bmtGaWxlTmFtZXM6IGNodW5rRmlsZU5hbWVzXG4gICAgICB9LFxuICAgIH0sXG4gIH0sXG5cbiAgc2VydmVyOiB7XG4gICAgcG9ydDogNTE3MywgLy8gU3BlY2lmeSB0aGUgcG9ydCBmb3IgdGhlIFZpdGUgZGV2ZWxvcG1lbnQgc2VydmVyXG4gICAgcHJveHk6IHtcbiAgICAgICcvc3RhdGljJzoge1xuICAgICAgICB0YXJnZXQ6ICdodHRwOi8vbG9jYWxob3N0OjgwMDAnLCAvLyBQcm94eSByZXF1ZXN0cyB0byBEamFuZ28gZGV2ZWxvcG1lbnQgc2VydmVyXG4gICAgICAgIGNoYW5nZU9yaWdpbjogdHJ1ZSxcbiAgICAgIH0sXG4gICAgfSxcbiAgfSxcbn0pO1xuIl0sCiAgIm1hcHBpbmdzIjogIjtBQUE4VSxTQUFTLG9CQUFvQjtBQUMzVyxPQUFPLFdBQVc7QUFDbEIsT0FBTyxVQUFVO0FBQ2pCLE9BQU8sa0JBQWtCO0FBQ3pCLE9BQU8sVUFBVTtBQUVqQixPQUFPLGNBQWM7QUFFckIsT0FBTyxZQUFZO0FBQ25CLFNBQVMsZUFBZTtBQVR4QixJQUFNLG1DQUFtQztBQVd6QyxPQUFPLE9BQU8sRUFBRSxNQUFNLFFBQVEsa0NBQVcsTUFBTSxFQUFFLENBQUM7QUFPM0MsSUFBTSxXQUFXO0FBQ2pCLElBQU0saUJBQWlCLEdBQUcsUUFBUTtBQUNsQyxJQUFNLGlCQUFpQixHQUFHLFFBQVE7QUFFekMsSUFBTSxTQUE2QjtBQUFBLEVBQ2pDO0FBQUEsSUFDRSxRQUFRLEdBQUcsUUFBUTtBQUFBLElBQ25CLE9BQU87QUFBQSxFQUNUO0FBQUEsRUFDQTtBQUFBLElBQ0UsT0FBTztBQUFBLElBQ1AsUUFBUSxHQUFHLFFBQVE7QUFBQSxFQUNyQjtBQUFBLEVBQ0E7QUFBQSxJQUNFLFFBQVEsR0FBRyxRQUFRO0FBQUEsSUFDbkIsT0FBTztBQUFBLEVBQ1Q7QUFBQSxFQUNBO0FBQUEsSUFDRSxRQUFRLEdBQUcsUUFBUTtBQUFBLElBQ25CLE9BQU87QUFBQSxFQUNUO0FBQ0Y7QUFFTyxTQUFTLHNCQUFzQixNQUFnQztBQUNwRSxNQUFJLFFBQVEsS0FBSyxNQUFNO0FBQ3JCLFVBQU0sT0FBTyxLQUFLO0FBQ2xCLFVBQU0sU0FBUyxPQUFPLEtBQUssT0FBSyxFQUFFLE1BQU0sS0FBSyxJQUFJLENBQUM7QUFDbEQsUUFBSSxRQUFRO0FBQ1YsYUFBTyxPQUFPO0FBQUEsSUFDaEI7QUFBQSxFQUNGO0FBRUEsU0FBTyxHQUFHLFFBQVE7QUFDcEI7QUFFQSxJQUFPLHNCQUFRLGFBQWE7QUFBQSxFQUMxQixTQUFTO0FBQUEsSUFDUCxLQUFLO0FBQUEsSUFDTCxNQUFNO0FBQUEsSUFDTixhQUFhO0FBQUEsSUFDYixTQUFTO0FBQUEsRUFDWDtBQUFBLEVBQ0EsU0FBUztBQUFBLElBQ1AsT0FBTztBQUFBLE1BQ0wsdUJBQXVCO0FBQUEsSUFDekI7QUFBQSxFQUNGO0FBQUEsRUFDQSxRQUFRO0FBQUEsSUFDTixlQUFlLFFBQVE7QUFBQSxFQUN6QjtBQUFBLEVBQ0EsT0FBTztBQUFBLElBQ0wsZUFBZTtBQUFBLE1BQ2IsVUFBVTtBQUFBLElBQ1o7QUFBQTtBQUFBLElBR0EsUUFBUSxLQUFLLFFBQVEsa0NBQVcsU0FBUztBQUFBLElBQ3pDLFVBQVU7QUFBQSxJQUNWLGFBQWE7QUFBQTtBQUFBLElBQ2IsZUFBZTtBQUFBLE1BQ2IsVUFBVSxDQUFDLE1BQU07QUFBQSxNQUNqQixPQUFPO0FBQUEsUUFDTCxNQUFNLEtBQUssUUFBUSxrQ0FBVyxjQUFjO0FBQUE7QUFBQSxNQUM5QztBQUFBLE1BQ0EsUUFBUTtBQUFBLFFBQ047QUFBQSxRQUNBLGdCQUFnQjtBQUFBLFFBQ2hCO0FBQUEsTUFDRjtBQUFBLElBQ0Y7QUFBQSxFQUNGO0FBQUEsRUFFQSxRQUFRO0FBQUEsSUFDTixNQUFNO0FBQUE7QUFBQSxJQUNOLE9BQU87QUFBQSxNQUNMLFdBQVc7QUFBQSxRQUNULFFBQVE7QUFBQTtBQUFBLFFBQ1IsY0FBYztBQUFBLE1BQ2hCO0FBQUEsSUFDRjtBQUFBLEVBQ0Y7QUFDRixDQUFDOyIsCiAgIm5hbWVzIjogW10KfQo=
