import { alertsStore } from './alerts.svelte';
import { actionsStore } from './actions.svelte';

export class ActStore {
    selectedAlertId = $state(null);
    alertSearchQuery = $state("");

    init(initialAlerts, initialActions, initialPredefined, apiUrl) {
        if (initialAlerts) {
            alertsStore.init(initialAlerts, apiUrl);
        }
        if (initialActions || initialPredefined) {
            actionsStore.init(initialActions, initialPredefined, apiUrl);
        }
        // Auto-select the first confirmed alert if available
        const confirmed = this.confirmedAlerts;
        if (confirmed.length > 0 && !this.selectedAlertId) {
            this.selectedAlertId = confirmed[0].id;
        }
    }

    setSelectedAlertId(id) {
        this.selectedAlertId = id;
    }

    setSearchQuery(query) {
        this.alertSearchQuery = query;
        this.syncSelection();
    }

    syncSelection() {
        const confirmed = this.confirmedAlerts;
        if (confirmed.length > 0 && !confirmed.some(a => a.id === this.selectedAlertId)) {
            this.selectedAlertId = confirmed[0].id;
        } else if (confirmed.length === 0) {
            this.selectedAlertId = null;
        }
    }

    // Derived states (Svelte 5 getters)
    get selectedAlert() {
        return alertsStore.items.find(a => a.id === this.selectedAlertId) || null;
    }

    get confirmedAlerts() {
        // Only show alerts with status === 'acknowledged' (confirmed)
        let items = alertsStore.items.filter(a => a.status === 'acknowledged');
        
        if (this.alertSearchQuery.trim()) {
            const query = this.alertSearchQuery.toLowerCase();
            items = items.filter(a => 
                a.title.toLowerCase().includes(query) || 
                a.description.toLowerCase().includes(query)
            );
        }
        
        // Sort by date descending (most recent first)
        return items.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    }

    get relatedActions() {
        if (!this.selectedAlertId) return [];
        // Return actions linked to the selected alert, sorted by created_at descending
        return actionsStore.items
            .filter(act => act.alert_id === this.selectedAlertId)
            .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    }
}

export const actStore = new ActStore();
