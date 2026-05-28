<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue'
import TechSubsectionExplorer from '@/components/technologies/TechSubsectionExplorer.vue'
import {
  PRINT_SUB_TABS,
  TECH_SIDEBAR_ITEMS,
  TECHNOLOGY_SECTIONS,
  paragraphItemsToSubs,
  type PrintSubId,
  type TechnologySection,
} from '@/data/technologies'

const sections = TECHNOLOGY_SECTIONS
const sidebarItems = TECH_SIDEBAR_ITEMS

const openSectionId = ref<string | null>('print')
const printSubView = ref<PrintSubId>('formats')
const activePrintTypeId = ref('uv')
const activePaperId = ref('recycled-board')
const activePrepressId = ref('brand-design')
const activePostpressId = ref('piccolo')

const printSection = computed(() => sections.find((s) => s.id === 'print'))

const printTypesSubs = computed(() => {
  const types = printSection.value?.printSubs?.types
  if (!types) return { intro: [], items: [] }
  return paragraphItemsToSubs(types.items, types.intro)
})

const printPaperSubs = computed(() => {
  const paper = printSection.value?.printSubs?.paper
  if (!paper) return { intro: [], items: [] }
  return paragraphItemsToSubs(paper.items, paper.intro)
})

watch(printSubView, (view) => {
  if (view === 'types' && !activePrintTypeId.value) {
    activePrintTypeId.value = printTypesSubs.value.items[0]?.id ?? null
  }
  if (view === 'paper' && !activePaperId.value) {
    activePaperId.value = printPaperSubs.value.items[0]?.id ?? null
  }
})

function toggleSection(id: string) {
  openSectionId.value = openSectionId.value === id ? null : id
  if (id === 'print' && openSectionId.value === 'print') {
    printSubView.value = 'formats'
  }
  if (id === 'prepress' && openSectionId.value === 'prepress') {
    activePrepressId.value = 'brand-design'
  }
  if (id === 'postpress' && openSectionId.value === 'postpress') {
    activePostpressId.value = 'piccolo'
  }
}

function openSectionFromSidebar(title: string) {
  const section = sections.find((s) => s.title === title)
  if (!section) return
  openSectionId.value = section.id
  if (section.id === 'print') printSubView.value = 'formats'
  void nextTick(() => {
    document.getElementById(`tech-${section.id}`)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  })
}

function setPrintSub(id: PrintSubId) {
  printSubView.value = id
}

function isSectionOpen(section: TechnologySection) {
  return openSectionId.value === section.id
}
</script>

<template>
  <div class="app">
    <main class="main-content">
      <div class="container">
        <h1 class="page-title">Технологии</h1>
        <p class="page-subtitle">Современные полиграфические технологии для качественного результата</p>

        <div class="technologies-layout">
          <div class="technologies-main">
            <div class="tech-sections">
              <article
                v-for="section in sections"
                :id="`tech-${section.id}`"
                :key="section.id"
                class="tech-card"
                :class="{ 'tech-card--open': isSectionOpen(section) }"
              >
                <button
                  type="button"
                  class="tech-card-head"
                  :aria-expanded="isSectionOpen(section)"
                  @click="toggleSection(section.id)"
                >
                  <span class="tech-card-icon" :class="`tech-card-icon--${section.icon}`" aria-hidden="true">
                    <svg v-if="section.icon === 'print'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="6 9 6 2 18 2 18 9" />
                      <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2" />
                      <rect x="6" y="14" width="12" height="8" />
                    </svg>
                    <svg v-else-if="section.icon === 'prepress'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="3" width="18" height="18" rx="2" />
                      <circle cx="8.5" cy="8.5" r="1.5" />
                      <polyline points="21 15 16 10 5 21" />
                    </svg>
                    <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z" />
                    </svg>
                  </span>
                  <span class="tech-card-head-text">
                    <span class="tech-card-title">{{ section.title }}</span>
                    <span class="tech-card-desc">{{ section.description }}</span>
                  </span>
                  <span class="tech-card-chevron" :class="{ 'tech-card-chevron--open': isSectionOpen(section) }" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="6 9 12 15 18 9" />
                    </svg>
                  </span>
                </button>

                <div v-show="isSectionOpen(section)" class="tech-card-body">
                  <!-- Печать: три подраздела -->
                  <template v-if="section.id === 'print' && section.printSubs">
                    <nav class="print-tabs" role="tablist" aria-label="Подразделы печати">
                      <button
                        v-for="tab in PRINT_SUB_TABS"
                        :key="tab.id"
                        type="button"
                        role="tab"
                        class="print-tab"
                        :class="{ 'print-tab--active': printSubView === tab.id }"
                        :aria-selected="printSubView === tab.id"
                        @click="setPrintSub(tab.id)"
                      >
                        <span class="print-tab-full">{{ tab.label }}</span>
                        <span class="print-tab-short">{{ tab.shortLabel }}</span>
                      </button>
                    </nav>

                    <!-- 4+4, 4+1… -->
                    <div
                      v-show="printSubView === 'formats'"
                      class="print-panel"
                      role="tabpanel"
                    >
                      <h3 class="print-panel-title">{{ section.printSubs.formats.title }}</h3>
                      <p
                        v-for="(para, i) in section.printSubs.formats.intro"
                        :key="`intro-${i}`"
                        class="print-text"
                      >
                        {{ para }}
                      </p>
                      <p
                        v-for="(para, i) in section.printSubs.formats.cmyk"
                        :key="`cmyk-${i}`"
                        class="print-text print-text--muted"
                      >
                        {{ para }}
                      </p>
                      <div class="format-grid" role="list">
                        <article
                          v-for="fmt in section.printSubs.formats.formats"
                          :key="fmt.code"
                          class="format-chip"
                          role="listitem"
                        >
                          <span class="format-chip-code">{{ fmt.code }}</span>
                          <p class="format-chip-text">{{ fmt.text }}</p>
                        </article>
                      </div>
                    </div>

                    <!-- Виды печати -->
                    <div v-show="printSubView === 'types'" class="print-panel" role="tabpanel">
                      <h3 class="print-panel-title">{{ section.printSubs.types.title }}</h3>
                      <TechSubsectionExplorer
                        v-model:active-id="activePrintTypeId"
                        :subs="printTypesSubs"
                        hide-intro
                      />
                    </div>

                    <!-- Виды бумаги -->
                    <div v-show="printSubView === 'paper'" class="print-panel" role="tabpanel">
                      <h3 class="print-panel-title">{{ section.printSubs.paper.title }}</h3>
                      <TechSubsectionExplorer
                        v-model:active-id="activePaperId"
                        :subs="printPaperSubs"
                        hide-intro
                      />
                    </div>

                  </template>

                  <!-- Предпечатная / постпечатная подготовка -->
                  <TechSubsectionExplorer
                    v-else-if="section.id === 'prepress' && section.subs"
                    v-model:active-id="activePrepressId"
                    :subs="section.subs"
                  />
                  <TechSubsectionExplorer
                    v-else-if="section.id === 'postpress' && section.subs"
                    v-model:active-id="activePostpressId"
                    :subs="section.subs"
                  />

                  <router-link to="/contacts" class="tech-cta">
                    Узнать подробнее
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
                      <line x1="22" y1="2" x2="11" y2="13" />
                      <polygon points="22 2 15 22 11 13 2 9 22 2" />
                    </svg>
                  </router-link>
                </div>
              </article>
            </div>

            <section class="tech-benefits" aria-labelledby="benefits-heading">
              <h2 id="benefits-heading" class="tech-benefits-title">Наши преимущества</h2>
              <div class="tech-benefits-grid">
                <div class="tech-benefit">
                  <span class="tech-benefit-icon" aria-hidden="true">★</span>
                  <h3>Высокое качество</h3>
                  <p>Контроль на каждом этапе производства</p>
                </div>
                <div class="tech-benefit">
                  <span class="tech-benefit-icon" aria-hidden="true">⏱</span>
                  <h3>Сжатые сроки</h3>
                  <p>Оперативное выполнение заказов</p>
                </div>
                <div class="tech-benefit">
                  <span class="tech-benefit-icon" aria-hidden="true">✓</span>
                  <h3>Гарантия результата</h3>
                  <p>Соответствие требованиям заказчика</p>
                </div>
                <div class="tech-benefit">
                  <span class="tech-benefit-icon" aria-hidden="true">₽</span>
                  <h3>Доступные цены</h3>
                  <p>Оптимальное соотношение цены и качества</p>
                </div>
              </div>
            </section>
          </div>

          <aside class="tech-sidebar">
            <nav class="tech-sidebar-nav" aria-label="Разделы технологий">
              <button
                v-for="title in sidebarItems"
                :key="title"
                type="button"
                class="tech-sidebar-btn"
                :class="{ 'tech-sidebar-btn--active': openSectionId === sections.find((s) => s.title === title)?.id }"
                @click="openSectionFromSidebar(title)"
              >
                {{ title }}
              </button>
            </nav>

            <div class="tech-sidebar-cta">
              <h4>Нужна консультация?</h4>
              <p>Специалисты помогут подобрать технологию и материалы</p>
              <router-link to="/contacts" class="tech-sidebar-cta-link">Связаться с нами</router-link>
            </div>
          </aside>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.page-title {
  font-size: clamp(1.75rem, 4vw, 2.625rem);
  color: #008000;
  text-align: center;
  margin-bottom: 10px;
  font-weight: 700;
}

.page-subtitle {
  font-size: 1.05rem;
  color: #666;
  text-align: center;
  margin-bottom: 2.5rem;
  line-height: 1.5;
}

.technologies-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 260px;
  gap: 28px;
  margin-bottom: 48px;
  align-items: start;
}

.technologies-main {
  display: flex;
  flex-direction: column;
  gap: 32px;
  min-width: 0;
}

.tech-sections {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.tech-card {
  background: #f8f8f8;
  border: 1px solid #e8e8e8;
  border-radius: 16px;
  overflow: hidden;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.tech-card--open {
  border-color: #d0d0d0;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.tech-card-head {
  display: flex;
  align-items: center;
  gap: 16px;
  width: 100%;
  padding: 20px 22px;
  border: none;
  background: transparent;
  cursor: pointer;
  text-align: left;
  font: inherit;
  color: inherit;
}

.tech-card-head:hover {
  background: #f0f0f0;
}

.tech-card-icon {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #ff7722;
  color: #fff;
}

.tech-card-icon svg {
  width: 24px;
  height: 24px;
}

.tech-card-head-text {
  flex: 1;
  min-width: 0;
}

.tech-card-title {
  display: block;
  font-size: 1.2rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 4px;
}

.tech-card-desc {
  display: block;
  font-size: 0.9rem;
  color: #666;
  line-height: 1.45;
}

.tech-card-chevron {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #e8e8e8;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.25s, background 0.2s;
}

.tech-card-chevron svg {
  width: 18px;
  height: 18px;
  color: #666;
}

.tech-card-chevron--open {
  transform: rotate(180deg);
  background: rgba(255, 119, 34, 0.15);
}

.tech-card-chevron--open svg {
  color: #666;
}

.tech-card-body {
  padding: 0 22px 22px;
  border-top: 1px solid #ebebeb;
}

/* Подразделы «Печать» */
.print-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 18px 0 16px;
}

.print-tab {
  padding: 8px 14px;
  border: 1px solid #ddd;
  border-radius: 999px;
  background: #fff;
  font-size: 0.82rem;
  font-weight: 600;
  color: #555;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s, color 0.2s;
  line-height: 1.25;
}

.print-tab:hover {
  border-color: #bbb;
  color: #333;
}

.print-tab--active {
  background: #f5f5f5;
  border-color: #999;
  color: #333;
}

.print-tab-short {
  display: none;
}

.print-panel {
  animation: panel-in 0.2s ease;
}

@keyframes panel-in {
  from {
    opacity: 0;
    transform: translateY(4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.print-panel-title {
  margin: 0 0 8px;
  font-size: 1.05rem;
  font-weight: 700;
  color: #333;
  line-height: 1.35;
}

.print-text {
  margin: 0 0 12px;
  font-size: 0.94rem;
  line-height: 1.65;
  color: #3a3a3a;
}

.print-text--muted {
  color: #555;
  padding: 12px 14px;
  background: #fafafa;
  border-radius: 8px;
  border: 1px solid #eee;
}

.print-text--note {
  font-size: 0.88rem;
  color: #888;
  font-style: italic;
  margin-bottom: 14px;
}

.format-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(168px, 1fr));
  gap: 10px;
  margin-top: 6px;
}

.format-chip {
  padding: 12px 14px;
  background: #fff;
  border-radius: 8px;
  border: 1px solid #e8e8e8;
}

.format-chip-code {
  display: block;
  font-size: 1.05rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 6px;
  font-variant-numeric: tabular-nums;
}

.format-chip-text {
  margin: 0;
  font-size: 0.82rem;
  line-height: 1.5;
  color: #444;
}

.tech-simple-list {
  margin: 16px 0 0;
  padding: 0;
  list-style: none;
}

.tech-simple-list li {
  position: relative;
  padding: 10px 0 10px 22px;
  font-size: 0.94rem;
  color: #333;
  border-bottom: 1px solid #e8e8e8;
}

.tech-simple-list li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #888;
  font-weight: 700;
}

.tech-simple-list li:last-child {
  border-bottom: none;
}

.tech-cta {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-top: 18px;
  padding: 11px 22px;
  background: #ff7722;
  color: #fff;
  border-radius: 999px;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 600;
  transition: background 0.2s, transform 0.2s;
}

.tech-cta:hover {
  background: #e66611;
  transform: translateX(3px);
}

.tech-cta svg {
  width: 16px;
  height: 16px;
}

/* Преимущества */
.tech-benefits {
  background: #f5f5f5;
  border-radius: 16px;
  padding: 28px 24px;
}

.tech-benefits-title {
  text-align: center;
  font-size: 1.35rem;
  color: #333;
  margin-bottom: 20px;
}

.tech-benefits-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
}

.tech-benefit {
  background: #fff;
  border-radius: 12px;
  padding: 18px 14px;
  text-align: center;
  border-bottom: 3px solid #008000;
}

.tech-benefit-icon {
  display: block;
  font-size: 1.25rem;
  margin-bottom: 8px;
}

.tech-benefit h3 {
  font-size: 0.9rem;
  margin-bottom: 6px;
  color: #333;
}

.tech-benefit p {
  font-size: 0.78rem;
  color: #666;
  line-height: 1.45;
  margin: 0;
}

/* Сайдбар */
.tech-sidebar {
  position: sticky;
  top: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.tech-sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 16px;
  background: #f5f5f5;
  border-radius: 16px;
}

.tech-sidebar-btn {
  padding: 11px 14px;
  border: none;
  border-radius: 12px;
  background: #e8e8e8;
  font-size: 0.85rem;
  font-weight: 500;
  color: #333;
  cursor: pointer;
  text-align: center;
  transition: background 0.2s, color 0.2s;
}

.tech-sidebar-btn:hover,
.tech-sidebar-btn--active {
  background: #008000;
  color: #fff;
  font-weight: 600;
}

.tech-sidebar-cta {
  padding: 22px 18px;
  border-radius: 16px;
  background: linear-gradient(135deg, #ff7722, #ff9955);
  text-align: center;
  color: #fff;
}

.tech-sidebar-cta h4 {
  font-size: 1rem;
  margin-bottom: 8px;
}

.tech-sidebar-cta p {
  font-size: 0.85rem;
  opacity: 0.95;
  line-height: 1.45;
  margin-bottom: 14px;
}

.tech-sidebar-cta-link {
  display: inline-block;
  padding: 10px 20px;
  background: #fff;
  color: #ff7722;
  border-radius: 999px;
  text-decoration: none;
  font-size: 0.88rem;
  font-weight: 600;
}

@media (max-width: 1024px) {
  .technologies-layout {
    grid-template-columns: 1fr;
  }

  .tech-sidebar {
    position: static;
  }

  .tech-benefits-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .format-grid {
    grid-template-columns: 1fr;
  }

  .print-tab-full {
    display: none;
  }

  .print-tab-short {
    display: inline;
  }

  .tech-benefits-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .tech-card-head {
    padding: 16px;
  }

  .tech-card-body {
    padding: 0 16px 16px;
  }
}
</style>
