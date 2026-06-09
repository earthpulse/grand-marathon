<script>
	import "./layout.css";
	import { page } from "$app/stores";

	let { children } = $props();

	let collapsed = $state(false);

	function toggleSidebar() {
		collapsed = !collapsed;
	}

	const topItems = [
		{ label: "Dashboard", icon: "🔥", href: "/" },
		{ label: "Confirm", icon: "✅", href: "/confirm" },
		{ label: "Alerts", icon: "🔔", href: "/alerts" },
		{ label: "Actions", icon: "🚀", href: "/actions" },
		{ label: "Report", icon: "📋", href: "/report" },
	];

	const bottomItems = [{ label: "Docs", icon: "📚", href: "/docs" }];
</script>

<div class="flex h-screen w-screen overflow-hidden bg-slate-50 text-slate-800">
	<!-- Sidebar -->
	<aside
		class="bg-white border-r border-slate-100 flex flex-col h-full transition-all duration-300 ease-in-out relative {collapsed
			? 'w-16'
			: 'w-52'}"
	>
		<!-- Logo / Brand -->
		<div
			class="flex items-center justify-between px-4 py-5 border-b border-slate-100 h-16 flex-shrink-0"
		>
			<div class="flex items-center gap-2.5 min-w-0 overflow-hidden">
				<a
					href="https://earthpulse.ai"
					class="flex flex-row gap-2 items-center min-w-0"
					target="_blank"
				>
					<img
						src={collapsed
							? "https://earthpulse.ai/favicon.ico"
							: "logo_ep.png"}
						alt="logo earthpulse"
						class="w-auto h-auto transition-all duration-300 {collapsed
							? 'max-h-8 max-w-[32px]'
							: 'max-h-10'}"
					/>
				</a>
			</div>
			{#if !collapsed}
				<button
					class="p-1.5 rounded-lg text-slate-400 hover:bg-slate-50 hover:text-slate-600 transition-colors flex-shrink-0"
					onclick={toggleSidebar}
					title="Collapse sidebar"
					aria-label="Collapse sidebar"
				>
					<svg
						class="h-4 w-4"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						stroke-width="2"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M11 19l-7-7 7-7m8 14l-7-7 7-7"
						/>
					</svg>
				</button>
			{/if}
		</div>

		{#if collapsed}
			<!-- Mini Collapse Toggle for when sidebar is collapsed -->
			<div
				class="flex justify-center py-3 border-b border-slate-100 flex-shrink-0"
			>
				<button
					class="p-1.5 rounded-lg text-slate-400 hover:bg-slate-50 hover:text-slate-600 transition-colors"
					onclick={toggleSidebar}
					title="Expand sidebar"
					aria-label="Expand sidebar"
				>
					<svg
						class="h-4 w-4"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						stroke-width="2"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M13 5l7 7-7 7M5 5l7 7-7 7"
						/>
					</svg>
				</button>
			</div>
		{/if}

		<!-- Navigation Items -->
		<nav
			class="flex-1 flex flex-col justify-between py-6 px-2.5 min-h-0 overflow-y-auto"
		>
			<!-- Top Section Items -->
			<div class="flex flex-col gap-1.5">
				{#each topItems as item}
					{@const isActive =
						item.href === "/"
							? $page.url.pathname === "/"
							: $page.url.pathname.startsWith(item.href)}
					<a
						href={item.href}
						class="flex items-center gap-2.5 px-3 py-2.5 rounded-xl transition-all duration-150 {isActive
							? 'bg-[#e6f4f1] text-[#0f766e] font-semibold'
							: 'text-slate-500 hover:bg-slate-50 hover:text-slate-800 font-medium'}"
						title={collapsed ? item.label : ""}
					>
						<span
							class="text-lg flex-shrink-0 {isActive
								? 'scale-110'
								: 'opacity-80'}">{item.icon}</span
						>
						{#if !collapsed}
							<span class="text-sm truncate">{item.label}</span>
						{/if}
					</a>
				{/each}
			</div>

			<!-- Bottom Section Items -->
			<div class="flex flex-col gap-1.5 border-t border-slate-100 pt-4">
				{#each bottomItems as item}
					{@const isActive = $page.url.pathname === item.href}
					<a
						href={item.href}
						class="flex items-center gap-2.5 px-3 py-2.5 rounded-xl transition-all duration-150 {isActive
							? 'bg-[#e6f4f1] text-[#0f766e] font-semibold'
							: 'text-slate-500 hover:bg-slate-50 hover:text-slate-800 font-medium'}"
						title={collapsed ? item.label : ""}
					>
						<span
							class="text-lg flex-shrink-0 {isActive
								? 'scale-110'
								: 'opacity-80'}">{item.icon}</span
						>
						{#if !collapsed}
							<span class="text-sm truncate">{item.label}</span>
						{/if}
					</a>
				{/each}
			</div>
		</nav>
	</aside>

	<!-- Main Content Area -->
	<main class="flex-1 flex flex-col min-w-0 h-full overflow-hidden bg-white">
		{@render children()}
	</main>
</div>
