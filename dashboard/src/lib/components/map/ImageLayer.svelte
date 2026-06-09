<script>
  import { map } from "$lib/stores/map/map";
  import { imageLayers } from "$lib/stores/map/imageLayers";
  import { onDestroy } from "svelte";

  let {
    name,
    image,
    XYZ_URL,
    bands = "4,3,2",
    stretch = "0,4000",
    palette = "RdYlGn_r",
    options = {},
  } = $props();

  const pane = $derived(options.pane ?? "left");
  const url = $derived(
    `${XYZ_URL}/${image}/{z}/{x}/{y}.png?bands=${bands}&stretch=${stretch}&palette=${palette}`,
  );

  let layer;

  $effect(() => {
    if ($map && url) {
      if ($imageLayers[pane]?.[name]) {
        $imageLayers[pane][name].setUrl(url);
      } else {
        layer = L.tileLayer(url, options).addTo($map);
        imageLayers.addImageLayer(pane, name, layer);
      }
    }
  });

  onDestroy(() => {
    imageLayers.removeImageLayer(name, pane);
  });
</script>
