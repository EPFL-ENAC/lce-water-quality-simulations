<script setup lang="ts">
import LayerSelector from '@/components/LayerSelector.vue'
import MapLibreMap from '@/components/MapLibreMap.vue'
import type { Parameters } from '@/utils/jsonWebMap'
import axios from 'axios'
import { computed, ref, shallowRef, triggerRef, watch } from 'vue'

const props = defineProps<{
  styleUrl: string
  parametersUrl: string
}>()

const references = [
  {
    title: "Coupling remote sensing and particle tracking to estimate trajectories in large water bodies: 10.1016/j.jag.2022.102809",
    url: "https://doi.org/10.1016/j.jag.2022.102809"
  },
  {
    title: "Data",
    url: "https://zenodo.org/record/6511377#.ZFikIuxBzrw"
  },
  {
    title: "Original map",
    url: "https://ars.els-cdn.com/content/image/1-s2.0-S0043135422013823-gr4.jpg"
  },
  {
    title: "Environmental Chemistry Laboratory - LCE",
    url: "https://www.epfl.ch/labs/lce/"
  }
]

const map = ref<InstanceType<typeof MapLibreMap>>()
const selectedlayerId = ref<string>('')
const parameters = shallowRef<Parameters>({})

const selectedLayer = computed(() =>
  parameters.value.selectableItems ? parameters.value.selectableItems
    .filter((item) => item.ids.some((id) => selectedlayerId.value === id))
    .pop() : undefined
)

const selectedLegendColors = computed(() =>
  selectedLayer.value && selectedLayer.value.legend ? selectedLayer.value.legend.colors : undefined
)

watch(
  () => props.parametersUrl,
  (parametersUrl) => {
    axios
      .get<Parameters>(parametersUrl)
      .then((response) => response.data)
      .then((data) => {
        parameters.value = data
        triggerRef(parameters)
        map.value?.update(data.center, data.zoom)
      })
  },
  { immediate: true }
)
</script>

<template>
  <v-container class="fill-height pa-0" fluid>
    <v-row class="fill-height">
      <v-col cols="12" md="3" sm="6" class="pl-6">
        <v-row>
          <v-col>
            <LayerSelector v-model="selectedlayerId" :items="parameters.selectableItems" />
          </v-col>
        </v-row>
        <v-divider class="border-opacity-100 mx-n3" />
        <v-row>
          <v-col>
            <v-card title="Legend" flat>
              <v-card-text>
                <v-row class="mt-3 mb-3">
                  <b>GC/ml</b>
                </v-row>
                <v-row class="mt-3 mb-3" v-if="selectedLayer">
                  <div class="mr-1"><b>{{ selectedLayer.legend.min }}</b></div>
                  <div v-for="color in selectedLegendColors" :style="'height: 20px; width: 2px; background-color: ' + color">  </div>
                  <div class="ml-1"><b>{{ selectedLayer.legend.max }}</b></div>
                </v-row>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        <v-divider class="border-opacity-100 mx-n3" />
        <v-row>
          <v-col>
            <v-card title="References" flat>
              <v-card-text>
                <v-list tag='ul'>
                  <template v-for="item in references">
                    <v-list-item tag='li'>
                      <a :href="item.url" target="_blank">{{ item.title }}</a>
                    </v-list-item>
                  </template>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-col>
      <v-divider class="border-opacity-100" vertical />
      <v-col cols="12" md="9" sm="6" class="py-0 pl-0">
        <MapLibreMap
          ref="map"
          :center="parameters.center"
          :style-spec="styleUrl"
          :filter-id="selectedlayerId"
          :popup-layer-ids="parameters.popupLayerIds"
          :zoom="parameters.zoom"
        />
      </v-col>
    </v-row>
  </v-container>
</template>
