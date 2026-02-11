# Genomic Foundation Model (GFM) Platform

Welcome to the GFM Platform, an advanced web application designed for AI-powered genomic research. This platform provides a suite of tools for analyzing DNA sequences, managing research, and interacting with a specialized AI assistant.

## ✨ Features

Based on the integrated tutorial, the platform includes:

-   **Dashboard Overview**: A central hub to view your research activity, including total runs, confidence scores, recent results, and active jobs.
-   **New Analysis Runs**: Submit DNA sequences, FASTA files, or genomic regions for AI-powered predictions.
-   **Detailed Results**: View prediction scores, confidence assessments, and evidence panels with links to external databases like UCSC and Ensembl.
-   **Research Notebook**: A rich-text notebook to document research, embed result snapshots, and track version history for reproducibility.
-   **AI Assistant**: An integrated chat interface to help explain results, compare analyses, and answer questions about your genomic research.

## 🛠️ Tech Stack

This project is built with a modern, robust technology stack:

-   **Frontend Framework**: [React](https://reactjs.org/)
-   **Language**: [TypeScript](https://www.typescriptlang.org/)
-   **Styling**: [Tailwind CSS](https://tailwindcss.com/)
-   **UI Components**: Custom components, likely using a library like [shadcn/ui](https://ui.shadcn.com/).
-   **Data Fetching & State Management**: [TanStack Query (React Query)](https://tanstack.com/query/latest)
-   **Routing**: [React Router](https://reactrouter.com/)
-   **Icons**: [Lucide React](https://lucide.dev/)

## 🚀 Getting Started

Follow these instructions to get a local copy up and running for development and testing purposes.

### Prerequisites

Make sure you have the following installed on your machine:

-   [Node.js](https://nodejs.org/) (v18 or newer recommended)
-   [npm](https://www.npmjs.com/), [yarn](https://yarnpkg.com/), or [pnpm](https://pnpm.io/)

### Installation

1.  **Clone the repository:**
    ```sh
    git clone <your-repository-url>
    cd genomic_model_ai
    ```

2.  **Install dependencies:**
    ```sh
    npm install
    # or
    yarn install
    # or
    pnpm install
    ```

3.  **Set up environment variables:**

    The application requires an API key to communicate with the AI model. Create a `.env.local` file in the root of the project and add your key:

    ```env
    # For Create React App or similar setups
    REACT_APP_AI_API_KEY="your_api_key_here"

    # For Vite
    VITE_AI_API_KEY="your_api_key_here"
    ```
    *Note: The variable name (`REACT_APP_` or `VITE_`) depends on your build tool. Update the code in `src/components/Chatbox.tsx` to use the correct environment variable.*

### Running the Application

Start the development server:

```sh
npm run dev
# or
npm start
```

Open your browser and navigate to `http://localhost:5173` (for Vite) or `http://localhost:3000` (for Create React App).

## 📁 Project Structure

The `src` folder contains the core application code:

-   `components/`: Reusable React components (`Chatbox.tsx`, `Tutorial.tsx`, etc.).
-   `components/UI/`: Generic UI components like `Button`, `Dialog`, etc.
-   `lib/`: Utility functions, such as `cn` for merging class names.
-   `pages/` or `routes/`: (Likely) Components that represent full pages/routes.
-   `app.tsx`: The main application component that sets up routing and providers.
-   `main.tsx`: The entry point of the application.

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improving the platform, please feel free to open an issue or submit a pull request.

## 📄 License

This project is proprietary. All rights reserved. (Or specify an open-source license like MIT if applicable).