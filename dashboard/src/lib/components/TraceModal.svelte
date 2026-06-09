<script>
    let { isOpen, alert, onClose } = $props();

    function formatDate(isoString) {
        try {
            const date = new Date(isoString);
            return date.toLocaleString();
        } catch {
            return isoString;
        }
    }

    // Sort trace logs descending by timestamp (most recent at the top)
    let sortedTrace = $derived(
        alert && alert.trace
            ? [...alert.trace].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
            : []
    );
</script>

{#if isOpen && alert}
    <!-- Backdrop -->
    <div
        class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4 backdrop-blur-xs"
        onclick={onClose}
        role="button"
        tabindex="-1"
        onkeydown={(e) => e.key === 'Escape' && onClose()}
    >
        <!-- Modal Container -->
        <div
            class="bg-white rounded-lg shadow-xl w-full max-w-2xl overflow-hidden flex flex-col max-h-[85vh]"
            onclick={(e) => e.stopPropagation()}
            role="dialog"
            aria-modal="true"
        >
            <!-- Header -->
            <header class="bg-gray-50 px-6 py-4 border-b border-gray-200 flex items-center justify-between">
                <div>
                    <h2 class="text-xl font-bold text-gray-900">
                        🔍 Audit Trace Log
                    </h2>
                    <p class="text-xs text-gray-500 mt-0.5">
                        Track changes, modifications, and chronological history of alert: <span class="font-semibold text-gray-700">{alert.title}</span>
                    </p>
                </div>
                <button
                    class="text-gray-400 hover:text-gray-600 transition-colors text-2xl font-light cursor-pointer"
                    onclick={onClose}
                    aria-label="Close modal"
                >
                    &times;
                </button>
            </header>

            <!-- Body -->
            <div class="flex-1 overflow-y-auto p-6 space-y-6">
                {#if sortedTrace.length === 0}
                    <div class="text-center py-8 text-gray-500 text-sm">
                        No trace entries found for this alert.
                    </div>
                {:else}
                    <div class="relative border-l-2 border-gray-200 ml-3 pl-6 space-y-6">
                        {#each sortedTrace as entry}
                            <div class="relative">
                                <!-- Bullet marker -->
                                <span
                                    class={`absolute -left-[31px] top-1 rounded-full w-4 h-4 border-2 border-white flex items-center justify-center shadow-xs ${
                                        entry.change_type === 'create'
                                            ? 'bg-blue-500'
                                            : 'bg-amber-500'
                                    }`}
                                ></span>

                                <div class="bg-gray-50 rounded-lg p-4 border border-gray-200/60 shadow-2xs space-y-2">
                                    <!-- Meta Row -->
                                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
                                        <span class="text-xs font-bold uppercase tracking-wider text-gray-500 flex items-center gap-1.5">
                                            {#if entry.change_type === 'create'}
                                                <span class="text-blue-600 font-bold">🟢 Create</span>
                                            {:else}
                                                <span class="text-amber-600 font-bold">🟡 Update</span>
                                            {/if}
                                        </span>
                                        <span class="text-xs text-gray-400 font-mono">
                                            {formatDate(entry.timestamp)}
                                        </span>
                                    </div>

                                    <!-- Summary / Info -->
                                    {#if entry.info}
                                        <p class="text-sm text-gray-700 font-medium">
                                            {entry.info}
                                        </p>
                                    {/if}

                                    <!-- Specific modifications -->
                                    {#if entry.changes && entry.changes.length > 0}
                                        <div class="mt-2 border-t border-gray-200/50 pt-2 space-y-1.5">
                                            <p class="text-[11px] font-bold text-gray-400 uppercase tracking-wider">
                                                Field Changes:
                                            </p>
                                            <div class="grid gap-1.5">
                                                {#each entry.changes as change}
                                                    <div class="flex flex-col sm:flex-row sm:items-center text-xs gap-1 sm:gap-2 bg-white px-2.5 py-1.5 rounded border border-gray-200/50 font-mono">
                                                        <span class="font-bold text-gray-600 sm:w-24 shrink-0 truncate">
                                                            {change.field}:
                                                        </span>
                                                        <div class="flex items-center gap-1.5 flex-wrap min-w-0">
                                                            <span class="bg-red-50 text-red-700 px-1.5 py-0.5 rounded border border-red-100/50 truncate max-w-[150px]" title={change.old_value}>
                                                                {change.old_value !== null && change.old_value !== undefined ? change.old_value.toString() : "null"}
                                                            </span>
                                                            <span class="text-gray-400">➔</span>
                                                            <span class="bg-emerald-50 text-emerald-700 px-1.5 py-0.5 rounded border border-emerald-100/50 truncate max-w-[150px]" title={change.new_value}>
                                                                {change.new_value !== null && change.new_value !== undefined ? change.new_value.toString() : "null"}
                                                            </span>
                                                        </div>
                                                    </div>
                                                {/each}
                                            </div>
                                        </div>
                                    {/if}
                                </div>
                            </div>
                        {/each}
                    </div>
                {/if}
            </div>

            <!-- Footer -->
            <footer class="bg-gray-50 px-6 py-4 border-t border-gray-200 flex items-center justify-end">
                <button
                    type="button"
                    class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 transition-colors cursor-pointer"
                    onclick={onClose}
                >
                    Close
                </button>
            </footer>
        </div>
    </div>
{/if}
