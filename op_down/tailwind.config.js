/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './downloader/templates/**/*.html',  // Adjust this path to match your template structure
    './downloader/static/**/*.js',       // Include any JavaScript files if you're using Tailwind in JavaScript
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
