<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import ChatBot from './components/ChatBot.vue'
import SiteFooter from './components/SiteFooter.vue'
import SiteHeader from './components/SiteHeader.vue'

const route = useRoute()
const showSiteChrome = computed(() => !route.path.startsWith('/staff'))
</script>

<template>
  <div class="app-shell">
    <div class="app-shell-main">
      <SiteHeader v-if="showSiteChrome" />
      <router-view />
    </div>
    <SiteFooter v-if="showSiteChrome" />
    <ChatBot />
  </div>
</template>
