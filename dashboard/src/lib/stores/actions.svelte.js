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

export class ActionsStore {
    items = $state([]);
    predefined = $state([]);
    loading = $state(false);
    error = $state(null);
    apiUrl = $state("");

    init(initialActions, initialPredefined, apiUrl) {
        this.items = initialActions || [];
        this.predefined = initialPredefined || [];
        this.apiUrl = apiUrl || "";
    }

    async load(alertId = null) {
        this.loading = true;
        this.error = null;
        if (!this.apiUrl) {
            this.loading = false;
            this.error = "API URL not initialized";
            return;
        }
        try {
            const url = alertId 
                ? `${this.apiUrl}/actions?alert_id=${alertId}`
                : `${this.apiUrl}/actions`;
            const res = await fetch(url);
            if (!res.ok) throw new Error("Failed to load actions from server");
            this.items = await res.json();
        } catch (err) {
            this.error = err.message || "An unexpected error occurred during loading actions.";
            throw err;
        } finally {
            this.loading = false;
        }
    }

    async loadPredefined() {
        this.loading = true;
        this.error = null;
        if (!this.apiUrl) {
            this.loading = false;
            this.error = "API URL not initialized";
            return;
        }
        try {
            const res = await fetch(`${this.apiUrl}/actions/predefined`);
            if (!res.ok) throw new Error("Failed to load predefined actions");
            this.predefined = await res.json();
        } catch (err) {
            this.error = err.message || "An unexpected error occurred during loading predefined actions.";
            throw err;
        } finally {
            this.loading = false;
        }
    }

    async create(actionData) {
        this.loading = true;
        this.error = null;
        try {
            const res = await fetch(`${this.apiUrl}/actions/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(actionData)
            });
            if (!res.ok) {
                const message = await getErrorMessage(res, "Failed to create action");
                throw new Error(message);
            }
            const newAction = await res.json();
            this.items = [...this.items, newAction];
            return newAction;
        } catch (err) {
            this.error = err.message || "An unexpected error occurred during action creation.";
            throw err;
        } finally {
            this.loading = false;
        }
    }

    async update(actionId, actionData) {
        this.loading = true;
        this.error = null;
        try {
            const res = await fetch(`${this.apiUrl}/actions/${actionId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(actionData)
            });
            if (!res.ok) {
                const message = await getErrorMessage(res, "Failed to update action");
                throw new Error(message);
            }
            const updatedAction = await res.json();
            this.items = this.items.map(item => item.id === actionId ? updatedAction : item);
            return updatedAction;
        } catch (err) {
            this.error = err.message || "An unexpected error occurred during action update.";
            throw err;
        } finally {
            this.loading = false;
        }
    }

    async delete(actionId) {
        this.loading = true;
        this.error = null;
        try {
            const res = await fetch(`${this.apiUrl}/actions/${actionId}`, {
                method: "DELETE"
            });
            if (!res.ok) {
                const message = await getErrorMessage(res, "Failed to delete action");
                throw new Error(message);
            }
            this.items = this.items.filter(item => item.id !== actionId);
        } catch (err) {
            this.error = err.message || "An unexpected error occurred during action deletion.";
            throw err;
        } finally {
            this.loading = false;
        }
    }

    clearError() {
        this.error = null;
    }
}

export const actionsStore = new ActionsStore();
