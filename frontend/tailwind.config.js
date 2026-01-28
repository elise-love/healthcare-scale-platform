import colors from "tailwindcss/colors";

/** @type {import('tailwindcss').Config} */)}
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
        "../app/templates/**/*.html"
    ],
    theme: {
        colors: {
            gray: colors.slate,
            blue: colors.sky,
            red: colors.rose,
            pink: colors.fuchsia,
        },
        fontFamily: {
            sans: ["Graphik", "ui-sans-serif", "system-ui", "sans-serif"],
            serif: ["Merriweather", "ui-serif", "Georgia", "serif"],
        },
        extend: {
            spacing: {
                '128': '32rem',
                '144': '36rem',
            },
            borderRadius: {
                '4xl': '2rem',
      },
    },
  },
  plugins: [],
};
{
  "css.lint.unknownAtRules": "ignore"
}

