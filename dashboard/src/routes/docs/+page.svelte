<script>
	let activeTab = $state("chapter1");

	const chapters = [
		{
			id: "chapter1",
			title: "1. Dashboard",
			steps: "Steps 1 - 3",
			icon: "🔥",
		},
		{
			id: "chapter2",
			title: "2. Confirm",
			steps: "Steps 4 - 6",
			icon: "✅",
		},
		{
			id: "chapter3",
			title: "3. Alerts",
			steps: "Steps 7 - 9",
			icon: "🔔",
		},
		{
			id: "chapter4",
			title: "4. Actions",
			steps: "Steps 10 - 13",
			icon: "🚀",
		},
		{
			id: "chapter5",
			title: "5. Report",
			steps: "Steps 14 - 17",
			icon: "📋",
		},
	];

	function selectTab(id) {
		activeTab = id;
	}
</script>

<div class="flex-1 flex flex-col h-full bg-slate-50 overflow-hidden">
	<!-- Top Bar -->
	<header
		class="bg-white border-b border-slate-200/80 px-6 py-4 flex-shrink-0 flex items-center justify-between shadow-xs"
	>
		<div class="flex items-center gap-3">
			<span class="text-3xl">📚</span>
			<div>
				<h1
					class="text-xl font-black text-slate-900 tracking-tight flex items-center gap-2"
				>
					Documentation
					<span
						class="text-xs font-bold bg-[#e6f4f1] text-[#0f766e] px-2 py-0.5 rounded-full uppercase tracking-wider font-mono"
						>Operator Manual</span
					>
				</h1>
				<p class="text-xs text-slate-500 mt-0.5 leading-none">
					A complete walkthrough of the Confirm and Actions
					capabilities.
				</p>
			</div>
		</div>
	</header>

	<!-- Main Workspace Split -->
	<div class="flex-1 flex flex-col md:flex-row min-h-0 overflow-hidden">
		<!-- Documentation Sidebar (Table of Contents / Chapters) -->
		<aside
			class="w-full md:w-64 bg-white border-r border-slate-200/80 p-4 flex-shrink-0 flex flex-col gap-3 min-h-0 overflow-y-auto"
		>
			<div class="px-2 py-1">
				<h2
					class="text-xs font-extrabold text-slate-400 uppercase tracking-widest font-mono"
				>
					Walkthrough
				</h2>
			</div>

			<div
				class="flex flex-row md:flex-col gap-2 overflow-x-auto md:overflow-x-visible pb-2 md:pb-0"
			>
				{#each chapters as ch}
					<button
						onclick={() => selectTab(ch.id)}
						class="flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all text-left shrink-0 md:shrink border {activeTab ===
						ch.id
							? 'bg-[#e6f4f1] text-[#0f766e] border-[#0f766e]/20 font-bold shadow-xs'
							: 'text-slate-600 border-transparent hover:bg-slate-50 hover:text-slate-900 font-medium'}"
					>
						<span class="text-lg flex-shrink-0">{ch.icon}</span>
						<div class="min-w-0">
							<p class="text-xs leading-none truncate">
								{ch.title}
							</p>
							<p
								class="text-[10px] opacity-75 mt-1 leading-none font-mono"
							>
								{ch.steps}
							</p>
						</div>
					</button>
				{/each}
			</div>

			<div
				class="mt-auto border-t border-slate-100 pt-4 hidden md:block px-2 space-y-3"
			>
				<div
					class="bg-teal-50/50 rounded-xl p-3 border border-teal-100/30"
				>
					<div
						class="flex items-center gap-1.5 text-xs font-bold text-teal-800"
					>
						<span>⚡</span> Confirm & Actions Pillars
					</div>
					<p class="text-[10px] text-teal-700 mt-1.5 leading-relaxed">
						The platform's operational integrity relies heavily on
						the <strong>Confirm</strong> page (verifying raw sensor
						signals using geolocated web scrapers) and the
						<strong>Actions</strong> page (prioritizing assets and deploying
						SOPs).
					</p>
				</div>

				<div class="bg-slate-50 rounded-xl p-3 border border-slate-100">
					<div
						class="flex items-center gap-1.5 text-xs font-bold text-slate-700"
					>
						<span>🛡️</span> Incident Audit Trail
					</div>
					<p
						class="text-[10px] text-slate-500 mt-1.5 leading-relaxed"
					>
						All actions, alerts, and evidence confirmation stages
						shown here compile a tamper-proof audit trail of the
						emergency response.
					</p>
				</div>
			</div>
		</aside>

		<!-- Content Pane -->
		<main class="flex-1 overflow-y-auto p-6 min-w-0">
			<!-- Header of Chapter -->
			{#if activeTab === "chapter1"}
				<div class="space-y-8 max-w-5xl mx-auto pb-12">
					<div class="border-b border-slate-200 pb-4">
						<span
							class="text-xs font-extrabold text-[#0f766e] uppercase tracking-widest font-mono"
							>Walkthrough Chapter 1</span
						>
						<h2 class="text-2xl font-black text-slate-900 mt-1">
							Dashboard & Risk Assessment
						</h2>
						<p class="text-sm text-slate-500 mt-1">
							Understanding conditions to fire occurrence and
							breaking down risk into explainable components.
						</p>
					</div>

					<!-- Step 1 -->
					<div
						class="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden grid grid-cols-1 lg:grid-cols-12"
					>
						<div
							class="p-6 lg:col-span-5 flex flex-col justify-between border-b lg:border-b-0 lg:border-r border-slate-100"
						>
							<div>
								<div class="flex items-center gap-2">
									<span
										class="flex items-center justify-center bg-slate-100 text-slate-700 font-extrabold text-xs w-6 h-6 rounded-full border border-slate-200 font-mono"
										>1</span
									>
									<h3
										class="text-sm font-black text-slate-900"
									>
										Baseline Observation Window
									</h3>
								</div>

								<div class="mt-4 space-y-3">
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											Operator Action
										</h4>
										<p
											class="text-xs text-slate-700 mt-1 font-medium bg-slate-50 p-2 rounded-lg border border-slate-100"
										>
											Open the target wildfire scenario.
										</p>
									</div>
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											System Output
										</h4>
										<p
											class="text-xs text-slate-600 mt-1 leading-relaxed"
										>
											Dashboard automatically centers the
											map onto the selected area under
											observation, loading sentinel
											imagery and risk maps.
										</p>
									</div>
								</div>
							</div>

							<div class="mt-6 pt-4 border-t border-slate-100">
								<span
									class="text-[9px] font-extrabold bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full uppercase tracking-wider font-mono"
									>Why it matters</span
								>
								<p
									class="text-[11px] text-slate-500 mt-1.5 leading-relaxed"
								>
									Sets the operational context for the
									walkthrough, showing how emergency personnel
									can pre-select and monitor critical regions
									under observation.
								</p>
							</div>
						</div>

						<!-- Visual Mockup Column -->
						<div
							class="p-6 lg:col-span-7 bg-slate-50/50 flex flex-col justify-center"
						>
							<h4
								class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono mb-3"
							>
								System View Example
							</h4>
							<div
								class="bg-white rounded-xl border border-slate-200 p-4 shadow-xs relative"
							>
								<div
									class="flex items-center justify-between border-b border-slate-100 pb-2.5 mb-3"
								>
									<div class="flex items-center gap-2">
										<span
											class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"
										></span>
										<span
											class="text-[10px] font-bold text-slate-700"
											>Scenario Active: Target Region</span
										>
									</div>
									<span
										class="text-[9px] bg-slate-100 text-slate-600 font-medium px-2 py-0.5 rounded-md"
										>Baseline State</span
									>
								</div>

								<div class="space-y-3">
									<div
										class="flex items-center justify-between text-xs text-slate-600 bg-slate-50 p-2.5 rounded-lg border border-slate-100"
									>
										<span class="font-medium"
											>Selected Location:</span
										>
										<span class="font-bold text-slate-800"
											>Observation Zone</span
										>
									</div>
									<div
										class="flex items-center justify-between text-xs text-slate-600 bg-slate-50 p-2.5 rounded-lg border border-slate-100"
									>
										<span class="font-medium"
											>Active Timeline Date:</span
										>
										<span class="font-bold text-blue-600"
											>August 15
										</span>
									</div>

									<div
										class="border border-slate-150 rounded-lg h-24 overflow-hidden relative flex items-center justify-center bg-slate-200"
									>
										<span
											class="absolute top-2 left-2 text-[9px] bg-white/90 font-bold px-1.5 py-0.5 rounded shadow-xs text-slate-700"
											>🛰️ Sentinel-2 L2A</span
										>
										<div class="text-center text-slate-400">
											<span class="text-xl">🗺️</span>
											<p
												class="text-[9px] font-semibold mt-1"
											>
												Satellite Base Map Loaded
											</p>
											<p class="text-[8px] opacity-75">
												No thermal anomalies detected in
												the observation grid.
											</p>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>

					<!-- Step 2 -->
					<div
						class="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden grid grid-cols-1 lg:grid-cols-12"
					>
						<div
							class="p-6 lg:col-span-5 flex flex-col justify-between border-b lg:border-b-0 lg:border-r border-slate-100"
						>
							<div>
								<div class="flex items-center gap-2">
									<span
										class="flex items-center justify-center bg-slate-100 text-slate-700 font-extrabold text-xs w-6 h-6 rounded-full border border-slate-200 font-mono"
										>2</span
									>
									<h3
										class="text-sm font-black text-slate-900"
									>
										View the Risk Map
									</h3>
								</div>

								<div class="mt-4 space-y-3">
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											Operator Action
										</h4>
										<p
											class="text-xs text-slate-700 mt-1 font-medium bg-slate-50 p-2 rounded-lg border border-slate-100"
										>
											View the integrated risk map layer.
										</p>
									</div>
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											System Output
										</h4>
										<p
											class="text-xs text-slate-600 mt-1 leading-relaxed"
										>
											Map displays hazard, exposure and
											vulnerability components combined
											into a unified risk representation.
										</p>
									</div>
								</div>
							</div>

							<div class="mt-6 pt-4 border-t border-slate-100">
								<span
									class="text-[9px] font-extrabold bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full uppercase tracking-wider font-mono"
									>Why it matters</span
								>
								<p
									class="text-[11px] text-slate-500 mt-1.5 leading-relaxed"
								>
									Shows that risk is not only fire danger
									(hazard), but fire danger combined with what
									may actually be affected (exposure and
									vulnerability). This avoids treating remote
									deep-forest alerts the same as
									near-settlement alerts.
								</p>
							</div>
						</div>

						<!-- Visual Mockup Column -->
						<div
							class="p-6 lg:col-span-7 bg-slate-50/50 flex flex-col justify-center"
						>
							<h4
								class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono mb-3"
							>
								System View Example
							</h4>
							<div
								class="bg-white rounded-xl border border-slate-200 p-4 shadow-xs relative"
							>
								<div
									class="text-[10px] font-bold text-slate-700 mb-2 flex items-center gap-1"
								>
									<span>📊</span> Risk Components Breakdown
								</div>

								<div class="space-y-2.5">
									<div>
										<div
											class="flex justify-between text-[10px] mb-1"
										>
											<span
												class="font-medium text-slate-500"
												>1. Meteorological Hazard (FWI)</span
											>
											<span
												class="font-extrabold text-red-600"
												>82% - Critical</span
											>
										</div>
										<div
											class="w-full bg-slate-100 h-2 rounded-full overflow-hidden"
										>
											<div
												class="bg-red-500 h-full rounded-full"
												style="width: 82%"
											></div>
										</div>
									</div>

									<div>
										<div
											class="flex justify-between text-[10px] mb-1"
										>
											<span
												class="font-medium text-slate-500"
												>2. Population & Asset Exposure</span
											>
											<span
												class="font-extrabold text-amber-600"
												>65% - High</span
											>
										</div>
										<div
											class="w-full bg-slate-100 h-2 rounded-full overflow-hidden"
										>
											<div
												class="bg-amber-500 h-full rounded-full"
												style="width: 65%"
											></div>
										</div>
									</div>

									<div>
										<div
											class="flex justify-between text-[10px] mb-1"
										>
											<span
												class="font-medium text-slate-500"
												>3. Territorial Vulnerability
												(Access/Escape)</span
											>
											<span
												class="font-extrabold text-amber-500"
												>55% - Moderate</span
											>
										</div>
										<div
											class="w-full bg-slate-100 h-2 rounded-full overflow-hidden"
										>
											<div
												class="bg-amber-500 h-full rounded-full"
												style="width: 55%"
											></div>
										</div>
									</div>

									<div
										class="pt-2 border-t border-slate-150 mt-1"
									>
										<div
											class="flex justify-between items-center bg-red-50 p-2 rounded-lg border border-red-100"
										>
											<span
												class="text-[10px] font-black text-red-800 uppercase tracking-wider font-mono"
												>Combined Risk Score</span
											>
											<span
												class="text-xs font-black text-red-700"
												>72 / 100 (HIGH RISK)</span
											>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>

					<!-- Step 3 -->
					<div
						class="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden grid grid-cols-1 lg:grid-cols-12"
					>
						<div
							class="p-6 lg:col-span-5 flex flex-col justify-between border-b lg:border-b-0 lg:border-r border-slate-100"
						>
							<div>
								<div class="flex items-center gap-2">
									<span
										class="flex items-center justify-center bg-slate-100 text-slate-700 font-extrabold text-xs w-6 h-6 rounded-full border border-slate-200 font-mono"
										>3</span
									>
									<h3
										class="text-sm font-black text-slate-900"
									>
										Toggle Risk Components
									</h3>
								</div>

								<div class="mt-4 space-y-3">
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											Operator Action
										</h4>
										<p
											class="text-xs text-slate-700 mt-1 font-medium bg-slate-50 p-2 rounded-lg border border-slate-100"
										>
											Toggle between risk components
											(hazard, exposure, vulnerability and
											combined risk).
										</p>
									</div>
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											System Output
										</h4>
										<p
											class="text-xs text-slate-600 mt-1 leading-relaxed"
										>
											Operator switches between hazard,
											exposure, vulnerability and combined
											risk indices on the active map
											display, exploring future dates with
											early fires.
										</p>
									</div>
								</div>
							</div>

							<div class="mt-6 pt-4 border-t border-slate-100">
								<span
									class="text-[9px] font-extrabold bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full uppercase tracking-wider font-mono"
									>Why it matters</span
								>
								<p
									class="text-[11px] text-slate-500 mt-1.5 leading-relaxed"
								>
									Makes the analytical logic explainable to
									judges and legal bodies. Demonstrates
									exactly what components caused a specific
									region to be classified as high risk.
								</p>
							</div>
						</div>

						<!-- Visual Mockup Column -->
						<div
							class="p-6 lg:col-span-7 bg-slate-50/50 flex flex-col justify-center"
						>
							<h4
								class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono mb-3"
							>
								System View Example
							</h4>
							<div
								class="bg-white rounded-xl border border-slate-200 p-4 shadow-xs relative"
							>
								<span
									class="absolute top-2 right-2 text-[8px] bg-amber-50 text-amber-700 font-bold px-1.5 py-0.5 rounded shadow-xs"
									>Timeline: Date Advanced (Early Anomaly
									Signs)</span
								>
								<div
									class="text-[10px] font-bold text-slate-700 mb-2.5 flex items-center gap-1.5 font-mono"
								>
									<span>⚙️</span> Map Layers Control Panel
								</div>

								<div class="space-y-2">
									<label
										class="flex items-center gap-2.5 p-2 rounded-lg bg-slate-50 hover:bg-slate-100/50 border border-slate-150 cursor-pointer transition-all"
									>
										<input
											type="radio"
											name="docs-layer"
											class="text-teal-600 focus:ring-teal-500 h-3.5 w-3.5"
											checked
										/>
										<div class="text-left">
											<span
												class="text-[11px] font-bold text-slate-800"
												>Combined Risk Index
												(Multi-criteria)</span
											>
											<p
												class="text-[9px] text-slate-500 leading-none"
											>
												Hazard × Exposure ×
												Vulnerability
											</p>
										</div>
									</label>

									<label
										class="flex items-center gap-2.5 p-2 rounded-lg bg-white hover:bg-slate-100/50 border border-transparent cursor-pointer transition-all"
									>
										<input
											type="radio"
											name="docs-layer"
											class="text-teal-600 focus:ring-teal-500 h-3.5 w-3.5"
										/>
										<div class="text-left">
											<span
												class="text-[11px] font-medium text-slate-700"
												>Component A: Weather Fire
												Danger (FWI)</span
											>
											<p
												class="text-[9px] text-slate-400 leading-none"
											>
												Wind speed, relative humidity,
												fuel dryness
											</p>
										</div>
									</label>

									<label
										class="flex items-center gap-2.5 p-2 rounded-lg bg-white hover:bg-slate-100/50 border border-transparent cursor-pointer transition-all"
									>
										<input
											type="radio"
											name="docs-layer"
											class="text-teal-600 focus:ring-teal-500 h-3.5 w-3.5"
										/>
										<div class="text-left">
											<span
												class="text-[11px] font-medium text-slate-700"
												>Component B: Exposed Inhabited
												Settlements</span
											>
											<p
												class="text-[9px] text-slate-400 leading-none"
											>
												Urban-wildland interface
												intersections
											</p>
										</div>
									</label>
								</div>
							</div>
						</div>
					</div>
				</div>
			{/if}

			{#if activeTab === "chapter2"}
				<div class="space-y-8 max-w-5xl mx-auto pb-12">
					<div class="border-b border-slate-200 pb-4">
						<span
							class="text-xs font-extrabold text-teal-700 uppercase tracking-widest font-mono"
							>CRITICAL PHASE: STEP-BY-STEP</span
						>
						<h2 class="text-2xl font-black text-slate-900 mt-1">
							The "Confirm" Step: Multi-Source Verification
						</h2>
						<p class="text-sm text-slate-500 mt-1">
							Aggregating social media scraping, geolocated
							reports, and civil protection channels to verify
							candidate alerts. This critical gatekeeper step
							filters out false alarms before deployable assets
							are committed.
						</p>
					</div>

					<!-- Step 4 -->
					<div
						class="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden grid grid-cols-1 lg:grid-cols-12"
					>
						<div
							class="p-6 lg:col-span-5 flex flex-col justify-between border-b lg:border-b-0 lg:border-r border-slate-100"
						>
							<div>
								<div class="flex items-center gap-2">
									<span
										class="flex items-center justify-center bg-slate-100 text-slate-700 font-extrabold text-xs w-6 h-6 rounded-full border border-slate-200 font-mono"
										>4</span
									>
									<h3
										class="text-sm font-black text-slate-900"
									>
										Open Confirmation Page
									</h3>
								</div>

								<div class="mt-4 space-y-3">
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											Operator Action
										</h4>
										<p
											class="text-xs text-slate-700 mt-1 font-medium bg-slate-50 p-2 rounded-lg border border-slate-100"
										>
											Navigate to the 'Confirm' module
											workspace.
										</p>
									</div>
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											System Output
										</h4>
										<p
											class="text-xs text-slate-600 mt-1 leading-relaxed"
										>
											Page shows prepared scraped sources,
											web/social evidence, manual
											confirmation option and API
											confirmation option.
										</p>
									</div>
								</div>
							</div>

							<div class="mt-6 pt-4 border-t border-slate-100">
								<span
									class="text-[9px] font-extrabold bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full uppercase tracking-wider font-mono"
									>Why it matters</span
								>
								<p
									class="text-[11px] text-slate-500 mt-1.5 leading-relaxed"
								>
									Demonstrates how the system checks whether
									the alert deserves escalation using
									multi-spectral evidence correlation.
								</p>
							</div>
						</div>

						<!-- Visual Mockup Column -->
						<div
							class="p-6 lg:col-span-7 bg-slate-50/50 flex flex-col justify-center"
						>
							<h4
								class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono mb-3"
							>
								System View Example
							</h4>
							<div
								class="bg-white rounded-xl border border-slate-200 p-4 shadow-xs relative"
							>
								<div
									class="text-[10px] font-bold text-slate-700 mb-2 flex items-center justify-between border-b border-slate-100 pb-1.5 font-mono"
								>
									<span class="flex items-center gap-1"
										>🌐 Real-time Evidence Aggregation</span
									>
									<span
										class="text-[8px] bg-teal-100 text-teal-800 font-extrabold px-1.5 py-0.5 rounded"
										>Scraper Online</span
									>
								</div>

								<div class="space-y-2">
									<div
										class="border border-teal-50 bg-[#e6f4f1]/30 p-2 rounded-lg"
									>
										<div
											class="flex items-center justify-between"
										>
											<span
												class="text-[9px] text-[#0f766e] font-extrabold"
												>📻 Civil Protection Feed</span
											>
											<span
												class="text-[8px] text-slate-400 font-mono font-normal"
												>14:18 (3m ago)</span
											>
										</div>
										<p
											class="text-[10px] text-slate-700 mt-1 font-normal leading-relaxed"
										>
											"Units dispatched to investigate
											vegetation fire ignition near local
											high-risk forest area."
										</p>
									</div>

									<div
										class="border border-slate-150 p-2 rounded-lg"
									>
										<div
											class="flex items-center justify-between"
										>
											<span
												class="text-[9px] text-blue-600 font-bold"
												>📱 Social Media Report</span
											>
											<span
												class="text-[8px] text-slate-400 font-mono font-normal"
												>14:16 (5m ago)</span
											>
										</div>
										<p
											class="text-[10px] text-slate-700 mt-1 font-normal leading-relaxed"
										>
											"@Emergency112 Column of dark smoke
											rising behind the hill. Smells like
											pine. #ForestFire #Fire"
										</p>
									</div>
								</div>
							</div>
						</div>
					</div>

					<!-- Step 5 -->
					<div
						class="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden grid grid-cols-1 lg:grid-cols-12"
					>
						<div
							class="p-6 lg:col-span-5 flex flex-col justify-between border-b lg:border-b-0 lg:border-r border-slate-100"
						>
							<div>
								<div class="flex items-center gap-2">
									<span
										class="flex items-center justify-center bg-slate-100 text-slate-700 font-extrabold text-xs w-6 h-6 rounded-full border border-slate-200 font-mono"
										>5</span
									>
									<h3
										class="text-sm font-black text-slate-900"
									>
										Confirm the Alert
									</h3>
								</div>

								<div class="mt-4 space-y-3">
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											Operator Action
										</h4>
										<p
											class="text-xs text-slate-700 mt-1 font-medium bg-slate-50 p-2 rounded-lg border border-slate-100"
										>
											Execute validation (manually using
											the confirm button or wait for the
											programmatic webhook integration).
										</p>
									</div>
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											System Output
										</h4>
										<p
											class="text-xs text-slate-600 mt-1 leading-relaxed"
										>
											Operator validates evidence
											manually, or confirmation arrives
											through the API.
										</p>
									</div>
								</div>
							</div>

							<div class="mt-6 pt-4 border-t border-slate-100">
								<span
									class="text-[9px] font-extrabold bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full uppercase tracking-wider font-mono"
									>Why it matters</span
								>
								<p
									class="text-[11px] text-slate-500 mt-1.5 leading-relaxed"
								>
									Shows the “Confirm” part of the product and
									reduces false positives, protecting limited
									emergency response assets.
								</p>
							</div>
						</div>

						<!-- Visual Mockup Column -->
						<div
							class="p-6 lg:col-span-7 bg-slate-50/50 flex flex-col justify-center"
						>
							<h4
								class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono mb-3"
							>
								System View Example
							</h4>
							<div
								class="bg-white rounded-xl border border-slate-200 p-4 shadow-xs relative text-center"
							>
								<p
									class="text-[11px] text-slate-700 font-bold mb-3"
								>
									Operator Decision Terminal
								</p>
								<div class="flex gap-3 justify-center">
									<button
										class="px-3 py-1.5 text-[10px] font-bold bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg cursor-not-allowed"
									>
										Dismiss (False Alarm)
									</button>
									<button
										class="px-3 py-1.5 text-[10px] font-extrabold bg-[#0f766e] hover:bg-[#0d5e58] text-white rounded-lg shadow-sm cursor-not-allowed"
									>
										Acknowledge & Confirm Alert ✓
									</button>
								</div>
								<div
									class="mt-3 text-[8px] text-slate-400 bg-slate-50 p-1.5 rounded border border-slate-100 font-mono"
								>
									API command equivalent: PATCH
									/api/alerts/ALT-FIRE-082/confirm
								</div>
							</div>
						</div>
					</div>

					<!-- Step 6 -->
					<div
						class="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden grid grid-cols-1 lg:grid-cols-12"
					>
						<div
							class="p-6 lg:col-span-5 flex flex-col justify-between border-b lg:border-b-0 lg:border-r border-slate-100"
						>
							<div>
								<div class="flex items-center gap-2">
									<span
										class="flex items-center justify-center bg-slate-100 text-slate-700 font-extrabold text-xs w-6 h-6 rounded-full border border-slate-200 font-mono"
										>6</span
									>
									<h3
										class="text-sm font-black text-slate-900"
									>
										Promote Alert
									</h3>
								</div>

								<div class="mt-4 space-y-3">
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											Operator Action
										</h4>
										<p
											class="text-xs text-slate-700 mt-1 font-medium bg-slate-50 p-2 rounded-lg border border-slate-100"
										>
											Watch the transition of the alert
											into confirmed states.
										</p>
									</div>
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											System Output
										</h4>
										<p
											class="text-xs text-slate-600 mt-1 leading-relaxed"
										>
											System escalates the candidate alert
											into a confirmed alert.
										</p>
									</div>
								</div>
							</div>

							<div class="mt-6 pt-4 border-t border-slate-100">
								<span
									class="text-[9px] font-extrabold bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full uppercase tracking-wider font-mono"
									>Why it matters</span
								>
								<p
									class="text-[11px] text-slate-500 mt-1.5 leading-relaxed"
								>
									Shows the transition from initial raw risk
									signal to an actionable, prioritized
									operational alert.
								</p>
							</div>
						</div>

						<!-- Visual Mockup Column -->
						<div
							class="p-6 lg:col-span-7 bg-slate-50/50 flex flex-col justify-center"
						>
							<h4
								class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono mb-3"
							>
								System View Example
							</h4>
							<div
								class="bg-white rounded-xl border border-slate-200 p-4 shadow-xs relative overflow-hidden"
							>
								<div
									class="absolute left-0 top-0 bottom-0 w-1 bg-red-600"
								></div>
								<div
									class="flex justify-between items-center bg-red-50/50 p-2 rounded-lg border border-red-100"
								>
									<div class="flex items-center gap-1.5">
										<span
											class="w-2 h-2 rounded-full bg-red-600 animate-ping"
										></span>
										<span
											class="text-[10px] font-bold text-red-800 uppercase tracking-wide"
											>CONFIRMED ACTIVE INCIDENT</span
										>
									</div>
									<span
										class="text-[9px] font-mono text-slate-500"
										>14:30 UTC</span
									>
								</div>

								<div
									class="mt-2 text-[10px] text-slate-600 leading-snug font-normal"
								>
									<strong>Status Updated:</strong> Candidate alert
									promoted to active incident object. Standard
									Response Protocol activated.
								</div>
							</div>
						</div>
					</div>
				</div>
			{/if}

			{#if activeTab === "chapter3"}
				<div class="space-y-8 max-w-5xl mx-auto pb-12">
					<div class="border-b border-slate-200 pb-4">
						<span
							class="text-xs font-extrabold text-[#0f766e] uppercase tracking-widest font-mono"
							>Walkthrough Chapter 3</span
						>
						<h2 class="text-2xl font-black text-slate-900 mt-1">
							Multi-Channel Ingestion & Alert Processing
						</h2>
						<p class="text-sm text-slate-500 mt-1">
							How the system automatically registers hot targets
							from sensors, webhooks, or manual dispatches.
						</p>
					</div>

					<!-- Step 7 -->
					<div
						class="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden grid grid-cols-1 lg:grid-cols-12"
					>
						<div
							class="p-6 lg:col-span-5 flex flex-col justify-between border-b lg:border-b-0 lg:border-r border-slate-100"
						>
							<div>
								<div class="flex items-center gap-2">
									<span
										class="flex items-center justify-center bg-slate-100 text-slate-700 font-extrabold text-xs w-6 h-6 rounded-full border border-slate-200 font-mono"
										>7</span
									>
									<h3
										class="text-sm font-black text-slate-900"
									>
										Generate or Receive Alert
									</h3>
								</div>

								<div class="mt-4 space-y-3">
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											Operator Action
										</h4>
										<p
											class="text-xs text-slate-700 mt-1 font-medium bg-slate-50 p-2 rounded-lg border border-slate-100"
										>
											Observe alert generation
											(automatically, manually with a
											button, or through an incoming API
											webhook).
										</p>
									</div>
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											System Output
										</h4>
										<p
											class="text-xs text-slate-600 mt-1 leading-relaxed"
										>
											Alert is created automatically,
											manually with a button, or through
											the API.
										</p>
									</div>
								</div>
							</div>

							<div class="mt-6 pt-4 border-t border-slate-100">
								<span
									class="text-[9px] font-extrabold bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full uppercase tracking-wider font-mono"
									>Why it matters</span
								>
								<p
									class="text-[11px] text-slate-500 mt-1.5 leading-relaxed"
								>
									Demonstrates multiple ways the system can
									receive operational signals:
									programmatically via IoT fields, active
									human command, or third-party webhooks.
								</p>
							</div>
						</div>

						<!-- Visual Mockup Column -->
						<div
							class="p-6 lg:col-span-7 bg-slate-50/50 flex flex-col justify-center"
						>
							<h4
								class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono mb-3"
							>
								System View Example
							</h4>
							<div
								class="bg-white rounded-xl border border-slate-200 p-4 shadow-xs relative"
							>
								<div
									class="text-[10px] font-bold text-slate-700 mb-3 border-b border-slate-100 pb-1.5"
								>
									🔌 Ingestion Channel Status
								</div>
								<div class="grid grid-cols-3 gap-2.5">
									<div
										class="border border-slate-100 rounded-lg p-2 text-center bg-slate-50"
									>
										<span class="text-md">🛰️</span>
										<p
											class="text-[10px] font-bold text-slate-800 mt-1 leading-none"
										>
											Automated API
										</p>
										<span
											class="text-[8px] bg-emerald-100 text-emerald-800 font-extrabold px-1 py-0.5 rounded mt-1 inline-block"
											>Active</span
										>
									</div>
									<div
										class="border border-teal-100 rounded-lg p-2 text-center bg-[#e6f4f1]"
									>
										<span class="text-md">🖱️</span>
										<p
											class="text-[10px] font-bold text-slate-800 mt-1 leading-none"
										>
											UI Manual
										</p>
										<span
											class="text-[8px] bg-[#0f766e] text-white font-extrabold px-1 py-0.5 rounded mt-1 inline-block"
											>+ Create</span
										>
									</div>
									<div
										class="border border-slate-100 rounded-lg p-2 text-center bg-slate-50"
									>
										<span class="text-md">🔌</span>
										<p
											class="text-[10px] font-bold text-slate-800 mt-1 leading-none"
										>
											External Webhook
										</p>
										<span
											class="text-[8px] bg-emerald-100 text-emerald-800 font-extrabold px-1 py-0.5 rounded mt-1 inline-block"
											>POST Ready</span
										>
									</div>
								</div>
							</div>
						</div>
					</div>

					<!-- Step 8 -->
					<div
						class="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden grid grid-cols-1 lg:grid-cols-12"
					>
						<div
							class="p-6 lg:col-span-5 flex flex-col justify-between border-b lg:border-b-0 lg:border-r border-slate-100"
						>
							<div>
								<div class="flex items-center gap-2">
									<span
										class="flex items-center justify-center bg-slate-100 text-slate-700 font-extrabold text-xs w-6 h-6 rounded-full border border-slate-200 font-mono"
										>8</span
									>
									<h3
										class="text-sm font-black text-slate-900"
									>
										Open Alert Details
									</h3>
								</div>

								<div class="mt-4 space-y-3">
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											Operator Action
										</h4>
										<p
											class="text-xs text-slate-700 mt-1 font-medium bg-slate-50 p-2 rounded-lg border border-slate-100"
										>
											Click on any alert in the list panel
											to open its detail views.
										</p>
									</div>
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											System Output
										</h4>
										<p
											class="text-xs text-slate-600 mt-1 leading-relaxed"
										>
											Alert card shows location,
											timestamp, alert level, risk score
											and current status.
										</p>
									</div>
								</div>
							</div>

							<div class="mt-6 pt-4 border-t border-slate-100">
								<span
									class="text-[9px] font-extrabold bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full uppercase tracking-wider font-mono"
									>Why it matters</span
								>
								<p
									class="text-[11px] text-slate-500 mt-1.5 leading-relaxed"
								>
									Turns raw spatial geographic sensor data
									into a structured operational alert object
									with real-time tracking.
								</p>
							</div>
						</div>

						<!-- Visual Mockup Column -->
						<div
							class="p-6 lg:col-span-7 bg-slate-50/50 flex flex-col justify-center"
						>
							<h4
								class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono mb-3"
							>
								System View Example
							</h4>
							<div
								class="bg-white rounded-xl border border-slate-200 p-4 shadow-xs relative overflow-hidden"
							>
								<div
									class="absolute left-0 top-0 bottom-0 w-1 bg-amber-500"
								></div>
								<div class="flex justify-between items-start">
									<div>
										<span
											class="text-[8px] bg-amber-50 border border-amber-200 text-amber-700 font-bold uppercase px-2 py-0.5 rounded-full"
											>Warning</span
										>
										<h3
											class="text-xs font-bold text-slate-900 mt-1"
										>
											ALT-FIRE-082: Forest Fire Signal
										</h3>
									</div>
									<span
										class="text-[9px] font-bold text-slate-500 bg-slate-100 px-2 py-0.5 rounded"
										>Unconfirmed</span
									>
								</div>

								<p
									class="text-[10px] text-slate-500 mt-2 leading-relaxed font-normal"
								>
									Detected hotspot clusters in proximity to
									protected natural pine woodland in target
									forest.
								</p>
								ongoing

								<div
									class="grid grid-cols-2 gap-2 mt-3 pt-2.5 border-t border-slate-100 text-[9px]"
								>
									<div class="bg-slate-50 p-1.5 rounded">
										<span
											class="text-slate-400 block font-medium"
											>Coordinates</span
										>
										<span class="font-bold text-slate-700"
											>41.9542° N, -7.4231° W</span
										>
									</div>
									<div class="bg-slate-50 p-1.5 rounded">
										<span
											class="text-slate-400 block font-medium"
											>Risk Score Impact</span
										>
										<span class="font-bold text-red-600"
											>78 / 100</span
										>
									</div>
								</div>
							</div>
						</div>
					</div>

					<!-- Step 9 -->
					<div
						class="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden grid grid-cols-1 lg:grid-cols-12"
					>
						<div
							class="p-6 lg:col-span-5 flex flex-col justify-between border-b lg:border-b-0 lg:border-r border-slate-100"
						>
							<div>
								<div class="flex items-center gap-2">
									<span
										class="flex items-center justify-center bg-slate-100 text-slate-700 font-extrabold text-xs w-6 h-6 rounded-full border border-slate-200 font-mono"
										>9</span
									>
									<h3
										class="text-sm font-black text-slate-900"
									>
										Review Alert Type & Driver
									</h3>
								</div>

								<div class="mt-4 space-y-3">
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											Operator Action
										</h4>
										<p
											class="text-xs text-slate-700 mt-1 font-medium bg-slate-50 p-2 rounded-lg border border-slate-100"
										>
											Inspect diagnostic classification
											panel on the alert asset.
										</p>
									</div>
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											System Output
										</h4>
										<p
											class="text-xs text-slate-600 mt-1 leading-relaxed"
										>
											Alert card shows type, main driver
											and suggested confirmation route.
										</p>
									</div>
								</div>
							</div>

							<div class="mt-6 pt-4 border-t border-slate-100">
								<span
									class="text-[9px] font-extrabold bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full uppercase tracking-wider font-mono"
									>Why it matters</span
								>
								<p
									class="text-[11px] text-slate-500 mt-1.5 leading-relaxed"
								>
									Differentiates whether the alert is
									hazard-driven, exposure-driven or
									evidence-driven, proposing specific
									validation routes for responders.
								</p>
							</div>
						</div>

						<!-- Visual Mockup Column -->
						<div
							class="p-6 lg:col-span-7 bg-slate-50/50 flex flex-col justify-center"
						>
							<h4
								class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono mb-3"
							>
								System View Example
							</h4>
							<div
								class="bg-white rounded-xl border border-slate-200 p-4 shadow-xs relative"
							>
								<div
									class="text-[10px] font-bold text-slate-700 mb-2 flex items-center gap-1.5 font-mono"
								>
									<span>🧠</span> Intelligent Driver Diagnostic
								</div>
								<div class="space-y-2">
									<div
										class="flex items-center justify-between text-[10px] p-2 bg-amber-50 rounded-lg border border-amber-100"
									>
										<span class="font-bold text-amber-800"
											>Primary Alert Driver:</span
										>
										<span
											class="font-extrabold text-amber-700 uppercase"
											>Hazard-Driven (FWI dry anomalies)</span
										>
									</div>
									<div
										class="text-[10px] p-2 bg-slate-50 rounded-lg border border-slate-100"
									>
										<span
											class="font-bold text-slate-700 block"
											>Suggested Confirmation Route:</span
										>
										<p class="text-slate-500 mt-1">
											Check local scraped emergency civil
											protection Twitter (X) and physical
											remote sensing validation.
										</p>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			{/if}

			{#if activeTab === "chapter4"}
				<div class="space-y-8 max-w-5xl mx-auto pb-12">
					<div class="border-b border-slate-200 pb-4">
						<span
							class="text-xs font-extrabold text-teal-700 uppercase tracking-widest font-mono"
							>CRITICAL PHASE: STEP-BY-STEP</span
						>
						<h2 class="text-2xl font-black text-slate-900 mt-1">
							The "Actions" Step: Tactical Spatial Analysis &
							Deployment
						</h2>
						<p class="text-sm text-slate-500 mt-1">
							Evaluating Area of Interest (AOI) buffers, executing
							intersecting exposure analysis, and prioritizing
							tactical deployments. This critical step maps
							specific, ranked Standard Operating Procedures
							(SOPs) onto vulnerable assets for real-world
							dispatch.
						</p>
					</div>

					<!-- Step 10 -->
					<div
						class="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden grid grid-cols-1 lg:grid-cols-12"
					>
						<div
							class="p-6 lg:col-span-5 flex flex-col justify-between border-b lg:border-b-0 lg:border-r border-slate-100"
						>
							<div>
								<div class="flex items-center gap-2">
									<span
										class="flex items-center justify-center bg-slate-100 text-slate-700 font-extrabold text-xs w-6 h-6 rounded-full border border-slate-200 font-mono"
										>10</span
									>
									<h3
										class="text-sm font-black text-slate-900"
									>
										Show AOI / Affected Area
									</h3>
								</div>

								<div class="mt-4 space-y-3">
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											Operator Action
										</h4>
										<p
											class="text-xs text-slate-700 mt-1 font-medium bg-slate-50 p-2 rounded-lg border border-slate-100"
										>
											Review the bounding Area of Interest
											(AOI) generated around the anomaly.
										</p>
									</div>
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											System Output
										</h4>
										<p
											class="text-xs text-slate-600 mt-1 leading-relaxed"
										>
											AOI polygon appears on the map
											around the risk or affected zone.
										</p>
									</div>
								</div>
							</div>

							<div class="mt-6 pt-4 border-t border-slate-100">
								<span
									class="text-[9px] font-extrabold bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full uppercase tracking-wider font-mono"
									>Why it matters</span
								>
								<p
									class="text-[11px] text-slate-500 mt-1.5 leading-relaxed"
								>
									Defines the physical boundaries where
									geographic analysis and tactical actions
									should focus.
								</p>
							</div>
						</div>

						<!-- Visual Mockup Column -->
						<div
							class="p-6 lg:col-span-7 bg-slate-50/50 flex flex-col justify-center"
						>
							<h4
								class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono mb-3"
							>
								System View Example
							</h4>
							<div
								class="bg-white rounded-xl border border-slate-200 p-4 shadow-xs relative flex items-center justify-center bg-slate-100 min-h-[140px]"
							>
								<div
									class="absolute top-2 left-2 text-[9px] bg-white/90 border border-slate-200 px-1.5 py-0.5 rounded shadow-xs font-bold text-slate-700"
								>
									🧭 Map AOI Grid Layer
								</div>
								<div class="text-center p-3">
									<div
										class="inline-block border-2 border-dashed border-red-500 bg-red-500/10 rounded-full w-14 h-14 animate-pulse mb-1 flex items-center justify-center"
									>
										<span
											class="text-xs text-red-600 font-bold"
											>5km AOI</span
										>
									</div>
									<p
										class="text-[10px] font-bold text-slate-800 leading-none"
									>
										AOI-Target-082 Generated
									</p>
									<p
										class="text-[8px] text-slate-500 mt-1 font-normal"
									>
										Intersecting spatial elements inside the
										containment buffer (1,240 hectares
										total).
									</p>
								</div>
							</div>
						</div>
					</div>

					<!-- Step 11 -->
					<div
						class="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden grid grid-cols-1 lg:grid-cols-12"
					>
						<div
							class="p-6 lg:col-span-5 flex flex-col justify-between border-b lg:border-b-0 lg:border-r border-slate-100"
						>
							<div>
								<div class="flex items-center gap-2">
									<span
										class="flex items-center justify-center bg-slate-100 text-slate-700 font-extrabold text-xs w-6 h-6 rounded-full border border-slate-200 font-mono"
										>11</span
									>
									<h3
										class="text-sm font-black text-slate-900"
									>
										Exposure & Vulnerability Analysis
									</h3>
								</div>

								<div class="mt-4 space-y-3">
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											Operator Action
										</h4>
										<p
											class="text-xs text-slate-700 mt-1 font-medium bg-slate-50 p-2 rounded-lg border border-slate-100"
										>
											Run geographic intersection reports
											inside the AOI.
										</p>
									</div>
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											System Output
										</h4>
										<p
											class="text-xs text-slate-600 mt-1 leading-relaxed"
										>
											System shows exposed population,
											roads, settlements, assets and
											access constraints.
										</p>
									</div>
								</div>
							</div>

							<div class="mt-6 pt-4 border-t border-slate-100">
								<span
									class="text-[9px] font-extrabold bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full uppercase tracking-wider font-mono"
									>Why it matters</span
								>
								<p
									class="text-[11px] text-slate-500 mt-1.5 leading-relaxed"
								>
									Explains who or what may be affected inside
									the active hazard zone, identifying
									potential bottlenecks early.
								</p>
							</div>
						</div>

						<!-- Visual Mockup Column -->
						<div
							class="p-6 lg:col-span-7 bg-slate-50/50 flex flex-col justify-center"
						>
							<h4
								class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono mb-3"
							>
								System View Example
							</h4>
							<div
								class="bg-white rounded-xl border border-slate-200 p-4 shadow-xs relative"
							>
								<div
									class="text-[10px] font-bold text-slate-700 mb-2.5 flex items-center justify-between border-b border-slate-100 pb-1.5 font-mono"
								>
									<span>📊 Intersected Asset Matrix</span>
									<span
										class="text-[8px] bg-red-100 text-red-800 font-extrabold px-1.5 py-0.5 rounded"
										>High Risk Zone</span
									>
								</div>

								<div
									class="grid grid-cols-2 gap-2 text-[10px] font-normal"
								>
									<div
										class="border border-slate-100 bg-slate-50 p-2 rounded"
									>
										<span
											class="text-slate-400 font-medium block"
											>Exposed Population</span
										>
										<span
											class="font-extrabold text-slate-800"
											>1,420 Citizens</span
										>
									</div>
									<div
										class="border border-slate-100 bg-slate-50 p-2 rounded"
									>
										<span
											class="text-slate-400 font-medium block"
											>Key Roads Intersected</span
										>
										<span
											class="font-extrabold text-red-600"
											>Primary Highway (Escape corridor)</span
										>
									</div>
									<div
										class="border border-slate-100 bg-slate-50 p-2 rounded"
									>
										<span
											class="text-slate-400 font-medium block"
											>Access Constraints</span
										>
										<span
											class="font-extrabold text-amber-600"
											>Narrow steep gorges (West)</span
										>
									</div>
									<div
										class="border border-slate-100 bg-slate-50 p-2 rounded"
									>
										<span
											class="text-slate-400 font-medium block"
											>High-Value Assets</span
										>
										<span
											class="font-extrabold text-[#0f766e]"
											>Protected Historic Asset, School</span
										>
									</div>
								</div>
							</div>
						</div>
					</div>

					<!-- Step 12 -->
					<div
						class="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden grid grid-cols-1 lg:grid-cols-12"
					>
						<div
							class="p-6 lg:col-span-5 flex flex-col justify-between border-b lg:border-b-0 lg:border-r border-slate-100"
						>
							<div>
								<div class="flex items-center gap-2">
									<span
										class="flex items-center justify-center bg-slate-100 text-slate-700 font-extrabold text-xs w-6 h-6 rounded-full border border-slate-200 font-mono"
										>12</span
									>
									<h3
										class="text-sm font-black text-slate-900"
									>
										Review Elements at Risk & Prioritised
										Action
									</h3>
								</div>

								<div class="mt-4 space-y-3">
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											Operator Action
										</h4>
										<p
											class="text-xs text-slate-700 mt-1 font-medium bg-slate-50 p-2 rounded-lg border border-slate-100"
										>
											Inspect priority tables for the
											active scenario.
										</p>
									</div>
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											System Output
										</h4>
										<p
											class="text-xs text-slate-600 mt-1 leading-relaxed"
										>
											System ranks exposed population,
											roads, settlements and sensitive
											assets by operational priority.
											Actions are ranked as Immediate /
											Next / Monitor, with rationale and
											linked element at risk.
										</p>
									</div>
								</div>
							</div>

							<div class="mt-6 pt-4 border-t border-slate-100">
								<span
									class="text-[9px] font-extrabold bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full uppercase tracking-wider font-mono"
									>Why it matters</span
								>
								<p
									class="text-[11px] text-slate-500 mt-1.5 leading-relaxed"
								>
									Shows where action should focus first. Turns
									complex risk and GIS recommendations into a
									structured, executable operational response
									package.
								</p>
							</div>
						</div>

						<!-- Visual Mockup Column -->
						<div
							class="p-6 lg:col-span-7 bg-slate-50/50 flex flex-col justify-center"
						>
							<h4
								class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono mb-3"
							>
								System View Example
							</h4>
							<div
								class="bg-white rounded-xl border border-slate-200 p-4 shadow-xs relative"
							>
								<div
									class="text-[10px] font-bold text-slate-700 mb-2 border-b border-slate-100 pb-1.5"
								>
									🛡️ Tactical Asset Prioritization Matrix
								</div>
								<div class="space-y-2 text-[10px] font-normal">
									<div
										class="flex items-start gap-2 bg-red-50 p-2 rounded border border-red-100"
									>
										<span
											class="bg-red-600 text-white font-black px-1.5 py-0.5 rounded text-[8px] font-mono"
											>IMMEDIATE</span
										>
										<div>
											<span
												class="font-bold text-red-900 block"
												>Pre-evacuate Target Primary
												School</span
											>
											<p
												class="text-slate-600 mt-0.5 leading-tight text-[9px]"
											>
												Rationale: High-density
												vulnerable youth. School
												boundary falls inside 1.5km
												thermal propagation vector.
											</p>
										</div>
									</div>

									<div
										class="flex items-start gap-2 bg-amber-50 p-2 rounded border border-amber-100"
									>
										<span
											class="bg-amber-500 text-white font-black px-1.5 py-0.5 rounded text-[8px] font-mono"
											>NEXT</span
										>
										<div>
											<span
												class="font-bold text-amber-900 block"
												>Traffic Blockade on Primary
												Escape Route</span
											>
											<p
												class="text-slate-600 mt-0.5 leading-tight text-[9px]"
											>
												Rationale: Secure critical
												transport flow for fire truck
												dispatches. Re-route civilian
												escapees east.
											</p>
										</div>
									</div>

									<div
										class="flex items-start gap-2 bg-slate-50 p-2 rounded border border-slate-100"
									>
										<span
											class="bg-slate-500 text-white font-black px-1.5 py-0.5 rounded text-[8px] font-mono"
											>MONITOR</span
										>
										<div>
											<span
												class="font-bold text-slate-900 block"
												>Establish Protective Buffer:
												Historic Castle</span
											>
											<p
												class="text-slate-600 mt-0.5 leading-tight text-[9px]"
											>
												Rationale: Heavy stone
												fortification, low fire ignition
												velocity. Needs active aerial
												survey monitoring.
											</p>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>

					<!-- Step 13 -->
					<div
						class="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden grid grid-cols-1 lg:grid-cols-12"
					>
						<div
							class="p-6 lg:col-span-5 flex flex-col justify-between border-b lg:border-b-0 lg:border-r border-slate-100"
						>
							<div>
								<div class="flex items-center gap-2">
									<span
										class="flex items-center justify-center bg-slate-100 text-slate-700 font-extrabold text-xs w-6 h-6 rounded-full border border-slate-200 font-mono"
										>13</span
									>
									<h3
										class="text-sm font-black text-slate-900"
									>
										Generate Recommended Actions
									</h3>
								</div>

								<div class="mt-4 space-y-3">
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											Operator Action
										</h4>
										<p
											class="text-xs text-slate-700 mt-1 font-medium bg-slate-50 p-2 rounded-lg border border-slate-100"
										>
											Deploy standard response guidelines
											mapped to this alert profile.
										</p>
									</div>
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											System Output
										</h4>
										<p
											class="text-xs text-slate-600 mt-1 leading-relaxed"
										>
											System recommends actions based on
											alert level, risk, exposure and
											vulnerability.
										</p>
									</div>
								</div>
							</div>

							<div class="mt-6 pt-4 border-t border-slate-100">
								<span
									class="text-[9px] font-extrabold bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full uppercase tracking-wider font-mono"
									>Why it matters</span
								>
								<p
									class="text-[11px] text-slate-500 mt-1.5 leading-relaxed"
								>
									Demonstrates active decision support, not
									just visualization. Ensures consistent
									standard guidelines are deployed in seconds.
								</p>
							</div>
						</div>

						<!-- Visual Mockup Column -->
						<div
							class="p-6 lg:col-span-7 bg-slate-50/50 flex flex-col justify-center"
						>
							<h4
								class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono mb-3"
							>
								System View Example
							</h4>
							<div
								class="bg-white rounded-xl border border-slate-200 p-4 shadow-xs relative"
							>
								<div
									class="text-[10px] font-bold text-slate-700 mb-2 flex items-center justify-between border-b border-slate-100 pb-1.5 font-mono"
								>
									<span>🚀 Recommended Action Templates</span>
									<span class="text-[8px] text-slate-400"
										>SOP Generator v1.2</span
									>
								</div>

								<div class="space-y-2 font-normal">
									<div
										class="flex items-center justify-between p-2 bg-[#e6f4f1] rounded-lg border border-[#0f766e]/10"
									>
										<div>
											<span
												class="text-[10px] font-bold text-[#0f766e] block"
												>Deploy Regional Fire Crew
												(Local Station)</span
											>
											<span
												class="text-[8px] text-slate-500"
												>Asset Target: Primary Fire Core</span
											>
										</div>
										<button
											class="px-2.5 py-1 text-[9px] font-extrabold bg-[#0f766e] hover:bg-[#0d5e58] text-white rounded cursor-not-allowed"
											>Deploy</button
										>
									</div>

									<div
										class="flex items-center justify-between p-2 bg-[#e6f4f1] rounded-lg border border-[#0f766e]/10"
									>
										<div>
											<span
												class="text-[10px] font-bold text-[#0f766e] block"
												>Activate Public Broadcast
												Evacuation Protocol</span
											>
											<span
												class="text-[8px] text-slate-500"
												>Asset Target: Primary North
												Sector</span
											>
										</div>
										<button
											class="px-2.5 py-1 text-[9px] font-extrabold bg-[#0f766e] hover:bg-[#0d5e58] text-white rounded cursor-not-allowed"
											>Deploy</button
										>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			{/if}

			{#if activeTab === "chapter2" || activeTab === "chapter4"}
				<!-- Floating historical helper note for temporal views -->
				<div
					class="mt-4 bg-amber-50 border border-amber-200 rounded-xl p-4 max-w-5xl mx-auto flex items-start gap-3"
				>
					<span class="text-lg">🕒</span>
					<div>
						<h4 class="text-xs font-bold text-amber-950 font-mono">
							Timeline Replay Observation
						</h4>
						<p class="text-xs text-amber-900 mt-1 leading-relaxed">
							The operator has the flexibility to travel to other
							dates during the fire event, reviewing how maps,
							threat overlays, and validation priorities update at
							different times.
						</p>
					</div>
				</div>
			{/if}

			{#if activeTab === "chapter5"}
				<div class="space-y-8 max-w-5xl mx-auto pb-12">
					<div class="border-b border-slate-200 pb-4">
						<span
							class="text-xs font-extrabold text-[#0f766e] uppercase tracking-widest font-mono"
							>Walkthrough Chapter 5</span
						>
						<h2 class="text-2xl font-black text-slate-900 mt-1">
							Audit, Operational Briefings & Feedback Loop
						</h2>
						<p class="text-sm text-slate-500 mt-1">
							Closing the operational loop through chronological
							timelines, shareable briefing reports, and
							post-incident auditing.
						</p>
					</div>

					<!-- Step 14 -->
					<div
						class="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden grid grid-cols-1 lg:grid-cols-12"
					>
						<div
							class="p-6 lg:col-span-5 flex flex-col justify-between border-b lg:border-b-0 lg:border-r border-slate-100"
						>
							<div>
								<div class="flex items-center gap-2">
									<span
										class="flex items-center justify-center bg-slate-100 text-slate-700 font-extrabold text-xs w-6 h-6 rounded-full border border-slate-200 font-mono"
										>14</span
									>
									<h3
										class="text-sm font-black text-slate-900"
									>
										Show Alert Lifecycle Timeline
									</h3>
								</div>

								<div class="mt-4 space-y-3">
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											Operator Action
										</h4>
										<p
											class="text-xs text-slate-700 mt-1 font-medium bg-slate-50 p-2 rounded-lg border border-slate-100"
										>
											Open the audit log or trace modal to
											view historical actions.
										</p>
									</div>
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											System Output
										</h4>
										<p
											class="text-xs text-slate-600 mt-1 leading-relaxed"
										>
											Timeline shows alert creation,
											confirmation, escalation and
											updates, including actions that were
											taken or not (and why).
										</p>
									</div>
								</div>
							</div>

							<div class="mt-6 pt-4 border-t border-slate-100">
								<span
									class="text-[9px] font-extrabold bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full uppercase tracking-wider font-mono"
									>Why it matters</span
								>
								<p
									class="text-[11px] text-slate-500 mt-1.5 leading-relaxed"
								>
									Provides complete traceability, historical
									transparency, and operational credibility
									for review boards.
								</p>
							</div>
						</div>

						<!-- Visual Mockup Column -->
						<div
							class="p-6 lg:col-span-7 bg-slate-50/50 flex flex-col justify-center"
						>
							<h4
								class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono mb-3"
							>
								System View Example
							</h4>
							<div
								class="bg-white rounded-xl border border-slate-200 p-4 shadow-xs relative"
							>
								<div
									class="text-[10px] font-bold text-slate-700 mb-3 border-b border-slate-100 pb-1.5 flex items-center gap-1.5 font-mono"
								>
									<span>⏱️</span> Chronological Audit Trail
								</div>

								<div
									class="space-y-3 relative pl-4 border-l-2 border-slate-100 text-[10px] text-slate-600 font-normal"
								>
									<div class="relative">
										<span
											class="absolute -left-[21px] top-0 bg-red-500 text-white rounded-full w-2.5 h-2.5 border border-white"
										></span>
										<strong>14:15</strong> - Alert Created automatically
										via satellite active-thermal sensor intersection.
									</div>
									<div class="relative">
										<span
											class="absolute -left-[21px] top-0 bg-blue-500 text-white rounded-full w-2.5 h-2.5 border border-white"
										></span>
										<strong>14:22</strong> - Scrape verification
										evidence compiled from 2 news reports & 3
										geolocated tweets.
									</div>
									<div class="relative">
										<span
											class="absolute -left-[21px] top-0 bg-emerald-500 text-white rounded-full w-2.5 h-2.5 border border-white"
										></span>
										<strong>14:30</strong> - Alert status updated
										to "Acknowledged/Confirmed" by Incident Operator.
									</div>
									<div class="relative">
										<span
											class="absolute -left-[21px] top-0 bg-[#0f766e] text-white rounded-full w-2.5 h-2.5 border border-white"
										></span>
										<strong>14:33</strong> - Response Action
										"Primary Escape Route Traffic Closure" deployed
										to Field Dispatch.
									</div>
								</div>
							</div>
						</div>
					</div>

					<!-- Step 15 -->
					<div
						class="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden grid grid-cols-1 lg:grid-cols-12"
					>
						<div
							class="p-6 lg:col-span-5 flex flex-col justify-between border-b lg:border-b-0 lg:border-r border-slate-100"
						>
							<div>
								<div class="flex items-center gap-2">
									<span
										class="flex items-center justify-center bg-slate-100 text-slate-700 font-extrabold text-xs w-6 h-6 rounded-full border border-slate-200 font-mono"
										>15</span
									>
									<h3
										class="text-sm font-black text-slate-900"
									>
										Generate Operational Brief
									</h3>
								</div>

								<div class="mt-4 space-y-3">
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											Operator Action
										</h4>
										<p
											class="text-xs text-slate-700 mt-1 font-medium bg-slate-50 p-2 rounded-lg border border-slate-100"
										>
											Click 'Download PDF' inside the
											Report tab.
										</p>
									</div>
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											System Output
										</h4>
										<p
											class="text-xs text-slate-600 mt-1 leading-relaxed"
										>
											Brief includes map, alert level,
											confidence, evidence, exposure and
											recommended actions.
										</p>
									</div>
								</div>
							</div>

							<div class="mt-6 pt-4 border-t border-slate-100">
								<span
									class="text-[9px] font-extrabold bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full uppercase tracking-wider font-mono"
									>Why it matters</span
								>
								<p
									class="text-[11px] text-slate-500 mt-1.5 leading-relaxed"
								>
									Compiles the final shareable output for
									offline commanders, review boards, and
									external stakeholders.
								</p>
							</div>
						</div>

						<!-- Visual Mockup Column -->
						<div
							class="p-6 lg:col-span-7 bg-slate-50/50 flex flex-col justify-center"
						>
							<h4
								class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono mb-3"
							>
								System View Example
							</h4>
							<div
								class="bg-white rounded-xl border border-slate-200 p-4 shadow-xs relative"
							>
								<div
									class="border-2 border-slate-150 rounded-lg p-3 bg-slate-50"
								>
									<div
										class="flex justify-between items-center border-b border-slate-200 pb-2 mb-2"
									>
										<div
											class="text-[9px] font-bold text-slate-800"
										>
											📋 INCIDENT_BRIEF_REPORT.pdf
										</div>
										<span
											class="text-[8px] font-bold bg-[#0f766e] text-white px-1.5 py-0.5 rounded uppercase leading-none font-mono"
											>Draft Compiled</span
										>
									</div>

									<div
										class="space-y-1.5 text-[8px] text-slate-600 font-normal"
									>
										<p>
											• <strong>Incident Level:</strong> Level
											2 Alert (Warning Severity)
										</p>
										<p>
											• <strong>Location:</strong> Active Region
											(Incident centroid coordinate)
										</p>
										<p>
											• <strong>Confidence Index:</strong>
											94% (Combined Sensor & Scraping Confirmations)
										</p>
										<p>
											• <strong>Exposed Assets:</strong> Target
											Primary School, 1,420 Residents, Primary
											Escape Route Corridor
										</p>
										<p>
											• <strong>Deployed Actions:</strong>
											2 active dispatches routed to Local Station
										</p>
									</div>
								</div>
							</div>
						</div>
					</div>

					<!-- Step 16 -->
					<div
						class="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden grid grid-cols-1 lg:grid-cols-12"
					>
						<div
							class="p-6 lg:col-span-5 flex flex-col justify-between border-b lg:border-b-0 lg:border-r border-slate-100"
						>
							<div>
								<div class="flex items-center gap-2">
									<span
										class="flex items-center justify-center bg-slate-100 text-slate-700 font-extrabold text-xs w-6 h-6 rounded-full border border-slate-200 font-mono"
										>16</span
									>
									<h3
										class="text-sm font-black text-slate-900"
									>
										Send Brief
									</h3>
								</div>

								<div class="mt-4 space-y-3">
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											Operator Action
										</h4>
										<p
											class="text-xs text-slate-700 mt-1 font-medium bg-slate-50 p-2 rounded-lg border border-slate-100"
										>
											Type recipient address and click
											Send Email.
										</p>
									</div>
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											System Output
										</h4>
										<p
											class="text-xs text-slate-600 mt-1 leading-relaxed"
										>
											Brief is sent by email or webhook,
											with delivery confirmation.
										</p>
									</div>
								</div>
							</div>

							<div class="mt-6 pt-4 border-t border-slate-100">
								<span
									class="text-[9px] font-extrabold bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full uppercase tracking-wider font-mono"
									>Why it matters</span
								>
								<p
									class="text-[11px] text-slate-500 mt-1.5 leading-relaxed"
								>
									Demonstrates how the digital environmental
									control center connects to real-world
									command networks and stakeholders
									immediately.
								</p>
							</div>
						</div>

						<!-- Visual Mockup Column -->
						<div
							class="p-6 lg:col-span-7 bg-slate-50/50 flex flex-col justify-center"
						>
							<h4
								class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono mb-3"
							>
								System View Example
							</h4>
							<div
								class="bg-white rounded-xl border border-slate-200 p-4 shadow-xs relative text-center"
							>
								<div
									class="inline-flex items-center gap-1 bg-emerald-50 text-emerald-800 font-bold text-[9px] px-2.5 py-1 rounded-full border border-emerald-150 mb-2"
								>
									<span>✅</span> Brief dispatched successfully
								</div>

								<div
									class="text-[9px] text-slate-500 text-left space-y-1 bg-slate-50 p-2 rounded border border-slate-100 font-mono"
								>
									<div>
										Email: dispatched to <span
											class="text-slate-700"
											>incident-commander@emergency.gov</span
										>
									</div>
									<div>
										Webhook: POST 200 OK -> <span
											class="text-slate-700"
											>https://webhook.emergency.gov/dispatches</span
										>
									</div>
								</div>
							</div>
						</div>
					</div>

					<!-- Step 17 -->
					<div
						class="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden grid grid-cols-1 lg:grid-cols-12"
					>
						<div
							class="p-6 lg:col-span-5 flex flex-col justify-between border-b lg:border-b-0 lg:border-r border-slate-100"
						>
							<div>
								<div class="flex items-center gap-2">
									<span
										class="flex items-center justify-center bg-slate-100 text-slate-700 font-extrabold text-xs w-6 h-6 rounded-full border border-slate-200 font-mono"
										>17</span
									>
									<h3
										class="text-sm font-black text-slate-900"
									>
										Closing the Loop
									</h3>
								</div>

								<div class="mt-4 space-y-3">
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											Operator Action
										</h4>
										<p
											class="text-xs text-slate-700 mt-1 font-medium bg-slate-50 p-2 rounded-lg border border-slate-100"
										>
											Evaluate incident outcomes to feed
											performance metrics back into
											models.
										</p>
									</div>
									<div>
										<h4
											class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono"
										>
											System Output
										</h4>
										<p
											class="text-xs text-slate-600 mt-1 leading-relaxed"
										>
											Summary of everything that happened
											during the fire event.
										</p>
									</div>
								</div>
							</div>

							<div class="mt-6 pt-4 border-t border-slate-100">
								<span
									class="text-[9px] font-extrabold bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full uppercase tracking-wider font-mono"
									>Why it matters</span
								>
								<p
									class="text-[11px] text-slate-500 mt-1.5 leading-relaxed"
								>
									Continuous improvement loop. Data can be
									used by the system to improve threat weight
									models and optimized for future auditing.
								</p>
							</div>
						</div>

						<!-- Visual Mockup Column -->
						<div
							class="p-6 lg:col-span-7 bg-slate-50/50 flex flex-col justify-center"
						>
							<h4
								class="text-[10px] font-extrabold text-slate-400 uppercase tracking-widest font-mono mb-3"
							>
								System View Example
							</h4>
							<div
								class="bg-white rounded-xl border border-slate-200 p-4 shadow-xs relative"
							>
								<div
									class="text-[10px] font-bold text-[#0f766e] mb-2 flex items-center gap-1 font-mono"
								>
									<span>🔄</span> Continuous Machine Learning Loop
								</div>

								<div
									class="space-y-1.5 text-[10px] text-slate-600 font-normal"
								>
									<div
										class="bg-slate-50 p-2 rounded border border-slate-100"
									>
										<strong>Response Efficacy Score:</strong
										>
										<span class="text-emerald-600 font-bold"
											>96% (Optimal response latency)</span
										>
									</div>
									<div
										class="bg-slate-50 p-2 rounded border border-slate-100"
									>
										<strong>Feedback Action:</strong> Regional
										model updated to prioritize 1.5km school
										buffers on low fuel-moisture days.
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			{/if}
		</main>
	</div>
</div>
