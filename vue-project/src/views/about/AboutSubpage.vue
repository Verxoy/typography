<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AboutSubnav from '@/components/about/AboutSubnav.vue'
import { ABOUT_SUBPAGES, type AboutBlock } from '@/data/about'

const route = useRoute()

const sectionId = computed(() => {
  const path = route.path
  if (path.includes('/clients')) return 'clients' as const
  if (path.includes('/partners')) return 'partners' as const
  if (path.includes('/advantages')) return 'advantages' as const
  return null
})

const page = computed(() => {
  const id = sectionId.value
  return id ? ABOUT_SUBPAGES[id] : null
})

const photoSlots = computed(() => {
  const count = page.value?.photoCount ?? 0
  return Array.from({ length: count }, (_, i) => i + 1)
})

function blockKey(block: AboutBlock, index: number) {
  return `${block.type}-${index}`
}
</script>

<template>
  <div v-if="page" class="app about-subpage">
    <main class="main-content about-subpage__main">
      <div class="container about-subpage__container">
        <h1 class="page-title about-subpage__title">{{ page.title }}</h1>
        <p v-if="page.subtitle" class="page-subtitle about-subpage__subtitle">{{ page.subtitle }}</p>

        <AboutSubnav />

        <!-- Заказчикам: технические требования -->
        <article v-if="page.layout === 'prose'" class="about-prose">
          <template v-for="(block, index) in page.blocks" :key="blockKey(block, index)">
            <p v-if="block.type === 'paragraph'" class="about-prose__p">{{ block.text }}</p>
            <div v-else-if="block.type === 'warning'" class="about-prose__warning" role="note">
              {{ block.text }}
            </div>
            <h2 v-else-if="block.type === 'heading'" class="about-prose__h">{{ block.text }}</h2>
            <ul v-else-if="block.type === 'list'" class="about-prose__list">
              <li v-for="(item, i) in block.items" :key="i">{{ item }}</li>
            </ul>
            <aside v-else-if="block.type === 'note'" class="about-prose__note">
              <h3 class="about-prose__note-title">{{ block.title }}</h3>
              <ul class="about-prose__list">
                <li v-for="(item, i) in block.items" :key="i">{{ item }}</li>
              </ul>
            </aside>
          </template>
        </article>

        <!-- Партнёры: письмо + фото -->
        <template v-else-if="page.layout === 'partners'">
          <div class="about-partners">
          <article class="about-letter">
            <p v-for="(text, index) in page.blocks" :key="index" class="about-letter__p">
              {{ text.type === 'paragraph' ? text.text : '' }}
            </p>
            <footer v-if="page.signature?.length" class="about-letter__sign">
              <p v-for="(line, index) in page.signature" :key="index">{{ line }}</p>
            </footer>
          </article>
          <div class="about-gallery about-gallery--partners">
            <div
              v-for="n in photoSlots"
              :key="n"
              class="about-photo-slot about-photo-slot--partner"
            >
              <span class="about-photo-slot__label">Фото {{ n }}</span>
              <span class="about-photo-slot__hint">Загрузите изображение партнёра</span>
            </div>
          </div>
          </div>
        </template>

        <!-- Преимущества: заголовок + крупные фото -->
        <template v-else-if="page.layout === 'advantages'">
          <p v-if="page.lead" class="about-advantages-lead">{{ page.lead }}</p>
          <p
            v-for="(block, index) in page.blocks"
            :key="index"
            class="about-advantages-text"
          >
            {{ block.type === 'paragraph' ? block.text : '' }}
          </p>
          <div class="about-gallery about-gallery--advantages">
            <div
              v-for="n in photoSlots"
              :key="n"
              class="about-photo-slot about-photo-slot--hero"
            >
              <span class="about-photo-slot__label">Фото {{ n }}</span>
              <span class="about-photo-slot__hint">Место для фотографии</span>
            </div>
          </div>
        </template>
      </div>
    </main>
  </div>
</template>

<style scoped>
.about-subpage__main {
  padding-top: 28px;
  padding-bottom: 36px;
}

.about-subpage__title {
  margin-bottom: 6px;
}

.about-subpage__subtitle {
  margin-bottom: 22px;
}

/* ——— Заказчикам ——— */
.about-prose {
  max-width: 920px;
  margin: 0 auto;
}

.about-prose__p {
  font-size: 15px;
  line-height: 1.72;
  color: #555;
  margin: 0 0 14px;
}

.about-prose__h {
  font-size: 20px;
  color: #333;
  margin: 22px 0 12px;
  font-family: var(--font-heading);
}

.about-prose__list {
  margin: 0 0 16px;
  padding-left: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.about-prose__list li {
  font-size: 15px;
  line-height: 1.65;
  color: #555;
}

.about-prose__warning {
  background: #fff5ec;
  border-left: 4px solid #ff7722;
  border-radius: 0 12px 12px 0;
  padding: 14px 18px;
  margin: 16px 0;
  font-size: 15px;
  line-height: 1.65;
  color: #444;
  font-weight: 500;
}

.about-prose__note {
  background: #f8f8f8;
  border-radius: 14px;
  padding: 20px 22px;
  margin: 20px 0 16px;
  border: 1px solid #ebebeb;
}

.about-prose__note-title {
  font-size: 17px;
  color: #333;
  margin: 0 0 12px;
  font-family: var(--font-heading);
}

/* ——— Партнёры ——— */
.about-partners {
  width: 100%;
}

.about-letter {
  width: 100%;
  max-width: none;
  margin: 0 0 28px;
}

.about-letter__p {
  font-size: 17px;
  line-height: 1.75;
  color: #444;
  margin: 0 0 16px;
  text-align: justify;
}

.about-letter__sign {
  margin-top: 28px;
  padding-top: 20px;
  border-top: 1px solid #e8e8e8;
}

.about-letter__sign p {
  margin: 0 0 4px;
  font-size: 16px;
  color: #333;
  font-style: italic;
}

.about-letter__sign p:last-child {
  font-weight: 600;
  font-style: normal;
}

.about-gallery--partners {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 20px;
  width: 100%;
}

.about-photo-slot--partner {
  min-height: 220px;
}

/* ——— Преимущества ——— */
.about-advantages-lead {
  font-size: clamp(20px, 3vw, 26px);
  font-weight: 700;
  text-align: center;
  color: #008000;
  margin: 0 0 16px;
  font-family: var(--font-heading);
  line-height: 1.35;
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
}

.about-advantages-text {
  text-align: center;
  font-size: 18px;
  color: #555;
  margin: 0 0 28px;
  line-height: 1.6;
}

.about-gallery--advantages {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20px;
  width: 100%;
}

.about-photo-slot--hero {
  min-height: min(34vh, 380px);
  aspect-ratio: 4 / 3;
}

.about-gallery--advantages .about-photo-slot--hero:nth-child(3) {
  grid-column: 1 / -1;
  min-height: min(40vh, 440px);
  aspect-ratio: 21 / 9;
}

/* ——— Плейсхолдеры фото ——— */
.about-photo-slot {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: linear-gradient(145deg, #f5f5f5 0%, #ebebeb 100%);
  border: 2px dashed #ccc;
  border-radius: 16px;
  text-align: center;
  padding: 24px;
  transition: border-color 0.25s;
}

.about-photo-slot:hover {
  border-color: rgba(255, 119, 34, 0.5);
}

.about-photo-slot__label {
  font-size: 18px;
  font-weight: 600;
  color: #888;
  font-family: var(--font-heading);
}

.about-photo-slot__hint {
  font-size: 13px;
  color: #aaa;
}

@media (max-width: 992px) {
  .about-gallery--partners {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .about-photo-slot--partner {
    min-height: 180px;
  }
}

@media (max-width: 768px) {
  .about-gallery--advantages {
    grid-template-columns: 1fr;
  }

  .about-gallery--advantages .about-photo-slot--hero:nth-child(3) {
    grid-column: auto;
    aspect-ratio: 4 / 3;
  }

  .about-photo-slot--hero {
    min-height: 260px;
    aspect-ratio: 16 / 9;
  }
}

@media (max-width: 600px) {
  .about-gallery--partners {
    grid-template-columns: 1fr;
  }
}
</style>
