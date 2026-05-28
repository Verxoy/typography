<script setup lang="ts">
import { computed } from 'vue'
import type { TechSubs } from '@/data/technologies'

const props = defineProps<{
  subs: TechSubs
  /** Скрыть вводные абзацы (оставить только подсказку и список) */
  hideIntro?: boolean
}>()

const activeId = defineModel<string>('activeId', { required: true })

const activeItem = computed(() => props.subs.items.find((item) => item.id === activeId.value) ?? null)
</script>

<template>
  <div class="tech-sub">
    <template v-if="!hideIntro">
      <p
        v-for="(para, i) in subs.intro"
        :key="`intro-${i}`"
        class="tech-sub-intro"
        :class="{ 'tech-sub-intro--lead': i === 0 }"
      >
        {{ para }}
      </p>
    </template>
    <p v-if="subs.itemsIntro" class="tech-sub-hint">{{ subs.itemsIntro }}</p>

    <div class="tech-sub-layout">
      <ul class="tech-sub-nav" role="list">
        <li v-for="item in subs.items" :key="item.id" role="listitem">
          <button
            type="button"
            class="tech-sub-nav-btn"
            :class="{ 'tech-sub-nav-btn--active': activeId === item.id }"
            @click="activeId = item.id"
          >
            <span class="tech-sub-nav-marker" aria-hidden="true" />
            <span class="tech-sub-nav-label">{{ item.title }}</span>
          </button>
        </li>
      </ul>

      <article v-if="activeItem" class="tech-sub-detail">
        <h4 class="tech-sub-detail-title">{{ activeItem.title }}</h4>
        <template v-for="(block, bi) in activeItem.blocks" :key="bi">
          <p v-if="block.type === 'paragraph'" class="tech-sub-text">{{ block.text }}</p>
          <h5 v-else-if="block.type === 'heading'" class="tech-sub-heading">{{ block.text }}</h5>
          <ul v-else-if="block.type === 'list'" class="tech-sub-list">
            <li v-for="(line, li) in block.items" :key="li">{{ line }}</li>
          </ul>
        </template>
      </article>
    </div>
  </div>
</template>

<style scoped>
.tech-sub-intro {
  margin: 0 0 10px;
  font-size: 0.94rem;
  line-height: 1.65;
  color: #555;
}

.tech-sub-intro--lead {
  font-weight: 600;
  color: #333;
}

.tech-sub-hint {
  margin: 0 0 14px;
  font-size: 0.88rem;
  color: #888;
}

.tech-sub-layout {
  display: grid;
  grid-template-columns: minmax(0, 260px) minmax(0, 1fr);
  gap: 16px;
  align-items: start;
}

.tech-sub-nav {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.tech-sub-nav-btn {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  background: #fff;
  cursor: pointer;
  text-align: left;
  font: inherit;
  color: inherit;
  transition: border-color 0.2s, background 0.2s;
}

.tech-sub-nav-btn:hover {
  border-color: #d0d0d0;
  background: #fafafa;
}

.tech-sub-nav-btn--active {
  border-color: #c8c8c8;
  background: #f5f5f5;
}

.tech-sub-nav-marker {
  flex-shrink: 0;
  width: 3px;
  align-self: stretch;
  min-height: 18px;
  border-radius: 2px;
  background: #e0e0e0;
  transition: background 0.2s;
}

.tech-sub-nav-btn--active .tech-sub-nav-marker {
  background: #008000;
}

.tech-sub-nav-label {
  font-size: 0.84rem;
  font-weight: 500;
  line-height: 1.35;
  color: #444;
}

.tech-sub-nav-btn--active .tech-sub-nav-label {
  font-weight: 600;
  color: #333;
}

.tech-sub-detail {
  padding: 18px 20px;
  background: #fff;
  border: 1px solid #e8e8e8;
  border-radius: 10px;
  max-height: 480px;
  overflow-y: auto;
}

.tech-sub-detail-title {
  margin: 0 0 14px;
  padding-bottom: 10px;
  font-size: 1.05rem;
  font-weight: 700;
  color: #333;
  border-bottom: 1px solid #eee;
}

.tech-sub-text {
  margin: 0 0 12px;
  font-size: 0.94rem;
  line-height: 1.65;
  color: #555;
}

.tech-sub-text:last-child {
  margin-bottom: 0;
}

.tech-sub-heading {
  margin: 16px 0 8px;
  font-size: 0.92rem;
  font-weight: 600;
  color: #444;
}

.tech-sub-list {
  margin: 0 0 12px;
  padding-left: 20px;
  font-size: 0.9rem;
  line-height: 1.6;
  color: #555;
}

.tech-sub-list li {
  margin-bottom: 6px;
}

.tech-sub-list li:last-child {
  margin-bottom: 0;
}

@media (max-width: 768px) {
  .tech-sub-layout {
    grid-template-columns: 1fr;
  }

  .tech-sub-nav {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 6px;
  }

  .tech-sub-detail {
    max-height: none;
  }
}

@media (max-width: 480px) {
  .tech-sub-nav {
    grid-template-columns: 1fr;
  }
}
</style>
