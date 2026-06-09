<script>
    let { isOpen, alert = null, onClose, onSave, apiUrl = "http://localhost:8000" } = $props();

    let title = $state("");
    let description = $state("");
    let severity = $state("info");
    let status = $state("active");
    let latitude = $state("");
    let longitude = $state("");

    let error = $state("");
    let activeTab = $state("form");
    let activeSubTab = $state("curl"); // 'curl' | 'python' | 'js'
    let copied = $state(false);

    $effect(() => {
        if (isOpen) {
            error = "";
            activeTab = "form";
            activeSubTab = "curl";
            copied = false;
            if (alert) {
                title = alert.title || "";
                description = alert.description || "";
                severity = alert.severity || "info";
                status = alert.status || "active";
                latitude = alert.latitude !== null && alert.latitude !== undefined ? alert.latitude.toString() : "";
                longitude = alert.longitude !== null && alert.longitude !== undefined ? alert.longitude.toString() : "";
            } else {
                title = "";
                description = "";
                severity = "info";
                status = "active";
                latitude = "";
                longitude = "";
            }
        }
    });

    const payloadObj = $derived.by(() => {
        const latVal = latitude.trim() === "" ? null : parseFloat(latitude);
        const lonVal = longitude.trim() === "" ? null : parseFloat(longitude);
        return {
            title: title.trim() || "Title of the alert",
            description: description.trim() || "Detailed description...",
            severity,
            status,
            latitude: isNaN(latVal) || latVal === null ? null : latVal,
            longitude: isNaN(lonVal) || lonVal === null ? null : lonVal
        };
    });

    const curlPayload = $derived(JSON.stringify(payloadObj, null, 2));

    const method = $derived(alert ? "PUT" : "POST");
    const path = $derived(alert ? `/alerts/${alert.id}` : "/alerts/");
    const fullUrl = $derived(`${apiUrl}${path}`);

    // Generate instructions for each active subtab
    const snippets = $derived.by(() => {
        const curl = `curl -X ${method} "${fullUrl}" \\
  -H "Content-Type: application/json" \\
  -d '${curlPayload}'`;

        const python = `import requests

url = "${fullUrl}"
headers = {
    "Content-Type": "application/json"
}
payload = ${JSON.stringify(payloadObj, null, 4)}

response = requests.request("${method}", url, headers=headers, json=payload)
print(f"Status Code: {response.status_code}")
print(response.json())`;

        const js = `const url = "${fullUrl}";
const payload = ${JSON.stringify(payloadObj, null, 2)};

try {
  const response = await fetch(url, {
    method: "${method}",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error(\`HTTP error! status: \${response.status}\`);
  }

  const data = await response.json();
  console.log("Success:", data);
} catch (error) {
  console.error("Error:", error);
}`;

        return { curl, python, js };
    });

    const currentCode = $derived(snippets[activeSubTab]);

    const skillsMarkdown = $derived.by(() => {
        return `# Skill: Managing Environmental Alerts

This skill guides AI agents and LLMs in autonomously inspecting, creating, updating, resolving, and auditing environmental alerts.

## 🛠️ API Reference

### 1. Retrieve All Alerts
Fetches sorted alerts (most recent first), with optional filtering.

* **Method**: \`GET\`
* **Path**: \`/alerts/\`
* **Query Parameters**:
  * \`severity\` (optional): \`info\`, \`warning\`, \`critical\`
  * \`status\` (optional): \`active\`, \`resolved\`, \`acknowledged\`

#### cURL Example:
\`\`\`bash
curl -X GET "/alerts/?status=active&severity=critical"
\`\`\`

---

### 2. Create a New Alert
Generates a new environmental alert.

* **Method**: \`POST\`
* **Path**: \`/alerts/\`
* **Request Body Schema**:
  \`\`\`json
  {
    "title": "string (Required)",
    "description": "string (Required - detailed description of fire/event)",
    "severity": "string (Optional: 'info' | 'warning' | 'critical'. Default: 'info')",
    "status": "string (Optional: 'active' | 'resolved' | 'acknowledged'. Default: 'active')",
    "latitude": "float (Optional: -90.0 to 90.0)",
    "longitude": "float (Optional: -180.0 to 180.0)"
  }
  \`\`\`

#### Python Example:
\`\`\`python
import requests

url = "/alerts/"
payload = {
    "title": "Smoke plume near Larouco",
    "description": "Active thermal hotspot detected via Sentinel-2 imagery.",
    "severity": "warning",
    "status": "active",
    "latitude": 42.3456,
    "longitude": -7.2625
}
res = requests.post(url, json=payload)
print(res.json())
\`\`\`

---

### 3. Update an Existing Alert
Modifies fields on an existing alert.

* **Method**: \`PUT\`
* **Path**: \`/alerts/{alert_id}\`
* **Request Body Schema**: All fields are optional. Only pass fields that need modification.

#### JavaScript Fetch Example:
\`\`\`javascript
const response = await fetch("/alerts/seed-alert-001", {
  method: "PUT",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    status: "resolved",
    severity: "info"
  })
});
const updatedAlert = await response.json();
console.log(updatedAlert);
\`\`\`

---

### 4. Delete an Alert
Deletes an alert permanently.

* **Method**: \`DELETE\`
* **Path**: \`/alerts/{alert_id}\`
* **Response**: \`204 No Content\`

---

## 🔍 Audit & Traceability

Every alert has an auditable trace timeline in the \`trace\` property. Inspect this timeline to understand historical changes.

### Trace Schema Structure:
\`\`\`json
"trace": [
  {
    "timestamp": "2025-08-21T09:46:00Z",
    "change_type": "update",
    "changes": [
      {
        "field": "severity",
        "old_value": "warning",
        "new_value": "critical"
      }
    ],
    "info": "Upgraded severity to CRITICAL as burned area surpassed historical records."
  }
]
\`\`\``;
    });

    function handleCopy() {
        const textToCopy = activeTab === 'skills' ? skillsMarkdown : currentCode;
        navigator.clipboard.writeText(textToCopy);
        copied = true;
        setTimeout(() => {
            copied = false;
        }, 2000);
    }

    function handleSubmit(e) {
        e.preventDefault();
        
        if (!title.trim()) {
            error = "Title is required.";
            activeTab = "form";
            return;
        }
        if (!description.trim()) {
            error = "Description is required.";
            activeTab = "form";
            return;
        }

        const latVal = latitude.trim() === "" ? null : parseFloat(latitude);
        const lonVal = longitude.trim() === "" ? null : parseFloat(longitude);

        if (latVal !== null && (isNaN(latVal) || latVal < -90 || latVal > 90)) {
            error = "Latitude must be a valid number between -90 and 90.";
            activeTab = "form";
            return;
        }
        if (lonVal !== null && (isNaN(lonVal) || lonVal < -180 || lonVal > 180)) {
            error = "Longitude must be a valid number between -180 and 180.";
            activeTab = "form";
            return;
        }

        onSave({
            title: title.trim(),
            description: description.trim(),
            severity,
            status,
            latitude: latVal,
            longitude: lonVal
        });
    }
</script>

{#if isOpen}
    <!-- Backdrop -->
    <div
        class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4 backdrop-blur-xs"
        onclick={onClose}
        role="button"
        tabindex="-1"
        onkeydown={(e) => e.key === 'Escape' && onClose()}
    >
        <!-- Modal Content Container -->
        <div
            class="bg-white rounded-lg shadow-xl w-full max-w-xl overflow-hidden flex flex-col"
            onclick={(e) => e.stopPropagation()}
            role="dialog"
            aria-modal="true"
        >
            <!-- Header -->
            <header class="bg-gray-50 px-6 py-4 border-b border-gray-200 flex items-center justify-between">
                <h2 class="text-xl font-semibold text-gray-800">
                    {alert ? "Edit Alert" : "Create New Alert"}
                </h2>
                <button
                    class="text-gray-400 hover:text-gray-600 transition-colors text-2xl font-light cursor-pointer"
                    onclick={onClose}
                    aria-label="Close modal"
                >
                    &times;
                </button>
            </header>

            <!-- Tabs Selector -->
            <div class="flex border-b border-gray-200 bg-gray-50/50">
                <button
                    type="button"
                    class={`flex-1 py-3 text-sm font-semibold border-b-2 text-center transition-all cursor-pointer ${
                        activeTab === 'form'
                            ? 'border-blue-600 text-blue-600 bg-blue-50/10'
                            : 'border-transparent text-gray-500 hover:text-gray-700 hover:bg-gray-50/50'
                    }`}
                    onclick={() => activeTab = 'form'}
                >
                    📝 Form Editor
                </button>
                <button
                    type="button"
                    class={`flex-1 py-3 text-sm font-semibold border-b-2 text-center transition-all cursor-pointer ${
                        activeTab === 'instructions'
                            ? 'border-blue-600 text-blue-600 bg-blue-50/10'
                            : 'border-transparent text-gray-500 hover:text-gray-700 hover:bg-gray-50/50'
                    }`}
                    onclick={() => { activeTab = 'instructions'; copied = false; }}
                >
                    💻 API Instructions
                </button>
                <button
                    type="button"
                    class={`flex-1 py-3 text-sm font-semibold border-b-2 text-center transition-all cursor-pointer ${
                        activeTab === 'skills'
                            ? 'border-blue-600 text-blue-600 bg-blue-50/10'
                            : 'border-transparent text-gray-500 hover:text-gray-700 hover:bg-gray-50/50'
                    }`}
                    onclick={() => { activeTab = 'skills'; copied = false; }}
                >
                    🤖 Agent SKILL.md
                </button>
            </div>

            <!-- Body -->
            {#if activeTab === 'form'}
                <form onsubmit={handleSubmit} class="flex-1 overflow-y-auto p-6 space-y-4">
                    {#if error}
                        <div class="bg-red-50 border-l-4 border-red-500 p-3 rounded">
                            <p class="text-sm text-red-700">{error}</p>
                        </div>
                    {/if}

                    <div>
                        <label for="alert-title" class="block text-sm font-medium text-gray-700 mb-1">
                            Title <span class="text-red-500">*</span>
                        </label>
                        <input
                            id="alert-title"
                            type="text"
                            bind:value={title}
                            placeholder="e.g., Temperature spike detected"
                            class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                            required
                        />
                    </div>

                    <div>
                        <label for="alert-description" class="block text-sm font-medium text-gray-700 mb-1">
                            Description <span class="text-red-500">*</span>
                        </label>
                        <textarea
                            id="alert-description"
                            bind:value={description}
                            placeholder="Provide details about the alert..."
                            rows="3"
                            class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                            required
                        ></textarea>
                    </div>

                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label for="alert-severity" class="block text-sm font-medium text-gray-700 mb-1">
                                Severity
                            </label>
                            <select
                                id="alert-severity"
                                bind:value={severity}
                                class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 bg-white"
                            >
                                <option value="info">Info</option>
                                <option value="warning">Warning</option>
                                <option value="critical">Critical</option>
                            </select>
                        </div>

                        <div>
                            <label for="alert-status" class="block text-sm font-medium text-gray-700 mb-1">
                                Status
                            </label>
                            <select
                                id="alert-status"
                                bind:value={status}
                                class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 bg-white"
                            >
                                <option value="active">Active</option>
                                <option value="resolved">Resolved</option>
                                <option value="acknowledged">Acknowledged</option>
                            </select>
                        </div>
                    </div>

                    <div class="grid grid-cols-2 gap-4 pt-2">
                        <div>
                            <label for="alert-latitude" class="block text-sm font-medium text-gray-700 mb-1">
                                Latitude <span class="text-gray-400 font-normal text-xs">(optional)</span>
                            </label>
                            <input
                                id="alert-latitude"
                                type="number"
                                step="any"
                                bind:value={latitude}
                                placeholder="e.g., 42.345"
                                class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                            />
                        </div>

                        <div>
                            <label for="alert-longitude" class="block text-sm font-medium text-gray-700 mb-1">
                                Longitude <span class="text-gray-400 font-normal text-xs">(optional)</span>
                            </label>
                            <input
                                id="alert-longitude"
                                type="number"
                                step="any"
                                bind:value={longitude}
                                placeholder="e.g., -7.234"
                                class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                            />
                        </div>
                    </div>

                    <!-- Footer -->
                    <footer class="pt-4 border-t border-gray-100 flex items-center justify-end gap-3">
                        <button
                            type="button"
                            class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 transition-colors cursor-pointer"
                            onclick={onClose}
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-hidden focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors cursor-pointer"
                        >
                            Save
                        </button>
                    </footer>
                </form>
            {:else if activeTab === 'instructions'}
                <div class="flex-1 overflow-y-auto p-6 space-y-4 flex flex-col">
                    <p class="text-xs text-gray-500 leading-normal">
                        Select a tab below to inspect or copy ready-to-use instructions for performing this API request in different languages.
                    </p>

                    <!-- Subtabs Selector -->
                    <div class="flex gap-1.5 p-1 bg-gray-100 rounded-lg self-start">
                        <button
                            type="button"
                            class={`px-3 py-1 text-xs font-semibold rounded-md transition-all cursor-pointer ${
                                activeSubTab === 'curl'
                                    ? 'bg-white text-gray-900 shadow-xs'
                                    : 'text-gray-500 hover:text-gray-900'
                            }`}
                            onclick={() => { activeSubTab = 'curl'; copied = false; }}
                        >
                            cURL
                        </button>
                        <button
                            type="button"
                            class={`px-3 py-1 text-xs font-semibold rounded-md transition-all cursor-pointer ${
                                activeSubTab === 'python'
                                    ? 'bg-white text-gray-900 shadow-xs'
                                    : 'text-gray-500 hover:text-gray-900'
                            }`}
                            onclick={() => { activeSubTab = 'python'; copied = false; }}
                        >
                            Python
                        </button>
                        <button
                            type="button"
                            class={`px-3 py-1 text-xs font-semibold rounded-md transition-all cursor-pointer ${
                                activeSubTab === 'js'
                                    ? 'bg-white text-gray-900 shadow-xs'
                                    : 'text-gray-500 hover:text-gray-900'
                            }`}
                            onclick={() => { activeSubTab = 'js'; copied = false; }}
                        >
                            JavaScript
                        </button>
                    </div>

                    <!-- Code block -->
                    <div class="relative bg-gray-900 rounded-lg p-4 font-mono text-xs text-blue-400 overflow-x-auto whitespace-pre border border-gray-800 shadow-inner max-h-[250px] min-h-[160px] flex-1">
                        <code>{currentCode}</code>
                    </div>

                    <!-- Footer -->
                    <footer class="pt-4 border-t border-gray-100 flex items-center justify-end gap-3 shrink-0">
                        <button
                            type="button"
                            class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 transition-colors cursor-pointer"
                            onclick={onClose}
                        >
                            Close
                        </button>
                        <button
                            type="button"
                            class={`px-4 py-2 text-sm font-medium text-white border border-transparent rounded-md transition-colors cursor-pointer flex items-center gap-1.5 ${
                                copied 
                                    ? 'bg-emerald-600 hover:bg-emerald-700' 
                                    : 'bg-blue-600 hover:bg-blue-700'
                            }`}
                            onclick={handleCopy}
                        >
                            {#if copied}
                                <span>✓</span> Copied!
                            {:else}
                                <span>📋</span> Copy Code
                            {/if}
                        </button>
                    </footer>
                </div>
            {:else if activeTab === 'skills'}
                <div class="flex-1 overflow-y-auto p-6 space-y-4 flex flex-col">
                    <p class="text-xs text-gray-500 leading-normal">
                        Copy the agent-native skill definition below to paste it into your AI agent or save it as a <code class="bg-gray-100 text-gray-800 px-1 rounded font-mono">SKILL.md</code> file in your agent's directory.
                    </p>

                    <!-- Code block -->
                    <div class="relative bg-gray-900 rounded-lg p-4 font-mono text-[10px] text-gray-300 overflow-x-auto whitespace-pre border border-gray-800 shadow-inner max-h-[250px] min-h-[160px] flex-1">
                        <code>{skillsMarkdown}</code>
                    </div>

                    <!-- Footer -->
                    <footer class="pt-4 border-t border-gray-100 flex items-center justify-end gap-3 shrink-0">
                        <button
                            type="button"
                            class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 transition-colors cursor-pointer"
                            onclick={onClose}
                        >
                            Close
                        </button>
                        <button
                            type="button"
                            class={`px-4 py-2 text-sm font-medium text-white border border-transparent rounded-md transition-colors cursor-pointer flex items-center gap-1.5 ${
                                copied 
                                    ? 'bg-emerald-600 hover:bg-emerald-700' 
                                    : 'bg-blue-600 hover:bg-blue-700'
                            }`}
                            onclick={handleCopy}
                        >
                            {#if copied}
                                <span>✓</span> Copied!
                            {:else}
                                <span>📋</span> Copy SKILL.md
                            {/if}
                        </button>
                    </footer>
                </div>
            {/if}
        </div>
    </div>
{/if}
