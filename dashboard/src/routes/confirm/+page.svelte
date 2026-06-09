<script>
    import { confirmStore } from "$lib/stores/confirm.svelte";
    import { actionsStore } from "$lib/stores/actions.svelte";
    import { untrack } from "svelte";
    import AlertFilters from "$lib/components/AlertFilters.svelte";

    const { data } = $props();

    // Sync SvelteKit's initial server load data into our Svelte 5 store untracked
    $effect(() => {
        const { news, alerts, actions, api_url } = data;
        untrack(() => {
            confirmStore.init(news, alerts, api_url, actions);
        });
    });

    // Reactive bindings to store properties
    let alerts = $derived(confirmStore.filteredAlerts);
    let selectedAlert = $derived(confirmStore.selectedAlert);
    let relatedNews = $derived(confirmStore.relatedNews);
    let recentNews = $derived(confirmStore.recentNews);
    let recommendation = $derived(confirmStore.recommendation);
    let selectedAlertId = $derived(confirmStore.selectedAlertId);
    let statusFilter = $derived(confirmStore.statusFilter);
    let alertSearchQuery = $derived(confirmStore.alertSearchQuery);
    let hasPlannedActions = $derived(confirmStore.hasPlannedActions);
    let selectedAlertActions = $derived(actionsStore.items.filter(act => act.alert_id === selectedAlertId));

    let activeNewsTab = $state("related");

    let displayedNews = $derived(
        activeNewsTab === "recent"
            ? recentNews.map(item => ({ ...item, isRecentOnly: false }))
            : relatedNews.length === 0
              ? recentNews.map(item => ({ ...item, isRecentOnly: true }))
              : relatedNews.length < 3
                ? [
                    ...relatedNews.map(item => ({ ...item, isRecentOnly: false })),
                    ...recentNews
                        .filter(r => !relatedNews.some(rel => rel.id === r.id))
                        .map(item => ({ ...item, isRecentOnly: true }))
                  ]
                : relatedNews.map(item => ({ ...item, isRecentOnly: false }))
    );

    function handleSelectAlert(id) {
        confirmStore.setSelectedAlertId(id);
    }

    function handleSearchInput(e) {
        confirmStore.setSearchQuery(e.target.value);
    }

    function handleStatusFilter(filter) {
        confirmStore.setStatusFilter(filter);
    }

    async function handleUpdateStatus(alertId, newStatus, newSeverity = null) {
        try {
            await confirmStore.updateAlertStatus(
                alertId,
                newStatus,
                newSeverity,
            );
        } catch (err) {
            console.error("Action failed:", err);
        }
    }

    function handleHelperAction(actionType) {
        // These are just helpers that should redirect the operator (for now, do nothing)
    }

    function formatDate(isoString) {
        try {
            const date = new Date(isoString);
            return date.toLocaleString();
        } catch {
            return isoString;
        }
    }
</script>

<div class="flex-1 flex flex-col min-h-0 bg-gray-50/50">
    <!-- Main Dual-Pane Workspace -->
    <div
        class="flex-1 grid grid-cols-1 lg:grid-cols-12 min-h-0 divide-y lg:divide-y-0 lg:divide-x divide-gray-200"
    >
        <!-- ================= LEFT PANEL: ALERTS FEED (5 cols) ================= -->
        <section class="lg:col-span-5 flex flex-col min-h-0 bg-white">
            <!-- Search & Filters Header -->
            <div class="p-4 border-b border-gray-200 space-y-3 shrink-0">
                <div class="flex items-center justify-between">
                    <h2
                        class="text-lg font-bold text-gray-900 flex items-center gap-2"
                    >
                        <span>✅ Confirm</span>
                    </h2>
                    <span
                        class="text-xs bg-gray-100 text-gray-700 font-medium px-2 py-0.5 rounded-full"
                    >
                        {alerts.length} found
                    </span>
                </div>

                <AlertFilters
                    searchQuery={alertSearchQuery}
                    {statusFilter}
                    excludeResolved={true}
                    onSearchChange={(val) => confirmStore.setSearchQuery(val)}
                    onStatusChange={(val) => confirmStore.setStatusFilter(val)}
                />
            </div>

            <!-- Scrollable Alerts Feed -->
            <div class="flex-1 overflow-y-auto p-4 space-y-3">
                {#if alerts.length === 0}
                    <div
                        class="text-center py-12 border-2 border-dashed border-gray-200 rounded-lg"
                    >
                        <p class="text-sm text-gray-400">
                            No alerts match your criteria.
                        </p>
                    </div>
                {:else}
                    {#each alerts as alert (alert.id)}
                        <button
                            onclick={() => handleSelectAlert(alert.id)}
                            class={`w-full text-left p-4 rounded-lg border transition-all flex flex-col gap-2 relative cursor-pointer ${
                                selectedAlertId === alert.id
                                    ? "border-blue-500 bg-blue-50/20 ring-1 ring-blue-100 shadow-xs"
                                    : "border-gray-200 bg-white hover:bg-gray-50/80 shadow-2xs"
                            }`}
                        >
                            <!-- Severity tag & Title -->
                            <div class="flex justify-between items-start gap-2">
                                <h3
                                    class="font-bold text-sm text-gray-900 leading-tight"
                                >
                                    {alert.title}
                                </h3>
                                <span
                                    class={`text-[9px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded-full shrink-0 border ${
                                        alert.severity === "critical"
                                            ? "bg-red-50 text-red-700 border-red-200"
                                            : alert.severity === "warning"
                                              ? "bg-amber-50 text-amber-700 border-amber-200"
                                              : "bg-blue-50 text-blue-700 border-blue-200"
                                    }`}
                                >
                                    {alert.severity}
                                </span>
                            </div>

                            <!-- Description -->
                            <p
                                class="text-xs text-gray-500 line-clamp-2 leading-relaxed"
                            >
                                {alert.description}
                            </p>

                            <!-- Bottom stats -->
                            <div
                                class="flex justify-between items-center text-[10px] text-gray-400 mt-1 pt-2 border-t border-gray-100"
                            >
                                <div class="flex items-center gap-1.5">
                                    <!-- Status tag -->
                                    <span
                                        class={`font-semibold uppercase px-1.5 py-0.5 rounded text-[9px] ${
                                            alert.status === "active"
                                                ? "bg-orange-100 text-orange-800"
                                                : alert.status ===
                                                    "acknowledged"
                                                  ? "bg-blue-100 text-blue-800"
                                                  : "bg-gray-100 text-gray-800"
                                        }`}
                                    >
                                        {alert.status === "active"
                                            ? "unconfirmed"
                                            : alert.status}
                                    </span>
                                    {#if alert.latitude !== null && alert.longitude !== null}
                                        <span
                                            >📍 {alert.latitude.toFixed(3)}, {alert.longitude.toFixed(
                                                3,
                                            )}</span
                                        >
                                    {/if}
                                </div>
                                <span class="text-[9px]"
                                    >{formatDate(alert.created_at).split(
                                        ",",
                                    )[0]}</span
                                >
                            </div>
                        </button>
                    {/each}
                {/if}
            </div>
        </section>

        <!-- ================= RIGHT PANEL: EVIDENCE WORKSPACE (7 cols) ================= -->
        <section class="lg:col-span-7 flex flex-col min-h-0 bg-gray-50">
            {#if selectedAlert}
                <!-- Workspace Header: Active Alert details -->
                <div
                    class="bg-white p-5 border-b border-gray-200 shrink-0 shadow-2xs"
                >
                    <div
                        class="flex flex-wrap items-center justify-between gap-3 mb-2"
                    >
                        <div class="flex items-center gap-2">
                            <span class="text-xl">🔔</span>
                            <span
                                class="text-xs font-semibold text-gray-400 uppercase tracking-widest"
                                >Selected Target</span
                            >
                        </div>
                        <div class="flex gap-2">
                            {#if selectedAlert.status === "active"}
                                <button
                                    onclick={() =>
                                        handleUpdateStatus(
                                            selectedAlert.id,
                                            "acknowledged",
                                        )}
                                    class="px-3 py-1.5 text-xs font-bold rounded-md bg-blue-600 text-white hover:bg-blue-700 transition-colors cursor-pointer shadow-xs"
                                >
                                    Confirm
                                </button>
                            {:else if selectedAlert.status === "acknowledged"}
                                <button
                                    onclick={() =>
                                        handleUpdateStatus(
                                            selectedAlert.id,
                                            "active",
                                        )}
                                    disabled={hasPlannedActions}
                                    title={hasPlannedActions ? "Cannot unconfirm: there are active response actions planned for this alert." : "Revert alert to unconfirmed status"}
                                    class="px-3 py-1.5 text-xs font-bold rounded-md bg-amber-600 text-white hover:bg-amber-700 disabled:bg-gray-100 disabled:text-gray-400 disabled:cursor-not-allowed transition-colors cursor-pointer shadow-xs"
                                >
                                    Unconfirm
                                </button>
                            {/if}
                        </div>
                    </div>

                    <h1 class="text-lg font-bold text-gray-900 leading-snug">
                        {selectedAlert.title}
                    </h1>
                    <p
                        class="text-xs text-gray-600 mt-2 bg-gray-50 p-3 rounded-md border border-gray-100 whitespace-pre-line leading-relaxed"
                    >
                        {selectedAlert.description}
                    </p>

                    {#if (selectedAlert.affected_roads_count !== undefined && selectedAlert.affected_roads_count !== null) || (selectedAlert.affected_buildings_count !== undefined && selectedAlert.affected_buildings_count !== null) || (selectedAlert.affected_amenities_count !== undefined && selectedAlert.affected_amenities_count !== null) || (selectedAlert.affected_population !== undefined && selectedAlert.affected_population !== null)}
                        <div class="mt-3 p-3 bg-slate-50 border border-slate-200 rounded-lg flex flex-col gap-2">
                            <h3 class="text-xs font-bold text-slate-700 uppercase tracking-wider">Affected in 1km Buffer</h3>
                            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                                {#if selectedAlert.affected_roads_count !== undefined && selectedAlert.affected_roads_count !== null}
                                    <div class="bg-white p-2 rounded border border-slate-100 flex flex-col gap-0.5">
                                        <span class="text-[10px] text-gray-400 font-semibold uppercase">🛣️ Number of Affected Roads</span>
                                        <span class="text-sm font-extrabold text-blue-600">{selectedAlert.affected_roads_count}</span>
                                    </div>
                                {/if}
                                {#if selectedAlert.affected_buildings_count !== undefined && selectedAlert.affected_buildings_count !== null}
                                    <div class="bg-white p-2 rounded border border-slate-100 flex flex-col gap-0.5">
                                        <span class="text-[10px] text-gray-400 font-semibold uppercase">🏢 Number of Affected Buildings</span>
                                        <span class="text-sm font-extrabold text-amber-600">{selectedAlert.affected_buildings_count}</span>
                                    </div>
                                {/if}
                                {#if selectedAlert.affected_amenities_count !== undefined && selectedAlert.affected_amenities_count !== null}
                                    <div class="bg-white p-2 rounded border border-slate-100 flex flex-col gap-0.5">
                                        <span class="text-[10px] text-gray-400 font-semibold uppercase">🏥 Number of Affected Amenities</span>
                                        <span class="text-sm font-extrabold text-purple-600">{selectedAlert.affected_amenities_count}</span>
                                    </div>
                                {/if}
                                {#if selectedAlert.affected_population !== undefined && selectedAlert.affected_population !== null}
                                    <div class="bg-white p-2 rounded border border-slate-100 flex flex-col gap-0.5">
                                        <span class="text-[10px] text-gray-400 font-semibold uppercase">👥 Amount of Affected Population</span>
                                        <span class="text-sm font-extrabold text-emerald-600">{selectedAlert.affected_population}</span>
                                    </div>
                                {/if}
                            </div>
                        </div>
                    {/if}

                    {#if selectedAlert.severity === "critical" && selectedAlert.status === "active"}
                        <div class="mt-4 p-4 bg-red-50/40 border border-red-100 rounded-lg flex flex-col gap-3">
                            <div class="flex items-center gap-2">
                                <span class="text-lg">🚨</span>
                                <div>
                                    <h3 class="text-xs font-bold text-red-900 uppercase tracking-wider">Critical Alert Action Helpers</h3>
                                    <p class="text-[10px] text-red-700">Use these external communication and dispatch helpers to coordinate response. Click to open or redirect (for now, do nothing). Confirm the alert manually above afterwards.</p>
                                </div>
                            </div>
                            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
                                <button
                                    onclick={() => handleHelperAction("call")}
                                    class="flex flex-col items-center justify-center gap-1.5 p-2.5 bg-white hover:bg-red-50 border border-red-200 hover:border-red-300 text-red-800 rounded-lg transition-all shadow-2xs hover:scale-[1.02] active:scale-[0.98] cursor-pointer"
                                >
                                    <span class="text-lg">📞</span>
                                    <span class="text-[10px] font-bold text-center leading-tight">Call Emergency</span>
                                </button>
                                <button
                                    onclick={() => handleHelperAction("drone")}
                                    class="flex flex-col items-center justify-center gap-1.5 p-2.5 bg-white hover:bg-red-50 border border-red-200 hover:border-red-300 text-red-800 rounded-lg transition-all shadow-2xs hover:scale-[1.02] active:scale-[0.98] cursor-pointer"
                                >
                                    <span class="text-lg">🛸</span>
                                    <span class="text-[10px] font-bold text-center leading-tight">Deploy Drone</span>
                                </button>
                                <button
                                    onclick={() => handleHelperAction("dispatch")}
                                    class="flex flex-col items-center justify-center gap-1.5 p-2.5 bg-white hover:bg-red-50 border border-red-200 hover:border-red-300 text-red-800 rounded-lg transition-all shadow-2xs hover:scale-[1.02] active:scale-[0.98] cursor-pointer"
                                >
                                    <span class="text-lg">🚒</span>
                                    <span class="text-[10px] font-bold text-center leading-tight">Dispatch Crew</span>
                                </button>
                                <button
                                    onclick={() => handleHelperAction("warning")}
                                    class="flex flex-col items-center justify-center gap-1.5 p-2.5 bg-white hover:bg-red-50 border border-red-200 hover:border-red-300 text-red-800 rounded-lg transition-all shadow-2xs hover:scale-[1.02] active:scale-[0.98] cursor-pointer"
                                >
                                    <span class="text-lg">📢</span>
                                    <span class="text-[10px] font-bold text-center leading-tight">Public Warning</span>
                                </button>
                            </div>
                        </div>
                    {/if}

                    {#if selectedAlertActions.length > 0}
                        <div class="mt-4 pt-3 border-t border-gray-100">
                            <h4 class="text-[10px] font-extrabold text-gray-400 uppercase tracking-wider mb-2">Dispatched Actions</h4>
                            <div class="space-y-2">
                                {#each selectedAlertActions as action (action.id)}
                                    <div class="flex items-start justify-between gap-3 p-2.5 bg-gray-50 border border-gray-100 rounded-md">
                                        <div class="flex-1 min-w-0">
                                            <div class="flex items-center gap-1.5">
                                                <span class="text-xs font-bold text-gray-900">{action.title}</span>
                                                <span class={`text-[8px] font-extrabold uppercase px-1.5 py-0.5 rounded-md border tracking-wider shrink-0 ${
                                                    action.status === "completed"
                                                        ? "bg-emerald-50 text-emerald-700 border-emerald-200"
                                                        : action.status === "in_progress"
                                                          ? "bg-blue-50 text-blue-700 border-blue-200"
                                                          : action.status === "cancelled"
                                                            ? "bg-gray-100 text-gray-700 border-gray-300"
                                                            : "bg-amber-50 text-amber-700 border-amber-200"
                                                }`}>{action.status}</span>
                                            </div>
                                            <p class="text-[10px] text-gray-500 mt-0.5 leading-relaxed">{action.description}</p>
                                        </div>
                                    </div>
                                {/each}
                            </div>
                        </div>
                    {/if}
                </div>

                <!-- Suggested Actions and Matched Evidence Workspace -->
                <div class="flex-1 overflow-y-auto p-5 space-y-5">
                    <!-- Recommendation Widget -->
                    {#if recommendation}
                        <div
                            class={`p-4 rounded-lg border shadow-sm transition-all duration-300 ${
                                recommendation.type === "success"
                                    ? "bg-emerald-50 border-emerald-200 text-emerald-900"
                                    : "bg-amber-50 border-amber-200 text-amber-900"
                            }`}
                        >
                            <div
                                class="flex flex-col sm:flex-row sm:items-center justify-between gap-4"
                            >
                                <div class="space-y-1">
                                    <h4
                                        class="font-bold text-sm flex items-center gap-1.5"
                                    >
                                        {recommendation.title}
                                    </h4>
                                    <p
                                        class="text-xs opacity-90 leading-relaxed"
                                    >
                                        {recommendation.message}
                                    </p>
                                </div>
                                <button
                                    onclick={() =>
                                        handleUpdateStatus(
                                            selectedAlert.id,
                                            recommendation.targetStatus,
                                            recommendation.targetSeverity,
                                        )}
                                    class={`shrink-0 px-4 py-2 text-xs font-bold rounded shadow-xs transition-all hover:scale-102 active:scale-98 cursor-pointer ${
                                        recommendation.type === "success"
                                            ? "bg-emerald-600 text-white hover:bg-emerald-700 border border-emerald-700"
                                            : "bg-amber-600 text-white hover:bg-amber-700 border border-amber-700"
                                    }`}
                                >
                                    {recommendation.applyText}
                                </button>
                            </div>
                        </div>
                    {/if}

                    <!-- Evidence News Stream -->
                    <div class="space-y-4">
                        <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-3 border-b border-gray-200 pb-2">
                            <div class="flex gap-4">
                                <button
                                    onclick={() => activeNewsTab = "related"}
                                    class={`pb-2 px-1 border-b-2 font-bold text-xs uppercase tracking-wider transition-colors cursor-pointer ${
                                        activeNewsTab === "related"
                                            ? "border-blue-500 text-blue-600"
                                            : "border-transparent text-gray-400 hover:text-gray-600 hover:border-gray-300"
                                    }`}
                                >
                                    📰 Related News ({relatedNews.length})
                                </button>
                                <button
                                    onclick={() => activeNewsTab = "recent"}
                                    class={`pb-2 px-1 border-b-2 font-bold text-xs uppercase tracking-wider transition-colors cursor-pointer ${
                                        activeNewsTab === "recent"
                                            ? "border-blue-500 text-blue-600"
                                            : "border-transparent text-gray-400 hover:text-gray-600 hover:border-gray-300"
                                    }`}
                                >
                                    🕒 All Recent News ({recentNews.length})
                                </button>
                            </div>
                            {#if activeNewsTab === "related" && relatedNews.length > 0}
                                <span
                                    class="text-[9px] text-blue-700 font-semibold bg-blue-50 border border-blue-100 px-2 py-0.5 rounded-full self-start sm:self-center"
                                >
                                    Correlated by Location & Content
                                </span>
                            {/if}
                        </div>

                        {#if activeNewsTab === "related" && relatedNews.length === 0}
                            <!-- Fallback message for related news -->
                            <div class="bg-amber-50 border border-amber-200 rounded-lg p-4 text-amber-900 text-xs flex flex-col gap-2">
                                <div class="flex items-center gap-2 font-bold">
                                    <span>🔍</span>
                                    <span>No matching news reports found for this alert.</span>
                                </div>
                                <p class="opacity-90 leading-relaxed">
                                    We couldn't find news reports matching this alert's geography (e.g., area tags) or fire keywords. Showing all recent news reports below:
                                </p>
                            </div>
                        {/if}

                        {#if displayedNews.length === 0}
                            <div
                                class="bg-white rounded-lg border border-gray-200 p-8 text-center shadow-2xs"
                            >
                                <div class="text-3xl mb-2">📰</div>
                                <h4 class="text-sm font-bold text-gray-700">
                                    No news reports found
                                </h4>
                            </div>
                        {:else}
                            <div class="space-y-4">
                                {#each displayedNews as entry, i (entry.id)}
                                    {#if entry.isRecentOnly && (i === 0 || !displayedNews[i - 1].isRecentOnly)}
                                        <div class="pt-4 pb-2 border-t border-dashed border-gray-300 mt-6">
                                            <h4 class="text-xs font-bold uppercase tracking-wider text-gray-400 flex items-center gap-2">
                                                🕒 Other Recent News Reports
                                            </h4>
                                            <p class="text-[10px] text-gray-400">Showing more recent updates to help with investigation</p>
                                        </div>
                                    {/if}

                                    <article
                                        class="bg-white rounded-lg border border-gray-200/80 p-4 shadow-2xs relative overflow-hidden flex flex-col gap-3 hover:shadow-xs transition-shadow"
                                    >
                                        <!-- Top source & match status indicators -->
                                        <div
                                            class="flex justify-between items-center text-[10px]"
                                        >
                                            <div
                                                class="flex items-center gap-2"
                                            >
                                                <span
                                                    class="bg-blue-100 text-blue-800 text-[10px] font-bold px-2 py-0.5 rounded"
                                                >
                                                    {entry.source_name}
                                                </span>
                                                <span class="text-gray-400"
                                                    >{entry.publication_date}</span
                                                >
                                            </div>

                                            <div
                                                class="flex items-center gap-1"
                                            >
                                                {#if entry.score > 0}
                                                    <span
                                                        class="text-gray-400 text-[9px]"
                                                        >Match score:</span
                                                    >
                                                    <span
                                                        class="font-bold text-blue-600 bg-blue-50 px-1.5 py-0.2 rounded border border-blue-100"
                                                    >
                                                        {entry.score}
                                                    </span>
                                                {:else}
                                                    <span class="text-[9px] text-gray-400 font-semibold bg-gray-100 px-1.5 py-0.5 rounded border border-gray-200/30">
                                                        Recent
                                                    </span>
                                                {/if}
                                            </div>
                                        </div>

                                        <!-- Title -->
                                        <a
                                            href={entry.source_link}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            class="font-bold text-sm text-blue-700 hover:underline leading-snug"
                                        >
                                            {entry.title}
                                        </a>

                                        <!-- Summary content -->
                                        <p
                                            class="text-xs text-gray-600 leading-relaxed"
                                        >
                                            {entry.summary}
                                        </p>

                                        <!-- Tags & Attributes row -->
                                        <div
                                            class="flex flex-wrap items-center justify-between gap-3 pt-2.5 border-t border-gray-100"
                                        >
                                            <!-- Matched tags -->
                                            <div
                                                class="flex flex-wrap gap-1 text-[9px]"
                                            >
                                                {#each entry.area_tags as tag}
                                                    <span
                                                        class={`rounded px-1.5 py-0.5 font-medium ${
                                                            entry.matchedTags && entry.matchedTags.includes(
                                                                tag,
                                                            )
                                                                ? "bg-green-100 text-green-800 font-bold border border-green-200/60"
                                                                : "bg-gray-100 text-gray-500 border border-gray-200/20"
                                                        }`}
                                                    >
                                                        {tag}
                                                    </span>
                                                {/each}
                                            </div>

                                            <!-- Reported Status and Fire metrics -->
                                            <div
                                                class="flex items-center gap-1.5"
                                            >
                                                {#if entry.hectares_reported}
                                                    <span
                                                        class="text-[9px] text-gray-600 font-medium bg-gray-100 border border-gray-200 px-1.5 py-0.5 rounded"
                                                    >
                                                        🔥 {entry.hectares_reported.toLocaleString()}
                                                        ha
                                                    </span>
                                                {/if}
                                                {#if entry.fire_status_reported}
                                                    <span
                                                        class={`text-[9px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full border ${
                                                            [
                                                                "activo",
                                                                "sin control",
                                                            ].includes(
                                                                entry.fire_status_reported.toLowerCase(),
                                                            )
                                                                ? "bg-red-50 text-red-700 border-red-200"
                                                                : [
                                                                        "estabilizado",
                                                                        "controlado",
                                                                    ].includes(
                                                                        entry.fire_status_reported.toLowerCase(),
                                                                    )
                                                                  ? "bg-amber-50 text-amber-700 border-amber-200"
                                                                  : "bg-green-50 text-green-700 border-green-200"
                                                        }`}
                                                    >
                                                        {entry.fire_status_reported}
                                                    </span>
                                                {/if}
                                            </div>
                                        </div>
                                    </article>
                                {/each}
                            </div>
                        {/if}
                    </div>
                </div>
            {:else}
                <!-- Default empty state (shown if no alerts) -->
                <div
                    class="flex-1 flex flex-col items-center justify-center p-12 text-center text-gray-500"
                >
                    <span class="text-4xl mb-4">👈</span>
                    <h3 class="text-base font-bold text-gray-800">
                        Select an alert for investigation
                    </h3>
                    <p
                        class="text-xs text-gray-400 max-w-sm mt-1 leading-relaxed"
                    >
                        Choose an alert from the left panel. The correlation
                        engine will find matching local news articles, compute
                        scores, and recommend action paths.
                    </p>
                </div>
            {/if}
        </section>
    </div>
</div>
