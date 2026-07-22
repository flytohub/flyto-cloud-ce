import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./tests/setupStorage.js'],
    include: [
      'tests/**/*.spec.js',
      'tests/**/*.test.js',
      'src/**/__tests__/*.test.js',
      'src/**/__tests__/*.spec.js'
    ],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      include: ['src/**/*.{js,vue}'],
      exclude: ['src/**/*.spec.js', 'src/**/*.test.js'],
      thresholds: {
        statements: 21,
        branches: 77,
        functions: 53,
        lines: 21
      }
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  }
})
