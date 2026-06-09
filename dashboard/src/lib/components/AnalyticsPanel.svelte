<script>
    let { analytics = null, loading = false, error = null } = $props();

    const riskLevels = [
        {
            id: "1",
            label: "Level 1 (Low)",
            bgClass: "bg-emerald-500",
            textClass: "text-emerald-600",
        },
        {
            id: "2",
            label: "Level 2 (Medium)",
            bgClass: "bg-amber-400",
            textClass: "text-amber-500",
        },
        {
            id: "3",
            label: "Level 3 (High)",
            bgClass: "bg-orange-500",
            textClass: "text-orange-500",
        },
        {
            id: "4",
            label: "Level 4 (Critical)",
            bgClass: "bg-red-600",
            textClass: "text-red-600",
        },
    ];

    function getTotalsAndDistribution(counts, percents) {
        if (!counts) return { total: 0, items: [] };
        const total = Object.values(counts).reduce(
            (sum, val) => sum + (val || 0),
            0,
        );
        const items = riskLevels.map((lvl) => {
            const rawCount = counts[lvl.id] || 0;
            const count = Math.round(rawCount);
            const percent =
                percents && percents[lvl.id] !== undefined
                    ? percents[lvl.id]
                    : total > 0
                      ? (rawCount / total) * 100
                      : 0;
            return {
                ...lvl,
                count,
                percent,
            };
        });
        return { total: Math.round(total), items };
    }
</script>

{#if loading}
    <div
        class="bg-white border border-gray-100 rounded-xl p-3 shadow-xs animate-pulse flex flex-col gap-3"
    >
        <div class="flex justify-between items-center">
            <div class="h-5 bg-gray-200 rounded w-1/3"></div>
            <div class="h-5 bg-gray-200 rounded w-1/4"></div>
        </div>
        <div class="h-10 bg-gray-100 rounded w-full"></div>
        <div class="grid grid-cols-3 gap-3">
            <div class="h-12 bg-gray-100 rounded"></div>
            <div class="h-12 bg-gray-100 rounded"></div>
            <div class="h-12 bg-gray-100 rounded"></div>
        </div>
        <div class="grid grid-cols-2 gap-3">
            <div class="h-24 bg-gray-100 rounded"></div>
            <div class="h-24 bg-gray-100 rounded"></div>
        </div>
    </div>
{:else if error}
    <div
        class="bg-red-50 border border-red-200 text-red-700 rounded-xl p-3 shadow-xs flex items-center gap-2"
    >
        <span class="text-base">⚠️</span>
        <div>
            <h4 class="font-bold text-xs">Failed to load analytics</h4>
            <p class="text-[10px]">{error}</p>
        </div>
    </div>
{:else if analytics}
    <div
        class="bg-white border border-gray-200 rounded-xl p-3 shadow-xs flex flex-col gap-3"
    >
        <!-- Header -->
        <div
            class="flex flex-col sm:flex-row sm:items-center justify-between gap-1.5 border-b border-gray-100 pb-2"
        >
            <div class="flex items-center gap-1.5">
                <span class="text-lg">📊</span>
                <div>
                    <h3 class="text-xs font-bold text-gray-900">
                        Risk Analytics
                    </h3>
                    <!-- <p class="text-[9px] text-gray-400">
                        Rule Set: {analytics.rule_set} • Generated: {new Date(
                            analytics.generated_at,
                        ).toLocaleString()}
                    </p> -->
                </div>
            </div>
            <div class="flex items-center gap-1 flex-wrap">
                <span
                    class="bg-blue-50 border border-blue-200 text-blue-700 text-[9px] font-bold px-2 py-0.5 rounded-full"
                >
                    📅 {analytics.analysis_date}
                </span>
            </div>
        </div>

        <!-- Key Metrics Grid -->
        <!-- <div class="grid grid-cols-3 gap-2">
            <div
                class="bg-gray-50/50 border border-gray-100 rounded-lg p-1.5 text-center"
            >
                <span
                    class="text-[9px] font-bold text-gray-400 uppercase tracking-wider block mb-0.5"
                    >Mean Hazard</span
                >
                <span
                    class={`text-xs font-extrabold ${
                        analytics.mean_hazard < 0.25
                            ? "text-emerald-600"
                            : analytics.mean_hazard < 0.45
                              ? "text-amber-500"
                              : "text-red-600"
                    }`}>{analytics.mean_hazard.toFixed(4)}</span
                >
            </div>
            <div
                class="bg-gray-50/50 border border-gray-100 rounded-lg p-1.5 text-center"
            >
                <span
                    class="text-[9px] font-bold text-gray-400 uppercase tracking-wider block mb-0.5"
                    >Mean Exposure</span
                >
                <span
                    class={`text-xs font-extrabold ${
                        analytics.mean_exposure < 0.05
                            ? "text-emerald-600"
                            : analytics.mean_exposure < 0.15
                              ? "text-amber-500"
                              : "text-red-600"
                    }`}>{analytics.mean_exposure.toFixed(4)}</span
                >
            </div>
            <div
                class="bg-gray-50/50 border border-gray-100 rounded-lg p-1.5 text-center"
            >
                <span
                    class="text-[9px] font-bold text-gray-400 uppercase tracking-wider block mb-0.5"
                    >Mean Vulnerability</span
                >
                <span
                    class={`text-xs font-extrabold ${
                        analytics.mean_vulnerability < 0.15
                            ? "text-emerald-600"
                            : analytics.mean_vulnerability < 0.35
                              ? "text-amber-500"
                              : "text-red-600"
                    }`}>{analytics.mean_vulnerability.toFixed(4)}</span
                >
            </div>
        </div> -->

        <!-- Distributions Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-0.5">
            <!-- Hazard Distribution -->
            <div
                class="border border-gray-100 rounded-lg p-2 flex flex-col gap-2"
            >
                <h4
                    class="text-[11px] font-bold text-gray-900 flex items-center gap-1 border-b border-gray-50 pb-1"
                >
                    ⚠️ Hazard Distribution
                </h4>
                <div class="space-y-1.5">
                    <!-- Low -->
                    <div class="flex flex-col gap-0.5">
                        <div class="flex justify-between text-[10px] font-bold">
                            <span class="text-gray-500">Low</span>
                            <span class="text-emerald-700"
                                >{analytics.hazard_pct_low.toFixed(2)}%</span
                            >
                        </div>
                        <div
                            class="w-full bg-gray-100 h-1.5 rounded-full overflow-hidden"
                        >
                            <div
                                class="bg-emerald-500 h-full rounded-full"
                                style="width: {analytics.hazard_pct_low}%"
                            ></div>
                        </div>
                    </div>
                    <!-- Medium -->
                    <div class="flex flex-col gap-0.5">
                        <div class="flex justify-between text-[10px] font-bold">
                            <span class="text-gray-500">Medium</span>
                            <span class="text-amber-700"
                                >{analytics.hazard_pct_medium.toFixed(2)}%</span
                            >
                        </div>
                        <div
                            class="w-full bg-gray-100 h-1.5 rounded-full overflow-hidden"
                        >
                            <div
                                class="bg-amber-500 h-full rounded-full"
                                style="width: {analytics.hazard_pct_medium}%"
                            ></div>
                        </div>
                    </div>
                    <!-- High -->
                    <div class="flex flex-col gap-0.5">
                        <div class="flex justify-between text-[10px] font-bold">
                            <span class="text-gray-500">High</span>
                            <span class="text-orange-700"
                                >{analytics.hazard_pct_high.toFixed(2)}%</span
                            >
                        </div>
                        <div
                            class="w-full bg-gray-100 h-1.5 rounded-full overflow-hidden"
                        >
                            <div
                                class="bg-orange-500 h-full rounded-full"
                                style="width: {analytics.hazard_pct_high}%"
                            ></div>
                        </div>
                    </div>
                    <!-- Critical -->
                    <div class="flex flex-col gap-0.5">
                        <div class="flex justify-between text-[10px] font-bold">
                            <span class="text-gray-500">Critical</span>
                            <span class="text-red-700"
                                >{analytics.hazard_pct_critical.toFixed(
                                    2,
                                )}%</span
                            >
                        </div>
                        <div
                            class="w-full bg-gray-100 h-1.5 rounded-full overflow-hidden"
                        >
                            <div
                                class="bg-red-600 h-full rounded-full"
                                style="width: {analytics.hazard_pct_critical}%"
                            ></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Operational Priority Distribution -->
            <div
                class="border border-gray-100 rounded-lg p-2 flex flex-col gap-2"
            >
                <h4
                    class="text-[11px] font-bold text-gray-900 flex items-center gap-1 border-b border-gray-50 pb-1"
                >
                    🎯 Operational Priority Distribution
                </h4>
                <div class="space-y-1.5">
                    <!-- Low -->
                    <div class="flex flex-col gap-0.5">
                        <div class="flex justify-between text-[10px] font-bold">
                            <span class="text-gray-500">Low</span>
                            <span class="text-emerald-700"
                                >{analytics.priority_pct_low.toFixed(2)}%</span
                            >
                        </div>
                        <div
                            class="w-full bg-gray-100 h-1.5 rounded-full overflow-hidden"
                        >
                            <div
                                class="bg-emerald-500 h-full rounded-full"
                                style="width: {analytics.priority_pct_low}%"
                            ></div>
                        </div>
                    </div>
                    <!-- Medium -->
                    <div class="flex flex-col gap-0.5">
                        <div class="flex justify-between text-[10px] font-bold">
                            <span class="text-gray-500">Medium</span>
                            <span class="text-amber-700"
                                >{analytics.priority_pct_medium.toFixed(
                                    2,
                                )}%</span
                            >
                        </div>
                        <div
                            class="w-full bg-gray-100 h-1.5 rounded-full overflow-hidden"
                        >
                            <div
                                class="bg-amber-500 h-full rounded-full"
                                style="width: {analytics.priority_pct_medium}%"
                            ></div>
                        </div>
                    </div>
                    <!-- High -->
                    <div class="flex flex-col gap-0.5">
                        <div class="flex justify-between text-[10px] font-bold">
                            <span class="text-gray-500">High</span>
                            <span class="text-orange-700"
                                >{analytics.priority_pct_high.toFixed(2)}%</span
                            >
                        </div>
                        <div
                            class="w-full bg-gray-100 h-1.5 rounded-full overflow-hidden"
                        >
                            <div
                                class="bg-orange-500 h-full rounded-full"
                                style="width: {analytics.priority_pct_high}%"
                            ></div>
                        </div>
                    </div>
                    <!-- Critical -->
                    <div class="flex flex-col gap-0.5">
                        <div class="flex justify-between text-[10px] font-bold">
                            <span class="text-gray-500">Critical</span>
                            <span class="text-red-700"
                                >{analytics.priority_pct_critical.toFixed(
                                    2,
                                )}%</span
                            >
                        </div>
                        <div
                            class="w-full bg-gray-100 h-1.5 rounded-full overflow-hidden"
                        >
                            <div
                                class="bg-red-600 h-full rounded-full"
                                style="width: {analytics.priority_pct_critical}%"
                            ></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Exposure Risk by Asset Category -->
        <div class="border-t border-gray-100 pt-3 flex flex-col gap-3">
            <h4
                class="text-xs font-bold text-gray-900 flex items-center gap-1.5 pb-1 border-b border-gray-100"
            >
                🔍 Exposure Risk Analytics
            </h4>

            <div class="space-y-4">
                <!-- Population at Risk -->
                {#if analytics.population_risk_counts}
                    {@const population = getTotalsAndDistribution(
                        analytics.population_risk_counts,
                        analytics.population_risk_percents,
                    )}
                    <div
                        class="bg-gray-50/30 border border-gray-100/80 rounded-xl p-3 flex flex-col gap-2.5"
                    >
                        <div class="flex justify-between items-center">
                            <span
                                class="text-xs font-bold text-gray-800 flex items-center gap-1.5"
                            >
                                👥 Amount of Affected Population
                            </span>
                            <span
                                class="text-[10px] font-extrabold bg-blue-50 text-blue-700 border border-blue-100 px-2 py-0.5 rounded-md"
                            >
                                Total: {population.total.toLocaleString()}
                            </span>
                        </div>
                        <div class="space-y-2">
                            {#each population.items as item}
                                <div class="flex flex-col gap-1">
                                    <div
                                        class="flex justify-between items-center text-[10px] font-bold"
                                    >
                                        <span class="text-gray-500"
                                            >{item.label}</span
                                        >
                                        <span class={item.textClass}>
                                            {item.count.toLocaleString()} ({item.percent.toFixed(
                                                2,
                                            )}%)
                                        </span>
                                    </div>
                                    <div
                                        class="w-full bg-gray-100 h-2 rounded-full overflow-hidden"
                                    >
                                        <div
                                            class="{item.bgClass} h-full rounded-full transition-all duration-300"
                                            style="width: {item.percent}%"
                                        ></div>
                                    </div>
                                </div>
                            {/each}
                        </div>
                    </div>
                {/if}

                <!-- Roads -->
                {#if analytics.road_risk_counts}
                    {@const roads = getTotalsAndDistribution(
                        analytics.road_risk_counts,
                        analytics.road_risk_percents,
                    )}
                    <div
                        class="bg-gray-50/30 border border-gray-100/80 rounded-xl p-3 flex flex-col gap-2.5"
                    >
                        <div class="flex justify-between items-center">
                            <span
                                class="text-xs font-bold text-gray-800 flex items-center gap-1.5"
                            >
                                🛣️ Number of Affected Roads
                            </span>
                            <span
                                class="text-[10px] font-extrabold bg-blue-50 text-blue-700 border border-blue-100 px-2 py-0.5 rounded-md"
                            >
                                Total: {roads.total.toLocaleString()}
                            </span>
                        </div>
                        <div class="space-y-2">
                            {#each roads.items as item}
                                <div class="flex flex-col gap-1">
                                    <div
                                        class="flex justify-between items-center text-[10px] font-bold"
                                    >
                                        <span class="text-gray-500"
                                            >{item.label}</span
                                        >
                                        <span class={item.textClass}>
                                            {item.count.toLocaleString()} ({item.percent.toFixed(
                                                2,
                                            )}%)
                                        </span>
                                    </div>
                                    <div
                                        class="w-full bg-gray-100 h-2 rounded-full overflow-hidden"
                                    >
                                        <div
                                            class="{item.bgClass} h-full rounded-full transition-all duration-300"
                                            style="width: {item.percent}%"
                                        ></div>
                                    </div>
                                </div>
                            {/each}
                        </div>
                    </div>
                {/if}

                <!-- Buildings -->
                {#if analytics.building_risk_counts}
                    {@const buildings = getTotalsAndDistribution(
                        analytics.building_risk_counts,
                        analytics.building_risk_percents,
                    )}
                    <div
                        class="bg-gray-50/30 border border-gray-100/80 rounded-xl p-3 flex flex-col gap-2.5"
                    >
                        <div class="flex justify-between items-center">
                            <span
                                class="text-xs font-bold text-gray-800 flex items-center gap-1.5"
                            >
                                🏢 Number of Affected Buildings
                            </span>
                            <span
                                class="text-[10px] font-extrabold bg-blue-50 text-blue-700 border border-blue-100 px-2 py-0.5 rounded-md"
                            >
                                Total: {buildings.total.toLocaleString()}
                            </span>
                        </div>
                        <div class="space-y-2">
                            {#each buildings.items as item}
                                <div class="flex flex-col gap-1">
                                    <div
                                        class="flex justify-between items-center text-[10px] font-bold"
                                    >
                                        <span class="text-gray-500"
                                            >{item.label}</span
                                        >
                                        <span class={item.textClass}>
                                            {item.count.toLocaleString()} ({item.percent.toFixed(
                                                2,
                                            )}%)
                                        </span>
                                    </div>
                                    <div
                                        class="w-full bg-gray-100 h-2 rounded-full overflow-hidden"
                                    >
                                        <div
                                            class="{item.bgClass} h-full rounded-full transition-all duration-300"
                                            style="width: {item.percent}%"
                                        ></div>
                                    </div>
                                </div>
                            {/each}
                        </div>
                    </div>
                {/if}

                <!-- Amenities -->
                {#if analytics.amenity_risk_counts}
                    {@const amenities = getTotalsAndDistribution(
                        analytics.amenity_risk_counts,
                        analytics.amenity_risk_percents,
                    )}
                    <div
                        class="bg-gray-50/30 border border-gray-100/80 rounded-xl p-3 flex flex-col gap-2.5"
                    >
                        <div class="flex justify-between items-center">
                            <span
                                class="text-xs font-bold text-gray-800 flex items-center gap-1.5"
                            >
                                🏥 Number of Affected Amenities
                            </span>
                            <span
                                class="text-[10px] font-extrabold bg-blue-50 text-blue-700 border border-blue-100 px-2 py-0.5 rounded-md"
                            >
                                Total: {amenities.total.toLocaleString()}
                            </span>
                        </div>
                        <div class="space-y-2">
                            {#each amenities.items as item}
                                <div class="flex flex-col gap-1">
                                    <div
                                        class="flex justify-between items-center text-[10px] font-bold"
                                    >
                                        <span class="text-gray-500"
                                            >{item.label}</span
                                        >
                                        <span class={item.textClass}>
                                            {item.count.toLocaleString()} ({item.percent.toFixed(
                                                2,
                                            )}%)
                                        </span>
                                    </div>
                                    <div
                                        class="w-full bg-gray-100 h-2 rounded-full overflow-hidden"
                                    >
                                        <div
                                            class="{item.bgClass} h-full rounded-full transition-all duration-300"
                                            style="width: {item.percent}%"
                                        ></div>
                                    </div>
                                </div>
                            {/each}
                        </div>
                    </div>
                {/if}
            </div>
        </div>
    </div>
{/if}
