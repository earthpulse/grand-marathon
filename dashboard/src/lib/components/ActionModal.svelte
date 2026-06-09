<script>
    let {
        isOpen,
        action = null,
        alertId = "",
        onClose,
        onSave,
        apiUrl = "http://localhost:8000",
        predefinedActions = [],
    } = $props();

    let title = $state("");
    let description = $state("");
    let status = $state("pending");
    let predefinedId = $state("");

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
            if (action) {
                title = action.title || "";
                description = action.description || "";
                status = action.status || "pending";
                predefinedId = action.predefined_id || "";
            } else {
                title = "";
                description = "";
                status = "pending";
                predefinedId = "";
            }
        }
    });

    function handlePredefinedChange(e) {
        const selectedId = e.target.value;
        predefinedId = selectedId;
        if (selectedId) {
            const selected = predefinedActions.find(
                (item) => item.id === selectedId,
            );
            if (selected) {
                title = selected.title;
                description = selected.description;
            }
        } else {
            title = "";
            description = "";
        }
    }

    const payloadObj = $derived.by(() => {
        return {
            alert_id: action ? action.alert_id || alertId : alertId,
            title: title.trim() || "Title of the action",
            description: description.trim() || "Detailed description...",
            status,
            predefined_id: predefinedId || null,
        };
    });

    const curlPayload = $derived(JSON.stringify(payloadObj, null, 2));

    const method = $derived(action ? "PUT" : "POST");
    const path = $derived(action ? `/actions/${action.id}` : "/actions/");
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
        return `# Skill: Managing Response Actions

This skill guides AI agents and LLMs in autonomously creating, updating, and tracing response actions for confirmed environmental alerts.

## 🛠️ API Reference

### 1. Retrieve All Actions
Fetches actions, with optional filtering by alert_id or status.

* **Method**: \`GET\`
* **Path**: \`/actions/\`
* **Query Parameters**:
  * \`alert_id\` (optional): Filter actions linked to a specific alert
  * \`status\` (optional): \`pending\`, \`in_progress\`, \`completed\`, \`cancelled\`

#### cURL Example:
\`\`\`bash
curl -X GET "/actions/?alert_id=some-alert-uuid"
\`\`\`

---

### 2. Retrieve Predefined Actions List
Fetches predefined action templates to auto-fill response plans.

* **Method**: \`GET\`
* **Path**: \`/actions/predefined\`

---

### 3. Create a New Action
Generates a new response action linked to a confirmed alert.

* **Method**: \`POST\`
* **Path**: \`/actions/\`
* **Request Body Schema**:
  \`\`\`json
  {
    "alert_id": "string (Required - link to confirmed alert)",
    "title": "string (Required - action title)",
    "description": "string (Required - response instruction)",
    "status": "string (Optional: 'pending' | 'in_progress' | 'completed' | 'cancelled'. Default: 'pending')",
    "predefined_id": "string (Optional: template ID)"
  }
  \`\`\`

---

### 4. Update an Action
Modifies fields on an action (e.g. status transition, adding log details).

* **Method**: \`PUT\`
* **Path**: \`/actions/{action_id}\`

---

### 5. Delete an Action
Permanently removes a response action.

* **Method**: \`DELETE\`
* **Path**: \`/actions/{action_id}\`

## 🔍 Traceability & Logging

Every response action contains an auditable \`trace\` timeline of status updates, ensuring compliance and chronological tracking of emergency response efforts.`;
    });

    function handleCopy() {
        const textToCopy =
            activeTab === "skills" ? skillsMarkdown : currentCode;
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

        onSave({
            alert_id: action ? action.alert_id || alertId : alertId,
            title: title.trim(),
            description: description.trim(),
            status,
            predefined_id: predefinedId || null,
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
        onkeydown={(e) => e.key === "Escape" && onClose()}
    >
        <!-- Modal Content Container -->
        <div
            class="bg-white rounded-lg shadow-xl w-full max-w-xl overflow-hidden flex flex-col"
            onclick={(e) => e.stopPropagation()}
            role="dialog"
            aria-modal="true"
        >
            <!-- Header -->
            <header
                class="bg-gray-50 px-6 py-4 border-b border-gray-200 flex items-center justify-between"
            >
                <h2 class="text-xl font-semibold text-gray-800">
                    {action ? "Edit Action" : "Create New Action"}
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
                        activeTab === "form"
                            ? "border-blue-600 text-blue-600 bg-blue-50/10"
                            : "border-transparent text-gray-500 hover:text-gray-700 hover:bg-gray-50/50"
                    }`}
                    onclick={() => (activeTab = "form")}
                >
                    📝 Form Editor
                </button>
                <button
                    type="button"
                    class={`flex-1 py-3 text-sm font-semibold border-b-2 text-center transition-all cursor-pointer ${
                        activeTab === "instructions"
                            ? "border-blue-600 text-blue-600 bg-blue-50/10"
                            : "border-transparent text-gray-500 hover:text-gray-700 hover:bg-gray-50/50"
                    }`}
                    onclick={() => {
                        activeTab = "instructions";
                        copied = false;
                    }}
                >
                    💻 API Instructions
                </button>
                <button
                    type="button"
                    class={`flex-1 py-3 text-sm font-semibold border-b-2 text-center transition-all cursor-pointer ${
                        activeTab === "skills"
                            ? "border-blue-600 text-blue-600 bg-blue-50/10"
                            : "border-transparent text-gray-500 hover:text-gray-700 hover:bg-gray-50/50"
                    }`}
                    onclick={() => {
                        activeTab = "skills";
                        copied = false;
                    }}
                >
                    🤖 Agent SKILL.md
                </button>
            </div>

            <!-- Body -->
            {#if activeTab === "form"}
                <form
                    onsubmit={handleSubmit}
                    class="flex-1 overflow-y-auto p-6 space-y-4"
                >
                    {#if error}
                        <div
                            class="bg-red-50 border-l-4 border-red-500 p-3 rounded"
                        >
                            <p class="text-sm text-red-700">{error}</p>
                        </div>
                    {/if}

                    <!-- Template Selector (Only on Creation mode) -->
                    {#if !action && predefinedActions.length > 0}
                        <div>
                            <label
                                for="predefined-select"
                                class="block text-sm font-semibold text-blue-800 mb-1"
                            >
                                ✨ Predefined Action Template (Optional)
                            </label>
                            <select
                                id="predefined-select"
                                value={predefinedId}
                                onchange={handlePredefinedChange}
                                class="w-full border border-blue-200 bg-blue-50/20 text-blue-900 rounded px-3 py-2 text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                            >
                                <option value=""
                                    >-- Select a predefined template or write
                                    custom --</option
                                >
                                {#each predefinedActions as item}
                                    <option value={item.id}>{item.title}</option
                                    >
                                {/each}
                            </select>
                            <p class="text-[10px] text-gray-400 mt-1">
                                Selecting a template will auto-populate the
                                fields below.
                            </p>
                        </div>
                    {/if}

                    <div>
                        <label
                            for="action-title"
                            class="block text-sm font-medium text-gray-700 mb-1"
                        >
                            Action Title <span class="text-red-500">*</span>
                        </label>
                        <input
                            id="action-title"
                            type="text"
                            bind:value={title}
                            placeholder="e.g., Deploy support unit"
                            class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                            required
                        />
                    </div>

                    <div>
                        <label
                            for="action-description"
                            class="block text-sm font-medium text-gray-700 mb-1"
                        >
                            Instruction Description <span class="text-red-500"
                                >*</span
                            >
                        </label>
                        <textarea
                            id="action-description"
                            bind:value={description}
                            placeholder="Provide specific response instructions..."
                            rows="4"
                            class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                            required
                        ></textarea>
                    </div>

                    <div>
                        <label
                            for="action-status"
                            class="block text-sm font-medium text-gray-700 mb-1"
                        >
                            Status
                        </label>
                        <select
                            id="action-status"
                            bind:value={status}
                            class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 bg-white"
                        >
                            <option value="pending">Pending</option>
                            <option value="in_progress">In Progress</option>
                            <option value="completed">Completed</option>
                            <option value="cancelled">Cancelled</option>
                        </select>
                    </div>

                    <!-- Footer -->
                    <footer
                        class="pt-4 border-t border-gray-100 flex items-center justify-end gap-3"
                    >
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
            {:else if activeTab === "instructions"}
                <div class="flex-1 overflow-y-auto p-6 space-y-4 flex flex-col">
                    <p class="text-xs text-gray-500 leading-normal">
                        Select a tab below to inspect or copy ready-to-use
                        instructions for performing this API request in
                        different languages.
                    </p>

                    <!-- Subtabs Selector -->
                    <div
                        class="flex gap-1.5 p-1 bg-gray-100 rounded-lg self-start"
                    >
                        <button
                            type="button"
                            class={`px-3 py-1 text-xs font-semibold rounded-md transition-all cursor-pointer ${
                                activeSubTab === "curl"
                                    ? "bg-white text-gray-900 shadow-xs"
                                    : "text-gray-500 hover:text-gray-900"
                            }`}
                            onclick={() => {
                                activeSubTab = "curl";
                                copied = false;
                            }}
                        >
                            cURL
                        </button>
                        <button
                            type="button"
                            class={`px-3 py-1 text-xs font-semibold rounded-md transition-all cursor-pointer ${
                                activeSubTab === "python"
                                    ? "bg-white text-gray-900 shadow-xs"
                                    : "text-gray-500 hover:text-gray-900"
                            }`}
                            onclick={() => {
                                activeSubTab = "python";
                                copied = false;
                            }}
                        >
                            Python
                        </button>
                        <button
                            type="button"
                            class={`px-3 py-1 text-xs font-semibold rounded-md transition-all cursor-pointer ${
                                activeSubTab === "js"
                                    ? "bg-white text-gray-900 shadow-xs"
                                    : "text-gray-500 hover:text-gray-900"
                            }`}
                            onclick={() => {
                                activeSubTab = "js";
                                copied = false;
                            }}
                        >
                            JavaScript
                        </button>
                    </div>

                    <!-- Code block -->
                    <div
                        class="relative bg-gray-900 rounded-lg p-4 font-mono text-xs text-blue-400 overflow-x-auto whitespace-pre border border-gray-800 shadow-inner max-h-[250px] min-h-[160px] flex-1"
                    >
                        <code>{currentCode}</code>
                    </div>

                    <!-- Footer -->
                    <footer
                        class="pt-4 border-t border-gray-100 flex items-center justify-end gap-3 shrink-0"
                    >
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
                                    ? "bg-emerald-600 hover:bg-emerald-700"
                                    : "bg-blue-600 hover:bg-blue-700"
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
            {:else if activeTab === "skills"}
                <div class="flex-1 overflow-y-auto p-6 space-y-4 flex flex-col">
                    <p class="text-xs text-gray-500 leading-normal">
                        Copy the agent-native skill definition below to paste it
                        into your AI agent or save it as a <code
                            class="bg-gray-100 text-gray-800 px-1 rounded font-mono"
                            >SKILL.md</code
                        > file in your agent's directory.
                    </p>

                    <!-- Code block -->
                    <div
                        class="relative bg-gray-900 rounded-lg p-4 font-mono text-[10px] text-gray-300 overflow-x-auto whitespace-pre border border-gray-800 shadow-inner max-h-[250px] min-h-[160px] flex-1"
                    >
                        <code>{skillsMarkdown}</code>
                    </div>

                    <!-- Footer -->
                    <footer
                        class="pt-4 border-t border-gray-100 flex items-center justify-end gap-3 shrink-0"
                    >
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
                                    ? "bg-emerald-600 hover:bg-emerald-700"
                                    : "bg-blue-600 hover:bg-blue-700"
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
