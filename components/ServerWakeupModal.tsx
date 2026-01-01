
import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Server, Clock, AlertTriangle, ArrowRight } from 'lucide-react';
import Link from 'next/link';

interface ServerWakeupModalProps {
    status: 'checking' | 'online' | 'offline';
}

export default function ServerWakeupModal({ status }: ServerWakeupModalProps) {
    const [progress, setProgress] = useState(0);

    // Fake progress bar to manage user patience (45s duration)
    useEffect(() => {
        if (status === 'online') {
            setProgress(100);
            return;
        }

        const interval = setInterval(() => {
            setProgress(prev => {
                if (prev >= 95) return 95; // Stall at 95% until actually online
                return prev + (100 / 450); // Increment to reach 100 in ~45s (assuming 100ms interval)
            });
        }, 100);

        return () => clearInterval(interval);
    }, [status]);

    if (status === 'online') return null;

    return (
        <div className="fixed inset-0 z-[100] bg-[#0a0a0a] flex items-center justify-center p-6">
            <div className="max-w-md w-full text-center space-y-8">

                {/* Icon Animation */}
                <div className="relative w-24 h-24 mx-auto">
                    <div className="absolute inset-0 bg-blue-500/20 rounded-full animate-ping"></div>
                    <div className="relative z-10 w-full h-full bg-[#111] border border-blue-500/30 rounded-full flex items-center justify-center text-blue-400">
                        <Server size={40} />
                    </div>
                </div>

                <div className="space-y-4">
                    <h2 className="text-2xl font-bold text-white">Waking up Analysis Engine</h2>
                    <p className="text-slate-400">
                        The backend is spinning up from a cold start on the Render Network.
                        This usually takes about <span className="text-white font-bold">30-50 seconds</span>.
                    </p>
                </div>

                {/* Progress Bar */}
                <div className="space-y-2">
                    <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
                        <motion.div
                            className="h-full bg-blue-500"
                            initial={{ width: 0 }}
                            animate={{ width: `${progress}%` }}
                            transition={{ ease: "linear" }}
                        />
                    </div>
                    <div className="flex justify-between text-xs text-slate-500 font-mono">
                        <span>ESTIMATING RESOURCES...</span>
                        <span>{Math.round(progress)}%</span>
                    </div>
                </div>

                {/* Actions */}
                <div className="pt-8 border-t border-white/10">
                    <p className="text-sm text-slate-500 mb-4">While you wait, you can read about the tech:</p>
                    <div className="flex gap-4 justify-center">
                        <Link href="/" className="text-sm text-slate-400 hover:text-white flex items-center gap-1 transition-colors">
                            Home <ArrowRight size={14} />
                        </Link>
                        <Link href="/about" className="text-sm text-slate-400 hover:text-white flex items-center gap-1 transition-colors">
                            Technical Architecture <ArrowRight size={14} />
                        </Link>
                    </div>
                </div>

            </div>
        </div>
    );
}
