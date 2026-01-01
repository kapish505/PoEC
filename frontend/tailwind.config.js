/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./components/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            colors: {
                background: "#ffffff",
                foreground: "#0f172a",
                muted: "#f1f5f9",
                "muted-foreground": "#64748b",
                primary: "#0f172a",
                "primary-foreground": "#ffffff",
                accent: "#f8fafc",
                border: "#e2e8f0",
            },
            fontFamily: {
                sans: ["Inter", "sans-serif"],
            }
        },
    },
    plugins: [],
};
