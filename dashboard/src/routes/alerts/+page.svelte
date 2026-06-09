<script>
    import { alertsStore } from "$lib/stores/alerts.svelte";
    import AlertModal from "$lib/components/AlertModal.svelte";
    import TraceModal from "$lib/components/TraceModal.svelte";
    import AlertFilters from "$lib/components/AlertFilters.svelte";

    const { data } = $props();

    // Sync SvelteKit's initial server load data into our Svelte 5 store
    $effect(() => {
        alertsStore.init(data.alerts, data.api_url);
    });

    // Reactive filter states
    let searchQuery = $state("");
    let statusFilter = $state("all");

    // Directly bind to Svelte 5 class state properties and sort most recent first
    let filteredAlerts = $derived.by(() => {
        let items = [...alertsStore.items];
        
        if (statusFilter !== "all") {
            items = items.filter(a => a.status === statusFilter);
        }
        
        if (searchQuery.trim()) {
            const query = searchQuery.toLowerCase();
            items = items.filter(a => 
                a.title.toLowerCase().includes(query) || 
                a.description.toLowerCase().includes(query)
            );
        }

        return items.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    });

    let loading = $derived(alertsStore.loading);
    let apiError = $derived(alertsStore.error);
    let api_url = $derived(alertsStore.apiUrl);

    // Modal state
    let isModalOpen = $state(false);
    let selectedAlert = $state(null);

    // Trace Modal state
    let isTraceModalOpen = $state(false);
    let traceAlert = $state(null);

    function openCreateModal() {
        selectedAlert = null;
        isModalOpen = true;
    }

    function openEditModal(alert) {
        selectedAlert = alert;
        isModalOpen = true;
    }

    function closeModal() {
        isModalOpen = false;
        selectedAlert = null;
    }

    function openTraceModal(alert) {
        traceAlert = alert;
        isTraceModalOpen = true;
    }

    function closeTraceModal() {
        isTraceModalOpen = false;
        traceAlert = null;
    }

    async function handleSave(alertData) {
        try {
            if (selectedAlert) {
                // Edit mode
                await alertsStore.update(selectedAlert.id, alertData);
            } else {
                // Create mode
                await alertsStore.create(alertData);
            }
            closeModal();
        } catch (err) {
            console.error("Save failed:", err);
        }
    }

    async function handleDelete(alertId) {
        if (!confirm("Are you sure you want to delete this alert?")) {
            return;
        }
        try {
            await alertsStore.delete(alertId);
        } catch (err) {
            console.error("Delete failed:", err);
        }
    }

    async function handleResolve(alertId) {
        try {
            await alertsStore.update(alertId, { status: "resolved", severity: "info" });
        } catch (err) {
            console.error("Resolve failed:", err);
        }
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

<div class="flex-1 overflow-y-auto bg-gray-50/50 p-6 min-h-0">
    <div class="w-full space-y-6">
        <!-- Header -->
        <header class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-lg border border-gray-200/80 shadow-xs">
            <div>
                <h1 class="text-3xl font-bold text-gray-900 flex items-center gap-2">
                    🔔 Alerts Control Center
                </h1>
                <p class="text-sm text-gray-500 mt-1">
                    Monitor, update, and manage active environmental alerts and critical notifications.
                </p>
            </div>
            <button
                onclick={openCreateModal}
                disabled={loading}
                class="px-5 py-2.5 text-sm font-semibold text-white bg-blue-600 rounded-md hover:bg-blue-700 active:bg-blue-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-xs flex items-center gap-2 cursor-pointer"
            >
                <span>+</span> Create Alert
            </button>
        </header>

        <!-- Filters Block -->
        <div class="bg-white p-4 rounded-lg border border-gray-200/80 shadow-xs">
            <AlertFilters 
                bind:searchQuery={searchQuery}
                bind:statusFilter={statusFilter}
            />
        </div>

        {#if apiError}
            <div class="bg-red-50 border-l-4 border-red-500 p-4 rounded-md shadow-xs flex items-center justify-between">
                <div class="flex items-center gap-2">
                    <span class="text-red-500 text-lg">⚠️</span>
                    <p class="text-sm font-medium text-red-800">{apiError}</p>
                </div>
                <button onclick={() => alertsStore.clearError()} class="text-red-400 hover:text-red-600 transition-colors text-sm cursor-pointer">
                    Dismiss
                </button>
            </div>
        {/if}

        <!-- Alerts Content -->
        {#if loading && filteredAlerts.length === 0}
            <div class="text-center py-12">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                <p class="text-sm text-gray-500 mt-2">Loading alerts...</p>
            </div>
        {:else if filteredAlerts.length === 0}
            <div class="bg-white rounded-lg border border-gray-200 p-12 text-center shadow-xs">
                <div class="text-gray-300 text-5xl mb-4">📭</div>
                <h3 class="text-lg font-semibold text-gray-700">No alerts found</h3>
                <p class="text-sm text-gray-500 max-w-sm mx-auto mt-1">
                    There are currently no environmental alerts matching your criteria.
                </p>
            </div>
        {:else}
            <div class="grid gap-4">
                {#each filteredAlerts as alert (alert.id)}
                    <article
                        class="bg-white rounded-lg border border-gray-200 shadow-xs hover:shadow-md transition-shadow flex flex-col md:flex-row md:items-stretch overflow-hidden"
                    >
                        <!-- Severity Colored Bar -->
                        <div
                            class={`w-full md:w-1.5 h-1.5 md:h-auto shrink-0 ${
                                alert.severity === 'critical'
                                    ? 'bg-red-500'
                                    : alert.severity === 'warning'
                                      ? 'bg-amber-500'
                                      : 'bg-blue-500'
                            }`}
                        ></div>

                        <!-- Content Area -->
                        <div class="p-5 flex-1 flex flex-col justify-between gap-4">
                            <div>
                                <div class="flex flex-wrap items-center justify-between gap-3 mb-2">
                                    <div class="flex items-center gap-2 flex-wrap">
                                        <h2 class="text-lg font-bold text-gray-900 leading-tight">
                                            {alert.title}
                                        </h2>
                                        
                                        <!-- Severity tag -->
                                        <span
                                            class={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full border ${
                                                alert.severity === 'critical'
                                                    ? 'bg-red-50 text-red-700 border-red-200'
                                                    : alert.severity === 'warning'
                                                      ? 'bg-amber-50 text-amber-700 border-amber-200'
                                                      : 'bg-blue-50 text-blue-700 border-blue-200'
                                            }`}
                                        >
                                            {alert.severity}
                                        </span>

                                        <!-- Status tag -->
                                        <span
                                            class={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full border ${
                                                alert.status === 'active'
                                                    ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                                                    : alert.status === 'acknowledged'
                                                      ? 'bg-indigo-50 text-indigo-700 border-indigo-200'
                                                      : 'bg-gray-100 text-gray-700 border-gray-300'
                                            }`}
                                        >
                                            {alert.status}
                                        </span>
                                    </div>

                                    {#if alert.latitude !== null && alert.longitude !== null}
                                        <div class="flex items-center gap-1 text-xs text-gray-500 font-medium bg-gray-50 px-2.5 py-1 rounded border border-gray-200/60">
                                            <span>📍</span>
                                            <span>{alert.latitude.toFixed(4)}, {alert.longitude.toFixed(4)}</span>
                                        </div>
                                    {/if}
                                    {#if (alert.affected_roads_count !== undefined && alert.affected_roads_count !== null) || (alert.affected_buildings_count !== undefined && alert.affected_buildings_count !== null) || (alert.affected_amenities_count !== undefined && alert.affected_amenities_count !== null) || (alert.affected_population !== undefined && alert.affected_population !== null)}
                                        <div class="flex items-center gap-4 text-xs text-gray-500 font-medium bg-gray-50 px-3.5 py-1 rounded border border-gray-200/60">
                                            <span class="text-[9px] font-bold text-gray-400 uppercase tracking-wider">Affected in Buffer:</span>
                                            <div class="flex items-center gap-1.5" title="Number of Affected Roads">
                                                <span>🛣️</span> <span>Number of Affected Roads: <strong class="text-blue-600 font-extrabold">{alert.affected_roads_count ?? 0}</strong></span>
                                            </div>
                                            <div class="flex items-center gap-1.5" title="Number of Affected Buildings">
                                                <span>🏢</span> <span>Number of Affected Buildings: <strong class="text-amber-600 font-extrabold">{alert.affected_buildings_count ?? 0}</strong></span>
                                            </div>
                                            <div class="flex items-center gap-1.5" title="Number of Affected Amenities">
                                                <span>🏥</span> <span>Number of Affected Amenities: <strong class="text-purple-600 font-extrabold">{alert.affected_amenities_count ?? 0}</strong></span>
                                            </div>
                                            <div class="flex items-center gap-1.5" title="Amount of Affected Population">
                                                <span>👥</span> <span>Amount of Affected Population: <strong class="text-emerald-600 font-extrabold">{alert.affected_population ?? 0}</strong></span>
                                            </div>
                                        </div>
                                    {/if}
                                </div>

                                <p class="text-gray-700 text-sm leading-relaxed whitespace-pre-line">
                                    {alert.description}
                                </p>
                            </div>

                            <!-- Footer & Actions -->
                            <footer class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pt-3 border-t border-gray-100/80">
                                <div class="flex flex-wrap gap-x-4 gap-y-1 text-xs text-gray-400">
                                    <span>
                                        <strong>Created:</strong> {formatDate(alert.created_at)}
                                    </span>
                                    {#if alert.updated_at !== alert.created_at}
                                        <span>•</span>
                                        <span>
                                            <strong>Updated:</strong> {formatDate(alert.updated_at)}
                                        </span>
                                    {/if}
                                </div>

                                <div class="flex items-center gap-2 self-end sm:self-auto">
                                    <button
                                        onclick={() => openTraceModal(alert)}
                                        class="px-3 py-1.5 text-xs font-semibold text-blue-600 bg-white border border-blue-200 rounded hover:bg-blue-50 hover:border-blue-300 transition-all cursor-pointer mr-1"
                                    >
                                        🔍 Trace
                                    </button>
                                    {#if alert.status !== 'resolved'}
                                        <button
                                            onclick={() => handleResolve(alert.id)}
                                            disabled={loading}
                                            class="px-3 py-1.5 text-xs font-semibold text-green-600 bg-white border border-green-200 rounded hover:bg-green-50 hover:border-green-300 disabled:opacity-50 disabled:cursor-not-allowed transition-all cursor-pointer mr-1"
                                        >
                                            Resolve
                                        </button>
                                    {/if}
                                    <button
                                        onclick={() => openEditModal(alert)}
                                        disabled={loading}
                                        class="px-3 py-1.5 text-xs font-semibold text-gray-700 bg-white border border-gray-300 rounded hover:bg-gray-50 hover:text-blue-600 hover:border-blue-300 disabled:opacity-50 disabled:cursor-not-allowed transition-all cursor-pointer"
                                    >
                                        Edit
                                    </button>
                                    <button
                                        onclick={() => handleDelete(alert.id)}
                                        disabled={loading}
                                        class="px-3 py-1.5 text-xs font-semibold text-red-600 bg-white border border-red-200 rounded hover:bg-red-50 hover:border-red-300 disabled:opacity-50 disabled:cursor-not-allowed transition-all cursor-pointer"
                                    >
                                        Delete
                                    </button>
                                </div>
                            </footer>
                        </div>
                    </article>
                {/each}
            </div>
        {/if}
    </div>
</div>

<AlertModal
    isOpen={isModalOpen}
    alert={selectedAlert}
    apiUrl={api_url}
    onClose={closeModal}
    onSave={handleSave}
/>

<TraceModal
    isOpen={isTraceModalOpen}
    alert={traceAlert}
    onClose={closeTraceModal}
/>
