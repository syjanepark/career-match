/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./*.html",
    "./*.js"
  ],
  theme: {
    extend: {
      fontFamily: {
        'manrope': ['Manrope', 'sans-serif'],
      },
      colors: {
        primary: {
          50: '#f4f9ff',
          100: '#cce7ff',
          200: '#b6dcfa',
          300: '#7db9e8',
          400: '#111518',
          500: '#555',
        }
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
} 