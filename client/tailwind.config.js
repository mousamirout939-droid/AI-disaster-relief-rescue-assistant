/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#fff1f1', 100: '#ffe0e0', 200: '#ffc6c6', 300: '#ff9d9d',
          400: '#ff6666', 500: '#f83b3b', 600: '#e51f1f', 700: '#c11515',
          800: '#9f1616', 900: '#841919',
        },
        safe: {
          50: '#eefdf3', 100: '#d6f9e2', 200: '#b0f0c9', 300: '#7ce2ab',
          400: '#45cc89', 500: '#20b06d', 600: '#148d58', 700: '#127048',
          800: '#12593b', 900: '#104a32',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
    },
  },
  plugins: [],
}
