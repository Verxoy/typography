<script setup lang="ts">
import { formatRuPhone, parseRuPhoneDigits, RU_PHONE_PLACEHOLDER } from '@/utils/ruPhone'

const model = defineModel<string>({ default: '' })

withDefaults(
  defineProps<{
    id?: string
    required?: boolean
    inputClass?: string
    placeholder?: string
  }>(),
  {
    required: false,
    inputClass: 'form-input',
    placeholder: RU_PHONE_PLACEHOLDER,
  },
)

function onInput(event: Event) {
  const el = event.target as HTMLInputElement
  const formatted = formatRuPhone(el.value)
  model.value = formatted
  if (el.value !== formatted) {
    el.value = formatted
  }
}

function onFocus() {
  if (!model.value.trim()) {
    model.value = '+7 '
  }
}

function onBlur() {
  const digits = parseRuPhoneDigits(model.value)
  if (digits.length <= 1) {
    model.value = ''
  }
}
</script>

<template>
  <input
    :id="id"
    type="tel"
    inputmode="tel"
    autocomplete="tel"
    :class="inputClass"
    :placeholder="placeholder"
    :required="required"
    :value="model"
    @input="onInput"
    @focus="onFocus"
    @blur="onBlur"
  />
</template>
