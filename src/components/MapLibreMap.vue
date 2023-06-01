<script setup lang="ts">
import 'maplibre-gl/dist/maplibre-gl.css'

import {
  FullscreenControl,
  GeolocateControl,
  Map,
  NavigationControl,
  Popup,
  ScaleControl,
  type LngLatLike,
  type StyleSpecification
} from 'maplibre-gl'
import { onMounted, ref, unref, watch } from 'vue'

defineExpose({
  update
})
const props = withDefaults(
  defineProps<{
    styleSpec: string | StyleSpecification
    center?: LngLatLike
    zoom?: number
    aspectRatio?: number
    minZoom?: number
    maxZoom?: number
    filterId?: string
    popupLayerIds?: string[]
    areaLayerIds?: string[]
  }>(),
  {
    center: undefined,
    zoom: 12,
    aspectRatio: undefined,
    minZoom: undefined,
    maxZoom: undefined,
    filterId: undefined,
    popupLayerIds: () => [],
    areaLayerIds: () => []
  }
)

const loading = ref(true)
let map: Map | undefined = undefined
const dates = ['20_08', '25_08']

onMounted(() => {
  map = new Map({
    container: 'maplibre-map',
    style: props.styleSpec,
    center: props.center,
    zoom: props.zoom
  })
  map.addControl(new NavigationControl({}))
  map.addControl(new GeolocateControl({}))
  map.addControl(new ScaleControl({}))
  map.addControl(new FullscreenControl({}))

  map.once('load', () => {
    // Create an image from SVG
    const svgImage = new Image(100, 100)
    svgImage.onload = () => {
        map?.addImage('arrow', svgImage)
    }
    function svgStringToImageSrc (svgString) {
        return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgString)
    }
    svgImage.src = svgStringToImageSrc(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16"><path d="M8.22 2.97a.75.75 0 0 1 1.06 0l4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042l2.97-2.97H3.75a.75.75 0 0 1 0-1.5h7.44L8.22 4.03a.75.75 0 0 1 0-1.06Z"></path></svg>`);

    // Create a popup, but don't add it to the map yet.
    const popup = new Popup({
      closeButton: false,
      closeOnClick: true
    })

    // Add a geojson Noro concentration point source.
    // Heatmap layers also work with a vector tile source.
    for (const date of dates) {
      map?.addSource(`noro-${date}`, {
        'type': 'geojson',
        'data':
            `https://raw.githubusercontent.com/EPFL-ENAC/lce-water-quality-simulations/wind/data/concentrations_${date}.geojson`
      });
      // Add a geojson wind point source
      map?.addSource(`wind-${date}`, {
          'type': 'geojson',
          'data':
              `https://raw.githubusercontent.com/EPFL-ENAC/lce-water-quality-simulations/wind/data/wind_${date}.geojson`
      });

      map?.addLayer(
            {
                'id': `noro-point-${date}`,
                'type': 'circle',
                'source': `noro-${date}`,
                'minzoom': 11,
                'paint': {
                    // Size circle radius by noro concentration and zoom level
                    'circle-radius': [
                        'interpolate',
                        ['linear'],
                        ['zoom'],
                        7,
                        ['interpolate', ['linear'], ['get', 'concentration'], 1, 1, 6, 6],
                        16,
                        ['interpolate', ['linear'], ['get', 'concentration'], 1, 5, 6, 15]
                    ],
                    // Color circle by noro concentration
                    'circle-color': [
                        'string',
                        ['get', 'color'],
                        '#ffffff'
                    ],
                    'circle-stroke-color': 'white',
                    'circle-stroke-width': 1,
                    // Transition from heatmap to circle layer by zoom level
                    'circle-opacity': [
                        'interpolate',
                        ['linear'],
                        ['zoom'],
                        7, 0,
                        8, 1
                    ]
                }
            },
            'waterway'
        )
        
      	map?.addLayer(
            {
                'id': `noro-heat-${date}`,
                'type': 'heatmap',
                'source': `noro-${date}`,
                'maxzoom': 15,
                'paint': {
                    // Increase the heatmap weight based on frequency and property concentration
                    'heatmap-weight': [
                        'interpolate',
                        ['linear'],
                        ['get', 'concentration'],
                        0, 0,
                        10, 0.5,
                        100, 0.8,
                        150, 1
                    ],
                    // Increase the heatmap color weight weight by zoom level
                    // heatmap-intensity is a multiplier on top of heatmap-weight
                    'heatmap-intensity': [
                        'interpolate',
                        ['linear'],
                        ['zoom'],
                        0, 1,
                        8, 2,
                        12, 3
                    ],
                    // Color ramp for heatmap.  Domain is 0 (low) to 1 (high).
                    // Begin color ramp at 0-stop with a 0-transparancy color
                    // to create a blur-like effect.
                    'heatmap-color': [
                        'interpolate',
                        ['linear'],
                        ['heatmap-density'],
                        0,
                        'rgba(33,102,172,0)',
                        0.2,
                        'rgb(103,169,207)',
                        0.4,
                        'rgb(209,229,240)',
                        0.6,
                        'rgb(253,219,199)',
                        0.8,
                        'rgb(239,138,98)',
                        1,
                        'rgb(178,24,43)'
                    ],
                    // Adjust the heatmap radius by zoom level
                    'heatmap-radius': [
                        'interpolate',
                        ['linear'],
                        ['zoom'],
                        0, 2,
                        12, 20
                    ],
                    // Transition from heatmap to circle layer by zoom level
                    'heatmap-opacity': [
                        'interpolate',
                        ['linear'],
                        ['zoom'],
                        7, 1,
                        12, 0
                    ]
                }
            },
            'waterway'
        )

				// wind arrow
        map?.addLayer(
          {
            'id': `wind-point-${date}`,
            'type': 'symbol',
            'source': `wind-${date}`,
            'layout': {
              'icon-image': 'arrow',
              'icon-size': [
                  'number',
                  ['get', 'speed'],
                  0
              ],
              'icon-rotate': [
                  'number',
                  ['get', 'angle'], 
                  0
              ]
            },
            'paint': {
                'icon-opacity': 0.5,
            }
          }
        )

      map?.on('mouseenter', `noro-point-${date}`, function (e) {
        // Change the cursor style as a UI indicator.
        // map?.getCanvas().style.cursor = 'pointer';

        var coordinates = e.features[0].geometry.coordinates.slice();
        var description = '<b>Concentration</b> [GC/ml]<br/>' + e.features[0].properties.concentration;

        // Ensure that if the map is zoomed out such that multiple
        // copies of the feature are visible, the popup appears
        // over the copy being pointed to.
        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
          coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
        }

        // Populate the popup and set its coordinates
        // based on the feature found.
        popup.setLngLat(coordinates).setHTML(description).addTo(map);
      });

      map?.on('mouseleave', `noro-point-${date}`, function () {
        // map?.getCanvas().style.cursor = '';
        popup.remove();
      });

      /*
      map.on('mouseenter', `wind-point-${date}`, function (e) {
        // Change the cursor style as a UI indicator.
        // map.getCanvas().style.cursor = 'pointer';

        var coordinates = e.features[0].geometry.coordinates.slice();
        var description = '<b>Speed</b> [m/s]<br/>' + e.features[0].properties.speed + '<br/>' + 
          '<b>Angle</b> [deg]<br/>' + e.features[0].properties.angle;

        // Ensure that if the map is zoomed out such that multiple
        // copies of the feature are visible, the popup appears
        // over the copy being pointed to.
        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
          coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
        }

        // Populate the popup and set its coordinates
        // based on the feature found.
        popup.setLngLat(coordinates).setHTML(description).addTo(map);
      });

      map?.on('mouseleave', `wind-point-${date}`, function () {
        // map?.getCanvas().style.cursor = '';
        popup.remove();
      });
      */

    }

    filterLayers(props.filterId)
  })
  loading.value = false
})

watch(
  () => props.filterId,
  (filterId) => filterLayers(filterId),
  { immediate: true }
)

function update(center?: LngLatLike, zoom?: number) {
  if (center !== undefined) {
    map?.setCenter(center)
  }
  if (zoom !== undefined) {
    map?.setZoom(zoom)
  }
}

function filterLayers(filterId?: string) {
  if (filterId) {
    map
      ?.getStyle()
      .layers.filter((layer) => layer.id.startsWith('noro-') || layer.id.startsWith('wind-'))
      .forEach((layer) => {
        const date = layer.id.split('-').pop()
        map?.setLayoutProperty(
          layer.id,
          'visibility',
          filterId === date ? 'visible' : 'none'
        )
      })
  }
}
</script>

<template>
  <v-progress-linear v-if="loading" active color="primary" indeterminate />
  <v-responsive :aspect-ratio="aspectRatio" height="100%">
    <div id="maplibre-map" />
  </v-responsive>
</template>

<style scoped>
#maplibre-map {
  height: 100%;
}
</style>
