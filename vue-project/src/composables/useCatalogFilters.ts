import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  CATALOG_SECTIONS,
  DEFAULT_CATALOG_SECTION_TITLE,
  getProductsForSectionTitle,
  searchProductsByTitle,
  WHOLE_CATALOG_TITLE,
  CATALOG_SECTION_BY_ID,
  CATALOG_SECTION_BY_TITLE,
} from '../data/catalog'

function readQueryString(value: unknown): string {
  if (typeof value === 'string') return value
  if (Array.isArray(value) && typeof value[0] === 'string') return value[0]
  return ''
}

function parseSectionTitle(raw: string): string {
  if (!raw || raw === 'all') return WHOLE_CATALOG_TITLE
  if (raw === WHOLE_CATALOG_TITLE) return WHOLE_CATALOG_TITLE
  if (raw in CATALOG_SECTION_BY_TITLE) return raw
  const byId = CATALOG_SECTION_BY_ID[raw as keyof typeof CATALOG_SECTION_BY_ID]
  if (byId) return byId.title
  return DEFAULT_CATALOG_SECTION_TITLE
}

function isGlobalRouteQuery(sectionRaw: string, routeMode: string): boolean {
  return (
    routeMode === 'search' ||
    sectionRaw === 'all' ||
    sectionRaw === WHOLE_CATALOG_TITLE
  )
}

/** Один раз при открытии страницы — дальше только локальное состояние. */
function readInitialCatalogState(route: ReturnType<typeof useRoute>) {
  const activeSectionTitle = ref(DEFAULT_CATALOG_SECTION_TITLE)
  const searchQuery = ref('')
  const isGlobalSearch = ref(false)

  if (route.name !== 'Catalog') {
    return { activeSectionTitle, searchQuery, isGlobalSearch }
  }

  const sectionRaw = readQueryString(route.query.section)
  const routeMode = readQueryString(route.query.mode)

  if (isGlobalRouteQuery(sectionRaw, routeMode)) {
    isGlobalSearch.value = true
    activeSectionTitle.value = WHOLE_CATALOG_TITLE
    searchQuery.value = readQueryString(route.query.q)
  } else if (sectionRaw) {
    activeSectionTitle.value = parseSectionTitle(sectionRaw)
  }

  return { activeSectionTitle, searchQuery, isGlobalSearch }
}

export function useCatalogFilters() {
  const route = useRoute()
  const router = useRouter()

  const { activeSectionTitle, searchQuery, isGlobalSearch } = readInitialCatalogState(route)

  function replaceCatalogQuery(query: Record<string, string>) {
    void router.replace({ path: '/catalog', query }).catch(() => {})
  }

  function startGlobalSearch() {
    isGlobalSearch.value = true
    activeSectionTitle.value = WHOLE_CATALOG_TITLE
    searchQuery.value = ''
  }

  function clearSearch() {
    searchQuery.value = ''
  }

  function exitGlobalSearch() {
    searchQuery.value = ''
    isGlobalSearch.value = false
    activeSectionTitle.value = DEFAULT_CATALOG_SECTION_TITLE
    replaceCatalogQuery({ section: DEFAULT_CATALOG_SECTION_TITLE })
  }

  function selectSection(sectionTitle: string) {
    searchQuery.value = ''
    isGlobalSearch.value = false
    activeSectionTitle.value = sectionTitle
    replaceCatalogQuery({ section: sectionTitle })
  }

  const filteredProducts = computed(() => {
    if (isGlobalSearch.value) {
      return searchProductsByTitle(searchQuery.value)
    }
    return getProductsForSectionTitle(activeSectionTitle.value)
  })

  const catalogGridKey = computed(() =>
    isGlobalSearch.value ? `global:${searchQuery.value}` : `section:${activeSectionTitle.value}`
  )

  const isSearchActive = computed(
    () => isGlobalSearch.value && Boolean(searchQuery.value.trim())
  )

  const pageTitle = computed(() =>
    isGlobalSearch.value ? WHOLE_CATALOG_TITLE : activeSectionTitle.value
  )

  const resultsCount = computed(() => filteredProducts.value.length)

  return {
    CATALOG_SECTIONS,
    WHOLE_CATALOG_TITLE,
    activeSectionTitle,
    isGlobalSearch,
    pageTitle,
    searchQuery,
    catalogGridKey,
    isSearchActive,
    filteredProducts,
    resultsCount,
    selectSection,
    startGlobalSearch,
    clearSearch,
    exitGlobalSearch,
  }
}
