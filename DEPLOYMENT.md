# 🚀 Deployment Guide for CampusPal

This project consists of two parts:
1.  **Backend** (FastAPI/Python) -> Deploy on **Render** (Free).
2.  **Frontend** (React/Vite) -> Deploy on **Vercel** (Free).

---

## 1. Deploy Backend (Render)

**Option A: The Easy Way (Blueprint)** 🌟
1.  Push your code to GitHub.
2.  Go to [dashboard.render.com/blueprints](https://dashboard.render.com/blueprints).
3.  Click **"New Blueprint Instance"**.
4.  Select your `CampusPal` repository.
5.  Render will automatically read the `render.yaml` file and configure everything for you!
6.  You will be prompted to enter your `GROQ_API_KEY`.
7.  Click **"Apply"** and wait for it to go Live.

**Option B: Manual Setup**
1.  Create a **"New Web Service"**.
    *   **Runtime**: Python 3
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `uvicorn backend:app --host 0.0.0.0 --port $PORT`
2.  Add Environment Variable: `GROQ_API_KEY`.

---

## 2. Deploy Frontend (Vercel)

1.  Go to [vercel.com](https://vercel.com/) and "Add New Project".
2.  Import the same GitHub repository (`CampusPal`).
3.  Configure the project:
    *   **Framework Preset**: **Vite** (Should auto-detect).
    *   **Root Directory**: Click "Edit" and select `frontend`. **(Crucial Step!)**
4.  **Environment Variables**:
    *   Key: `VITE_API_URL`
    *   Value: `https://campuspal-backend.onrender.com` (The URL you copied from Render).
    *   *Note: Do not add a trailing slash `/`.*
5.  Click **"Deploy"**.

---

## 3. Verification

1.  Open your Vercel App URL (e.g., `https://campuspal-frontend.vercel.app`).
2.  The Chat Widget should appear.
3.  Type "Hi".
    *   If it responds, **Success!** 🎉
    *   If it says "Error: Could not connect", check:
        *   Did you add `GROQ_API_KEY` in Render?
        *   Did you add `VITE_API_URL` in Vercel?
    
---

## 4. Run with Docker 🐳

Prefer to run everything continuously in containers? We support Docker!

### Prerequisites
*   [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
*   A `.env` file in the root directory with your `GROQ_API_KEY`.

### Steps
1.  Open a terminal in the project root.
2.  Run the following command:
    ```bash
    docker-compose up --build
    ```
3.  Wait for the build to complete.
4.  **Access the App**:
    *   Frontend: `http://localhost` (Port 80)
    *   Backend API: `http://localhost:8000`

### Troubleshooting Docker
*   **"Groq API Key missing"**: Ensure your `.env` file exists and is populated.
*   **"Ports already allocated"**: Make sure you stopped the local `uvicorn` and `npm run dev` processes before running Docker.
