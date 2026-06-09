<script>
	let {
		layers = ["satellite", "streets"],
		layer = null,
		onLayerChange = () => {},
	} = $props();
</script>

<form>
	{#each layers as layerOption}
		<label>
			<input
				type="radio"
				name="layers"
				value={layerOption}
				checked={layerOption === (layer ?? layers[0])}
				onchange={() => onLayerChange(layerOption)}
			/>
			{layerOption}
		</label>
	{/each}
</form>

<style>
	form {
		position: absolute;
		z-index: 999999;
		left: 10px;
		bottom: 10px;
		background-color: #fafafa;
		padding: 5px;
		border-radius: 5px;
		border: 1px solid gray;
		display: flex;
		flex-direction: row;
		gap: 5px;
	}

	label {
		display: flex;
		flex-direction: row;
		align-items: center;
		gap: 2px;
	}
</style>
