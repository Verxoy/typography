<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { ABOUT_NAV, type AboutNavId } from '@/data/about'

const route = useRoute()

const activeId = computed<AboutNavId>(() => {
  if (route.path.startsWith('/about/clients')) return 'clients'
  if (route.path.startsWith('/about/partners')) return 'partners'
  if (route.path.startsWith('/about/advantages')) return 'advantages'
  return 'company'
})
</script>

<template>
  <nav class="about-subnav" aria-label="Раздел «О нас»">
    <router-link
      v-for="item in ABOUT_NAV"
      :key="item.id"
      :to="item.to"
      class="about-subnav__link"
      :class="{ 'about-subnav__link--active': activeId === item.id }"
    >
      {{ item.label }}
    </router-link>
  </nav>
</template>

<style scoped>
.about-subnav {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  margin-bottom: 24px;
}

.about-subnav__link {
  padding: 10px 18px;
  border-radius: 999px;
  border: 1px solid #e0e0e0;
  background: #fff;
  color: #444;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: color 0.2s, background 0.2s, border-color 0.2s, box-shadow 0.2s;
}

.about-subnav__link:hover {
  color: #ff7722;
  border-color: rgba(255, 119, 34, 0.45);
  background: #fffaf5;
}

.about-subnav__link--active {
  color: #fff;
  background: #ff7722;
  border-color: #ff7722;
  box-shadow: 0 4px 14px rgba(255, 119, 34, 0.28);
}

@media (max-width: 600px) {
  .about-subnav__link {
    flex: 1 1 calc(50% - 10px);
    text-align: center;
    padding: 10px 12px;
    font-size: 13px;
  }
}
</style>
