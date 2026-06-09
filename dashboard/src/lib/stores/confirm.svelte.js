import { alertsStore } from './alerts.svelte';
import { actionsStore } from './actions.svelte';

export class ConfirmStore {
    news = $state(null);
    selectedAlertId = $state(null);
    alertSearchQuery = $state("");
    statusFilter = $state("all"); // 'all', 'active', 'acknowledged', 'resolved'

    init(initialNews, initialAlerts, apiUrl, initialActions = null) {
        this.news = initialNews;
        if (initialAlerts) {
            alertsStore.init(initialAlerts, apiUrl);
        }
        if (initialActions) {
            actionsStore.init(initialActions, null, apiUrl);
        }
        // Auto-select the first alert if available
        const filtered = this.filteredAlerts;
        if (filtered.length > 0 && !this.selectedAlertId) {
            this.selectedAlertId = filtered[0].id;
        }
    }

    // Setters
    setSelectedAlertId(id) {
        this.selectedAlertId = id;
    }

    setSearchQuery(query) {
        this.alertSearchQuery = query;
        this.syncSelection();
    }

    setStatusFilter(filter) {
        this.statusFilter = filter;
        this.syncSelection();
    }

    syncSelection() {
        const filtered = this.filteredAlerts;
        if (filtered.length > 0 && !filtered.some(a => a.id === this.selectedAlertId)) {
            this.selectedAlertId = filtered[0].id;
        } else if (filtered.length === 0) {
            this.selectedAlertId = null;
        }
    }

    // Derived states (Svelte 5 getters)
    get selectedAlert() {
        return alertsStore.items.find(a => a.id === this.selectedAlertId) || null;
    }

    get filteredAlerts() {
        // Filter out resolved alerts from the confirm workspace
        let items = alertsStore.items.filter(a => a.status !== "resolved");
        
        if (this.statusFilter !== "all") {
            items = items.filter(a => a.status === this.statusFilter);
        }
        
        if (this.alertSearchQuery.trim()) {
            const query = this.alertSearchQuery.toLowerCase();
            items = items.filter(a => 
                a.title.toLowerCase().includes(query) || 
                a.description.toLowerCase().includes(query)
            );
        }
        
        // Sort: active (unconfirmed) first, then by date descending (most recent first)
        return items.sort((a, b) => {
            if (a.status === 'active' && b.status !== 'active') return -1;
            if (b.status === 'active' && a.status !== 'active') return 1;
            return new Date(b.created_at) - new Date(a.created_at);
        });
    }

    get relatedNews() {
        const alert = this.selectedAlert;
        if (!alert || !this.news || !this.news.entries) return [];

        const titleLower = alert.title.toLowerCase();
        const descLower = alert.description.toLowerCase();

        return this.news.entries.map(entry => {
            // 1. Geographic Area Tag Matches (Weight: 3)
            const matchedTags = entry.area_tags.filter(tag => 
                titleLower.includes(tag.toLowerCase()) || descLower.includes(tag.toLowerCase())
            );

            // 2. Contextual Keywords Matches (Weight: 1)
            const keywords = ["fire", "incendio", "quiroga", "larouco", "seadur", "valdeorras", "petín", "petin", "alvaredos", "folgoso", "courel", "sil", "ourense", "lugo", "galicia"];
            const matchedKeywords = keywords.filter(word => 
                (titleLower.includes(word) || descLower.includes(word)) && 
                (entry.title.toLowerCase().includes(word) || entry.summary.toLowerCase().includes(word))
            );

            const score = (matchedTags.length * 3) + matchedKeywords.length;

            return {
                ...entry,
                matchedTags,
                matchedKeywords,
                score
            };
        })
        .filter(entry => entry.score > 0)
        .sort((a, b) => b.score - a.score || new Date(b.publication_date) - new Date(a.publication_date));
    }

    get recentNews() {
        if (!this.news || !this.news.entries) return [];
        
        const alert = this.selectedAlert;
        const titleLower = alert ? alert.title.toLowerCase() : "";
        const descLower = alert ? alert.description.toLowerCase() : "";

        return this.news.entries.map(entry => {
            const matchedTags = alert ? entry.area_tags.filter(tag => 
                titleLower.includes(tag.toLowerCase()) || descLower.includes(tag.toLowerCase())
            ) : [];

            const keywords = ["fire", "incendio", "quiroga", "larouco", "seadur", "valdeorras", "petín", "petin", "alvaredos", "folgoso", "courel", "sil", "ourense", "lugo", "galicia"];
            const matchedKeywords = alert ? keywords.filter(word => 
                (titleLower.includes(word) || descLower.includes(word)) && 
                (entry.title.toLowerCase().includes(word) || entry.summary.toLowerCase().includes(word))
            ) : [];

            const score = alert ? ((matchedTags.length * 3) + matchedKeywords.length) : 0;

            return {
                ...entry,
                matchedTags,
                matchedKeywords,
                score
            };
        })
        .sort((a, b) => new Date(b.publication_date) - new Date(a.publication_date));
    }

    get recommendation() {
        const alert = this.selectedAlert;
        const related = this.relatedNews;
        if (!alert || related.length === 0) return null;

        const topNews = related[0];
        const statusReported = topNews.fire_status_reported?.toLowerCase() || "";

        const isActive = ["activo", "sin control", "avance incontrolado", "situación delicada"].some(s => statusReported.includes(s));

        if (alert.status === "active") {
            if (isActive) {
                return {
                    action: "confirm",
                    type: "success",
                    title: "✅ Suggested Action: Confirm Alert Active",
                    message: `Evidence from "${topNews.source_name}" (${topNews.publication_date}) reports the fire is still ${statusReported.toUpperCase()}. We recommend confirming active status (Acknowledge).`,
                    applyText: "Confirm & Acknowledge Alert",
                    targetStatus: "acknowledged",
                    targetSeverity: alert.severity
                };
            }
        }

        return null;
    }

    async updateAlertStatus(alertId, newStatus, newSeverity = null) {
        const updatePayload = { status: newStatus };
        if (newSeverity) {
            updatePayload.severity = newSeverity;
        }
        await alertsStore.update(alertId, updatePayload);
    }

    get hasPlannedActions() {
        if (!this.selectedAlertId) return false;
        return actionsStore.items.some(act => act.alert_id === this.selectedAlertId);
    }
}

export const confirmStore = new ConfirmStore();
