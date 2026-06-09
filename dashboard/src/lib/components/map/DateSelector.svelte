<script>
	let { dates, selected = $bindable(null), position = "left-2" } = $props();
</script>

{#if dates}
	<select
		class={`py-2 px-2 absolute z-[9999] mt-2 bg-white border-black rounded-md hover:bg-gray-100 ${position}`}
		bind:value={selected}
	>
		{#each dates as date}
			<option value={date} selected={date == selected}>{date}</option>
		{/each}
	</select>
{/if}
