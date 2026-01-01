# PoEC Deployment Guide

You have chosen the **Hybrid Architecture**:
*   **Frontend**: Vercel (Fast, Global CDN)
*   **Backend**: Render (run as a Docker Container for PyTorch GNN)

## 1. Deploy Backend (Render)
1.  Log in to [dashboard.render.com](https://dashboard.render.com/).
2.  Click **New +** and select **Blueprint**.
3.  Connect your GitHub repository (`kapish505/PoEC`).
4.  Render will automatically detect `render.yaml`.
5.  Click **Apply**.
6.  Wait for the build to finish (it make take ~5-10 minutes for the first build).
7.  **Copy your Backend URL** (e.g., `https://poec-backend.onrender.com`).

## 2. Deploy Frontend (Vercel)
1.  Log in to [vercel.com](https://vercel.com/).
2.  Click **Add New Project**.
3.  Import the `kapish505/PoEC` repository.
4.  **Settings**: Leave everything as **Default**. (Root Directory should be empty/`.`).
5.  **Important**: In the **Environment Variables** section, add:
    *   **Name**: `NEXT_PUBLIC_API_URL`
    *   **Value**: `https://poec-backend.onrender.com` (The URL you copied from Render).
6.  Click **Deploy**.

## 3. Verify
Once Vercel finishes:
1.  Open your Vercel URL.
2.  Check the "Server Status" indicator in the dashboard header.
3.  Upload a CSV to confirm the full pipeline works.
