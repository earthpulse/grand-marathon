# Grand Marathon

This repository contains the code for the Grand Marathon delivery.

A deployed version of the application is available at [https://grand-marathon.earthpulse.ai/](https://grand-marathon.earthpulse.ai/).

## Running the Application locally

The easiest way to run the entire stack (API and Dashboard) is using **Docker Compose**.

### Prerequisites

1. **Docker and Docker Compose:** Ensure you have Docker installed on your machine.
2. **Git LFS (Large File Storage):** The datasets for this project are stored in the `data/` folder and are managed using Git LFS. You must pull the actual dataset files before running the application:
  - **macOS (Homebrew):**
  - **Ubuntu/Debian:**
    ```bash
    sudo apt-get install git-lfs
    git lfs install
    ```
  - **Windows:**
  Download and run the installer from the [Git LFS website](https://git-lfs.github.com/).
   Once Git LFS is installed, navigate to the project directory and pull the actual dataset files:

### Setup Environment Variables

The dashboard requires a `.env` file for configuration (such as the MapTiler API key). 

1. Copy the example environment file:
  ```bash
   cp dashboard/.env.example dashboard/.env
  ```
2. Open `dashboard/.env` and add your MapTiler API Key (obtainable from [MapTiler](https://www.maptiler.com/)):
  ```env
   API_URL=localhost:8000
   VITE_MAPTILER_API_KEY=your_maptiler_api_key_here
  ```

### Start the Application

To build and run both the backend API and the dashboard frontend, run the following command from the root directory:

```bash
docker compose up --build
```

Once the containers are running:

- **Dashboard (Frontend):** Accessible at [http://localhost:5173](http://localhost:5173)
- **API (Backend):** Accessible at [http://localhost:8000](http://localhost:8000)

## Recreating the data and AI Model

All the code to recreate the data and AI Model is available in the `model/` folder as Jupyter Notebooks.

First, you need to install the dependencies. We recommend using `uv`:

```bash
uv sync
```

This will create a virtual environment and install the dependencies.

More details about the data and AI Model are available in the `[model/README.md](model/README.md)` file.