<script>
    import { actStore } from "$lib/stores/act.svelte";
    import { actionsStore } from "$lib/stores/actions.svelte";
    import { alertsStore } from "$lib/stores/alerts.svelte";
    import { untrack } from "svelte";
    import ActionModal from "$lib/components/ActionModal.svelte";
    import ActionTraceModal from "$lib/components/ActionTraceModal.svelte";

    const { data } = $props();

    // Sync SvelteKit's initial server load data into our stores
    $effect(() => {
        const { alerts, actions, predefined, api_url } = data;
        untrack(() => {
            actStore.init(alerts, actions, predefined, api_url);
        });
    });

    // Reactive bindings to store properties
    let confirmedAlerts = $derived(actStore.confirmedAlerts);
    let selectedAlert = $derived(actStore.selectedAlert);
    let relatedActions = $derived(actStore.relatedActions);
    let selectedAlertId = $derived(actStore.selectedAlertId);
    let alertSearchQuery = $derived(actStore.alertSearchQuery);

    let loading = $derived(actionsStore.loading || alertsStore.loading);
    let apiError = $derived(actionsStore.error || alertsStore.error);
    let api_url = $derived(actionsStore.apiUrl);
    let predefinedActions = $derived(actionsStore.predefined);

    // Modal state
    let isModalOpen = $state(false);
    let selectedAction = $state(null);

    // Trace Modal state
    let isTraceModalOpen = $state(false);
    let traceAction = $state(null);

    function handleSelectAlert(id) {
        actStore.setSelectedAlertId(id);
    }

    function handleSearchInput(e) {
        actStore.setSearchQuery(e.target.value);
    }

    function openCreateActionModal() {
        selectedAction = null;
        isModalOpen = true;
    }

    function openEditActionModal(action) {
        selectedAction = action;
        isModalOpen = true;
    }

    function closeModal() {
        isModalOpen = false;
        selectedAction = null;
    }

    function openTraceModal(action) {
        traceAction = action;
        isTraceModalOpen = true;
    }

    function closeTraceModal() {
        isTraceModalOpen = false;
        traceAction = null;
    }

    async function handleSaveAction(actionData) {
        try {
            if (selectedAction) {
                // Edit mode
                await actionsStore.update(selectedAction.id, actionData);
            } else {
                // Create mode
                await actionsStore.create(actionData);
            }
            closeModal();
        } catch (err) {
            console.error("Save action failed:", err);
        }
    }

    async function handleDeleteAction(actionId) {
        if (!confirm("Are you sure you want to delete this response action?")) {
            return;
        }
        try {
            await actionsStore.delete(actionId);
        } catch (err) {
            console.error("Delete action failed:", err);
        }
    }

    async function handleUpdateStatus(actionId, newStatus) {
        try {
            await actionsStore.update(actionId, { status: newStatus });
        } catch (err) {
            console.error("Status update failed:", err);
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

<div class="flex-1 flex flex-col min-h-0 bg-gray-50/50">
    <!-- Main Dual-Pane Workspace -->
    <div
        class="flex-1 grid grid-cols-1 lg:grid-cols-12 min-h-0 divide-y lg:divide-y-0 lg:divide-x divide-gray-200"
    >
        <!-- ================= LEFT PANEL: CONFIRMED ALERTS FEED (5 cols) ================= -->
        <section class="lg:col-span-5 flex flex-col min-h-0 bg-white">
            <!-- Search Header -->
            <div class="p-4 border-b border-gray-200 space-y-3 shrink-0">
                <div class="flex items-center justify-between">
                    <h2
                        class="text-lg font-bold text-gray-900 flex items-center gap-2"
                    >
                        <span>🚀 Actions</span>
                    </h2>
                    <span
                        class="text-xs bg-blue-100 text-blue-700 font-bold px-2 py-0.5 rounded-full"
                    >
                        {confirmedAlerts.length} Confirmed
                    </span>
                </div>

                <!-- Custom Search Bar -->
                <div class="relative">
                    <input
                        type="text"
                        value={alertSearchQuery}
                        oninput={handleSearchInput}
                        placeholder="Search confirmed alerts..."
                        class="w-full text-sm pl-9 pr-3 py-2 border border-gray-300 rounded-md focus:outline-hidden focus:ring-1 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-900"
                    />
                    <span class="absolute left-3 top-2.5 text-gray-400 text-xs"
                        >🔍</span
                    >
                </div>
            </div>

            <!-- Scrollable Alerts Feed -->
            <div class="flex-1 overflow-y-auto p-4 space-y-3">
                {#if confirmedAlerts.length === 0}
                    <div
                        class="text-center py-12 border-2 border-dashed border-gray-200 rounded-lg"
                    >
                        <p class="text-sm text-gray-400">
                            No confirmed alerts found.
                        </p>
                        <p class="text-xs text-gray-400 mt-1">
                            Go to the <a
                                href="/confirm"
                                class="text-blue-600 font-semibold hover:underline"
                                >Confirm</a
                            > page to verify and acknowledge active alerts.
                        </p>
                    </div>
                {:else}
                    {#each confirmedAlerts as alert (alert.id)}
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

                            <!-- Affected Row in act sidebar -->
                            {#if (alert.affected_roads_count !== undefined && alert.affected_roads_count !== null) || (alert.affected_buildings_count !== undefined && alert.affected_buildings_count !== null) || (alert.affected_amenities_count !== undefined && alert.affected_amenities_count !== null) || (alert.affected_population !== undefined && alert.affected_population !== null)}
                                <div
                                    class="mt-1 pt-1.5 border-t border-gray-100 flex items-center justify-between text-[10px] text-gray-500 font-medium bg-gray-50 px-2 py-1 rounded border border-gray-150/40"
                                >
                                    <div
                                        class="flex items-center gap-1.5"
                                        title="Number of Affected Roads"
                                    >
                                        <span>🛣️</span>
                                        <span class="font-bold text-blue-600"
                                            >{alert.affected_roads_count ??
                                                0}</span
                                        >
                                    </div>
                                    <div
                                        class="flex items-center gap-1.5"
                                        title="Number of Affected Buildings"
                                    >
                                        <span>🏢</span>
                                        <span class="font-bold text-amber-600"
                                            >{alert.affected_buildings_count ??
                                                0}</span
                                        >
                                    </div>
                                    <div
                                        class="flex items-center gap-1.5"
                                        title="Number of Affected Amenities"
                                    >
                                        <span>🏥</span>
                                        <span class="font-bold text-purple-600"
                                            >{alert.affected_amenities_count ??
                                                0}</span
                                        >
                                    </div>
                                    <div
                                        class="flex items-center gap-1.5"
                                        title="Amount of Affected Population"
                                    >
                                        <span>👥</span>
                                        <span class="font-bold text-emerald-600"
                                            >{alert.affected_population ??
                                                0}</span
                                        >
                                    </div>
                                </div>
                            {/if}

                            <!-- Bottom stats -->
                            <div
                                class="flex justify-between items-center text-[10px] text-gray-400 mt-1 pt-2 border-t border-gray-100"
                            >
                                <div class="flex items-center gap-1.5">
                                    <!-- Status tag (Will always be acknowledged / confirmed) -->
                                    <span
                                        class="font-semibold uppercase px-1.5 py-0.5 rounded text-[9px] bg-blue-100 text-blue-800"
                                    >
                                        Confirmed
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

        <!-- ================= RIGHT PANEL: ACTIONS WORKSPACE (7 cols) ================= -->
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
                            <span class="text-xl">📢</span>
                            <span
                                class="text-xs font-semibold text-gray-400 uppercase tracking-widest"
                                >Active Incident Command</span
                            >
                        </div>
                        <span
                            class="text-xs font-bold uppercase px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200"
                        >
                            Verified Alert
                        </span>
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
                        <div
                            class="mt-3 p-3 bg-slate-50 border border-slate-200 rounded-lg flex flex-col gap-2"
                        >
                            <h3
                                class="text-xs font-bold text-slate-700 uppercase tracking-wider"
                            >
                                Affected in 1km Buffer
                            </h3>
                            <div
                                class="grid grid-cols-2 sm:grid-cols-4 gap-2.5"
                            >
                                {#if selectedAlert.affected_roads_count !== undefined && selectedAlert.affected_roads_count !== null}
                                    <div
                                        class="bg-white p-2 rounded border border-slate-100 flex flex-col gap-0.5"
                                    >
                                        <span
                                            class="text-[10px] text-gray-400 font-semibold uppercase"
                                            >🛣️ Number of Affected Roads</span
                                        >
                                        <span
                                            class="text-sm font-extrabold text-blue-600"
                                            >{selectedAlert.affected_roads_count}</span
                                        >
                                    </div>
                                {/if}
                                {#if selectedAlert.affected_buildings_count !== undefined && selectedAlert.affected_buildings_count !== null}
                                    <div
                                        class="bg-white p-2 rounded border border-slate-100 flex flex-col gap-0.5"
                                    >
                                        <span
                                            class="text-[10px] text-gray-400 font-semibold uppercase"
                                            >🏢 Number of Affected Buildings</span
                                        >
                                        <span
                                            class="text-sm font-extrabold text-amber-600"
                                            >{selectedAlert.affected_buildings_count}</span
                                        >
                                    </div>
                                {/if}
                                {#if selectedAlert.affected_amenities_count !== undefined && selectedAlert.affected_amenities_count !== null}
                                    <div
                                        class="bg-white p-2 rounded border border-slate-100 flex flex-col gap-0.5"
                                    >
                                        <span
                                            class="text-[10px] text-gray-400 font-semibold uppercase"
                                            >🏥 Number of Affected Amenities</span
                                        >
                                        <span
                                            class="text-sm font-extrabold text-purple-600"
                                            >{selectedAlert.affected_amenities_count}</span
                                        >
                                    </div>
                                {/if}
                                {#if selectedAlert.affected_population !== undefined && selectedAlert.affected_population !== null}
                                    <div
                                        class="bg-white p-2 rounded border border-slate-100 flex flex-col gap-0.5"
                                    >
                                        <span
                                            class="text-[10px] text-gray-400 font-semibold uppercase"
                                            >👥 Amount of Affected Population</span
                                        >
                                        <span
                                            class="text-sm font-extrabold text-emerald-600"
                                            >{selectedAlert.affected_population}</span
                                        >
                                    </div>
                                {/if}
                            </div>
                        </div>
                    {/if}
                </div>

                <!-- Response Plan Actions Feed -->
                <div class="flex-1 overflow-y-auto p-5 space-y-5">
                    {#if apiError}
                        <div
                            class="bg-red-50 border-l-4 border-red-500 p-4 rounded-md shadow-xs flex items-center justify-between"
                        >
                            <div class="flex items-center gap-2">
                                <span class="text-red-500 text-lg">⚠️</span>
                                <p class="text-sm font-medium text-red-800">
                                    {apiError}
                                </p>
                            </div>
                            <button
                                onclick={() => actionsStore.clearError()}
                                class="text-red-400 hover:text-red-600 transition-colors text-sm cursor-pointer"
                            >
                                Dismiss
                            </button>
                        </div>
                    {/if}

                    <div class="space-y-4">
                        <div class="flex justify-between items-center">
                            <div>
                                <h3
                                    class="font-bold text-xs uppercase tracking-wider text-gray-400 flex items-center gap-2"
                                >
                                    📋 Incident Response Plan ({relatedActions.length})
                                </h3>
                                <p class="text-[10px] text-gray-400 mt-0.5">
                                    Deploy, track, and record field
                                    countermeasures for this specific alert.
                                </p>
                            </div>
                            <button
                                onclick={openCreateActionModal}
                                disabled={loading}
                                class="px-3.5 py-1.5 text-xs font-bold text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-xs flex items-center gap-1.5 cursor-pointer"
                            >
                                <span>+</span> Create Action
                            </button>
                        </div>

                        {#if relatedActions.length === 0}
                            <div
                                class="bg-white rounded-lg border border-gray-200 p-12 text-center shadow-2xs"
                            >
                                <div class="text-4xl mb-3">🛠️</div>
                                <h4 class="text-sm font-bold text-gray-700">
                                    No response actions scheduled
                                </h4>
                                <p
                                    class="text-xs text-gray-400 max-w-sm mx-auto mt-1 leading-relaxed"
                                >
                                    No actions have been planned for this
                                    verified alert yet. Click "Create Action" to
                                    schedule predefined templates or custom
                                    tasks.
                                </p>
                            </div>
                        {:else}
                            <div class="space-y-4">
                                {#each relatedActions as action (action.id)}
                                    <article
                                        class="bg-white rounded-lg border border-gray-200 p-4 shadow-2xs flex flex-col gap-3 hover:shadow-xs transition-shadow"
                                    >
                                        <!-- Source and Status indicators -->
                                        <div
                                            class="flex justify-between items-center"
                                        >
                                            <div
                                                class="flex items-center gap-2"
                                            >
                                                {#if action.predefined_id}
                                                    <span
                                                        class="bg-blue-50 text-blue-700 text-[9px] font-bold px-2 py-0.5 rounded-full border border-blue-100"
                                                    >
                                                        Template Action
                                                    </span>
                                                {:else}
                                                    <span
                                                        class="bg-purple-50 text-purple-700 text-[9px] font-bold px-2 py-0.5 rounded-full border border-purple-100"
                                                    >
                                                        Custom Action
                                                    </span>
                                                {/if}
                                                <span
                                                    class="text-gray-400 text-[9px] font-mono"
                                                >
                                                    {formatDate(
                                                        action.created_at,
                                                    )}
                                                </span>
                                            </div>

                                            <!-- Status Tag -->
                                            <span
                                                class={`text-[9px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full border ${
                                                    action.status ===
                                                    "completed"
                                                        ? "bg-emerald-50 text-emerald-700 border-emerald-200"
                                                        : action.status ===
                                                            "in_progress"
                                                          ? "bg-amber-50 text-amber-700 border-amber-200"
                                                          : action.status ===
                                                              "cancelled"
                                                            ? "bg-red-50 text-red-700 border-red-200"
                                                            : "bg-gray-50 text-gray-600 border-gray-200"
                                                }`}
                                            >
                                                {action.status === "in_progress"
                                                    ? "In Progress"
                                                    : action.status}
                                            </span>
                                        </div>

                                        <!-- Title -->
                                        <h4
                                            class="font-bold text-sm text-gray-900 leading-snug"
                                        >
                                            {action.title}
                                        </h4>

                                        <!-- Description -->
                                        <p
                                            class="text-xs text-gray-600 leading-relaxed whitespace-pre-line"
                                        >
                                            {action.description}
                                        </p>

                                        <!-- Action buttons row -->
                                        <div
                                            class="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-gray-100"
                                        >
                                            <!-- Quick status transition -->
                                            <div
                                                class="flex items-center gap-1.5 text-xs text-gray-400"
                                            >
                                                <span
                                                    class="text-[9px] uppercase tracking-wider font-semibold"
                                                    >Transition Status:</span
                                                >
                                                <div class="flex gap-1">
                                                    <button
                                                        onclick={() =>
                                                            handleUpdateStatus(
                                                                action.id,
                                                                "in_progress",
                                                            )}
                                                        disabled={action.status ===
                                                            "in_progress"}
                                                        class="px-2 py-0.5 text-[9px] font-semibold border rounded cursor-pointer transition-colors border-amber-200 text-amber-700 bg-white hover:bg-amber-50 disabled:opacity-40 disabled:cursor-not-allowed"
                                                    >
                                                        Run
                                                    </button>
                                                    <button
                                                        onclick={() =>
                                                            handleUpdateStatus(
                                                                action.id,
                                                                "completed",
                                                            )}
                                                        disabled={action.status ===
                                                            "completed"}
                                                        class="px-2 py-0.5 text-[9px] font-semibold border rounded cursor-pointer transition-colors border-emerald-200 text-emerald-700 bg-white hover:bg-emerald-50 disabled:opacity-40 disabled:cursor-not-allowed"
                                                    >
                                                        Complete
                                                    </button>
                                                    <button
                                                        onclick={() =>
                                                            handleUpdateStatus(
                                                                action.id,
                                                                "cancelled",
                                                            )}
                                                        disabled={action.status ===
                                                            "cancelled"}
                                                        class="px-2 py-0.5 text-[9px] font-semibold border rounded cursor-pointer transition-colors border-red-200 text-red-700 bg-white hover:bg-red-50 disabled:opacity-40 disabled:cursor-not-allowed"
                                                    >
                                                        Cancel
                                                    </button>
                                                </div>
                                            </div>

                                            <!-- Controls (Edit, Trace, Delete) -->
                                            <div
                                                class="flex items-center gap-2"
                                            >
                                                <button
                                                    onclick={() =>
                                                        openTraceModal(action)}
                                                    class="px-2.5 py-1 text-[10px] font-semibold text-blue-600 bg-white border border-blue-200 rounded hover:bg-blue-50 transition-colors cursor-pointer"
                                                >
                                                    🔍 Trace
                                                </button>
                                                <button
                                                    onclick={() =>
                                                        openEditActionModal(
                                                            action,
                                                        )}
                                                    class="px-2.5 py-1 text-[10px] font-semibold text-gray-700 bg-white border border-gray-300 rounded hover:bg-gray-50 transition-colors cursor-pointer"
                                                >
                                                    Edit
                                                </button>
                                                <button
                                                    onclick={() =>
                                                        handleDeleteAction(
                                                            action.id,
                                                        )}
                                                    class="px-2.5 py-1 text-[10px] font-semibold text-red-600 bg-white border border-red-200 rounded hover:bg-red-50 transition-colors cursor-pointer"
                                                >
                                                    Delete
                                                </button>
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
                        Select a confirmed alert to dispatch actions
                    </h3>
                    <p
                        class="text-xs text-gray-400 max-w-sm mt-1 leading-relaxed"
                    >
                        Choose a verified alert from the left panel. From here,
                        you can execute predefined contingency actions, modify
                        state transitions, and track execution traces.
                    </p>
                </div>
            {/if}
        </section>
    </div>
</div>

<ActionModal
    isOpen={isModalOpen}
    action={selectedAction}
    alertId={selectedAlertId}
    apiUrl={api_url}
    {predefinedActions}
    onClose={closeModal}
    onSave={handleSaveAction}
/>

<ActionTraceModal
    isOpen={isTraceModalOpen}
    action={traceAction}
    onClose={closeTraceModal}
/>
