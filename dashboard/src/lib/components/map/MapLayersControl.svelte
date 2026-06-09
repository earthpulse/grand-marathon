<script>
    import ImageLayer from "./ImageLayer.svelte";
    import GeoJSONLayer from "./GeoJSONLayer.svelte";

    let {
        api_url,
        selected,
        hotspots = null,
        activeTab = $bindable("risk"),
        showRisk = $bindable(true),
        showHazard = $bindable(false),
        showHotspots = $bindable(false),
        showPopulation = $bindable(false),
        showBuildings = $bindable(false),
        showRoads = $bindable(false),
        showAmenities = $bindable(false),
        showMunicipalities = $bindable(false),
    } = $props();

    // Data cache
    let buildingsData = $state(null);
    let roadsData = $state(null);
    let amenitiesData = $state(null);
    let municipalitiesData = $state(null);

    // Loading states
    let loadingBuildings = $state(false);
    let loadingRoads = $state(false);
    let loadingAmenities = $state(false);
    let loadingMunicipalities = $state(false);

    const buildingsOptions = $derived({
        style: (feature) => {
            let riskVal = null;
            const risk = feature.properties?.risk;
            if (risk) {
                if (Array.isArray(risk)) {
                    for (const item of risk) {
                        if (
                            item &&
                            typeof item === "object" &&
                            item[selected] !== undefined
                        ) {
                            riskVal = item[selected];
                            break;
                        }
                    }
                } else if (typeof risk === "object") {
                    riskVal = risk[selected];
                }
            }

            let fillColor = "#718096"; // Default slate gray fill
            if (riskVal === 1)
                fillColor = "#48bb78"; // Green
            else if (riskVal === 2)
                fillColor = "#ecc94b"; // Yellow
            else if (riskVal === 3)
                fillColor = "#ed8936"; // Orange
            else if (riskVal === 4) fillColor = "#e53e3e"; // Red

            return {
                color: "#4a5568", // Dark slate gray border
                fillColor: fillColor,
                fillOpacity: 0.6,
                weight: 1,
                pane: "roadOutline",
            };
        },
        onEachFeature: (feature, layer) => {
            let riskVal = null;
            const risk = feature.properties?.risk;
            if (risk) {
                if (Array.isArray(risk)) {
                    for (const item of risk) {
                        if (
                            item &&
                            typeof item === "object" &&
                            item[selected] !== undefined
                        ) {
                            riskVal = item[selected];
                            break;
                        }
                    }
                } else if (typeof risk === "object") {
                    riskVal = risk[selected];
                }
            }
            const popupContent = `
                <div class="p-2.5 font-sans min-w-[140px]">
                    <h4 class="text-xs font-extrabold text-gray-900 border-b border-gray-100 pb-1 mb-1.5 uppercase tracking-wider">
                        🏢 Building
                    </h4>
                    <div class="flex flex-col gap-1 text-[10px] text-gray-600">
                        <div class="flex justify-between gap-2">
                            <span class="font-bold">ID:</span>
                            <span class="text-gray-900">${feature.properties?.id || "Unknown"}</span>
                        </div>
                        <div class="flex justify-between gap-2 items-center mt-0.5">
                            <span class="font-bold">Risk:</span>
                            <span class="font-extrabold uppercase tracking-wide px-1.5 py-0.5 rounded-sm text-[8px] border 
                                ${
                                    riskVal === 4
                                        ? "bg-red-50 text-red-700 border-red-200"
                                        : riskVal === 3
                                          ? "bg-orange-50 text-orange-700 border-orange-200"
                                          : riskVal === 2
                                            ? "bg-yellow-50 text-yellow-700 border-yellow-200"
                                            : riskVal === 1
                                              ? "bg-green-50 text-green-700 border-green-200"
                                              : "bg-blue-50 text-blue-700 border-blue-200"
                                }"
                            >
                                ${riskVal !== null && riskVal !== undefined ? `Level ${riskVal}` : "N/A"}
                            </span>
                        </div>
                    </div>
                </div>
            `;
            layer.bindPopup(popupContent);
        },
    });

    const roadsOptions = $derived({
        style: (feature) => {
            let riskVal = null;
            const risk = feature.properties?.risk;
            if (risk) {
                if (Array.isArray(risk)) {
                    for (const item of risk) {
                        if (
                            item &&
                            typeof item === "object" &&
                            item[selected] !== undefined
                        ) {
                            riskVal = item[selected];
                            break;
                        }
                    }
                } else if (typeof risk === "object") {
                    riskVal = risk[selected];
                }
            }

            let color = "#3182ce"; // Default blue
            if (riskVal === 1)
                color = "#48bb78"; // Green
            else if (riskVal === 2)
                color = "#ecc94b"; // Yellow
            else if (riskVal === 3)
                color = "#ed8936"; // Orange
            else if (riskVal === 4) color = "#e53e3e"; // Red

            return {
                color: color,
                weight: 2,
                opacity: 0.7,
                pane: "roadOutline",
            };
        },
        onEachFeature: (feature, layer) => {
            let riskVal = null;
            const risk = feature.properties?.risk;
            if (risk) {
                if (Array.isArray(risk)) {
                    for (const item of risk) {
                        if (
                            item &&
                            typeof item === "object" &&
                            item[selected] !== undefined
                        ) {
                            riskVal = item[selected];
                            break;
                        }
                    }
                } else if (typeof risk === "object") {
                    riskVal = risk[selected];
                }
            }
            const popupContent = `
                <div class="p-2.5 font-sans min-w-[140px]">
                    <h4 class="text-xs font-extrabold text-gray-900 border-b border-gray-100 pb-1 mb-1.5 uppercase tracking-wider">
                        🛣️ Road Segment
                    </h4>
                    <div class="flex flex-col gap-1 text-[10px] text-gray-600">
                        <div class="flex justify-between gap-2">
                            <span class="font-bold">ID:</span>
                            <span class="text-gray-900">${feature.properties?.id || "Unknown"}</span>
                        </div>
                        <div class="flex justify-between gap-2 items-center mt-0.5">
                            <span class="font-bold">Risk:</span>
                            <span class="font-extrabold uppercase tracking-wide px-1.5 py-0.5 rounded-sm text-[8px] border 
                                ${
                                    riskVal === 4
                                        ? "bg-red-50 text-red-700 border-red-200"
                                        : riskVal === 3
                                          ? "bg-orange-50 text-orange-700 border-orange-200"
                                          : riskVal === 2
                                            ? "bg-yellow-50 text-yellow-700 border-yellow-200"
                                            : riskVal === 1
                                              ? "bg-green-50 text-green-700 border-green-200"
                                              : "bg-blue-50 text-blue-700 border-blue-200"
                                }"
                            >
                                ${riskVal !== null && riskVal !== undefined ? `Level ${riskVal}` : "N/A"}
                            </span>
                        </div>
                    </div>
                </div>
            `;
            layer.bindPopup(popupContent);
        },
    });

    const amenitiesOptions = $derived({
        pointToLayer: (feature, latlng) => {
            if (typeof window !== "undefined" && window.L) {
                return window.L.circleMarker(latlng, {
                    radius: 6,
                    color: "#ffffff",
                    weight: 1.5,
                    opacity: 1,
                    fillOpacity: 0.9,
                });
            }
        },
        style: (feature) => {
            let riskVal = null;
            const risk = feature.properties?.risk;
            if (risk) {
                if (Array.isArray(risk)) {
                    for (const item of risk) {
                        if (
                            item &&
                            typeof item === "object" &&
                            item[selected] !== undefined
                        ) {
                            riskVal = item[selected];
                            break;
                        }
                    }
                } else if (typeof risk === "object") {
                    riskVal = risk[selected];
                }
            }

            let fillColor = "#3182ce"; // Default blue
            if (riskVal === 1)
                fillColor = "#48bb78"; // Green
            else if (riskVal === 2)
                fillColor = "#ecc94b"; // Yellow
            else if (riskVal === 3)
                fillColor = "#ed8936"; // Orange
            else if (riskVal === 4) fillColor = "#e53e3e"; // Red

            return {
                fillColor: fillColor,
                color: "#ffffff",
                weight: 1.5,
                opacity: 1,
                fillOpacity: 0.9,
                pane: "roadOutline",
            };
        },
        onEachFeature: (feature, layer) => {
            let riskVal = null;
            const risk = feature.properties?.risk;
            if (risk) {
                if (Array.isArray(risk)) {
                    for (const item of risk) {
                        if (
                            item &&
                            typeof item === "object" &&
                            item[selected] !== undefined
                        ) {
                            riskVal = item[selected];
                            break;
                        }
                    }
                } else if (typeof risk === "object") {
                    riskVal = risk[selected];
                }
            }
            const name = feature.properties?.name || "Unnamed Asset";
            const amenity = feature.properties?.amenity || "Critical Asset";
            const popupContent = `
                <div class="p-2.5 font-sans min-w-[160px]">
                    <h4 class="text-xs font-extrabold text-gray-900 border-b border-gray-100 pb-1 mb-1.5 uppercase tracking-wider">
                        🏪 ${amenity.replace(/_/g, " ")}
                    </h4>
                    <div class="flex flex-col gap-1 text-[10px] text-gray-600">
                        <div class="flex justify-between gap-2">
                            <span class="font-bold">Name:</span>
                            <span class="text-gray-900 font-semibold text-right">${name}</span>
                        </div>
                        <div class="flex justify-between gap-2 items-center mt-0.5">
                            <span class="font-bold">Risk:</span>
                            <span class="font-extrabold uppercase tracking-wide px-1.5 py-0.5 rounded-sm text-[8px] border 
                                ${
                                    riskVal === 4
                                        ? "bg-red-50 text-red-700 border-red-200"
                                        : riskVal === 3
                                          ? "bg-orange-50 text-orange-700 border-orange-200"
                                          : riskVal === 2
                                            ? "bg-yellow-50 text-yellow-700 border-yellow-200"
                                            : riskVal === 1
                                              ? "bg-green-50 text-green-700 border-green-200"
                                              : "bg-blue-50 text-blue-700 border-blue-200"
                                }"
                            >
                                ${riskVal !== null && riskVal !== undefined ? `Level ${riskVal}` : "N/A"}
                            </span>
                        </div>
                    </div>
                </div>
            `;
            layer.bindPopup(popupContent);
        },
        pane: "roadOutline",
    });

    const municipalitiesOptions = $derived({
        style: (feature) => {
            const level = feature.properties?.vulnerability_level || "Low";
            let fillColor = "#48bb78"; // Low (green)
            if (level === "Medium") fillColor = "#ecc94b"; // Medium (yellow)
            if (level === "High") fillColor = "#ed8936"; // High (orange)
            if (level === "Critical") fillColor = "#e53e3e"; // Critical (red)

            return {
                fillColor: fillColor,
                fillOpacity: 0.35,
                color: "#4a5568",
                weight: 1.5,
                pane: "roadOutline",
            };
        },
    });

    // Toggle handlers for Risk/Hazard (mutually exclusive)
    function toggleRisk() {
        if (!showRisk) {
            showRisk = true;
            showHazard = false;
        } else {
            showRisk = false;
        }
    }

    function toggleHazard() {
        if (!showHazard) {
            showHazard = true;
            showRisk = false;
        } else {
            showHazard = false;
        }
    }

    // Toggle handlers for Exposure
    function toggleBuildings() {
        showBuildings = !showBuildings;
    }

    function toggleRoads() {
        showRoads = !showRoads;
    }

    function toggleAmenities() {
        showAmenities = !showAmenities;
    }

    // Toggle handlers for Vulnerability
    function toggleMunicipalities() {
        showMunicipalities = !showMunicipalities;
    }

    // Reactive data fetching effects
    $effect(() => {
        if (showBuildings && !buildingsData && !loadingBuildings && api_url) {
            loadingBuildings = true;
            fetch(`${api_url}/exposure/buildings`)
                .then((res) => {
                    if (res.ok) return res.json();
                    throw new Error("Failed to load buildings");
                })
                .then((data) => {
                    buildingsData = data;
                })
                .catch((e) => console.error(e))
                .finally(() => {
                    loadingBuildings = false;
                });
        }
    });

    $effect(() => {
        if (showRoads && !roadsData && !loadingRoads && api_url) {
            loadingRoads = true;
            fetch(`${api_url}/exposure/roads`)
                .then((res) => {
                    if (res.ok) return res.json();
                    throw new Error("Failed to load roads");
                })
                .then((data) => {
                    roadsData = data;
                })
                .catch((e) => console.error(e))
                .finally(() => {
                    loadingRoads = false;
                });
        }
    });

    $effect(() => {
        if (showAmenities && !amenitiesData && !loadingAmenities && api_url) {
            loadingAmenities = true;
            fetch(`${api_url}/exposure/amenities`)
                .then((res) => {
                    if (res.ok) return res.json();
                    throw new Error("Failed to load amenities");
                })
                .then((data) => {
                    amenitiesData = data;
                })
                .catch((e) => console.error(e))
                .finally(() => {
                    loadingAmenities = false;
                });
        }
    });

    $effect(() => {
        if (showMunicipalities && !municipalitiesData && !loadingMunicipalities && api_url) {
            loadingMunicipalities = true;
            fetch(`${api_url}/vulnerability/municipalities`)
                .then((res) => {
                    if (res.ok) return res.json();
                    throw new Error("Failed to load municipalities");
                })
                .then((data) => {
                    municipalitiesData = data;
                })
                .catch((e) => console.error(e))
                .finally(() => {
                    loadingMunicipalities = false;
                });
        }
    });
</script>

<div class="flex flex-col gap-2.5">
    <!-- Tabs Header -->
    <div
        class="flex border-b border-gray-100 text-[10px] font-extrabold uppercase tracking-wider"
    >
        <button
            class="flex-1 text-center pb-2 border-b-2 cursor-pointer transition-all duration-150 {activeTab ===
            'risk'
                ? 'border-gray-900 text-gray-900'
                : 'border-transparent text-gray-400 hover:text-gray-600'}"
            onclick={() => (activeTab = "risk")}
        >
            Risk
        </button>
        <button
            class="flex-1 text-center pb-2 border-b-2 cursor-pointer transition-all duration-150 {activeTab ===
            'exposure'
                ? 'border-gray-900 text-gray-900'
                : 'border-transparent text-gray-400 hover:text-gray-600'}"
            onclick={() => (activeTab = "exposure")}
        >
            Exposure
        </button>
        <button
            class="flex-1 text-center pb-2 border-b-2 cursor-pointer transition-all duration-150 {activeTab ===
            'vulnerability'
                ? 'border-gray-900 text-gray-900'
                : 'border-transparent text-gray-400 hover:text-gray-600'}"
            onclick={() => (activeTab = "vulnerability")}
        >
            Vuln.
        </button>
    </div>

    <!-- Tab Contents -->
    <div class="flex flex-col gap-2">
        {#if activeTab === "risk"}
            <!-- Operational Priority (Risk) Toggle -->
            <label
                class="flex items-center justify-between cursor-pointer group py-0.5"
            >
                <div class="flex items-center gap-2">
                    <span class="text-xs">🛡️</span>
                    <span
                        class="text-[11px] font-semibold text-gray-600 group-hover:text-gray-900 transition-colors"
                    >
                        Operational Priority (Risk)
                    </span>
                </div>
                <input
                    type="checkbox"
                    checked={showRisk}
                    onchange={toggleRisk}
                    class="sr-only peer"
                />
                <div
                    class="relative w-7 h-4 bg-gray-200 peer-focus:outline-hidden rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-3 after:w-3 after:transition-all peer-checked:bg-emerald-500"
                ></div>
            </label>

            <!-- Hazard Class Toggle -->
            <label
                class="flex items-center justify-between cursor-pointer group py-0.5"
            >
                <div class="flex items-center gap-2">
                    <span class="text-xs">⚠️</span>
                    <span
                        class="text-[11px] font-semibold text-gray-600 group-hover:text-gray-900 transition-colors"
                    >
                        Hazard Class
                    </span>
                </div>
                <input
                    type="checkbox"
                    checked={showHazard}
                    onchange={toggleHazard}
                    class="sr-only peer"
                />
                <div
                    class="relative w-7 h-4 bg-gray-200 peer-focus:outline-hidden rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-3 after:w-3 after:transition-all peer-checked:bg-emerald-500"
                ></div>
            </label>

            <!-- Hotspots Toggle -->
            <label
                class="flex items-center justify-between cursor-pointer group py-0.5"
            >
                <div class="flex items-center gap-2">
                    <span class="text-xs">🔥</span>
                    <span
                        class="text-[11px] font-semibold text-gray-600 group-hover:text-gray-900 transition-colors"
                    >
                        Active Hotspots
                    </span>
                </div>
                <input
                    type="checkbox"
                    bind:checked={showHotspots}
                    class="sr-only peer"
                />
                <div
                    class="relative w-7 h-4 bg-gray-200 peer-focus:outline-hidden rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-3 after:w-3 after:transition-all peer-checked:bg-emerald-500"
                ></div>
            </label>
        {:else if activeTab === "exposure"}
            <!-- Population Density Toggle -->
            <label
                class="flex items-center justify-between cursor-pointer group py-0.5"
            >
                <div class="flex items-center gap-2">
                    <span class="text-xs">👥</span>
                    <span
                        class="text-[11px] font-semibold text-gray-600 group-hover:text-gray-900 transition-colors"
                    >
                        Amount of Affected Population
                    </span>
                </div>
                <input
                    type="checkbox"
                    bind:checked={showPopulation}
                    class="sr-only peer"
                />
                <div
                    class="relative w-7 h-4 bg-gray-200 peer-focus:outline-hidden rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-3 after:w-3 after:transition-all peer-checked:bg-emerald-500"
                ></div>
            </label>

            <!-- Buildings Toggle -->
            <label
                class="flex items-center justify-between cursor-pointer group py-0.5"
            >
                <div class="flex items-center gap-2">
                    <span class="text-xs">🏢</span>
                    <span
                        class="text-[11px] font-semibold text-gray-600 group-hover:text-gray-900 transition-colors"
                    >
                        Number of Affected Buildings
                    </span>
                    {#if loadingBuildings}
                        <span class="animate-spin text-[10px] text-gray-400"
                            >⏳</span
                        >
                    {/if}
                </div>
                <input
                    type="checkbox"
                    checked={showBuildings}
                    onchange={toggleBuildings}
                    class="sr-only peer"
                    disabled={loadingBuildings}
                />
                <div
                    class="relative w-7 h-4 bg-gray-200 peer-focus:outline-hidden rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-3 after:w-3 after:transition-all peer-checked:bg-emerald-500 {loadingBuildings
                        ? 'opacity-50'
                        : ''}"
                ></div>
            </label>

            <!-- Roads Toggle -->
            <label
                class="flex items-center justify-between cursor-pointer group py-0.5"
            >
                <div class="flex items-center gap-2">
                    <span class="text-xs">🛣️</span>
                    <span
                        class="text-[11px] font-semibold text-gray-600 group-hover:text-gray-900 transition-colors"
                    >
                        Number of Affected Roads
                    </span>
                    {#if loadingRoads}
                        <span class="animate-spin text-[10px] text-gray-400"
                            >⏳</span
                        >
                    {/if}
                </div>
                <input
                    type="checkbox"
                    checked={showRoads}
                    onchange={toggleRoads}
                    class="sr-only peer"
                    disabled={loadingRoads}
                />
                <div
                    class="relative w-7 h-4 bg-gray-200 peer-focus:outline-hidden rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-3 after:w-3 after:transition-all peer-checked:bg-emerald-500 {loadingRoads
                        ? 'opacity-50'
                        : ''}"
                ></div>
            </label>

            <!-- Amenities Toggle -->
            <label
                class="flex items-center justify-between cursor-pointer group py-0.5"
            >
                <div class="flex items-center gap-2">
                    <span class="text-xs">🏪</span>
                    <span
                        class="text-[11px] font-semibold text-gray-600 group-hover:text-gray-900 transition-colors"
                    >
                        Number of Affected Amenities
                    </span>
                    {#if loadingAmenities}
                        <span class="animate-spin text-[10px] text-gray-400"
                            >⏳</span
                        >
                    {/if}
                </div>
                <input
                    type="checkbox"
                    checked={showAmenities}
                    onchange={toggleAmenities}
                    class="sr-only peer"
                    disabled={loadingAmenities}
                />
                <div
                    class="relative w-7 h-4 bg-gray-200 peer-focus:outline-hidden rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-3 after:w-3 after:transition-all peer-checked:bg-emerald-500 {loadingAmenities
                        ? 'opacity-50'
                        : ''}"
                ></div>
            </label>
        {:else if activeTab === "vulnerability"}
            <!-- Municipalities Toggle -->
            <label
                class="flex items-center justify-between cursor-pointer group py-0.5"
            >
                <div class="flex items-center gap-2">
                    <span class="text-xs">🏛️</span>
                    <span
                        class="text-[11px] font-semibold text-gray-600 group-hover:text-gray-900 transition-colors"
                    >
                        Municipalities (Income)
                    </span>
                    {#if loadingMunicipalities}
                        <span class="animate-spin text-[10px] text-gray-400"
                            >⏳</span
                        >
                    {/if}
                </div>
                <input
                    type="checkbox"
                    checked={showMunicipalities}
                    onchange={toggleMunicipalities}
                    class="sr-only peer"
                    disabled={loadingMunicipalities}
                />
                <div
                    class="relative w-7 h-4 bg-gray-200 peer-focus:outline-hidden rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-3 after:w-3 after:transition-all peer-checked:bg-emerald-500 {loadingMunicipalities
                        ? 'opacity-50'
                        : ''}"
                ></div>
            </label>
        {/if}
    </div>
</div>

<!-- Map Layers Rendering -->

<!-- Risk & Hazard Layers -->
{#if showRisk}
    <ImageLayer
        XYZ_URL={`${api_url}/xyz`}
        name="risk"
        image={`final_risk_maps/operational_priority_class_${selected}`}
        bands="1"
        stretch="0,3"
        palette="risk_palette_3"
        options={{
            maxZoom: 20,
            pane: "left",
            opacity: 1,
        }}
    />
{/if}

{#if showHazard}
    <ImageLayer
        XYZ_URL={`${api_url}/xyz`}
        name="hazard"
        image={`final_risk_maps/hazard_class_${selected}`}
        bands="1"
        stretch="0,4"
        palette="risk_palette_4"
        options={{
            maxZoom: 20,
            pane: "left",
            opacity: 1,
        }}
    />
{/if}

<!-- Exposure Layers -->
{#if showPopulation}
    <ImageLayer
        XYZ_URL={`${api_url}/xyz`}
        name="population"
        image="exposure/population"
        bands="1"
        stretch="0,10"
        palette="YlOrRd"
        options={{
            maxZoom: 20,
            pane: "left",
            opacity: 0.65,
        }}
    />
{/if}

{#if showBuildings && buildingsData}
    <GeoJSONLayer
        name="buildings"
        geojson={buildingsData}
        options={buildingsOptions}
    />
{/if}

{#if showRoads && roadsData}
    <GeoJSONLayer name="roads" geojson={roadsData} options={roadsOptions} />
{/if}

{#if showAmenities && amenitiesData}
    <GeoJSONLayer
        name="amenities"
        geojson={amenitiesData}
        options={amenitiesOptions}
    />
{/if}

<!-- Vulnerability Layers -->
{#if showMunicipalities && municipalitiesData}
    <GeoJSONLayer
        name="municipalities"
        geojson={municipalitiesData}
        options={municipalitiesOptions}
    />
{/if}

<!-- Hotspots Layer -->
{#if showHotspots && hotspots}
    <GeoJSONLayer
        name="hotspots"
        geojson={(() => {
            // Clone the hotspots object to avoid mutating original
            const filtered = { ...hotspots };
            // Only filter if FeatureCollection
            if (
                filtered.type === "FeatureCollection" &&
                Array.isArray(filtered.features)
            ) {
                filtered.features = filtered.features.filter(
                    (f) => f?.properties?.date === selected,
                );
            }
            return filtered;
        })()}
        options={{ style: { color: "red", pane: "aoi" } }}
    />
{/if}
