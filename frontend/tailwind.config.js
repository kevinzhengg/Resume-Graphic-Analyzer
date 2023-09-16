/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        "accent-800": "#5f0f40",
        "accent-700": "#9a031e",
        "primary-500": "#fb8b24",
        "secondary-700": "#e36414",
        "tertiary-900": "#0f4c5c"
      }
    },
  },
  plugins: [],
}