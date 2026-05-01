/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0f1729",
        panel: "#121b30",
        teal: "#2dd4bf",
        coral: "#fb7185",
        sand: "#f4c95d",
        mist: "#d6e4ff",
      },
      boxShadow: {
        glow: "0 18px 50px rgba(45, 212, 191, 0.12)",
      },
      fontFamily: {
        display: ["'Space Grotesk'", "sans-serif"],
        body: ["'Manrope'", "sans-serif"],
      },
    },
  },
  plugins: [],
};
