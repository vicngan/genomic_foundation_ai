# Genomic Foundation Model (GFM) Platform

Welcome to the GFM Platform, an advanced web application designed for AI-powered genomic research. This platform provides a suite of tools for analyzing DNA sequences, managing research, and interacting with a specialized AI assistant.

## ✨ Features

Based on the integrated tutorial, the platform includes:

-   **Dashboard Overview**: A central hub to view your research activity, including total runs, confidence scores, recent results, and active jobs.
-   **New Analysis Runs**: Submit DNA sequences, FASTA files, or genomic regions for AI-powered predictions.
-   **Detailed Results**: View prediction scores, confidence assessments, and evidence panels with links to external databases like UCSC and Ensembl.
-   **Research Notebook**: A rich-text notebook to document research, embed result snapshots, and track version history for reproducibility.
-   **AI Assistant**: An integrated chat interface to help explain results, compare analyses, and answer questions about your genomic research.

## 🏛️ Architecture

This application uses a client-server architecture:

-   **Frontend**: A modern React single-page application (SPA) that provides the user interface.
-   **Backend**: A Python server built with FastAPI that hosts the Parlant AI agent and exposes a REST API for the frontend to consume.

## 🛠️ Tech Stack

This project is built with a modern, robust technology stack:

-   **Frontend**:
    -   **Framework**: [React](https://reactjs.org/)
    -   **Language**: [TypeScript](https://www.typescriptlang.org/)
    -   **Styling**: [Tailwind CSS](https://tailwindcss.com/)
    -   **UI Components**: Custom components, likely using a library like [shadcn/ui](https://ui.shadcn.com/).
    -   **Routing**: [React Router](https://reactrouter.com/)
-   **Backend**:
    -   **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
    -   **Language**: [Python](https://www.python.org/)
    -   **AI SDK**: [Parlant](https://www.parlant.io/docs/quickstart/installation/) 

## 🚀 Getting Started

Follow these instructions to get a local copy up and running for development and testing purposes.

### Prerequisites

Make sure you have the following installed on your machine:

-   [Node.js](https://nodejs.org/) (v18 or newer recommended)
-   [npm](https://www.npmjs.com/), [yarn](https://yarnpkg.com/), or [pnpm](https://pnpm.io/)
-   [Python](https://www.python.org/downloads/) (v3.8 or newer recommended) & `pip`

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone <your-repository-url>
    cd genomic_model_ai
    ```

2.  **Set up the Backend:**
    Navigate to the backend directory, create a virtual environment, and install dependencies.
    ```sh
    cd backend
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```
    This backend is a minimal FastAPI stub (`backend/main.py`) with `/health` and `/chat` endpoints.

3.  **Set up the Frontend:**
    From the root directory, install the Node.js dependencies.
    ```sh
    # In the root 'genomic_model_ai' directory
    npm install
    # or
    yarn install
    ```

4.  **Set up Parlant (Emcie) for the AI Assistant:**
    Parlant requires Python 3.10+ and installs via pip.
    ```sh
    pip install parlant
    ```
    Start the Parlant server in a dedicated folder (it uses the working directory for runtime data).
    ```sh
    mkdir -p parlant-server
    cd parlant-server
    parlant-server run
    ```
    In a new terminal, create an agent and copy its ID.
    ```sh
    parlant agent create --name "GFM Assistant"
    ```
    Set your Emcie API key (Emcie is the default NLP service for Parlant).
    ```sh
    export EMCIE_API_KEY="<YOUR_API_KEY>"
    ```
    Then set the frontend env vars (see `.env.example`):
    ```sh
    VITE_PARLANT_SERVER=http://localhost:8800
    VITE_PARLANT_AGENT_ID=<paste-agent-id>
    ```
    The chat UI is provided by the official React widget `parlant-chat-react`.

### Running the Application

You will need to run both the backend and frontend servers in separate terminal windows.

1.  **Start the Backend Server:**
    From the `backend` directory (with the virtual environment activated):
    ```sh
    uvicorn main:app --reload
    ```
    The backend API will be running at `http://localhost:8000`.

2.  **Start the Frontend Server:**
    From the root project directory:
    ```sh
    npm run dev
    ```
    The frontend will be running at `http://localhost:5173` (for Vite) or `http://localhost:3000` (for Create React App).



## 📁 Project Structure

-   `src/`: Contains the frontend React application code.
    -   `components/`: Reusable React components (`Chatbox.tsx`, etc.).
    -   `App.tsx`: The main application component.
-   `backend/`: Contains the backend Python/FastAPI application.
    -   `main.py`: The main API server file (minimal stub with `/health` and `/chat`).
    -   `requirements.txt`: Python package dependencies.

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improving the platform, please feel free to open an issue or submit a pull request.

## 📄 License

This project is proprietary. All rights reserved. (Or specify an open-source license like MIT if applicable).
