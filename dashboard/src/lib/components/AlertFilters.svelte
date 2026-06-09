<script>
    let { 
        searchQuery = $bindable(""), 
        statusFilter = $bindable("all"),
        excludeResolved = false,
        onSearchChange,
        onStatusChange
    } = $props();

    function handleSearchInput(e) {
        const value = e.target.value;
        searchQuery = value;
        if (onSearchChange) {
            onSearchChange(value);
        }
    }

    function selectStatus(id) {
        statusFilter = id;
        if (onStatusChange) {
            onStatusChange(id);
        }
    }

    const tabs = $derived.by(() => {
        const list = [
            { id: "all", label: "All" }, 
            { id: "active", label: "Unconfirmed" }, 
            { id: "acknowledged", label: "Confirmed" }
        ];
        if (!excludeResolved) {
            list.push({ id: "resolved", label: "Resolved" });
        }
        return list;
    });
</script>

<div class="space-y-3 shrink-0">
    <!-- Search input -->
    <div class="relative">
        <input
            type="text"
            value={searchQuery}
            oninput={handleSearchInput}
            placeholder="Search alerts by title, description..."
            class="w-full text-sm pl-9 pr-3 py-2 border border-gray-300 rounded-md focus:outline-hidden focus:ring-1 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-900"
        />
        <span class="absolute left-3 top-2.5 text-gray-400 text-xs">🔍</span>
    </div>

    <!-- Status Tabs -->
    <div class="flex gap-1 p-1 bg-gray-100 rounded-md text-xs">
        {#each tabs as tab (tab.id)}
            <button
                type="button"
                onclick={() => selectStatus(tab.id)}
                class={`flex-1 py-1.5 font-medium rounded-sm transition-all cursor-pointer text-center ${
                    statusFilter === tab.id
                        ? "bg-white text-gray-900 shadow-xs border border-gray-200/50"
                        : "text-gray-500 hover:text-gray-800"
                }`}
            >
                {tab.label}
            </button>
        {/each}
    </div>
</div>
