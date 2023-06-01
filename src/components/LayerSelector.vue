<script setup lang="ts">
import type { SelectableItem, SelectableSingleItem } from '@/utils/layerSelector'
import { computed, watch, ref } from 'vue'

interface CheckboxProps {
  label: string
  value: string[]
}

const props = withDefaults(
  defineProps<{
    modelValue?: string
    items?: SelectableItem[]
  }>(),
  {
    modelValue:  '20_08',
    items: () => []
  }
)
const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

const items = computed<(CheckboxProps | { label: string; children: CheckboxProps[] })[]>(() =>
  props.items.map((item) =>
    'children' in item
      ? {
          label: item.label,
          children: item.children.map((child) => ({
            label: child.label,
            value: child.ids
          }))
        }
      : {
          label: item.label,
          value: item.ids
        }
  )
)

const selectableItem = ref<string[]>(['20_08'])

watch(
  selectableItem,
  (value) => {
    emit(
      'update:modelValue',
      value[0]
    )
  },
  { immediate: true }
)
</script>

<template>
  <v-card flat>
    <v-card-item>
      <v-card-title class="text-capitalize">Dates</v-card-title>
    </v-card-item>
    <v-card-item>
      <v-radio-group
        v-model='selectableItem'
      >
        <v-radio  v-for="(item, index) in items" :key="index"
        :label="item.label"
        :value="item.value"></v-radio>
      </v-radio-group>
    </v-card-item>
  </v-card>
</template>
