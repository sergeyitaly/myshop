import { defineConfig } from 'vite';
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  build: {
    minify: 'esbuild',  // Minify the code using esbuild for faster builds
    sourcemap: false,  // Disable source maps in production
    rollupOptions: {
      plugins: [visualizer({ open: true })],  // Open the visualizer report in the browser
    },
  },
});
