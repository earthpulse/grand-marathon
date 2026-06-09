<script>
    import { onMount } from "svelte";

    // Svelte 5 props
    const { data } = $props();

    // Local states
    let showEmailToast = $state(false);
    let emailAddress = $state("incident-commander@earthpulse.ai");

    // Metrics derived from data focusing on Alerts and Actions
    const totalAlerts = $derived(data.alerts?.length || 0);
    const activeAlerts = $derived(
        data.alerts?.filter((a) => a.status === "active").length || 0,
    );
    const resolvedAlerts = $derived(
        data.alerts?.filter((a) => a.status === "resolved").length || 0,
    );
    const totalActions = $derived(data.actions?.length || 0);

    // Merge, classify and group Alert & Action events per day
    const eventsByDay = $derived.by(() => {
        const events = [];

        // 1. Add Alert Registrations (Creation)
        (data.alerts || []).forEach((alert) => {
            const dateStr = alert.created_at.substring(0, 10);
            events.push({
                id: `alert-create-${alert.id}`,
                date: dateStr,
                timestamp: new Date(alert.created_at),
                type: "alert_create",
                category: "hazard",
                title: "🚨 New Alert Registered",
                subtitle: alert.title,
                severity: alert.severity,
                icon: "🚨",
                description: alert.description,
                latitude: alert.latitude,
                longitude: alert.longitude,
                meta: { status: alert.status, id: alert.id },
            });

            // 2. Add Alert Audit Traces (Historical Status Updates)
            (alert.trace || []).forEach((tr, index) => {
                if (tr.change_type === "update") {
                    const traceDate = tr.timestamp.substring(0, 10);
                    let infoMsg = tr.info || "Status configuration updated.";

                    events.push({
                        id: `alert-trace-${alert.id}-${index}`,
                        date: traceDate,
                        timestamp: new Date(tr.timestamp),
                        type: "alert_update",
                        category: "lifecycle",
                        title: "🔄 Alert Status Updated",
                        subtitle: alert.title,
                        severity: alert.severity,
                        icon: "🔄",
                        description: infoMsg,
                        changes: tr.changes || [],
                        meta: { id: alert.id },
                    });
                }
            });
        });

        // 3. Add Response Actions Deployed
        (data.actions || []).forEach((action) => {
            const actionDate = action.created_at.substring(0, 10);
            events.push({
                id: `action-create-${action.id}`,
                date: actionDate,
                timestamp: new Date(action.created_at),
                type: "action_deploy",
                category: "response",
                title: "🚀 Response Action Deployed",
                subtitle: action.title,
                severity: "info",
                icon: "🚒",
                description: action.description,
                meta: { status: action.status, alertId: action.alert_id },
            });

            // 4. Add Action Traces (Historical Progress Updates)
            (action.trace || []).forEach((tr, index) => {
                if (tr.change_type === "update") {
                    const traceDate = tr.timestamp.substring(0, 10);
                    events.push({
                        id: `action-trace-${action.id}-${index}`,
                        date: traceDate,
                        timestamp: new Date(tr.timestamp),
                        type: "action_update",
                        category: "response",
                        title: "⚙️ Response Progress Updated",
                        subtitle: action.title,
                        severity: "info",
                        icon: "📋",
                        description:
                            tr.info ||
                            `Task status advanced to ${action.status}.`,
                        changes: tr.changes || [],
                        meta: { id: action.id, status: action.status },
                    });
                }
            });
        });

        // Grouping events by date
        const groups = {};
        events.forEach((event) => {
            if (!groups[event.date]) {
                groups[event.date] = [];
            }
            groups[event.date].push(event);
        });

        // Sort days chronologically (oldest first to tell a visual story)
        const sortedDays = Object.keys(groups).sort(
            (a, b) => new Date(a) - new Date(b),
        );

        return sortedDays.map((day) => {
            // Sort events within that day chronologically
            const dayEvents = groups[day].sort(
                (a, b) => a.timestamp - b.timestamp,
            );
            return {
                day,
                formattedDate: new Date(day + "T00:00:00").toLocaleDateString(
                    "en-US",
                    {
                        weekday: "long",
                        year: "numeric",
                        month: "long",
                        day: "numeric",
                    },
                ),
                events: dayEvents,
            };
        });
    });

    let downloading = $state(false);

    async function handlePDFDownload() {
        if (!data.api_url) {
            alert("API URL not configured.");
            return;
        }
        downloading = true;
        try {
            const response = await fetch(`${data.api_url}/report/download`);
            if (!response.ok) {
                throw new Error("Failed to generate PDF on the server.");
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);

            // Auto-trigger browser download
            const a = document.createElement("a");
            a.href = url;
            a.download = `incident_report_${new Date().toISOString().substring(0, 10)}.pdf`;
            document.body.appendChild(a);
            a.click();

            // Cleanup
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (error) {
            console.error("PDF generation failed:", error);
            alert(
                "Error: Failed to compile the PDF report on the server. Please check the backend.",
            );
        } finally {
            downloading = false;
        }
    }

    function triggerEmailDemo() {
        showEmailToast = true;
        setTimeout(() => {
            showEmailToast = false;
        }, 5000);
    }
</script>

<div class="flex-1 overflow-y-auto bg-slate-50/50 p-6 min-h-0 print-container">
    <div class="w-full space-y-6 pb-12">
        <!-- Header Panel -->
        <header
            class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-white p-6 rounded-xl border border-slate-200/80 shadow-xs"
        >
            <div>
                <div class="flex items-center gap-2">
                    <span class="text-3xl">📋</span>
                    <h1
                        class="text-2xl font-black text-slate-900 tracking-tight"
                    >
                        Report
                    </h1>
                </div>
                <p class="text-sm text-slate-500 mt-1">
                    An auditable daily breakdown of environmental alerts,
                    severity progressions, and tactical responses.
                </p>
            </div>

            <!-- Actions (Hidden in PDF Print) -->
            <div class="flex gap-2 no-print shrink-0">
                <button
                    onclick={handlePDFDownload}
                    disabled={downloading}
                    class="px-4 py-2.5 text-xs font-extrabold text-white bg-[#0f766e] hover:bg-[#0d5e58] rounded-lg transition-all shadow-xs flex items-center gap-2 cursor-pointer uppercase tracking-wider disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    {downloading ? "⏳ Compiling PDF..." : "📥 Download PDF"}
                </button>
                <button
                    onclick={triggerEmailDemo}
                    class="px-4 py-2.5 text-xs font-extrabold text-[#0f766e] bg-[#e6f4f1] hover:bg-[#d4ede9] rounded-lg transition-all flex items-center gap-2 cursor-pointer uppercase tracking-wider"
                >
                    📧 Send Email
                </button>
            </div>
        </header>

        <!-- KPI Scorecards -->
        <section class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div
                class="bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs flex flex-col justify-between"
            >
                <span
                    class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest"
                    >Total Alerts</span
                >
                <div class="flex items-baseline gap-1 mt-1">
                    <span class="text-2xl font-black text-slate-900"
                        >{totalAlerts}</span
                    >
                    <span class="text-xs text-slate-400 font-medium"
                        >registered</span
                    >
                </div>
            </div>
            <div
                class="bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs flex flex-col justify-between"
            >
                <span
                    class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest"
                    >Active Threats</span
                >
                <div class="flex items-baseline gap-1 mt-1">
                    <span class="text-2xl font-black text-red-600"
                        >{activeAlerts}</span
                    >
                    <span class="text-xs text-red-400 font-bold">active</span>
                </div>
            </div>
            <div
                class="bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs flex flex-col justify-between"
            >
                <span
                    class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest"
                    >Resolved Hazards</span
                >
                <div class="flex items-baseline gap-1 mt-1">
                    <span class="text-2xl font-black text-emerald-600"
                        >{resolvedAlerts}</span
                    >
                    <span class="text-xs text-emerald-400 font-bold">safe</span>
                </div>
            </div>
            <div
                class="bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs flex flex-col justify-between"
            >
                <span
                    class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest"
                    >Tactical Responses</span
                >
                <div class="flex items-baseline gap-1 mt-1">
                    <span class="text-2xl font-black text-indigo-600"
                        >{totalActions}</span
                    >
                    <span class="text-xs text-indigo-400 font-bold"
                        >deployed</span
                    >
                </div>
            </div>
        </section>

        <!-- Daily Grouped Timeline -->
        <main class="space-y-8">
            {#if eventsByDay.length === 0}
                <div
                    class="bg-white p-12 text-center rounded-xl border border-slate-200/80 shadow-xs"
                >
                    <span class="text-3xl">📭</span>
                    <h3 class="text-sm font-bold text-slate-700 mt-2">
                        No historical events recorded
                    </h3>
                    <p class="text-xs text-slate-400 mt-1">
                        Environmental logging returns clear.
                    </p>
                </div>
            {:else}
                {#each eventsByDay as group (group.day)}
                    <section
                        class="bg-white p-6 md:p-8 rounded-xl border border-slate-200/80 shadow-xs space-y-6"
                    >
                        <!-- Day Section Header -->
                        <div
                            class="flex flex-col md:flex-row justify-between items-start md:items-center border-b border-slate-100 pb-4 gap-2"
                        >
                            <div>
                                <h2 class="text-lg font-black text-slate-900">
                                    {group.formattedDate}
                                </h2>
                                <p
                                    class="text-[10px] text-[#0f766e] bg-[#e6f4f1] font-bold px-2 py-0.5 rounded inline-block mt-1"
                                >
                                    {group.day}
                                </p>
                            </div>
                            <span
                                class="text-xs font-extrabold text-slate-400 uppercase tracking-wider"
                            >
                                {group.events.length}
                                {group.events.length === 1 ? "event" : "events"}
                                recorded
                            </span>
                        </div>

                        <!-- Sub-timeline stream for the day -->
                        <div
                            class="relative pl-6 border-l border-slate-100 ml-4 space-y-6"
                        >
                            {#each group.events as event (event.id)}
                                <article class="relative">
                                    <!-- Event Node Dot Indicator -->
                                    <div
                                        class={`absolute -left-[37px] top-1 w-6 h-6 rounded-full flex items-center justify-center text-xs shadow-xs border bg-white ${
                                            event.type === "alert_create" &&
                                            event.severity === "critical"
                                                ? "border-red-500 ring-2 ring-red-50"
                                                : event.type ===
                                                        "alert_create" &&
                                                    event.severity === "warning"
                                                  ? "border-amber-400 ring-2 ring-amber-50"
                                                  : event.type ===
                                                      "alert_create"
                                                    ? "border-blue-400 ring-2 ring-blue-50"
                                                    : event.type ===
                                                        "action_deploy"
                                                      ? "border-indigo-500 ring-2 ring-indigo-50"
                                                      : "border-slate-200"
                                        }`}
                                    >
                                        <span class="scale-90"
                                            >{event.icon}</span
                                        >
                                    </div>

                                    <!-- Event Body -->
                                    <div
                                        class="p-4 rounded-lg border border-slate-100 bg-slate-50/10 hover:bg-slate-50/40 transition-colors"
                                    >
                                        <div
                                            class="flex justify-between items-start gap-4 flex-wrap md:flex-nowrap"
                                        >
                                            <div>
                                                <span
                                                    class="text-[10px] font-bold text-slate-400 block mb-0.5"
                                                >
                                                    {event.timestamp.toLocaleTimeString(
                                                        [],
                                                        {
                                                            hour: "2-digit",
                                                            minute: "2-digit",
                                                        },
                                                    )}
                                                </span>
                                                <h3
                                                    class="text-xs font-black text-slate-900 leading-snug"
                                                >
                                                    {event.title}
                                                </h3>
                                                <p
                                                    class="text-[11px] font-bold text-[#0f766e]"
                                                >
                                                    {event.subtitle}
                                                </p>
                                            </div>

                                            <!-- Badge indicators -->
                                            <div
                                                class="flex gap-1.5 items-center"
                                            >
                                                {#if event.severity && event.category === "hazard"}
                                                    <span
                                                        class={`text-[8px] font-black uppercase px-2 py-0.5 rounded-full border ${
                                                            event.severity ===
                                                            "critical"
                                                                ? "bg-red-50 border-red-200 text-red-700"
                                                                : event.severity ===
                                                                    "warning"
                                                                  ? "bg-amber-50 border-amber-200 text-amber-700"
                                                                  : "bg-blue-50 border-blue-200 text-blue-700"
                                                        }`}
                                                    >
                                                        {event.severity}
                                                    </span>
                                                {/if}
                                                {#if event.type === "action_deploy"}
                                                    <span
                                                        class={`text-[8px] font-black uppercase px-2 py-0.5 rounded-full border ${
                                                            event.meta
                                                                .status ===
                                                            "completed"
                                                                ? "bg-emerald-50 border-emerald-200 text-emerald-700"
                                                                : event.meta
                                                                        .status ===
                                                                    "in_progress"
                                                                  ? "bg-amber-50 border-amber-200 text-amber-700"
                                                                  : "bg-indigo-50 border-indigo-200 text-indigo-700"
                                                        }`}
                                                    >
                                                        {event.meta.status}
                                                    </span>
                                                {/if}
                                            </div>
                                        </div>

                                        <p
                                            class="text-xs text-slate-600 mt-2 leading-relaxed whitespace-pre-line"
                                        >
                                            {event.description}
                                        </p>

                                        <!-- Spatial metadata -->
                                        {#if event.latitude && event.longitude && event.type === "alert_create"}
                                            <div
                                                class="mt-2 text-[10px] text-slate-400 font-semibold flex items-center gap-1"
                                            >
                                                <span>📍 Coordinates:</span>
                                                <code
                                                    class="bg-slate-100 px-1 py-0.5 rounded text-slate-600"
                                                >
                                                    {event.latitude.toFixed(4)}, {event.longitude.toFixed(
                                                        4,
                                                    )}
                                                </code>
                                            </div>
                                        {/if}

                                        <!-- Audit changes what changed block -->
                                        {#if event.changes && event.changes.length > 0}
                                            <div
                                                class="mt-3 pt-2.5 border-t border-slate-100 space-y-1.5"
                                            >
                                                <span
                                                    class="text-[9px] font-extrabold text-slate-400 uppercase tracking-wider block"
                                                    >Audit Changes</span
                                                >
                                                <div
                                                    class="grid grid-cols-1 md:grid-cols-2 gap-2"
                                                >
                                                    {#each event.changes as change}
                                                        <div
                                                            class="flex items-center gap-1.5 text-[11px] bg-slate-50/50 p-1.5 rounded border border-slate-100"
                                                        >
                                                            <strong
                                                                class="font-extrabold text-slate-500 capitalize"
                                                                >{change.field}:</strong
                                                            >
                                                            <span
                                                                class="text-slate-400 line-through truncate max-w-[100px]"
                                                                >{change.old_value ||
                                                                    "None"}</span
                                                            >
                                                            <span
                                                                class="text-slate-400"
                                                                >➡️</span
                                                            >
                                                            <span
                                                                class="font-black text-slate-800 bg-[#e6f4f1] text-[#0f766e] px-1.5 py-0.5 rounded truncate max-w-[120px]"
                                                                >{change.new_value}</span
                                                            >
                                                        </div>
                                                    {/each}
                                                </div>
                                            </div>
                                        {/if}
                                    </div>
                                </article>
                            {/each}
                        </div>
                    </section>
                {/each}
            {/if}
        </main>
    </div>
</div>

<!-- Email Success Toast Alert -->
{#if showEmailToast}
    <div
        class="fixed bottom-6 right-6 z-9999 bg-slate-900 text-white px-5 py-4 rounded-xl shadow-2xl border border-slate-800 flex items-start gap-3 max-w-sm animate-bounce no-print"
    >
        <span class="text-2xl">📧</span>
        <div>
            <h4
                class="text-xs font-black text-teal-400 uppercase tracking-widest"
            >
                DEMO SCHEDULER
            </h4>
            <p class="text-xs text-slate-300 mt-1 leading-snug">
                Incident report package compiled & dispatched to: <strong
                    class="text-white font-extrabold">{emailAddress}</strong
                >.
            </p>
        </div>
    </div>
{/if}

<style>
    /* CSS Print Rules specifically for PDF downloading */
    @media print {
        :global(body) {
            background: white !important;
            color: #0f172a !important;
            font-size: 11px !important;
        }

        .print-container {
            width: 100% !important;
            max-width: 100% !important;
            margin: 0 !important;
            padding: 24px !important;
            background: white !important;
            overflow: visible !important;
        }

        :global(aside),
        :global(nav),
        .no-print {
            display: none !important;
        }

        section,
        article {
            page-break-inside: avoid;
        }

        header {
            page-break-inside: avoid;
        }
    }
</style>
