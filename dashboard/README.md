# Grand Marathon MVP - Operator Dashboard

A high-performance, responsive web dashboard built with **Svelte 5** and **SvelteKit** designed for wildfire risk assessment, multi-source alert verification, and tactical response deployment.

---

## 🌟 Key Features & Core Pages

The dashboard is structured around five core operational pillars, following the logical flow of emergency response:

### 1. 📊 Dashboard (Risk Assessment)
* **Interactive Map**: Displays multi-criteria risk maps by combining meteorological hazard (FWI), population/asset exposure, and territorial vulnerability.
* **Granular Layer Controls**: Toggle individual risk components (Hazard, Exposure, Vulnerability) to understand the exact drivers behind any risk classification.
* **Temporal Slider**: Travel through time to analyze how risk levels evolve across different dates.

### 2. ✅ Confirm (Multi-Source Verification)
* **False Alarm Filtering**: Serves as the critical gatekeeper before committing expensive emergency response assets.
* **Evidence Correlation**: Automatically aggregates geolocated web scraper results, social media reports (e.g., Twitter/X), and civil protection feeds.
* **Operator Decision Terminal**: Allows manual confirmation/dismissal of candidate alerts, or programmatic confirmation via PATCH API endpoints.

### 3. 🔔 Alerts (Management)
* **Lifecycle Tracking**: Complete CRUD management of alerts, tracking status (`Unconfirmed`, `Confirmed`, `Resolved`) and severity levels.
* **Intelligent Diagnostics**: Highlights primary alert drivers and suggests optimal verification routes.

### 4. 🚀 Actions (Deployment)
* **Tactical Spatial Analysis**: Automatically generates a bounding Area of Interest (AOI) around confirmed incidents.
* **Exposure Matrix**: Intersects the AOI with population density, critical infrastructure, escape corridors, and assets at risk.
* **SOP Generator**: Automatically recommends and ranks Standard Operating Procedures (SOPs) into priority tiers (`Immediate`, `Next`, `Monitor`) with clear rationales.

### 5. 📋 Report (Briefing)
* **Chronological Audit Trail**: Compiles a tamper-proof timeline of all sensor detections, scraper evidence, operator confirmations, and tactical dispatches.
* **Shareable Briefs**: Generates structured PDF reports containing incident details, confidence scores, and deployed actions.
* **Stakeholder Dispatch**: Integrates with email and external webhooks to instantly notify incident commanders and emergency networks.

---

## 🛠️ Tech Stack & Architecture

* **Frontend Framework**: [Svelte 5](https://svelte.dev/) & [SvelteKit](https://kit.svelte.dev/)
  * Implements Svelte 5 **Runes** (`$state`, `$derived`, `$effect`) for fine-grained, ultra-fast reactivity.
* **Styling**: [Tailwind CSS](https://tailwindcss.com/) for a clean, modern, and fully responsive UI.
* **Map Engine**: Custom map components integrating Leaflet/Mapbox for high-performance GeoJSON rendering and raster image overlays.
* **State Management**: Modular Svelte 5 class-based stores:
  * `confirmStore`: Handles multi-source verification and news correlation.
  * `alertsStore`: Manages the CRUD lifecycle of alerts.
  * `actionsStore`: Manages tactical response actions.
  * `actStore`: Coordinates the active workspace between confirmed alerts and actions.

---

## 🚀 Getting Started

### Prerequisites
Make sure you have [Bun](https://bun.sh/) (recommended) or [Node.js](https://nodejs.org/) installed.

### Installation
Install the project dependencies:
```bash
bun install
# or
npm install
```

### Environment Configuration
The dashboard uses environment variables to communicate with the backend API.
* `.env.development`: Used during local development.
* `.env.production`: Used in production builds.

Example configuration:
```env
API_URL=http://localhost:8000
```

### Developing
Start the local development server:
```bash
bun run dev
# or
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser to view the application.

### Building
To build a production-ready version of the dashboard:
```bash
bun run build
# or
npm run build
```
You can preview the production build locally using:
```bash
bun run preview
# or
npm run preview
```

---

## 📚 Built-in Documentation
The dashboard includes an interactive **Operator Manual** built directly into the app under the `/docs` route. It provides a step-by-step walkthrough of all 17 operational steps from initial risk assessment to closing the feedback loop.
