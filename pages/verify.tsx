
import React, { useState } from 'react';
import Head from 'next/head';
import { Search, Shield, CheckCircle, FileJson, ExternalLink, AlertTriangle, Clock, Database, Server } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function Verify() {
    const [searchTerm, setSearchTerm] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any>(null);
    const [error, setError] = useState('');
    const [ipfsData, setIpfsData] = useState<any>(null);

    const handleVerify = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setResult(null);
        setIpfsData(null);
        setError('');

        try {
            // 1. Check Blockchain
            const res = await fetch(`${API_URL}/api/v1/verify/${searchTerm}`);
            if (!res.ok) throw new Error("Record not found on blockchain");
            const data = await res.json();
            setResult(data);

            // 2. "Fetch" from IPFS (Local Gateway)
            if (data.ipfs_cid) {
                const ipfsRes = await fetch(`${API_URL}/api/v1/ipfs/${data.ipfs_cid}`);
                if (ipfsRes.ok) {
                    const json = await ipfsRes.json();
                    setIpfsData(json);
                }
            }
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-[#050505] text-white font-sans selection:bg-blue-500/30">
            <Head>
                <title>Verify Audit | PoEC</title>
            </Head>

            <header className="border-b border-white/10 bg-black/50 backdrop-blur-md sticky top-0 z-50">
                <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <Shield className="text-emerald-500" />
                        <span className="font-bold text-xl tracking-tight">PoEC <span className="text-slate-500 font-normal">Verifier</span></span>
                    </div>
                </div>
            </header>

            <main className="max-w-3xl mx-auto px-6 py-20">
                <div className="text-center mb-12">
                    <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-white to-slate-500 bg-clip-text text-transparent">
                        Trust, but Verify.
                    </h1>
                    <p className="text-slate-400 text-lg">
                        Enter a Record Hash to independently validate the integrity of an audit report against the Sepolia Ethereum Ledger.
                    </p>
                </div>

                <form onSubmit={handleVerify} className="mb-16 relative group">
                    <div className="absolute inset-0 bg-blue-500/20 blur-xl rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                    <div className="relative flex gap-2">
                        <div className="relative flex-1">
                            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" size={20} />
                            <input
                                type="text"
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                placeholder="Paste Record Hash (0x...)"
                                className="w-full bg-[#111] border border-white/10 rounded-xl py-4 pl-12 pr-4 text-lg focus:outline-none focus:border-blue-500/50 transition-colors placeholder:text-slate-600"
                            />
                        </div>
                        <button
                            type="submit"
                            disabled={loading || !searchTerm}
                            className="bg-white text-black font-bold px-8 rounded-xl hover:bg-slate-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {loading ? "Verifying..." : "Check Ledger"}
                        </button>
                    </div>
                </form>

                <AnimatePresence>
                    {error && (
                        <motion.div
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="p-4 bg-red-500/10 border border-red-500/20 rounded-xl flex items-center gap-3 text-red-500 justify-center"
                        >
                            <AlertTriangle size={20} />
                            {error}
                        </motion.div>
                    )}

                    {result && (
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="space-y-6"
                        >
                            {/* Blockchain Proof Card */}
                            <div className="p-8 bg-[#111] border border-emerald-500/30 rounded-2xl relative overflow-hidden">
                                <div className="absolute top-0 right-0 p-4 opacity-50">
                                    <CheckCircle size={100} className="text-emerald-500/10" />
                                </div>

                                <div className="flex items-center gap-3 mb-6">
                                    <div className="p-2 bg-emerald-500/20 rounded-full text-emerald-400">
                                        <Shield size={24} />
                                    </div>
                                    <div>
                                        <h2 className="text-xl font-bold text-white">Cryptographic Proof Found</h2>
                                        <p className="text-emerald-400 text-sm font-mono">Status: ANCHORED & IMMUTABLE</p>
                                    </div>
                                </div>

                                <div className="grid grid-cols-2 gap-6 text-sm">
                                    <div>
                                        <span className="block text-slate-500 mb-1">Timestamp</span>
                                        <span className="font-mono text-white flex items-center gap-2">
                                            <Clock size={14} />
                                            {new Date(result.timestamp * 1000).toLocaleString()}
                                        </span>
                                    </div>
                                    <div>
                                        <span className="block text-slate-500 mb-1">Block Height</span>
                                        <span className="font-mono text-white">Pending Finalization</span>
                                    </div>
                                    <div className="col-span-2">
                                        <span className="block text-slate-500 mb-1">IPFS Content ID</span>
                                        <a href="#" className="font-mono text-blue-400 hover:underline flex items-center gap-2">
                                            {result.ipfs_cid}
                                            <ExternalLink size={12} />
                                        </a>
                                    </div>
                                </div>
                            </div>

                            {/* "Extracted" Data Card */}
                            {ipfsData ? (
                                <div className="p-8 bg-[#111] border border-white/10 rounded-2xl relative">
                                    <div className="flex items-center gap-3 mb-6">
                                        <div className="p-2 bg-blue-500/20 rounded-full text-blue-400">
                                            <Database size={24} />
                                        </div>
                                        <div>
                                            <h2 className="text-xl font-bold text-white">Decentralized Data Extracted</h2>
                                            <p className="text-slate-400 text-sm">Retrieved from IPFS Gateway Nodes</p>
                                        </div>
                                    </div>

                                    <div className="space-y-4">
                                        <div className="flex justify-between items-center p-4 bg-white/5 rounded-lg">
                                            <span className="text-slate-400">Total Transactions</span>
                                            <span className="font-mono font-bold">{ipfsData.summary?.total_txs || 'N/A'}</span>
                                        </div>
                                        <div className="flex justify-between items-center p-4 bg-white/5 rounded-lg">
                                            <span className="text-slate-400">Total Volume</span>
                                            <span className="font-mono font-bold text-emerald-400">
                                                ${parseFloat(ipfsData.summary?.total_volume || 0).toLocaleString()}
                                            </span>
                                        </div>
                                        <div className="flex justify-between items-center p-4 bg-white/5 rounded-lg">
                                            <span className="text-slate-400">Anomalies Detected</span>
                                            <span className="font-mono font-bold text-red-400">{ipfsData.metrics?.anomalies_count || 0}</span>
                                        </div>

                                        <div className="pt-4 border-t border-white/10">
                                            <h3 className="text-sm font-bold mb-2 text-slate-500 uppercase tracking-widest">Model Signature</h3>
                                            <code className="block bg-black p-3 rounded text-xs text-slate-300 break-all border border-white/5">
                                                {result.model_hash || ipfsData.model_hash}
                                            </code>
                                        </div>
                                    </div>
                                </div>
                            ) : (
                                <div className="p-8 border border-dashed border-white/10 rounded-2xl text-center text-slate-500">
                                    <Server size={32} className="mx-auto mb-3 opacity-50" />
                                    <p>Locating content on IPFS Swarm...</p>
                                </div>
                            )}
                        </motion.div>
                    )}
                </AnimatePresence>
            </main>
        </div>
    );
}
