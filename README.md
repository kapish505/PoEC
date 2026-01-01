# PoEC: Proof of Economic Cyclic Anomaly Detection

A production-grade prototype for detecting economic anomalies in transaction networks and anchoring evidence to the blockchain.

## Features
- **Ingestion**: Upload CSV transaction data with schema validation.
- **Graph AI**: Detects circular trading (closed loops) and suspicious dense clusters.
- **Integrity**: Anchors dataset and result hashes to an Ethereum testnet (or local Hardhat network).
- **Dashboard**: Light-mode, institutional-grade UI for analysis and verification.

## Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.10+ (for local scripts, optional)

## Quick Start

### 1. Start Services
Run the entire stack with Docker Compose:
```bash
docker-compose up --build
```
This starts:
- **Backend API**: http://localhost:8000
- **Frontend Dashboard**: http://localhost:3000
- **PostgreSQL**: Port 5432

### 2. Deploy Smart Contract (Local)
In a separate terminal, deploy the ProofAnchor contract to the local Hardhat network (if running locally) or ensure environment variables are set for testnet.
```bash
cd contracts
npm install
npx hardhat node # Start local node
# In another tab
npx hardhat run scripts/deploy.js --network localhost
```
*Note: Docker backend is configured to look for host network; ensure `ETHEREUM_NODE_URL` is reachable.*

### 3. Generate Data
Generate a synthetic dataset with fraud patterns:
```bash
python3 generate_data.py
# Creates demo_dataset.csv
```

### 4. Run Analysis
1. Open http://localhost:3000
2. Upload `demo_dataset.csv`.
3. Click **Run Analysis**.
4. View the Graph and Anomalies (Circular Trading should be flagged).
5. Click **Anchor to Chain** (Mocked in UI for demo, or connects to backend).

## Verification
Use the `/api/v1/verify/{hash}` endpoint to prove that the analysis result hash matches the immutable record on-chain.
