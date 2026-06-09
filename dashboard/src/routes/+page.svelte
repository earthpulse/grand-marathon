<script>
    import { onMount } from "svelte";
    import { map } from "$lib/stores/map/map";
    import { dashboardSettings } from "$lib/stores/dashboardSettings";
    import Map from "$lib/components/map/Map.svelte";
    import TileLayer from "$lib/components/map/TileLayer.svelte";
    import LayersControl from "$lib/components/map/LayersControl.svelte";
    import DateSelector from "$lib/components/map/DateSelector.svelte";
    import ImageLayer from "$lib/components/map/ImageLayer.svelte";
    import GeoJSONLayer from "$lib/components/map/GeoJSONLayer.svelte";
    import AlertMarkers from "$lib/components/map/AlertMarkers.svelte";
    import Calendar from "$lib/components/map/Calendar.svelte";
    import MapLayersControl from "$lib/components/map/MapLayersControl.svelte";
    import AnalyticsPanel from "$lib/components/AnalyticsPanel.svelte";
    import Legend from "$lib/components/map/Legend.svelte";

    const { data } = $props();
    const API_KEY = import.meta.env.VITE_MAPTILER_API_KEY;
    const api_url = $derived(data.api_url);
    const aoi = $derived(data.aoi);
    let hotspots = $derived(data.hotspots);
    const {
        today,
        dates,
        hotspot_dates = [],
        date_colors = {},
    } = $derived(data.dates || {});
    // const hotspots = $derived(data.hotspots);
    const layers = ["light", "streets", "satellite"];
    const defaultDate = $derived.by(() => {
        if (!Array.isArray(dates) || dates.length === 0) {
            return null;
        }
        // Try to find a date that matches today (either exact or month-day)
        const todayMatch = dates.find(
            (d) => d === today || (d && today && d.slice(5) === today.slice(5)),
        );
        if (todayMatch) {
            return todayMatch;
        }
        // Fallback to latest date if today is not in the list
        return dates.reduce((latest, date) => (date > latest ? date : latest));
    });

    let selected = $state("");
    $effect(() => {
        if (!defaultDate) {
            selected = "";
            return;
        }

        if (!selected || !dates.includes(selected)) {
            selected = defaultDate;
        }
    });

    let analytics = $state(null);
    let analyticsLoading = $state(false);
    let analyticsError = $state(null);
    let layersCollapsed = $state(false);
    let sidebarTab = $state("analytics");

    $effect(() => {
        if (!selected || !api_url) {
            analytics = null;
            return;
        }

        let active = true;

        async function fetchAnalytics() {
            analyticsLoading = true;
            analyticsError = null;
            try {
                const res = await fetch(`${api_url}/analytics/${selected}`);
                if (!active) return;
                if (res.ok) {
                    analytics = await res.json();
                } else {
                    analytics = null;
                    analyticsError = `Failed to load analytics: ${res.statusText}`;
                }
            } catch (err) {
                if (!active) return;
                analytics = null;
                analyticsError = `Error fetching analytics: ${err.message}`;
            } finally {
                if (active) {
                    analyticsLoading = false;
                }
            }
        }

        fetchAnalytics();

        return () => {
            active = false;
        };
    });

    // Alert filter option for the right-side list panel:
    // 'confirmed' (acknowledged), 'all' [default], 'unconfirmed' (active), 'resolved'
    let filterOption = $state("all");
    let clickedAlert = $state(null);

    // Map layer states bound to MapLayersControl
    let showRisk = $state(true);
    let showHazard = $state(false);
    let showHotspots = $state(false);
    let showPopulation = $state(false);
    let showBuildings = $state(false);
    let showRoads = $state(false);
    let showAmenities = $state(false);
    let showMunicipalities = $state(false);
    let layersActiveTab = $state("risk");

    // Reset clicked alert when selected date changes
    $effect(() => {
        const _ = selected;
        clickedAlert = null;
    });

    function selectAlert(alert) {
        clickedAlert = alert;
        if (
            $map &&
            alert &&
            alert.latitude !== undefined &&
            alert.latitude !== null &&
            alert.longitude !== undefined &&
            alert.longitude !== null
        ) {
            $map.flyTo([alert.latitude, alert.longitude], 14);
        }
    }

    function handleAssetClick(assetType) {
        if (!selectedAlertDetail) return;

        // Zoom/fly to the alert's position
        if (
            $map &&
            selectedAlertDetail.latitude !== undefined &&
            selectedAlertDetail.longitude !== undefined
        ) {
            $map.flyTo(
                [selectedAlertDetail.latitude, selectedAlertDetail.longitude],
                14,
            );
        }

        // Toggle the corresponding layer and switch tab to exposure
        layersActiveTab = "exposure";
        if (assetType === "roads") {
            showRoads = !showRoads;
        } else if (assetType === "buildings") {
            showBuildings = !showBuildings;
        } else if (assetType === "amenities") {
            showAmenities = !showAmenities;
        } else if (assetType === "population") {
            showPopulation = !showPopulation;
        }
    }

    // Helper to revert state for selectedDate time-travel replaying
    function getHistoricalState(item, date) {
        if (!date) return item;
        const historical = { ...item };
        if (!historical.trace || !Array.isArray(historical.trace)) {
            return historical;
        }
        const sortedTrace = [...historical.trace].sort((a, b) => {
            return new Date(b.timestamp) - new Date(a.timestamp);
        });
        for (const entry of sortedTrace) {
            const entryDate = entry.timestamp.substring(0, 10);
            if (entryDate > date) {
                if (entry.changes && Array.isArray(entry.changes)) {
                    for (const change of entry.changes) {
                        historical[change.field] = change.old_value;
                    }
                }
            }
        }
        return historical;
    }

    // Reactively compute the historical list of alerts on or before the selected date
    const historicalAlerts = $derived.by(() => {
        const rawAlerts = data.alerts || [];
        if (!selected) return rawAlerts;
        return rawAlerts
            .filter((alert) => {
                const alertDate = alert.created_at.substring(0, 10);
                return alertDate <= selected;
            })
            .map((alert) => getHistoricalState(alert, selected));
    });

    const selectedAlertDetail = $derived.by(() => {
        if (!clickedAlert) return null;
        return (
            historicalAlerts.find((a) => a.id === clickedAlert.id) ||
            clickedAlert
        );
    });

    // Reactively compute the historical actions
    const historicalActions = $derived.by(() => {
        const rawActions = data.actions || [];
        if (!selected) return rawActions;
        return rawActions
            .filter((action) => {
                const actionDate = action.created_at.substring(0, 10);
                return actionDate <= selected;
            })
            .map((action) => getHistoricalState(action, selected));
    });

    // Apply the selected filter option to the historical alerts list
    const filteredAlerts = $derived.by(() => {
        let list = [...historicalAlerts];
        if (filterOption === "confirmed") {
            list = list.filter((a) => a.status === "acknowledged");
        } else if (filterOption === "unconfirmed") {
            list = list.filter((a) => a.status === "active");
        } else if (filterOption === "resolved") {
            list = list.filter((a) => a.status === "resolved");
        }
        return list;
    });

    function getActionsForAlert(alertId) {
        return historicalActions.filter((act) => act.alert_id === alertId);
    }

    const selectedAlertActions = $derived.by(() => {
        if (!selectedAlertDetail) return [];
        return getActionsForAlert(selectedAlertDetail.id);
    });
</script>

<div class="flex h-full w-full box-border flex-row gap-3 p-3">
    <div class="flex min-h-0 w-full flex-1 flex-col gap-3">
        <div class="min-h-0 flex-1 relative">
            <Map
                zoom={6}
                panes={[
                    { name: "roadOutline", zIndex: 99998 },
                    { name: "aoi", zIndex: 99999 },
                    { name: "left", zIndex: 999 },
                    { name: "right", zIndex: 999 },
                ]}
                {aoi}
            >
                <!-- {#if $dashboardSettings.layer == "light"}
                    <TileLayer
                        url={`https://api.maptiler.com/maps/dataviz/{z}/{x}/{y}.png?key=${API_KEY}`}
                        options={{ maxZoom: 20, zIndex: 1 }}
                    />
                {:else if $dashboardSettings.layer == "satellite"}
                    <TileLayer
                        url={`https://api.maptiler.com/maps/satellite/{z}/{x}/{y}.png?key=${API_KEY}`}
                        options={{ maxZoom: 20, zIndex: 1 }}
                    />
                {:else if $dashboardSettings.layer == "streets"}
                    <TileLayer
                        url={`https://api.maptiler.com/maps/streets/{z}/{x}/{y}.png?key=${API_KEY}`}
                        options={{ maxZoom: 20, zIndex: 1 }}
                    />
                {/if}
                <LayersControl
                    {layers}
                    layer={$dashboardSettings.layer}
                    onLayerChange={dashboardSettings.setLayer}
                /> -->

                <!-- <DateSelector {dates} bind:selected /> -->

                <TileLayer
                    url={`https://api.maptiler.com/maps/satellite/{z}/{x}/{y}.png?key=${API_KEY}`}
                    options={{ maxZoom: 20, zIndex: 1 }}
                />

                {#if data.alerts}
                    <AlertMarkers
                        alerts={data.alerts}
                        actions={data.actions}
                        selectedDate={selected}
                        {filterOption}
                        onAlertClick={selectAlert}
                    />
                {/if}
            </Map>

            <!-- Collapsible Layers Control Panel (Top-Left overlay on the Map) -->
            <div
                class="absolute top-3 left-3 z-[10000] flex flex-col items-start gap-2"
            >
                {#if layersCollapsed}
                    <button
                        onclick={() => (layersCollapsed = false)}
                        class="bg-white hover:bg-gray-50 text-gray-700 border border-gray-200 rounded-lg shadow-md p-2.5 flex items-center justify-center cursor-pointer transition-all duration-150 hover:scale-105"
                        title="Show Map Layers"
                    >
                        <span class="text-base">🥞</span>
                    </button>
                {/if}

                <div
                    class="bg-white rounded-xl shadow-lg border border-gray-200/80 p-3.5 w-72 flex flex-col gap-3 {layersCollapsed
                        ? 'hidden'
                        : ''}"
                >
                    <div
                        class="flex items-center justify-between border-b border-gray-100 pb-2"
                    >
                        <h3
                            class="text-xs font-bold text-gray-900 flex items-center gap-1.5"
                        >
                            🥞 Map Layers
                        </h3>
                        <button
                            onclick={() => (layersCollapsed = true)}
                            class="text-gray-400 hover:text-gray-600 transition-colors cursor-pointer text-[10px] font-bold p-1 hover:bg-gray-100 rounded"
                        >
                            ✕
                        </button>
                    </div>
                    <MapLayersControl
                        {api_url}
                        {selected}
                        {hotspots}
                        bind:showRisk
                        bind:showHazard
                        bind:showHotspots
                        bind:showPopulation
                        bind:showBuildings
                        bind:showRoads
                        bind:showAmenities
                        bind:showMunicipalities
                        bind:activeTab={layersActiveTab}
                    />
                </div>
            </div>

            <Legend
                {showRisk}
                {showHazard}
                {showHotspots}
                {showPopulation}
                {showBuildings}
                {showRoads}
                {showAmenities}
                {showMunicipalities}
            />
        </div>
        <!--<div class="h-[220px]">
           {#if $dashboardSettings.showRain}
                <RainTimeline height={220} data={rain} loading={false} />
            {:else}
                <ThresholdTimeline
                    height={220}
                    data={selectedRoadResults}
                    loading={false}
                    lowerThreshold={$dashboardSettings.lowerThreshold}
                    upperThreshold={$dashboardSettings.upperThreshold}
                />
            {/if}
        </div> -->
    </div>

    <!-- Right Sidebar - Active Alerts Tracker & Analytics -->
    <aside
        class="w-96 shrink-0 bg-white border border-gray-100 rounded-xl shadow-xs flex flex-col min-h-0 h-full overflow-hidden"
    >
        {#if selectedAlertDetail}
            <!-- Alert Details Panel -->
            <div class="flex flex-col h-full min-h-0 bg-white">
                <!-- Header -->
                <div
                    class="p-4 border-b border-gray-100 flex items-center justify-between shrink-0 bg-gray-50/50"
                >
                    <button
                        onclick={() => (clickedAlert = null)}
                        class="text-xs font-bold text-gray-600 hover:text-gray-900 transition-colors flex items-center gap-1.5 cursor-pointer bg-transparent border-0 p-0"
                    >
                        <span>← Back</span>
                    </button>
                    <!-- <span class="text-[10px] text-gray-400 font-medium">
                        ID: {selectedAlertDetail.id.slice(0, 8)}
                    </span> -->
                </div>

                <!-- Scrollable Content -->
                <div class="flex-1 overflow-y-auto p-4 space-y-4 min-h-0">
                    <!-- Title & Badges -->
                    <div class="space-y-2">
                        <div class="flex items-center gap-1.5 flex-wrap">
                            <span
                                class={`text-[9px] font-extrabold uppercase px-2.5 py-0.5 rounded-full border tracking-wider ${
                                    selectedAlertDetail.severity === "critical"
                                        ? "bg-red-50 border-red-200 text-red-700"
                                        : selectedAlertDetail.severity ===
                                            "warning"
                                          ? "bg-amber-50 border-amber-200 text-amber-700"
                                          : "bg-blue-50 border-blue-200 text-blue-700"
                                }`}
                            >
                                {selectedAlertDetail.severity}
                            </span>
                            <span
                                class={`text-[9px] font-extrabold uppercase px-2.5 py-0.5 rounded-full border tracking-wider ${
                                    selectedAlertDetail.status === "active"
                                        ? "bg-emerald-50 border-emerald-200 text-emerald-700"
                                        : selectedAlertDetail.status ===
                                            "acknowledged"
                                          ? "bg-indigo-50 border-indigo-200 text-indigo-700"
                                          : "bg-gray-50 border-gray-200 text-gray-500"
                                }`}
                            >
                                {selectedAlertDetail.status === "acknowledged"
                                    ? "confirmed"
                                    : selectedAlertDetail.status}
                            </span>
                        </div>
                        <h2
                            class="text-base font-bold text-gray-900 leading-snug"
                        >
                            {selectedAlertDetail.title}
                        </h2>
                        <p class="text-[11px] text-gray-400">
                            Detected on {new Date(
                                selectedAlertDetail.created_at,
                            ).toLocaleString()}
                        </p>
                    </div>

                    <!-- Regional Context for Selected Date -->
                    {#if analytics}
                        <div
                            class="p-3 bg-slate-50 border border-slate-200/80 rounded-xl space-y-2"
                        >
                            <div class="flex items-center justify-between">
                                <h4
                                    class="text-[10px] font-extrabold text-slate-500 uppercase tracking-wider flex items-center gap-1"
                                >
                                    Why this is a priority?
                                </h4>
                                <!-- <span class="text-[8px] bg-slate-200 text-slate-700 font-extrabold px-1.5 py-0.5 rounded-full">
                                    Rule-Based Risk
                                </span> -->
                            </div>
                            <div class="grid grid-cols-3 gap-2">
                                <div
                                    class="bg-white p-2 rounded-lg border border-slate-100 text-center flex flex-col justify-between shadow-3xs"
                                >
                                    <span
                                        class="text-[9px] font-bold text-gray-400 uppercase tracking-wider block mb-1"
                                    >
                                        Exposure
                                    </span>
                                    <span
                                        class={`text-xs font-extrabold ${
                                            analytics.mean_exposure < 0.05
                                                ? "text-emerald-600"
                                                : analytics.mean_exposure < 0.15
                                                  ? "text-amber-500"
                                                  : "text-red-600"
                                        }`}
                                    >
                                        {analytics.mean_exposure.toFixed(4)}
                                    </span>
                                </div>
                                <div
                                    class="bg-white p-2 rounded-lg border border-slate-100 text-center flex flex-col justify-between shadow-3xs"
                                >
                                    <span
                                        class="text-[9px] font-bold text-gray-400 uppercase tracking-wider block mb-1"
                                    >
                                        Hazard
                                    </span>
                                    <span
                                        class={`text-xs font-extrabold ${
                                            analytics.mean_hazard < 0.25
                                                ? "text-emerald-600"
                                                : analytics.mean_hazard < 0.45
                                                  ? "text-amber-500"
                                                  : "text-red-600"
                                        }`}
                                    >
                                        {analytics.mean_hazard.toFixed(4)}
                                    </span>
                                </div>
                                <div
                                    class="bg-white p-2 rounded-lg border border-slate-100 text-center flex flex-col justify-between shadow-3xs"
                                >
                                    <span
                                        class="text-[9px] font-bold text-gray-400 uppercase tracking-wider block mb-1"
                                    >
                                        Vulnerability
                                    </span>
                                    <span
                                        class={`text-xs font-extrabold ${
                                            analytics.mean_vulnerability < 0.25
                                                ? "text-emerald-600"
                                                : analytics.mean_vulnerability <
                                                    0.45
                                                  ? "text-amber-500"
                                                  : "text-red-600"
                                        }`}
                                    >
                                        {analytics.mean_vulnerability.toFixed(
                                            4,
                                        )}
                                    </span>
                                </div>
                            </div>
                        </div>
                    {/if}

                    <!-- Description -->
                    <div class="space-y-1.5">
                        <h4
                            class="text-[10px] font-extrabold text-gray-400 uppercase tracking-wider"
                        >
                            Description
                        </h4>
                        <p
                            class="text-xs text-gray-600 bg-gray-50 p-3 rounded-lg border border-gray-100 whitespace-pre-line leading-relaxed"
                        >
                            {selectedAlertDetail.description}
                        </p>
                    </div>

                    <!-- Affected Metrics -->
                    {#if (selectedAlertDetail.affected_roads_count !== undefined && selectedAlertDetail.affected_roads_count !== null) || (selectedAlertDetail.affected_buildings_count !== undefined && selectedAlertDetail.affected_buildings_count !== null) || (selectedAlertDetail.affected_amenities_count !== undefined && selectedAlertDetail.affected_amenities_count !== null) || (selectedAlertDetail.affected_population !== undefined && selectedAlertDetail.affected_population !== null)}
                        <div class="space-y-2">
                            <div class="flex items-center justify-between">
                                <h4
                                    class="text-[10px] font-extrabold text-gray-400 uppercase tracking-wider"
                                >
                                    Elements at risk
                                </h4>
                                <span class="text-[9px] text-gray-400 italic"
                                    >Click to zoom & toggle layer</span
                                >
                            </div>
                            <div class="grid grid-cols-2 gap-2">
                                {#if selectedAlertDetail.affected_roads_count !== undefined && selectedAlertDetail.affected_roads_count !== null}
                                    <button
                                        onclick={() =>
                                            handleAssetClick("roads")}
                                        class={`p-2.5 rounded-lg border flex flex-col gap-1 shadow-2xs text-left cursor-pointer transition-all hover:scale-[1.02] active:scale-[0.98] w-full ${showRoads ? "border-blue-500 bg-blue-50/20" : "bg-white border-gray-200/80 hover:bg-gray-50"}`}
                                    >
                                        <span
                                            class="text-[10px] text-gray-400 font-semibold uppercase"
                                            >Number of Affected Roads</span
                                        >
                                        <div class="flex items-center gap-1.5">
                                            <span class="text-base">🛣️</span>
                                            <span
                                                class="text-sm font-extrabold text-blue-600"
                                                >{selectedAlertDetail.affected_roads_count}</span
                                            >
                                        </div>
                                    </button>
                                {/if}
                                {#if selectedAlertDetail.affected_buildings_count !== undefined && selectedAlertDetail.affected_buildings_count !== null}
                                    <button
                                        onclick={() =>
                                            handleAssetClick("buildings")}
                                        class={`p-2.5 rounded-lg border flex flex-col gap-1 shadow-2xs text-left cursor-pointer transition-all hover:scale-[1.02] active:scale-[0.98] w-full ${showBuildings ? "border-amber-500 bg-amber-50/20" : "bg-white border-gray-200/80 hover:bg-gray-50"}`}
                                    >
                                        <span
                                            class="text-[10px] text-gray-400 font-semibold uppercase"
                                            >Number of Affected Buildings</span
                                        >
                                        <div class="flex items-center gap-1.5">
                                            <span class="text-base">🏢</span>
                                            <span
                                                class="text-sm font-extrabold text-amber-600"
                                                >{selectedAlertDetail.affected_buildings_count}</span
                                            >
                                        </div>
                                    </button>
                                {/if}
                                {#if selectedAlertDetail.affected_amenities_count !== undefined && selectedAlertDetail.affected_amenities_count !== null}
                                    <button
                                        onclick={() =>
                                            handleAssetClick("amenities")}
                                        class={`p-2.5 rounded-lg border flex flex-col gap-1 shadow-2xs text-left cursor-pointer transition-all hover:scale-[1.02] active:scale-[0.98] w-full ${showAmenities ? "border-purple-500 bg-purple-50/20" : "bg-white border-gray-200/80 hover:bg-gray-50"}`}
                                    >
                                        <span
                                            class="text-[10px] text-gray-400 font-semibold uppercase"
                                            >Number of Affected Amenities</span
                                        >
                                        <div class="flex items-center gap-1.5">
                                            <span class="text-base">🏥</span>
                                            <span
                                                class="text-sm font-extrabold text-purple-600"
                                                >{selectedAlertDetail.affected_amenities_count}</span
                                            >
                                        </div>
                                    </button>
                                {/if}
                                {#if selectedAlertDetail.affected_population !== undefined && selectedAlertDetail.affected_population !== null}
                                    <button
                                        onclick={() =>
                                            handleAssetClick("population")}
                                        class={`p-2.5 rounded-lg border flex flex-col gap-1 shadow-2xs text-left cursor-pointer transition-all hover:scale-[1.02] active:scale-[0.98] w-full ${showPopulation ? "border-emerald-500 bg-emerald-50/20" : "bg-white border-gray-200/80 hover:bg-gray-50"}`}
                                    >
                                        <span
                                            class="text-[10px] text-gray-400 font-semibold uppercase"
                                            >Amount of Affected Population</span
                                        >
                                        <div class="flex items-center gap-1.5">
                                            <span class="text-base">👥</span>
                                            <span
                                                class="text-sm font-extrabold text-emerald-600"
                                                >{selectedAlertDetail.affected_population}</span
                                            >
                                        </div>
                                    </button>
                                {/if}
                            </div>
                        </div>
                    {/if}

                    <!-- Response Actions -->
                    <div class="space-y-2">
                        <h4
                            class="text-[10px] font-extrabold text-gray-400 uppercase tracking-wider"
                        >
                            Recommended Actions
                        </h4>
                        {#if selectedAlertActions.length > 0}
                            <div class="space-y-2">
                                {#each selectedAlertActions as act (act.id)}
                                    <div
                                        class="p-3 bg-white border border-gray-200/80 rounded-lg shadow-2xs flex flex-col gap-1.5"
                                    >
                                        <div
                                            class="flex items-start justify-between gap-2.5"
                                        >
                                            <span
                                                class="text-xs font-bold text-gray-900 leading-snug"
                                            >
                                                {act.title}
                                            </span>
                                            <span
                                                class={`text-[8px] font-extrabold uppercase px-1.5 py-0.5 rounded-md border tracking-wider shrink-0 ${
                                                    act.status === "completed"
                                                        ? "bg-emerald-50 text-emerald-700 border-emerald-200"
                                                        : act.status ===
                                                            "in_progress"
                                                          ? "bg-blue-50 text-blue-700 border-blue-200"
                                                          : act.status ===
                                                              "cancelled"
                                                            ? "bg-gray-100 text-gray-700 border-gray-300"
                                                            : "bg-amber-50 text-amber-700 border-amber-200"
                                                }`}
                                            >
                                                {act.status}
                                            </span>
                                        </div>
                                        {#if act.description}
                                            <p
                                                class="text-[10px] text-gray-500 leading-relaxed"
                                            >
                                                {act.description}
                                            </p>
                                        {/if}
                                    </div>
                                {/each}
                            </div>
                        {:else}
                            <div
                                class="text-center py-6 px-4 border border-dashed border-gray-200 rounded-lg bg-gray-50/30"
                            >
                                <span class="text-xl">📋</span>
                                <p class="text-[10px] text-gray-400 mt-1">
                                    No response actions registered for this
                                    alert.
                                </p>
                            </div>
                        {/if}
                    </div>
                </div>
            </div>
        {:else}
            <!-- Interactive Calendar -->
            <div
                class="p-3 border-b border-gray-100 shrink-0 bg-gray-50/15 flex flex-col gap-2.5 items-stretch"
            >
                <Calendar {dates} bind:selected {today} {date_colors} />
            </div>

            <!-- Sidebar Tabs Header -->
            <div
                class="flex border-b border-gray-100 text-xs font-bold shrink-0 bg-gray-50/50"
            >
                <button
                    class="flex-1 text-center py-3 border-b-2 cursor-pointer transition-all duration-150 flex items-center justify-center gap-1.5 {sidebarTab ===
                    'analytics'
                        ? 'border-gray-900 text-gray-900 font-extrabold'
                        : 'border-transparent text-gray-500 hover:text-gray-700'}"
                    onclick={() => (sidebarTab = "analytics")}
                >
                    <span>📊 Analytics</span>
                </button>
                <button
                    class="flex-1 text-center py-3 border-b-2 cursor-pointer transition-all duration-150 flex items-center justify-center gap-1.5 {sidebarTab ===
                    'alerts'
                        ? 'border-gray-900 text-gray-900 font-extrabold'
                        : 'border-transparent text-gray-500 hover:text-gray-700'}"
                    onclick={() => (sidebarTab = "alerts")}
                >
                    <span>🔔 Alerts</span>
                    {#if filteredAlerts.length > 0}
                        <span
                            class="bg-red-100 text-red-700 text-[9px] font-extrabold px-1.5 py-0.5 rounded-full"
                        >
                            {filteredAlerts.length}
                        </span>
                    {/if}
                </button>
            </div>

            <!-- Tab Content -->
            {#if sidebarTab === "analytics"}
                <div class="flex-1 overflow-y-auto p-3 min-h-0 bg-white">
                    <AnalyticsPanel
                        {analytics}
                        loading={analyticsLoading}
                        error={analyticsError}
                    />
                </div>
            {:else if sidebarTab === "alerts"}
                <!-- Panel Header (Filters) -->
                <div
                    class="p-3 border-b border-gray-100 shrink-0 bg-gradient-to-b from-gray-50/50 to-white"
                >
                    <!-- Filters Toggle Option Buttons -->
                    <div
                        class="bg-gray-100 p-0.5 rounded-lg flex items-stretch text-[10px] font-bold"
                    >
                        <button
                            onclick={() => (filterOption = "confirmed")}
                            class={`flex-1 text-center py-1.5 rounded-md transition-all cursor-pointer ${filterOption === "confirmed" ? "bg-white text-gray-950 shadow-xs" : "text-gray-500 hover:text-gray-900"}`}
                        >
                            Confirmed
                        </button>
                        <button
                            onclick={() => (filterOption = "unconfirmed")}
                            class={`flex-1 text-center py-1.5 rounded-md transition-all cursor-pointer ${filterOption === "unconfirmed" ? "bg-white text-gray-950 shadow-xs" : "text-gray-500 hover:text-gray-900"}`}
                        >
                            Unconfirmed
                        </button>
                        <button
                            onclick={() => (filterOption = "resolved")}
                            class={`flex-1 text-center py-1.5 rounded-md transition-all cursor-pointer ${filterOption === "resolved" ? "bg-white text-gray-950 shadow-xs" : "text-gray-500 hover:text-gray-900"}`}
                        >
                            Resolved
                        </button>
                        <button
                            onclick={() => (filterOption = "all")}
                            class={`flex-1 text-center py-1.5 rounded-md transition-all cursor-pointer ${filterOption === "all" ? "bg-white text-gray-950 shadow-xs" : "text-gray-500 hover:text-gray-900"}`}
                        >
                            All
                        </button>
                    </div>
                </div>

                <!-- Scrollable Alerts List -->
                <div class="flex-1 overflow-y-auto p-3 space-y-3 min-h-0">
                    {#if filteredAlerts.length === 0}
                        <div
                            class="text-center py-12 px-4 border border-dashed border-gray-200 rounded-lg"
                        >
                            <span class="text-2xl">📭</span>
                            <h3
                                class="text-xs font-semibold text-gray-700 mt-2"
                            >
                                No alerts found
                            </h3>
                            <p
                                class="text-[10px] text-gray-400 mt-1 max-w-[180px] mx-auto leading-relaxed"
                            >
                                No alerts match this filter criteria on the
                                selected timeline date.
                            </p>
                        </div>
                    {:else}
                        {#each filteredAlerts as alert (alert.id)}
                            {@const alertActions = getActionsForAlert(alert.id)}
                            <article
                                onclick={() => selectAlert(alert)}
                                class="p-3 bg-white rounded-lg border border-gray-200/80 shadow-xs hover:border-gray-300 hover:shadow-md transition-all duration-200 relative overflow-hidden flex flex-col gap-2 cursor-pointer"
                            >
                                <!-- Left colored severity indicator edge -->
                                <div
                                    class={`absolute left-0 top-0 bottom-0 w-1 ${
                                        alert.severity === "critical"
                                            ? "bg-red-500"
                                            : alert.severity === "warning"
                                              ? "bg-amber-500"
                                              : "bg-blue-500"
                                    }`}
                                ></div>

                                <!-- Header & Badges -->
                                <div class="flex flex-col gap-1">
                                    <div
                                        class="flex items-center gap-1.5 flex-wrap"
                                    >
                                        <span
                                            class={`text-[8px] font-extrabold uppercase px-2 py-0.5 rounded-full border tracking-wider ${
                                                alert.severity === "critical"
                                                    ? "bg-red-50 border-red-200 text-red-700"
                                                    : alert.severity ===
                                                        "warning"
                                                      ? "bg-amber-50 border-amber-200 text-amber-700"
                                                      : "bg-blue-50 border-blue-200 text-blue-700"
                                            }`}
                                        >
                                            {alert.severity}
                                        </span>
                                        <span
                                            class={`text-[8px] font-extrabold uppercase px-2 py-0.5 rounded-full border tracking-wider ${
                                                alert.status === "active"
                                                    ? "bg-emerald-50 border-emerald-200 text-emerald-700"
                                                    : alert.status ===
                                                        "acknowledged"
                                                      ? "bg-indigo-50 border-indigo-200 text-indigo-700"
                                                      : "bg-gray-50 border-gray-200 text-gray-500"
                                            }`}
                                        >
                                            {alert.status === "acknowledged"
                                                ? "confirmed"
                                                : alert.status}
                                        </span>
                                    </div>
                                    <h3
                                        class="text-xs font-bold text-gray-900 leading-snug pr-1 mt-1"
                                    >
                                        {alert.title}
                                    </h3>
                                    {#if (alert.affected_roads_count !== undefined && alert.affected_roads_count !== null) || (alert.affected_buildings_count !== undefined && alert.affected_buildings_count !== null) || (alert.affected_amenities_count !== undefined && alert.affected_amenities_count !== null) || (alert.affected_population !== undefined && alert.affected_population !== null)}
                                        <div
                                            class="mt-1.5 pt-1.5 border-t border-gray-100 flex items-center justify-between text-[10px] text-gray-500 font-medium bg-gray-50 px-2 py-1 rounded border border-gray-150/40"
                                        >
                                            <div
                                                class="flex items-center gap-1.5"
                                                title="Number of Affected Roads"
                                            >
                                                <span>🛣️</span>
                                                <span
                                                    class="font-bold text-blue-600"
                                                    >{alert.affected_roads_count ??
                                                        0}</span
                                                >
                                            </div>
                                            <div
                                                class="flex items-center gap-1.5"
                                                title="Number of Affected Buildings"
                                            >
                                                <span>🏢</span>
                                                <span
                                                    class="font-bold text-amber-600"
                                                    >{alert.affected_buildings_count ??
                                                        0}</span
                                                >
                                            </div>
                                            <div
                                                class="flex items-center gap-1.5"
                                                title="Number of Affected Amenities"
                                            >
                                                <span>🏥</span>
                                                <span
                                                    class="font-bold text-purple-600"
                                                    >{alert.affected_amenities_count ??
                                                        0}</span
                                                >
                                            </div>
                                            <div
                                                class="flex items-center gap-1.5"
                                                title="Amount of Affected Population"
                                            >
                                                <span>👥</span>
                                                <span
                                                    class="font-bold text-emerald-600"
                                                    >{alert.affected_population ??
                                                        0}</span
                                                >
                                            </div>
                                        </div>
                                    {/if}
                                </div>

                                <!-- Attached Actions Sub-list -->
                                {#if alertActions.length > 0}
                                    <div
                                        class="mt-1 pt-2 border-t border-gray-100"
                                    >
                                        <h4
                                            class="text-[9px] font-extrabold text-gray-400 uppercase tracking-wider mb-2"
                                        >
                                            Response Actions:
                                        </h4>
                                        <ul class="space-y-1.5 list-none pl-0">
                                            {#each alertActions as act (act.id)}
                                                <li
                                                    class="flex items-start justify-between gap-2.5 text-[10px] py-0.5"
                                                >
                                                    <span
                                                        class="text-gray-700 font-medium leading-normal flex-1"
                                                    >
                                                        {act.title}
                                                    </span>
                                                    <span
                                                        class={`text-[8px] font-extrabold uppercase px-1.5 py-0.5 rounded-md border tracking-wider shrink-0 mt-0.5 ${
                                                            act.status ===
                                                            "completed"
                                                                ? "bg-emerald-50 text-emerald-700 border-emerald-200"
                                                                : act.status ===
                                                                    "in_progress"
                                                                  ? "bg-blue-50 text-blue-700 border-blue-200"
                                                                  : act.status ===
                                                                      "cancelled"
                                                                    ? "bg-gray-100 text-gray-700 border-gray-300"
                                                                    : "bg-amber-50 text-amber-700 border-amber-200"
                                                        }`}
                                                    >
                                                        {act.status}
                                                    </span>
                                                </li>
                                            {/each}
                                        </ul>
                                    </div>
                                {:else}
                                    <div
                                        class="mt-1 pt-2 border-t border-gray-100 text-[9px] text-gray-400 italic"
                                    >
                                        No response actions registered.
                                    </div>
                                {/if}
                            </article>
                        {/each}
                    {/if}
                </div>
            {/if}
        {/if}
    </aside>
</div>
