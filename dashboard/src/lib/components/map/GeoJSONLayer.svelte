<script>
  import { map } from "$lib/stores/map/map";
  import { GeoJSONLayers } from "$lib/stores/map/GeoJSONLayers";
  import { onDestroy } from "svelte";

  let { name, geojson, options, fit = false } = $props();

  $effect(() => {
    if ($map && geojson) {
      GeoJSONLayers.addGeoJSONLayer(name, geojson, options, $map, fit);
    }
  });

  onDestroy(() => {
    GeoJSONLayers.removeGeoJSONLayer(name);
  });
</script>
