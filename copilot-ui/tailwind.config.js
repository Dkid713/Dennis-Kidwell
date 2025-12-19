/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        copilot: {
          dark: '#0a1628',
          card: 'rgba(30, 41, 59, 0.7)',
          input: 'rgba(30, 41, 59, 0.9)',
          accent: '#3b82f6',
        }
      }
    },
  },
  plugins: [],
}
