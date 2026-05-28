<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { apiFetch } from '@/api/http'
import { resolveMediaUrl } from '@/composables/useCmsUpload'

type PortfolioItem = {
  id: number
  title: string
  imageUrl: string
  altText: string
}

type DisplayItem = PortfolioItem & { src: string }

const items = ref<PortfolioItem[]>([])
const activeIndex = ref(0)
const heroPaused = ref(false)
const marqueePaused = ref(false)
let timer: ReturnType<typeof setInterval> | null = null

/** Минимум карточек в одном «витке» ленты — чтобы на широком экране не было пустоты */
const MARQUEE_MIN_PER_LOOP = 10

const displayItems = computed<DisplayItem[]>(() =>
  items.value.map((item) => ({
    ...item,
    src: resolveMediaUrl(item.imageUrl),
  })),
)

/** Один цикл ленты: повторяем исходный список, пока не наберём достаточную длину */
const marqueeLoop = computed(() => {
  const list = displayItems.value
  if (!list.length) return []
  const loop: DisplayItem[] = []
  while (loop.length < MARQUEE_MIN_PER_LOOP) {
    for (const item of list) loop.push(item)
  }
  return loop
})

function goTo(index: number) {
  if (!displayItems.value.length) return
  activeIndex.value = (index + displayItems.value.length) % displayItems.value.length
}

function next() {
  goTo(activeIndex.value + 1)
}

function prev() {
  goTo(activeIndex.value - 1)
}

function startAutoplay() {
  stopAutoplay()
  if (displayItems.value.length < 2) return
  timer = setInterval(() => {
    if (!heroPaused.value) next()
  }, 4500)
}

function stopAutoplay() {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
}

onMounted(async () => {
  try {
    const data = await apiFetch<{ items: PortfolioItem[] }>('/portfolio/')
    items.value = data.items ?? []
    startAutoplay()
  } catch {
    items.value = []
  }
})

onUnmounted(stopAutoplay)
</script>

<template>
  <section v-if="displayItems.length" class="portfolio-showcase" aria-labelledby="portfolio-heading">
    <div class="container portfolio-showcase__head">
      <h2 id="portfolio-heading" class="portfolio-showcase__title">Готовые работы</h2>
      <p class="portfolio-showcase__lead">
        Примеры продукции с нашего производства — календари, упаковка, реклама и сувениры
      </p>
    </div>

    <div
      class="portfolio-showcase__hero"
      @mouseenter="heroPaused = true"
      @mouseleave="heroPaused = false"
      @focusin="heroPaused = true"
      @focusout="heroPaused = false"
    >
      <button
        type="button"
        class="portfolio-showcase__nav portfolio-showcase__nav--prev"
        aria-label="Предыдущее фото"
        @click="prev"
      >
        ‹
      </button>

      <div class="portfolio-showcase__stage">
        <transition-group name="portfolio-fade" tag="div" class="portfolio-showcase__slides">
          <figure
            v-for="(item, i) in displayItems"
            v-show="i === activeIndex"
            :key="item.id"
            class="portfolio-showcase__figure"
          >
            <img :src="item.src" :alt="item.altText" class="portfolio-showcase__img" loading="lazy" />
            <figcaption v-if="item.title" class="portfolio-showcase__caption">{{ item.title }}</figcaption>
          </figure>
        </transition-group>
      </div>

      <button
        type="button"
        class="portfolio-showcase__nav portfolio-showcase__nav--next"
        aria-label="Следующее фото"
        @click="next"
      >
        ›
      </button>

      <div class="portfolio-showcase__dots" role="tablist" aria-label="Выбор фотографии">
        <button
          v-for="(item, i) in displayItems"
          :key="`dot-${item.id}`"
          type="button"
          class="portfolio-showcase__dot"
          :class="{ 'portfolio-showcase__dot--active': i === activeIndex }"
          :aria-selected="i === activeIndex"
          :aria-label="item.title || `Фото ${i + 1}`"
          @click="goTo(i)"
        />
      </div>
    </div>

    <div
      v-if="marqueeLoop.length"
      class="portfolio-showcase__marquee"
      aria-hidden="true"
      @mouseenter="marqueePaused = true"
      @mouseleave="marqueePaused = false"
    >
      <div
        class="portfolio-showcase__marquee-track"
        :class="{ 'portfolio-showcase__marquee-track--paused': marqueePaused }"
        :style="{ '--marquee-duration': `${Math.max(28, marqueeLoop.length * 5)}s` }"
      >
        <div class="portfolio-showcase__marquee-group">
          <div
            v-for="(item, i) in marqueeLoop"
            :key="`a-${item.id}-${i}`"
            class="portfolio-showcase__marquee-item"
          >
            <img :src="item.src" alt="" loading="lazy" />
          </div>
        </div>
        <div class="portfolio-showcase__marquee-group" aria-hidden="true">
          <div
            v-for="(item, i) in marqueeLoop"
            :key="`b-${item.id}-${i}`"
            class="portfolio-showcase__marquee-item"
          >
            <img :src="item.src" alt="" loading="lazy" />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.portfolio-showcase {
  padding: 48px 0 56px;
  background: linear-gradient(180deg, #fafafa 0%, #fff 45%, #f7f4f0 100%);
  overflow: hidden;
}

.portfolio-showcase__head {
  text-align: center;
  margin-bottom: 28px;
}

.portfolio-showcase__title {
  font-size: clamp(1.5rem, 3vw, 2rem);
  font-weight: 700;
  color: #222;
  margin: 0 0 10px;
}

.portfolio-showcase__lead {
  margin: 0 auto;
  max-width: 640px;
  color: #666;
  font-size: 1rem;
  line-height: 1.5;
}

.portfolio-showcase__hero {
  position: relative;
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 48px;
}

.portfolio-showcase__stage {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.12);
  background: #111;
  aspect-ratio: 16 / 9;
  min-height: 220px;
}

.portfolio-showcase__slides {
  position: relative;
  width: 100%;
  height: 100%;
}

.portfolio-showcase__figure {
  position: absolute;
  inset: 0;
  margin: 0;
}

.portfolio-showcase__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.portfolio-showcase__caption {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  margin: 0;
  padding: 14px 20px;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.75));
  color: #fff;
  font-size: 1rem;
  font-weight: 600;
}

.portfolio-showcase__nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 2;
  width: 44px;
  height: 44px;
  border: none;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.92);
  color: #333;
  font-size: 1.75rem;
  line-height: 1;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transition: background 0.2s, transform 0.2s;
}

.portfolio-showcase__nav:hover {
  background: #fff;
  transform: translateY(-50%) scale(1.05);
}

.portfolio-showcase__nav--prev {
  left: 4px;
}

.portfolio-showcase__nav--next {
  right: 4px;
}

.portfolio-showcase__dots {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 16px;
}

.portfolio-showcase__dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: none;
  background: #ccc;
  cursor: pointer;
  padding: 0;
  transition: background 0.2s, transform 0.2s;
}

.portfolio-showcase__dot--active {
  background: #f72;
  transform: scale(1.2);
}

.portfolio-fade-enter-active,
.portfolio-fade-leave-active {
  transition: opacity 0.7s ease;
}

.portfolio-fade-enter-from,
.portfolio-fade-leave-to {
  opacity: 0;
}

.portfolio-showcase__marquee {
  margin-top: 32px;
  overflow: hidden;
  width: 100%;
  mask-image: linear-gradient(90deg, transparent, #000 6%, #000 94%, transparent);
}

.portfolio-showcase__marquee-track {
  display: flex;
  width: max-content;
  will-change: transform;
  animation: portfolio-marquee-scroll var(--marquee-duration, 50s) linear infinite;
}

.portfolio-showcase__marquee-track--paused {
  animation-play-state: paused;
}

.portfolio-showcase__marquee-group {
  display: flex;
  flex-shrink: 0;
  gap: 14px;
  padding-right: 14px;
}

.portfolio-showcase__marquee-item {
  flex: 0 0 auto;
  width: 200px;
  height: 120px;
  border-radius: 10px;
  overflow: hidden;
  opacity: 0.9;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}

.portfolio-showcase__marquee-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* Сдвиг ровно на ширину первой группы — бесшовный цикл */
@keyframes portfolio-marquee-scroll {
  0% {
    transform: translate3d(0, 0, 0);
  }
  100% {
    transform: translate3d(-50%, 0, 0);
  }
}

@media (max-width: 768px) {
  .portfolio-showcase__hero {
    padding: 0 12px;
  }

  .portfolio-showcase__nav {
    width: 36px;
    height: 36px;
    font-size: 1.4rem;
  }

  .portfolio-showcase__marquee-item {
    width: 140px;
    height: 88px;
  }
}
</style>
