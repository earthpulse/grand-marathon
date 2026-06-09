# Grand Marathon: Wildfire Hazard & Operational Priority Platform

Welcome to the **Grand Marathon** repository. This platform is an end-to-end machine learning and geospatial decision-support system designed to monitor daily wildfire hazard and compute operational response priorities. It was developed as an MVP validated against the catastrophic wildfire wave of August 2025 in Galicia, Spain.

For detailed local setup, Docker instructions, and dataset downloading, please refer to **[instructions.md](instructions.md)**.

This project was developed following an MVP-first approach, with priority given to delivering a complete operational platform rather than maximizing the sophistication of any single analytical component.

During the challenge, development focused on building and validating the full risk, alert, confirm, and act workflow, including wildfire hazard prediction, exposure and vulnerability assessment, operational prioritization, geospatial analytics, backend services, and an interactive decision-support dashboard.

The current hazard model represents the first operational implementation within this architecture and provides a validated baseline for the platform. The modular design allows individual capabilities to be progressively refined and expanded without requiring changes to the overall system.

[Deployed App](https://grand-marathon.earthpulse.ai/)

## 1. The August 2025 Galicia Wildfire Crisis

In August 2025, Galicia, Spain, suffered one of its most devastating wildfire crises, with the province of **Ourense** as the epicenter (accounting for **85.5%** of the region's total burned area with **101,584 hectares** burned). 

The largest single event was the **Larouco-Seadur megafire**:

- **Duration:** August 13 – August 31, 2025.
- **Burned Area:** **31,778.18 hectares** (19,630 ha of shrubland and 12,148 ha of woodland).
- **Impact:** Forced over 3,300 evacuations, confined nearly 10,000 residents, and caused widespread infrastructure and ecological damage.
- **Drivers:** Prolonged drought, extreme heat stress (WWA estimated extreme fire weather was made **40x more likely** by climate change), and high fuel loads from rural land abandonment.

## 2. AI Wildfire Hazard Model

The core predictive engine is a machine learning model that estimates daily fire hazard probabilities across the Area of Interest (AOI):

- **Model:** An **Optimized LightGBM Classifier** trained on a fire events dataset.
- **Ground Truth:** Real-world active fire hotspots detected by the **VIIRS** satellite instrument in 2025.
- **Features (Inputs):**
  1. `ndvi` (Normalized Difference Vegetation Index): Derived from Sentinel-2 L2A satellite imagery to measure fuel dryness and vegetation health.
  2. `t2m_1` to `t2m_5` (5-Day Temperature Series): Daily mean 2-meter air temperatures from **ERA5-Land reanalysis** looking back 5 days to capture cumulative heat stress.
- **Performance:** Achieved a stratified test accuracy of **71.04%** (with an F1 Score of **73.50%**, Precision of **69.00%**, Recall of **78.63%**, and ROC AUC of **0.7757**).
- **Model Selection & Tradeoffs:** After training and optimizing several candidate architectures (including Random Forest, XGBoost, LightGBM, and CatBoost), the **Optimized LightGBM Classifier** was selected and deployed for production. It delivers the highest predictive accuracy and generalization, maintains balanced calibration for smooth probability gradients, offers outstanding computational efficiency for daily map generation, and maximizes operational impact by providing the most reliable identification of high-risk areas. For a detailed comparative analysis and metrics, see the [model/README.md](model/README.md).

You can find the code for the AI model in the [model/01_hazard_model.ipynb](model/01_hazard_model.ipynb) notebook. Next palnned steps to improve the model can also be found in [model/README.md](model/README.md).

## 3. Rule-Based Operational Priority Framework

Rather than using a simple multiplicative risk index (`Hazard × Exposure × Vulnerability`), which often dilutes operational clarity, Grand Marathon implements a **decision-based, rule-based prioritization framework** using a **5×5×5 Lookup Table (LUT)**.

### Ordinal Scale (0–4)

All dimensions (Hazard, Exposure, Vulnerability) and the final Operational Priority are classified into five ordinal levels:

- `0`: No Data · `1`: Low · `2`: Medium · `3`: High · `4`: Critical / Critical Priority

### Core Decision Rules

- **Critical Priority (4):** Coincidence of High/Critical conditions across all dimensions, OR Critical hazard in areas with at least Medium exposure and vulnerability.
- **High Priority (3):** High/Critical hazard in highly exposed areas OR highly vulnerable communities.
- **Medium Priority (2):** Elevated hazard in areas with moderate exposure or vulnerability.
- **Low Priority (1):** All remaining valid combinations.

### High-Performance Architecture

To ensure sub-second daily runtimes, the pipeline is split into a **two-phase architecture**:

1. **Static Preprocessing (Run Once):** Heavy rasterization, reprojection, and alignment of population density (GHSL), OSM vector assets (roads, buildings, amenities), and municipal income vulnerability (INE) to the hazard grid template.
2. **Daily Execution (Run Daily):** Vectorized LUT calculations that combine daily hazard maps with the pre-aligned static layers in seconds.

## 4. End-to-End Technical Pipeline

The workflow is divided into six sequential Jupyter Notebooks located in the `model/` directory:

```text
+-------------------------+      +-------------------------+
|  01_hazard_model.ipynb  | ---> |  02_hazard_maps.ipynb   |
|  (Trains AI Model) |      | (Generates Daily Hazard)|
+-------------------------+      +------------+------------+
                                              |
                                              v  [Daily Hazard Maps]
+-------------------------+      +------------+------------+
| 03_vuln_exp_download    | ---> |  04_prepare_exp_vuln    |
| (Downloads Raw Vectors) |      | (Aligns Static Layers)  |
+-------------------------+      +------------+------------+
                                              |
                                              v  [Static Class Layers]
                                 +------------+------------+
                                 | 05_compute_operational  |
                                 | (Rule-Based LUT Engine) |
                                 +------------+------------+
                                              |
                                              v  [Base Analytics & Maps]
                                 +------------+------------+
                                 | 06_exposure_risk.ipynb  |
                                 | (Asset Risk Enrichment) |
                                 +-------------------------+
```

1. `01_hazard_model.ipynb`: Generates the training dataset and trains the AI model.
2. `02_hazard_maps.ipynb`: Generates daily continuous hazard maps for the AOI.
3. `03_vuln_exp_download.ipynb`: Downloads raw population (GHSL), OSM assets, and municipal vulnerability (INE).
4. `04_prepare_exp_vuln.ipynb`: Reprojects, rasterizes, and aligns static exposure and vulnerability layers to the hazard grid.
5. `05_compute_operational_priority.ipynb`: Computes daily classified hazard and operational priority maps, generating base analytics.
6. `06_exposure_risk.ipynb`: Samples specific OSM assets (buildings, roads, amenities) against daily priority maps to output risk-enriched vector layers and enriched analytics JSONs.

For a full technical and detailed report of the model, datasets, and pipeline, see the [Technical Report in model/README.md](model/README.md).

## 5. Repository Structure

- `model/`: Jupyter Notebooks, training scripts, and the technical report for the machine learning and geospatial pipeline.
- `api/`: FastAPI backend serving daily hazard maps, risk-enriched assets, and time-series analytics.
- `dashboard/`: React / Vite frontend featuring an interactive map, daily alerts, and analytical charts.
- `data/`: LFS-managed directory containing raw inputs, daily hazard GeoTIFFs, pre-calculated layers, and output JSON summaries.

## 6. Quick Start

To run the entire application locally using Docker Compose:

1. Pull datasets with Git LFS: `git lfs pull`
2. Create environment file: `cp dashboard/.env.example dashboard/.env` and add your MapTiler API Key.
3. Launch services: `docker compose up --build`
4. Open the frontend at [http://localhost:5173](http://localhost:5173) and the API docs at [http://localhost:8000/docs](http://localhost:8000/docs).

For step-by-step instructions, see **[instructions.md](instructions.md)**.

## 7. Platform Roadmap

The current MVP focuses on wildfire hazard prediction and operational prioritization. The broader platform vision extends across the full wildfire management lifecycle, from early risk identification and operational preparedness to active incident monitoring and post-event impact assessment.

Future development efforts may focus on:

- Increasing predictive accuracy through additional environmental variables and larger historical wildfire datasets, including nationwide records and European wildfire archives.
Extending the platform from hazard prediction to fire propagation analysis, enabling operational teams to assess not only where a wildfire is likely to occur, but also how it may evolve once active.
- Incorporating burned-area delineation, fire footprint reconstruction, and impact assessment capabilities using Earth Observation data acquired before, during, and after wildfire events.
- Leveraging both optical and SAR satellite imagery, together with high-resolution commercial Earth Observation data, to improve monitoring capabilities and damage assessment under a wider range of operational conditions.
- Benchmarking and validating platform outputs against established wildfire monitoring systems and services, including EFFIS and Copernicus products.
- Expanding operational analytics and decision-support capabilities through continued stakeholder engagement, co-design activities, and real-world operational validation.