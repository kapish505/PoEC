import React from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { ArrowLeft, ArrowRight, Cpu, Database, Link as LinkIcon, Layers, Network, ShieldCheck, Activity } from 'lucide-react';

export default function About() {
    return (
        <div className="min-h-screen bg-[#0a0a0a] text-stone-200 font-sans selection:bg-purple-500/30">
            <Head>
                <title>About PoEC | Technical Deep Dive</title>
            </Head>

            <nav className="fixed top-0 w-full z-50 backdrop-blur-md border-b border-white/10 bg-black/50">
                <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
                    <Link href="/" className="flex items-center gap-2 text-sm font-medium text-slate-400 hover:text-white transition-colors">
                        <ArrowLeft size={16} /> Back to Home
                    </Link>
                    <span className="text-xs font-mono text-slate-500 uppercase tracking-widest hidden md:block">
                        Technical Whitepaper v1.0
                    </span>
                </div>
            </nav>

            <main className="pt-32 pb-20 px-6 max-w-4xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    className="mb-20"
                >
                    <span className="text-purple-400 font-mono text-xs uppercase tracking-widest mb-4 block">System Architecture</span>
                    <h1 className="text-4xl md:text-6xl font-bold mb-8 text-white">The Hybrid Neuro-Symbolic Engine.</h1>
                    <p className="text-xl text-slate-400 leading-relaxed">
                        PoEC (Proof of Economic Cycle) bridges the gap between opaque Deep Learning models and rigid legacy rule engines.
                        It employs a dual-layer detection strategy to maximize recall while maintaining explainability.
                    </p>
                </motion.div>

                <div className="space-y-24">
                    {/* Section 1: The Math */}
                    <section className="group">
                        <div className="flex items-center gap-4 mb-8">
                            <div className="p-3 bg-purple-500/10 rounded-lg text-purple-400">
                                <Cpu size={24} />
                            </div>
                            <h2 className="text-3xl font-bold text-white">1. Geometric Deep Learning</h2>
                        </div>
                        <div className="pl-4 border-l-2 border-purple-500/20 space-y-6">
                            <p className="text-slate-400 leading-7">
                                At the core of PoEC is a <strong>Graph Autoencoder (GAE)</strong> built on PyTorch Geometric.
                                Unlike tabular models (Random Forest, XGBoost) that treat transactions as isolated rows, GAE understands the <em>topology</em> of the network.
                            </p>

                            <div className="bg-[#111] p-6 rounded-xl border border-white/10 my-8 font-mono text-sm text-slate-300">
                                <p className="mb-2 text-purple-400">// The Encoder</p>
                                <p className="mb-4">Z = GCN(X, A)</p>
                                <p className="mb-2 text-purple-400">// The Decoder</p>
                                <p>Â = σ(Z Z^T)</p>
                            </div>

                            <p className="text-slate-400 leading-7">
                                The model learns a low-dimensional embedding <code>Z</code> for every node. It then attempts to reconstruct the adjacency matrix <code>A</code>.
                                Financial crimes like <strong>Smurfing</strong> and <strong>Circular Trading</strong> create unnatural geometric distortions that are hard to compress.
                                The model fails to reconstruct these specific edges effectively, resulting in a high <strong>Reconstruction Error</strong>. This error becomes the "Anomaly Score".
                            </p>
                        </div>
                    </section>

                    {/* Section 2: Patterns */}
                    <section>
                        <div className="flex items-center gap-4 mb-8">
                            <div className="p-3 bg-blue-500/10 rounded-lg text-blue-400">
                                <Network size={24} />
                            </div>
                            <h2 className="text-3xl font-bold text-white">2. Detectable Topologies</h2>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pl-4 border-l-2 border-blue-500/20">
                            <div className="p-6 bg-white/5 rounded-xl border border-white/10 hover:border-blue-500/50 transition-colors">
                                <h3 className="text-white font-bold mb-2 flex items-center gap-2"><Activity size={16} className="text-blue-400" /> Circular Trading</h3>
                                <p className="text-sm text-slate-400">
                                    Funds moving A &rarr; B &rarr; C &rarr; A. This creates artificial volume to manipulate market sentiment or launder money without net value transfer.
                                </p>
                            </div>
                            <div className="p-6 bg-white/5 rounded-xl border border-white/10 hover:border-blue-500/50 transition-colors">
                                <h3 className="text-white font-bold mb-2 flex items-center gap-2"><Network size={16} className="text-blue-400" /> Dense Clusters</h3>
                                <p className="text-sm text-slate-400">
                                    Unnaturally high connectivity within a subgroup (Cliques). Often indicates botnets or collusion rings where members trade primarily with each other.
                                </p>
                            </div>
                            <div className="p-6 bg-white/5 rounded-xl border border-white/10 hover:border-blue-500/50 transition-colors">
                                <h3 className="text-white font-bold mb-2 flex items-center gap-2"><Layers size={16} className="text-blue-400" /> Structuring (Smurfing)</h3>
                                <p className="text-sm text-slate-400">
                                    Fan-out / Fan-in patterns where large sums are split into micro-transactions to evade reporting thresholds, then consolidated later.
                                </p>
                            </div>
                        </div>
                    </section>

                    {/* Section 3: Anchoring */}
                    <section>
                        <div className="flex items-center gap-4 mb-8">
                            <div className="p-3 bg-emerald-500/10 rounded-lg text-emerald-400">
                                <LinkIcon size={24} />
                            </div>
                            <h2 className="text-3xl font-bold text-white">3. Cryptographic Chain of Custody</h2>
                        </div>
                        <div className="pl-4 border-l-2 border-emerald-500/20 space-y-6">
                            <p className="text-slate-400 leading-7">
                                Machine Learning findings are statistically probabilistic, making them weak in court. PoEC solidifies them using the **ProofAnchor** protocol.
                            </p>
                            <p className="text-slate-400 leading-7">
                                Every detection event generates a hash triplet verifying:
                            </p>
                            <ul className="list-disc list-inside text-slate-400 space-y-2 ml-4">
                                <li><strong>Input Integrity:</strong> Hash of the raw CSV snapshot.</li>
                                <li><strong>Model Version:</strong> Hash of the GNN weights.</li>
                                <li><strong>Output Integrity:</strong> Hash of the resulting Anomaly JSON.</li>
                            </ul>
                            <p className="text-slate-400 leading-7">
                                This triplet is mined to the Ethereum blockchain. This makes it mathematically impossible for an admin to retroactively alter the evidence or the logs without breaking the chain.
                            </p>
                        </div>
                    </section>

                    {/* Section 4: Stack */}
                    <section>
                        <div className="flex items-center gap-4 mb-8">
                            <div className="p-3 bg-slate-800 rounded-lg text-slate-400">
                                <Database size={24} />
                            </div>
                            <h2 className="text-3xl font-bold text-white">4. Technology Stack</h2>
                        </div>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                            {[
                                ["Frontend", "Next.js 14", "React", "TailwindCSS"],
                                ["Visualization", "Cytoscape.js", "WebGL", "Framer Motion"],
                                ["Backend", "FastAPI", "Python 3.10", "NetworkX"],
                                ["AI Core", "PyTorch Geometric", "Pandas", "Scikit-Learn"],
                                ["Database", "PostgreSQL", "SQLAlchemy", "Alembic"],
                                ["Blockchain", "Solidity", "Hardhat", "Ethers.js"]
                            ].map((stack, i) => (
                                <div key={i} className="p-4 bg-white/5 rounded-lg border border-white/10">
                                    <h3 className="text-xs font-bold text-slate-500 uppercase mb-3">{stack[0]}</h3>
                                    <ul className="space-y-1">
                                        {stack.slice(1).map((item, j) => (
                                            <li key={j} className="text-sm text-slate-300 border-b border-white/5 pb-1 last:border-0">{item}</li>
                                        ))}
                                    </ul>
                                </div>
                            ))}
                        </div>
                    </section>
                </div>

                <div className="mt-20 pt-10 border-t border-white/10 text-center">
                    <h3 className="text-2xl font-bold text-white mb-6">Ready to deploy?</h3>
                    <Link href="/dashboard" className="inline-flex items-center gap-2 px-8 py-4 bg-purple-600 hover:bg-purple-500 text-white rounded-full font-bold transition-all shadow-lg hover:shadow-purple-500/25">
                        Launch Dashboard <ArrowRight size={18} />
                    </Link>
                </div>
            </main>
        </div>
    );
}
