import { browser } from "$app/environment";
import { writable } from "svelte/store";

const VALID_LAYERS = new Set(["light", "streets", "satellite"]);
const LOCAL_STORAGE_KEY = "dashboardSettings";

const defaultSettings = {
    layer: "satellite",
};

function loadSettings() {
    if (!browser) return defaultSettings;
    try {
        const json = localStorage.getItem(LOCAL_STORAGE_KEY);
        if (json) {
            const parsed = JSON.parse(json);
            // Validate layer
            if (parsed && VALID_LAYERS.has(parsed.layer)) {
                return { ...defaultSettings, ...parsed };
            }
        }
    } catch (e) {
        // fail gracefully, fallback to default
    }
    return defaultSettings;
}

function saveSettings(settings) {
    if (!browser) return;
    try {
        localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(settings));
    } catch (e) {
        // fail gracefully, do nothing
    }
}

function createDashboardSettings() {
    const initialSettings = loadSettings();
    const { subscribe, set, update } = writable(initialSettings);

    function setLayer(layer) {
        if (!VALID_LAYERS.has(layer)) {
            return;
        }
        update(current => {
            const newSettings = { ...current, layer };
            saveSettings(newSettings);
            return newSettings;
        });
    }

    // Optionally persist if settings are updated via set/use.
    function setAndPersist(value) {
        saveSettings(value);
        set(value);
    }

    return {
        subscribe,
        setLayer,
        set: setAndPersist
    };
}

export const dashboardSettings = createDashboardSettings();
