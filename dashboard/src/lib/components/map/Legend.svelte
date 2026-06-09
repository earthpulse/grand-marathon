<script>
    let {
        showRisk = false,
        showHazard = false,
        showHotspots = false,
        showPopulation = false,
        showBuildings = false,
        showRoads = false,
        showAmenities = false,
        showMunicipalities = false,
    } = $props();

    // Internal state to track if the legend is collapsed
    let isCollapsed = $state(false);

    // The legend is visible if any of the layers are active
    const isVisible = $derived(
        showRisk ||
        showHazard ||
        showHotspots ||
        showPopulation ||
        showBuildings ||
        showRoads ||
        showAmenities ||
        showMunicipalities
    );

    // Check if any risk/vulnerability-based layer is active
    const showRiskLegend = $derived(
        showRisk ||
        showHazard ||
        showBuildings ||
        showRoads ||
        showAmenities ||
        showMunicipalities
    );
</script>

{#if isVisible}
    <div class="absolute bottom-3 left-3 z-[10000] pointer-events-auto flex flex-col items-start gap-2">
        {#if isCollapsed}
            <button
                onclick={() => (isCollapsed = false)}
                class="bg-white hover:bg-gray-50 text-gray-700 border border-gray-200 rounded-lg shadow-md p-2.5 flex items-center justify-center cursor-pointer transition-all duration-150 hover:scale-105"
                title="Show Map Legend"
            >
                <span class="text-base">🗺️</span>
            </button>
        {:else}
            <div
                class="bg-white/95 backdrop-blur-xs rounded-xl shadow-lg border border-gray-200/80 p-3 w-52 flex flex-col gap-3 transition-all duration-200"
            >
                <div class="flex items-center justify-between border-b border-gray-100 pb-1.5">
                    <h3 class="text-[10px] font-bold text-gray-900 flex items-center gap-1.5 uppercase tracking-wider">
                        🗺️ Map Legend
                    </h3>
                    <button
                        onclick={() => (isCollapsed = true)}
                        class="text-gray-400 hover:text-gray-600 transition-colors cursor-pointer text-[10px] font-bold p-1 hover:bg-gray-100 rounded"
                        title="Collapse Legend"
                    >
                        ✕
                    </button>
                </div>

                <div class="flex flex-col gap-3">
                    <!-- Risk & Vulnerability Levels -->
                    {#if showRiskLegend}
                        <div class="flex flex-col">
                            <h4 class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1.5">
                                Risk & Vulnerability
                            </h4>
                            <div class="flex flex-col gap-1.5">
                                <div class="flex items-center gap-2">
                                    <div class="w-3.5 h-3.5 rounded bg-[#48bb78] border border-green-600/20 shadow-xs"></div>
                                    <span class="text-[10px] font-semibold text-gray-700">Low</span>
                                </div>
                                <div class="flex items-center gap-2">
                                    <div class="w-3.5 h-3.5 rounded bg-[#ecc94b] border border-yellow-600/20 shadow-xs"></div>
                                    <span class="text-[10px] font-semibold text-gray-700">Medium</span>
                                </div>
                                <div class="flex items-center gap-2">
                                    <div class="w-3.5 h-3.5 rounded bg-[#ed8936] border border-orange-600/20 shadow-xs"></div>
                                    <span class="text-[10px] font-semibold text-gray-700">High</span>
                                </div>
                                <div class="flex items-center gap-2">
                                    <div class="w-3.5 h-3.5 rounded bg-[#e53e3e] border border-red-600/20 shadow-xs"></div>
                                    <span class="text-[10px] font-semibold text-gray-700">Critical</span>
                                </div>
                            </div>
                        </div>
                    {/if}

                    <!-- Population Density -->
                    {#if showPopulation}
                        <div class="flex flex-col">
                            <h4 class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1.5">
                                Amount of Affected Population
                            </h4>
                            <div class="flex flex-col gap-1">
                                <div class="h-2.5 w-full rounded-sm bg-gradient-to-r from-[#ffffe5] via-[#fe9929] to-[#bd0026] border border-gray-200/50 shadow-xs"></div>
                                <div class="flex justify-between text-[9px] font-bold text-gray-500 px-0.5">
                                    <span>Low</span>
                                    <span>High</span>
                                </div>
                            </div>
                        </div>
                    {/if}

                    <!-- Active Hotspots -->
                    {#if showHotspots}
                        <div class="flex flex-col">
                            <h4 class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1.5">
                                Hotspots
                            </h4>
                            <div class="flex items-center gap-2">
                                <div class="w-3.5 h-3.5 rounded-full bg-red-500 border border-red-700/30 flex items-center justify-center shadow-xs">
                                    <div class="w-1.5 h-1.5 rounded-full bg-white"></div>
                                </div>
                                <span class="text-[10px] font-semibold text-gray-700">Active Hotspot</span>
                            </div>
                        </div>
                    {/if}

                    <!-- Base Asset Styles (Defaults) -->
                    {#if showBuildings || showRoads || showAmenities}
                        <div class="flex flex-col border-t border-gray-100 pt-2">
                            <h4 class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1.5">
                                Default Assets
                            </h4>
                            <div class="flex flex-col gap-1.5">
                                {#if showBuildings}
                                    <div class="flex items-center gap-2">
                                        <div class="w-3.5 h-3.5 rounded bg-[#718096] border border-gray-600/20 shadow-xs"></div>
                                        <span class="text-[10px] font-semibold text-gray-700">Building (No Risk Data)</span>
                                    </div>
                                {/if}
                                {#if showRoads || showAmenities}
                                    <div class="flex items-center gap-2">
                                        <div class="w-3.5 h-3.5 rounded bg-[#3182ce] border border-blue-600/20 shadow-xs"></div>
                                        <span class="text-[10px] font-semibold text-gray-700">Road / Amenity</span>
                                    </div>
                                {/if}
                            </div>
                        </div>
                    {/if}
                </div>
            </div>
        {/if}
    </div>
{/if}
