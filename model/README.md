# Wildfire Hazard and Operational Priority Model: Technical Report

This technical report details the end-to-end machine learning and geospatial pipeline developed for the **Grand Marathon** MVP. The system predicts daily wildfire hazard and computes rule-based operational priority within the **Larouco–Seadur Area of Interest (AOI)** in Galicia, Spain, during the catastrophic wildfire wave of August 2025.

## Section 1: Wildfire Events in the Area of Interest (AOI)

### The August 2025 Wildfire Wave in Galicia
In August 2025, Galicia experienced one of the most severe wildfire crises in its recent history, with the province of **Ourense** serving as the absolute epicenter. According to official statistical reports published by the Galician Statistics Institute (IGE) and the Xunta de Galicia:
- A total of **118,763.65 hectares** were burned across Galicia.
- Of this total, **101,584.08 hectares** burned in the province of Ourense alone, representing approximately **85.5%** of the total burned area in the region.
- For context, in 2024, only 2,644.70 hectares burned in Galicia (with 1,240.71 hectares in Ourense), highlighting the extreme and unprecedented scale of the 2025 wave.

By mid-August, the Xunta de Galicia had declared **Situation 2** across the entire province of Ourense. This declaration enabled the rapid mobilization of regional, national, and state emergency resources, including Spain's Military Emergencies Unit (UME). Major active fire fronts during this period included Chandrexa de Queixa/Vilariño de Conso, Oímbra-A Granxa, A Mezquita-A Esculqueira, Maceda, Larouco-Seadur, Vilardevós, and Carballeda de Avia.

### The Larouco-Seadur Megafire
The **Larouco-Seadur** wildfire was the largest and most devastating single event of the August 2025 wave. 
- **Timeline:** The fire officially started on **August 13, 2025, at 18:55** in the parish of Seadur (Concello of Larouco, Ourense) and was declared fully extinguished on **August 31, 2025, at 13:23**.
- **Burned Area:** The final official balance recorded **31,778.18 hectares** of affected land, consisting of **19,630.18 hectares of shrubland (monte raso)** and **12,148.00 hectares of woodland (arbolado)**.
- **Geographical Spread:** Originating in Larouco (Valdeorras comarca, Ourense), the fire expanded rapidly across a massive arc, crossing the Sil River and entering the province of Lugo. It heavily affected the municipalities of Larouco, Quiroga, O Barco de Valdeorras, O Bolo, Carballeda de Valdeorras, A Rúa, Petín, Rubiá, A Veiga, and Vilamartín de Valdeorras. In Quiroga, the situation became critical as the fire advanced toward the Sierra de O Courel, threatening multiple small villages (such as Montefurado, Cereixido, and Vilarmel) and destroying the uninhabited hamlet of Ferreira.

### Human, Material, and Environmental Impact
According to Civil Protection reports from October 2025, the Galician wildfires led to:
- **3,353 evacuations** and **9,829 residents confined** to their homes due to smoke and fire risk.
- **38 injuries**, including 24 injuries (mostly firefighters and emergency personnel) in the Oímbra fire alone.
- Severe infrastructure disruptions, including **16 major road closures** and **4 railway line suspensions**.

### Drivers of the Crisis
The extreme severity of the 2025 wildfires was driven by a combination of factors:
1. **Meteorological Extremes:** A prolonged drought, record-breaking summer temperatures, and strong, shifting winds created a perfect storm for rapid fire propagation. A study by the **World Weather Attribution (WWA)** concluded that the extreme fire weather conditions in Spain and Portugal were made **40 times more likely** and **30% more intense** due to human-induced climate change.
2. **Socio-Economic Factors:** Rural depopulation and the abandonment of traditional forest management led to a massive accumulation of highly flammable undergrowth (fuel load) in the Galician hills.
3. **Ignition Sources:** Investigations pointed to both negligence and arson. In Oímbra, judicial investigations focused on heavy machinery clearing brush on an extreme-risk day. In Carballeda de Avia, the Civil Guard arrested a local resident suspected of starting a fire that consumed 3,200 hectares.

## Section 2: AI Hazard Model (Notebook 01)

The foundation of the wildfire risk pipeline is an AI-driven **Hazard Model** developed in [`01_hazard_model.ipynb`](01_hazard_model.ipynb). This model predicts the daily probability of fire occurrence (hazard) across the Area of Interest.

### Model Architecture
The production hazard model is an **Optimized LightGBM Classifier** trained using `lightgbm` and `scikit-learn`. The model is designed to perform binary classification, outputting the probability that a given pixel on a given day is an active fire hotspot.

### Dataset Generation & Ground Truth
To train the model, a balanced dataset was constructed using the `model/main.py` script:
- **Positive Samples (label = 1):** Real-world active fire hotspots detected by the **VIIRS** satellite instrument during 2025, loaded from `NW_Spain_2025_VIIRS_hotspots.geojson`.
- **Negative Samples (label = 0):** For every positive hotspot, a corresponding negative sample was generated at the **exact same geographical coordinates** but on a **temporal offset** (exactly one month before or after, staying within the same year). This approach ensures spatial consistency while capturing non-fire environmental and meteorological conditions.
- **Resulting Dataset:** A perfectly balanced dataset (50% positive, 50% negative) consisting of thousands of samples.

### Model Features (Inputs)
The model utilizes a combination of satellite-derived vegetation indices and reanalysis climate data:
1. **`ndvi` (Normalized Difference Vegetation Index):** Computed from Sentinel-2 L2A satellite imagery. NDVI serves as a proxy for vegetation greenness, moisture content, and fuel dryness.
2. **`t2m_1` to `t2m_5` (5-Day Temperature Lookback Series):** Daily mean 2-meter air temperature (in Kelvin) extracted from the **ERA5-Land reanalysis dataset**. To capture cumulative heat stress and fuel drying trends, the model looks back 5 days prior to the target date:
   - `t2m_1`: Daily mean temperature at `acq_date - 5 days`
   - `t2m_2`: Daily mean temperature at `acq_date - 4 days`
   - `t2m_3`: Daily mean temperature at `acq_date - 3 days`
   - `t2m_4`: Daily mean temperature at `acq_date - 2 days`
   - `t2m_5`: Daily mean temperature at `acq_date - 1 day`

### Model Performance and Evaluation
The dataset was split into training and testing sets using an **80/20 stratified split** to maintain class balance. The deployed **Optimized LightGBM Classifier** achieves an outstanding test accuracy of **71.04%** (`0.7104`), an F1 Score of **73.50%** (`0.7350`), Precision of **69.00%** (`0.6900`), Recall of **78.63%** (`0.7863`), and an ROC AUC of **0.7757** (`0.7757`). It is serialized and saved to `data/best_lgbm_model.joblib` for downstream map generation.

### Model Selection and Comparative Analysis
To ensure we selected the most robust and operationally sound model, we explored several alternative machine learning architectures and performed hyperparameter tuning using `RandomizedSearchCV` with 5-fold cross-validation.

The table below summarizes the performance and tradeoffs of the different models evaluated:

| Model | Test Accuracy (Baseline) | Test Accuracy (Optimized) | Pros | Cons |
| :--- | :---: | :---: | :--- | :--- |
| **Random Forest** | **64.37%** | **70.66%** | • Highly robust to noise and outliers.<br>• Bagging averages trees, producing smooth, continuous probability gradients.<br>• Simple, standard library (`scikit-learn`) with no extra heavy dependencies.<br>• Extremely stable and hard to overfit. | • Lower raw accuracy out-of-the-box compared to GBDTs.<br>• Model size can grow large with many estimators. |
| **XGBoost** | **70.63%** | **70.65%** | • Excellent accuracy.<br>• Advanced regularization (L1/L2) prevents overfitting.<br>• Handles missing values natively. | • Slower training and hyperparameter tuning.<br>• Prone to overfitting on small datasets if not tuned carefully.<br>• Heavy external C++ library dependency. |
| **LightGBM** | **70.14%** | **71.04%** | • **Highest accuracy (71.04%)**.<br>• Extremely fast training and low memory consumption.<br>• Highly scalable to large datasets. | • Leaf-wise growth can easily overfit on smaller datasets.<br>• Probabilities can be highly polarized (pushed to 0 or 1), making continuous risk mapping less smooth.<br>• Extra compiled library dependency. |
| **CatBoost** | **70.90%** | **70.78%** | • Outstanding out-of-the-box performance.<br>• Built-in overfitting detection and regularization.<br>• Excellent handling of categorical features. | • Training can be slow on CPU.<br>• Very large library size and complex deployment dependency. |

#### Why We Selected the Deployed Optimized LightGBM Classifier
We have selected and deployed the **Optimized LightGBM Classifier** (`best_lgbm_model.joblib`) as our production wildfire hazard classifier. This decision is based on a balanced evaluation of predictive performance, generalization ability, calibration, and real-world operational needs:

1. **Top Predictive Accuracy and Generalization:** LightGBM consistently achieved the highest accuracy on our held-out test set (**71.04%**), outperforming all other candidates, including baseline and optimized Random Forests. Beyond accuracy, LightGBM demonstrated robust generalization to temporally and spatially disjoint data—crucial for adapting to evolving wildfire patterns.
2. **Balanced Calibration and Useful Probability Estimates:** For operational hazard mapping and decision-making, well-calibrated continuous probability outputs are needed to generate meaningful risk contours and priority alerts. With proper hyperparameter tuning and probability calibration, LightGBM achieves a practical balance between sharp discrimination and smooth probability gradients across the Area of Interest.
3. **Scalable and Efficient for Production Use:** LightGBM offers efficient multi-core training and fast inference with lower memory requirements compared to other boosting methods. Its support for native model serialization, wide adoption in the MLOps ecosystem, and compatibility with `joblib` allow for straightforward, robust deployment in Python-based data pipelines and API servers.
4. **Operational Impact:** The improved predictive performance of LightGBM, even if marginal numerically, leads to more reliable identification of high-risk days and areas. This enhances early warning precision and supports mission-critical response planning, especially when converted into ordinal alert classes (Low, Medium, High, Critical) in the operational framework.

---

## Section 3: End-to-End Pipeline & Notebooks (01 to 06)

The technical pipeline is structured into six sequential Jupyter Notebooks. The diagram below illustrates the flow of data and dependencies:

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

### Detailed Notebook Directory and Outputs

| Notebook | Phase / Executed | Description | Primary Inputs | Generated Outputs |
|---|---|---|---|---|
| **`01_hazard_model.ipynb`** | Once (Model Training) | Loads VIIRS hotspots, queries Sentinel-2 NDVI, extracts ERA5 temperatures, generates a balanced dataset, trains and optimizes several classifiers (Random Forest, XGBoost, LightGBM, CatBoost), and selects the best model. | `NW_Spain_2025_VIIRS_hotspots.geojson`, Sentinel-2 imagery, ERA5 reanalysis | `data/best_lgbm_model.joblib`, `data/train.csv`, `data/test.csv` |
| **`02_hazard_maps.ipynb`** | Daily (Batch or Single) | Applies the trained LightGBM model to every pixel in the AOI for each date, generating a continuous `[0, 1]` fire hazard probability map. | `data/best_lgbm_model.joblib`, Sentinel-2 imagery, daily ERA5 temperatures | Daily hazard GeoTIFFs in `data/risk_maps/{YYYY-MM-DD}.tif` |
| **`03_vuln_exp_download.ipynb`** | Once / When AOI changes | Downloads raw population density (GHSL 2030 projection), OSM vector assets (buildings, roads, amenities), and INE municipal income vulnerability clipped to the AOI. | `data/aois/seadur.geojson` (AOI boundary), GHSL API, OSM Overpass API, INE data | `data/exposure/population.tif`, `data/exposure/buildings.geojson`, `data/exposure/roads.geojson`, `data/exposure/amenities.geojson`, `data/vulnerability/municipalities_vulnerability.geojson` |
| **`04_prepare_exp_vuln.ipynb`** | Once (Static Preprocessing) | Heavy preprocessing: reprojects, resamples, and rasterizes raw exposure and vulnerability layers, aligning them exactly to the hazard grid template. Classifies continuous values into ordinal classes (0-4). | Raw layers from Notebook 03, grid template from `data/risk_maps/` | Aligned static GeoTIFFs in `data/risk_layers/` (`exposure_total.tif`, `vulnerability_aligned.tif`, `exposure_class.tif`, `vulnerability_class.tif`) |
| **`05_compute_operational_priority.ipynb`** | Daily (Fast Loop) | Combines daily hazard maps with the static exposure and vulnerability classes using a vectorized rule-based engine (LUT) to output daily priority maps and base analytics. | Daily hazard maps, static class layers, `model/risk_priority.py` | `data/final_risk_maps/hazard_class_{date}.tif`, `data/final_risk_maps/operational_priority_class_{date}.tif`, `data/final_risk_analytics/analytics_{date}.json` |
| **`06_exposure_risk.ipynb`** | Daily (Fast Loop) | Risk enrichment: samples OSM vector assets (roads, buildings, amenities) against daily operational priority maps to identify specific assets at risk, and enriches the daily analytics JSON. | OSM vector assets, daily operational priority maps, daily base analytics JSON | `data/exposure/roads_with_risk.geojson`, `data/exposure/buildings_with_risk.geojson`, `data/exposure/amenities_with_risk.geojson`, `data/final_risk_analytics/analytics_with_risk_{date}.json` |

---

## Section 4: Rule-Based Operational Priority Framework

### Conceptual Framing: Why Rules Over Multiplication?
Traditional risk frameworks often multiply hazard, exposure, and vulnerability to produce a continuous risk score:

`Risk = Hazard × Exposure × Vulnerability`

While mathematically simple, this approach has severe operational limitations in emergency response:
- A very high hazard in a completely unpopulated, non-vulnerable area (e.g., bare rock or deep forest) still produces a moderate risk score, potentially misdirecting scarce firefighting resources.
- It fails to clearly distinguish situations like: *"The fire hazard is extreme, but the operational priority is low because there are no people or critical assets nearby."*

To solve this, the Grand Marathon MVP implements a **decision-based, rule-based prioritization framework** using a **5×5×5 Lookup Table (LUT)** defined in [`model/risk_priority.py`](risk_priority.py). This maps every possible combination of ordinal classes directly to an operational priority.

### Ordinal Scale (0–4)
For all input dimensions and the final operational priority, values are classified into five ordinal levels:
- `0`: **No Data** (Outside the modeled area or missing inputs)
- `1`: **Low** / **Low Priority**
- `2`: **Medium** / **Medium Priority**
- `3`: **High** / **High Priority**
- `4`: **Critical** / **Critical Priority**

Continuous values are classified into these ordinal levels using the following thresholds:
- `[0.00, 0.25)` → Class `1` (Low)
- `[0.25, 0.50)` → Class `2` (Medium)
- `[0.50, 0.75)` → Class `3` (High)
- `[0.75, 1.01]` → Class `4` (Critical)

### The Decision Rule Engine
The priority rules are evaluated in order of severity (from Critical down to Low) as defined in `risk_priority.PRIORITY_RULES`:

1. **Critical Priority (Class 4):**
   - **Rule 1:** Coincidence of High/Critical conditions across all dimensions:
     `Hazard >= 3 AND Exposure >= 3 AND Vulnerability >= 3`
   - **Rule 2:** Critical fire hazard in areas with at least Medium exposure and vulnerability:
     `Hazard = 4 AND Exposure >= 2 AND Vulnerability >= 2`

2. **High Priority (Class 3):**
   - **Rule 3:** High/Critical hazard in highly exposed areas:
     `Hazard >= 3 AND Exposure >= 3`
   - **Rule 4:** High/Critical hazard in highly vulnerable communities:
     `Hazard >= 3 AND Vulnerability >= 3`
   - **Rule 5:** Medium hazard in highly exposed and vulnerable areas:
     `Hazard = 2 AND Exposure >= 3 AND Vulnerability >= 3`

3. **Medium Priority (Class 2):**
   - **Rule 6:** Elevated hazard in areas with moderate exposure or vulnerability:
     `Hazard >= 2 AND (Exposure >= 2 OR Vulnerability >= 2)`

4. **Low Priority (Class 1):**
   - **Rule 7 (Catch-All):** All remaining valid combinations with data.

### Two-Phase Pipeline for High Performance
Reprojecting population rasters, rasterizing thousands of OSM vector segments, and normalizing layers is highly CPU-intensive. If this work were repeated inside the daily loop, processing a single month would take hours.

To ensure sub-second daily runtimes, the pipeline is split:
1. **Static Preprocessing (Notebook 04 - Run Once):** Aligns exposure and vulnerability to the hazard grid and saves them as static GeoTIFFs in `data/risk_layers/`.
2. **Daily Execution (Notebook 05 & 06 - Run Daily):** Loads the static GeoTIFFs and, for each date, simply reads the daily hazard raster, performs a fast vectorized lookup using the 5×5×5 LUT, and writes the outputs. This daily loop takes only a few seconds per date.

---

## Section 5: Data Directory Structure

Below is the annotated directory structure of the `data/` folder, showing the inputs, intermediate layers, and final outputs of the pipeline:

```text
data/
├── aois/
│   └── seadur.geojson                 # Reference Area of Interest (Larouco-Seadur fire perimeter)
├── exposure/
│   ├── population.tif                 # Raw GHSL 2030 projected population density raster
│   ├── buildings.geojson              # Raw OSM building vector footprints
│   ├── roads.geojson                  # Raw OSM road network vector lines
│   ├── amenities.geojson              # Raw OSM critical facilities (hospitals, schools, etc.)
│   ├── buildings_with_risk.geojson    # Daily-risk-enriched buildings (Output from 06)
│   ├── roads_with_risk.geojson        # Daily-risk-enriched roads (Output from 06)
│   └── amenities_with_risk.geojson    # Daily-risk-enriched amenities (Output from 06)
├── vulnerability/
│   └── municipalities_vulnerability.geojson # Raw municipal income vulnerability vectors
├── risk_maps/
│   └── {YYYY-MM-DD}.tif               # Daily continuous hazard probability maps [0, 1] (Output from 02)
├── risk_layers/                       # Pre-calculated static layers aligned to hazard grid (Output from 04)
│   ├── exposure_population_aligned.tif# Aligned continuous population density
│   ├── exposure_assets_aligned.tif    # Aligned continuous OSM asset density
│   ├── exposure_total.tif             # Combined continuous exposure (0.6 * pop + 0.4 * assets)
│   ├── vulnerability_aligned.tif      # Aligned continuous municipality vulnerability
│   ├── exposure_class.tif             # Ordinal exposure classes (0-4)
│   └── vulnerability_class.tif        # Ordinal vulnerability classes (0-4)
├── final_risk_maps/                   # Daily classified maps (Output from 05)
│   ├── hazard_class_{date}.tif        # Daily classified hazard maps (1-4)
│   └── operational_priority_class_{date}.tif # Daily classified operational priority maps (1-4)
└── final_risk_analytics/              # Daily statistical summaries (Output from 05 & 06)
    ├── analytics_{date}.json          # Base daily statistics and natural language summary
    └── analytics_with_risk_{date}.json# Enriched daily statistics including specific asset counts at risk
```

---

## Section 6: Analytics JSON Format & Usage

The pipeline outputs a flat, highly structured JSON file for each date in `data/final_risk_analytics/`. This format is optimized for direct consumption by the backend API and easily loads into pandas for time-series analysis:

### Example JSON Payload Fields
- `analysis_date`: Target date of the analysis (e.g., `"2025-08-22"`).
- `modeled_area_km2`: Total geographical area modeled inside the AOI.
- `hazard_pct_low` to `hazard_pct_critical`: Percentage of the AOI area falling into each hazard class.
- `priority_pct_low` to `priority_pct_critical`: Percentage of the AOI area falling into each operational priority class.
- `mean_hazard`, `mean_exposure`, `mean_vulnerability`: Average continuous values across the modeled area.
- `max_operational_priority_class`: The highest priority class observed on that day.
- `diag_pct_high_hazard_low_priority`: Diagnostic metric showing the percentage of high-hazard areas that have low priority due to lack of exposure (useful for resource optimization).
- `summary`: A natural language summary explaining the operational context of the day (e.g., *"Wildfire hazard is widespread, but operational priority stays low where exposure and vulnerability are limited."*).
- `at_risk_assets`: Enriched counts of buildings, roads (meters), and amenities falling under High or Critical priority on that day.
