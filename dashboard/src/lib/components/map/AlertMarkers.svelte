<script>
    import { getContext, onDestroy } from "svelte";

    let {
        alerts = [],
        actions = [],
        selectedDate = "",
        filterOption = "confirmed",
        onAlertClick = null,
    } = $props();

    const { getMap } = getContext("map");

    let markers = [];

    // Helper to get historical state of an item (alert or action) based on its trace
    function getHistoricalState(item, date) {
        if (!date) return item;

        const historical = { ...item };

        if (!historical.trace || !Array.isArray(historical.trace)) {
            return historical;
        }

        // Sort trace entries descending by timestamp to revert newest changes first
        const sortedTrace = [...historical.trace].sort((a, b) => {
            return new Date(b.timestamp) - new Date(a.timestamp);
        });

        for (const entry of sortedTrace) {
            const entryDate = entry.timestamp.substring(0, 10);

            // If the change occurred AFTER the selected date, we revert it
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

    // Reactively filter and compute historical state for alerts on or before the selected date
    const filteredAlerts = $derived.by(() => {
        let list = alerts;
        if (selectedDate) {
            list = alerts.filter((alert) => {
                const alertDate = alert.created_at.substring(0, 10);
                return alertDate <= selectedDate;
            });
        }

        let mapped = list.map((alert) =>
            getHistoricalState(alert, selectedDate),
        );

        if (filterOption === "confirmed") {
            mapped = mapped.filter((a) => a.status === "acknowledged");
        } else if (filterOption === "unconfirmed") {
            mapped = mapped.filter((a) => a.status === "active");
        } else if (filterOption === "resolved") {
            mapped = mapped.filter((a) => a.status === "resolved");
        }

        return mapped;
    });

    // Reactively filter and compute historical state for actions on or before the selected date
    const filteredActions = $derived.by(() => {
        if (!selectedDate) return actions;
        return actions
            .filter((action) => {
                const actionDate = action.created_at.substring(0, 10);
                return actionDate <= selectedDate;
            })
            .map((action) => getHistoricalState(action, selectedDate));
    });

    // Helper to group actions by alert id
    function getActionsForAlert(alertId) {
        return filteredActions.filter((action) => action.alert_id === alertId);
    }

    function createMarkers(map) {
        // Clear any existing markers first
        clearMarkers();

        // Loop through alerts with valid coordinates
        filteredAlerts.forEach((alert) => {
            if (
                alert.latitude === null ||
                alert.longitude === null ||
                alert.latitude === undefined ||
                alert.longitude === undefined
            ) {
                return;
            }

            const markerColorClass =
                alert.severity === "critical"
                    ? "bg-red-500"
                    : alert.severity === "warning"
                      ? "bg-amber-500"
                      : "bg-blue-500";

            const severityLabel = alert.severity
                ? alert.severity.toUpperCase()
                : "INFO";
            const statusLabel = alert.status
                ? alert.status.toUpperCase()
                : "ACTIVE";

            // Create a premium pulsating marker icon using Tailwind
            const icon = L.divIcon({
                className: "flex h-5 w-5 justify-center items-center",
                html: `
                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full ${markerColorClass} opacity-75"></span>
                    <span class="relative inline-flex rounded-full h-3 w-3 ${markerColorClass} border-2 border-white shadow-md"></span>
                `,
                iconSize: [20, 20],
                iconAnchor: [10, 10],
            });

            // Get actions for this alert
            const alertActions = getActionsForAlert(alert.id);

            // Construct popup content HTML
            let actionsHtml = "";
            if (alertActions.length > 0) {
                actionsHtml = `
                    <div class="mt-2.5 border-t border-gray-100 pt-2">
                        <p class="text-[10px] font-bold text-gray-500 uppercase tracking-wider mb-1.5">Attached Actions:</p>
                        <ul class="space-y-1 max-h-36 overflow-y-auto pr-1">
                            ${alertActions
                                .map((act) => {
                                    const statusColors =
                                        act.status === "completed"
                                            ? "bg-emerald-50 text-emerald-700 border-emerald-200"
                                            : act.status === "in_progress"
                                              ? "bg-blue-50 text-blue-700 border-blue-200"
                                              : act.status === "cancelled"
                                                ? "bg-gray-100 text-gray-700 border-gray-300"
                                                : "bg-amber-50 text-amber-700 border-amber-200"; // pending
                                    return `
                                    <li class="flex items-start justify-between gap-2 text-xs py-0.5">
                                        <span class="text-gray-800 font-medium leading-tight">${act.title}</span>
                                        <span class="text-[9px] font-bold uppercase px-1.5 py-0.5 rounded-full border shrink-0 ${statusColors}">${act.status}</span>
                                    </li>
                                `;
                                })
                                .join("")}
                        </ul>
                    </div>
                `;
            } else {
                actionsHtml = `
                    <div class="mt-2.5 border-t border-gray-100 pt-2 text-xs text-gray-400 italic">
                        No actions registered.
                    </div>
                `;
            }

            // Severity styling for popup header
            const popupSeverityBg =
                alert.severity === "critical"
                    ? "bg-red-50 border-red-200 text-red-700"
                    : alert.severity === "warning"
                      ? "bg-amber-50 border-amber-200 text-amber-700"
                      : "bg-blue-50 border-blue-200 text-blue-700";

            const popupStatusBg =
                alert.status === "active"
                    ? "bg-emerald-50 border-emerald-200 text-emerald-700"
                    : alert.status === "acknowledged"
                      ? "bg-indigo-50 border-indigo-200 text-indigo-700"
                      : "bg-gray-100 border-gray-300 text-gray-700";

            let metricsHtml = "";
            if (
                (alert.affected_roads_count !== undefined &&
                    alert.affected_roads_count !== null) ||
                (alert.affected_buildings_count !== undefined &&
                    alert.affected_buildings_count !== null) ||
                (alert.affected_amenities_count !== undefined &&
                    alert.affected_amenities_count !== null) ||
                (alert.affected_population !== undefined &&
                    alert.affected_population !== null)
            ) {
                metricsHtml = `
                    <div class="mt-2.5 pt-2 border-t border-gray-100 flex flex-col gap-1 text-[11px] text-slate-600">
                        <p class="text-[9px] font-bold text-gray-400 uppercase tracking-wider mb-1">Affected:</p>
                        ${
                            alert.affected_roads_count !== undefined &&
                            alert.affected_roads_count !== null
                                ? `
                            <div class="flex justify-between items-center bg-gray-50 px-2 py-1 rounded border border-gray-200/40">
                                <span class="font-medium text-gray-500">🛣️ Number of Affected Roads:</span>
                                <span class="bg-blue-100 text-blue-800 text-[10px] font-bold px-1.5 py-0.5 rounded-full">${alert.affected_roads_count}</span>
                            </div>
                        `
                                : ""
                        }
                        ${
                            alert.affected_buildings_count !== undefined &&
                            alert.affected_buildings_count !== null
                                ? `
                            <div class="flex justify-between items-center bg-gray-50 px-2 py-1 rounded border border-gray-200/40">
                                <span class="font-medium text-gray-500">🏢 Number of Affected Buildings:</span>
                                <span class="bg-amber-100 text-amber-800 text-[10px] font-bold px-1.5 py-0.5 rounded-full">${alert.affected_buildings_count}</span>
                            </div>
                        `
                                : ""
                        }
                        ${
                            alert.affected_amenities_count !== undefined &&
                            alert.affected_amenities_count !== null
                                ? `
                            <div class="flex justify-between items-center bg-gray-50 px-2 py-1 rounded border border-gray-200/40">
                                <span class="font-medium text-gray-500">🏥 Number of Affected Amenities:</span>
                                <span class="bg-purple-100 text-purple-800 text-[10px] font-bold px-1.5 py-0.5 rounded-full">${alert.affected_amenities_count}</span>
                            </div>
                        `
                                : ""
                        }
                        ${
                            alert.affected_population !== undefined &&
                            alert.affected_population !== null
                                ? `
                            <div class="flex justify-between items-center bg-gray-50 px-2 py-1 rounded border border-gray-200/40">
                                <span class="font-medium text-gray-500">👥 Amount of Affected Population:</span>
                                <span class="bg-emerald-100 text-emerald-800 text-[10px] font-bold px-1.5 py-0.5 rounded-full">${alert.affected_population}</span>
                            </div>
                        `
                                : ""
                        }
                    </div>
                `;
            }

            const popupHtml = `
                <div class="p-0.5 min-w-[240px] max-w-[300px] text-sans">
                    <div class="flex items-center gap-1.5 mb-1.5 flex-wrap">
                        <span class="text-[9px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full border ${popupSeverityBg}">${severityLabel}</span>
                        <span class="text-[9px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full border ${popupStatusBg}">${statusLabel}</span>
                    </div>
                    <h3 class="text-sm font-bold text-gray-900 leading-snug m-0">${alert.title}</h3>
                    <p class="text-xs text-gray-600 mt-1 mb-0 leading-relaxed whitespace-pre-line">${alert.description}</p>
                    ${metricsHtml}
                    ${actionsHtml}
                </div>
            `;

            // Create Leaflet marker
            const marker = L.marker([alert.latitude, alert.longitude], {
                icon,
                pane: "markerPane", // Force markers onto the high z-index pane
            });

            // Bind popup with custom options
            marker.bindPopup(popupHtml, {
                maxWidth: 320,
                className: "custom-alert-popup",
            });

            // Handle hover: open on mouseover, close on mouseout
            marker.on("mouseover", function () {
                this.openPopup();
            });
            marker.on("mouseout", function () {
                this.closePopup();
            });

            // Handle click: trigger callback to show detail panel
            marker.on("click", function () {
                if (onAlertClick) {
                    onAlertClick(alert);
                }
            });

            marker.addTo(map);
            markers.push(marker);
        });
    }

    function clearMarkers() {
        markers.forEach((m) => m.remove());
        markers = [];
    }

    // React to changes in alerts, actions, or selected date
    $effect(() => {
        const map = getMap();
        if (map && filteredAlerts) {
            createMarkers(map);
        }
    });

    onDestroy(() => {
        clearMarkers();
    });
</script>
