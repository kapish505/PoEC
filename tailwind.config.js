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
            },
            animation: {
                'progress-indeterminate': 'progress-indeterminate 1.5s infinite linear',
            },
            keyframes: {
                'progress-indeterminate': {
                    '0%': { transform: 'translateX(0) scaleX(0)' },
                    '40%': { transform: 'translateX(0) scaleX(0.4)' },
                    '100%': { transform: 'translateX(100%) scaleX(0.5)' },
                }
            }
        },
    },
    plugins: [],
};
