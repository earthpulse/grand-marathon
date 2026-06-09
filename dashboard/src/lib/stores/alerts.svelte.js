async function getErrorMessage(res, defaultMsg) {
    try {
        const errText = await res.text();
        try {
            const parsed = JSON.parse(errText);
            if (parsed && typeof parsed === "object" && parsed.detail) {
                return parsed.detail;
            }
        } catch {}
        return errText || defaultMsg;
    } catch {
        return defaultMsg;
    }
}

export class AlertsStore {
    items = $state([]);
    loading = $state(false);
    error = $state(null);
    apiUrl = $state("");

    init(initialAlerts, apiUrl) {
        this.items = initialAlerts || [];
        this.apiUrl = apiUrl || "";
    }

    async load() {
        this.loading = true;
        this.error = null;
        if (!this.apiUrl) {
            this.loading = false;
            this.error = "API URL not initialized";
            return;
        }
        try {
            const res = await fetch(`${this.apiUrl}/alerts`);
            if (!res.ok) throw new Error("Failed to load alerts from server");
            this.items = await res.json();
        } catch (err) {
            this.error = err.message || "An unexpected error occurred during loading.";
            throw err;
        } finally {
            this.loading = false;
        }
    }

    async create(alertData) {
        this.loading = true;
        this.error = null;
        try {
            const res = await fetch(`${this.apiUrl}/alerts/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(alertData)
            });
            if (!res.ok) {
                const message = await getErrorMessage(res, "Failed to create alert");
                throw new Error(message);
            }
            const newAlert = await res.json();
            this.items = [...this.items, newAlert];
            return newAlert;
        } catch (err) {
            this.error = err.message || "An unexpected error occurred during creation.";
            throw err;
        } finally {
            this.loading = false;
        }
    }

    async update(alertId, alertData) {
        this.loading = true;
        this.error = null;
        try {
            const res = await fetch(`${this.apiUrl}/alerts/${alertId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(alertData)
            });
            if (!res.ok) {
                const message = await getErrorMessage(res, "Failed to update alert");
                throw new Error(message);
            }
            const updatedAlert = await res.json();
            this.items = this.items.map(item => item.id === alertId ? updatedAlert : item);
            return updatedAlert;
        } catch (err) {
            this.error = err.message || "An unexpected error occurred during update.";
            throw err;
        } finally {
            this.loading = false;
        }
    }

    async delete(alertId) {
        this.loading = true;
        this.error = null;
        try {
            const res = await fetch(`${this.apiUrl}/alerts/${alertId}`, {
                method: "DELETE"
            });
            if (!res.ok) {
                const message = await getErrorMessage(res, "Failed to delete alert");
                throw new Error(message);
            }
            this.items = this.items.filter(item => item.id !== alertId);
        } catch (err) {
            this.error = err.message || "An unexpected error occurred during deletion.";
            throw err;
        } finally {
            this.loading = false;
        }
    }

    clearError() {
        this.error = null;
    }
}

export const alertsStore = new AlertsStore();
