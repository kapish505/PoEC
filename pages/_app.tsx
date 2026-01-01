import "@/styles/globals.css";
import type { AppProps } from "next/app";
import { Inter } from "next/font/google";
import { BackendProvider } from "../components/BackendContext";
import GlobalStatus from "../components/GlobalStatus";

const inter = Inter({ subsets: ["latin"] });

export default function App({ Component, pageProps }: AppProps) {
    return (
        <div className={inter.className}>
            <BackendProvider>
                <Component {...pageProps} />
                <GlobalStatus />
            </BackendProvider>
        </div>
    );
}
