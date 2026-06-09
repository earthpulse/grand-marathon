<script>
	import { onMount, onDestroy, setContext } from "svelte";
	import { map } from "$lib/stores/map/map";
	import { browser } from "$app/environment";
	import "$lib/styles/map.css";

	const {
		options = {
			attributionControl: false,
			drawControls: true,
			max_zoom: 20,
		},
		zoomPosition = "bottomright",
		zoom = null,
		position = null,
		panes = null,
		aoi = null,
		children = null,
	} = $props();

	let _map;
	onMount(async () => {
		if (browser) {
			const leaflet = await import("leaflet");
			const L = leaflet.default ?? leaflet;
			window.L = L;
            _map = L.map("map", options);
            if (aoi) _map.fitBounds(L.geoJSON(aoi).getBounds());
            else _map.setView(position, zoom);
            _map.zoomControl.setPosition(zoomPosition);
            _map.getPane("popupPane").style.zIndex = 100001;
            _map.getPane("tooltipPane").style.zIndex = 100002;
            _map.getPane("markerPane").style.zIndex = 100000; // Place markers high above image tiles pane
            _map.getPane("shadowPane").style.zIndex = 99999;
            panes?.forEach(({ name, zIndex }) => {
				_map.createPane(name);
				_map.getPane(name).style.zIndex = zIndex;
				_map.getPane(name).style.pointerEvents = "none";
			});
			map.init(_map);
		}
	});

	onDestroy(() => {
		map.remove();
	});

	setContext("map", {
		getMap: () => _map,
	});
</script>

<div id="map" class="w-full h-full">
	{#if $map}
		{@render children()}
	{/if}
</div>
