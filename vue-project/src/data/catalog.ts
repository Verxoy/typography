/** Стабильный ключ раздела (URL, фильтры). */
export type CatalogSectionId =
  | 'reklamnaya-poligrafiya'
  | 'reklamnaya-produkciya-mps'
  | 'produkciya-dlya-restoranov'
  | 'kalendari'
  | 'knigi'
  | 'poligrafiya-med'
  | 'upakovka'
  | 'suveniry'

export type CatalogProduct = {
  id: string
  title: string
  sectionId: CatalogSectionId
  sectionTitle: string
  sortOrder: number
  slug?: string
  /** Slug родительской позиции (подраздел внутри «Креативные календари» и т.п.) */
  parentSlug?: string
  imageUrl?: string
}

export type CatalogSection = {
  id: CatalogSectionId
  title: string
  sortOrder: number
}

type SectionProductInput = {
  title: string
  slug?: string
  children?: SectionProductInput[]
}

type SectionInput = {
  id: CatalogSectionId
  title: string
  products: SectionProductInput[]
}

const SECTIONS_INPUT: SectionInput[] = [
  {
    id: 'reklamnaya-poligrafiya',
    title: 'Рекламная полиграфия',
    products: [
      { title: 'Каталоги, буклеты, брошюры', slug: 'katalogi-buklety-broshyury' },
      { title: 'Сертификаты, купоны', slug: 'sertifikaty-kupony' },
      { title: 'Плакаты, постеры, афиши', slug: 'plakaty-postery-afishi' },
      { title: 'Листовки', slug: 'listovki' },
      { title: 'Каталоги', slug: 'katalogi' },
      { title: 'Дисконтные карты', slug: 'diskontnye-karty' },
    ],
  },
  {
    id: 'reklamnaya-produkciya-mps',
    title: 'Рекламная продукция на местах продаж',
    products: [
      { title: 'Шелфтокеры', slug: 'shelftokery' },
      { title: 'Ценники', slug: 'tsenniki' },
      { title: 'Хенгеры', slug: 'henhery' },
      { title: 'Кассовые блюдца (монетницы)', slug: 'kassovye-blyudca-monetnicy' },
      { title: 'Коробки под бумажные чеки', slug: 'korobki-pod-bumazhnye-cheki' },
      { title: 'Воблеры', slug: 'voblery' },
    ],
  },
  {
    id: 'produkciya-dlya-restoranov',
    title: 'Продукция для ресторанов',
    products: [
      { title: 'Меню на болтах', slug: 'menyu-na-boltah' },
      { title: 'Меню с раздвижными кольцами', slug: 'menyu-s-razdvizhnymi-koltsami' },
      { title: 'Меню в твёрдом переплёте', slug: 'menyu-v-tverdom-pereplete' },
      { title: 'Меню-домик', slug: 'menyu-domik' },
      { title: 'Папки для счёта', slug: 'papki-dlya-scheta' },
      { title: 'Однолистовое меню', slug: 'odnolistovoe-menyu' },
      { title: 'Меню-подложка', slug: 'menyu-podlozhka' },
      { title: 'Меню-папка из дерева', slug: 'menyu-papka-iz-dereva' },
      { title: 'Меню-буклет', slug: 'menyu-buklet' },
      { title: 'Меню на пружине', slug: 'menyu-na-pruzhine' },
      { title: 'Меню детское', slug: 'menyu-detskoe' },
      { title: 'Меню вырубное', slug: 'menyu-vyrubnoe' },
      { title: 'Бирдекели', slug: 'birdekeli' },
      { title: 'Барное меню', slug: 'barnoe-menyu' },
    ],
  },
  {
    id: 'kalendari',
    title: 'Календари',
    products: [
      {
        title: 'Креативные календари',
        slug: 'kreativnye-kalendari',
        children: [
          { title: 'Фигурные календари', slug: 'figurnye-kalendari' },
          { title: 'Календарь-пирамида', slug: 'kalendar-piramida' },
          { title: 'Календарь-куб', slug: 'kalendar-kub' },
          { title: 'Календари-книжки', slug: 'kalendari-knizhki' },
          { title: 'Календари с часами', slug: 'kalendari-s-chasami' },
          { title: 'Додэкаэдр', slug: 'dodekaedr' },
          { title: 'Календари с грифельной доской', slug: 'kalendari-s-grifelnoy-doskoy' },
        ],
      },
      { title: 'Настольные календари' },
      { title: 'Настенные календари' },
      { title: 'Квартальные календари' },
      { title: 'Карманные календари' },
    ],
  },
  {
    id: 'knigi',
    title: 'Книги',
    products: [
      { title: 'Книги на скрепке' },
      { title: 'Книги в твёрдой обложке' },
      { title: 'Книги в мягкой обложке' },
    ],
  },
  {
    id: 'poligrafiya-med',
    title: 'Полиграфия для медучреждений',
    products: [
      { title: 'Самокопирующиеся бланки' },
      { title: 'Медицинские карты пациентов' },
      { title: 'Конверты для снимков и результатов анализов' },
      { title: 'Дорхенгеры' },
      { title: 'Бланочная продукция' },
      { title: 'Воблеры для аптек' },
    ],
  },
  {
    id: 'upakovka',
    title: 'Упаковка',
    products: [
      { title: 'Гребешки' },
      { title: 'Этикетки' },
      { title: 'Тубусы' },
      { title: 'Подарочные коробки' },
      { title: 'Обечайки' },
      { title: 'Коробки под различные изделия' },
      { title: 'Коробки под косметику' },
      { title: 'Коробки под кондитерские изделия' },
      { title: 'Коробки под ёлочные шары' },
      { title: 'Коробки под диски' },
      { title: 'Коробки для чая и кофе' },
      { title: 'Коробки для кружек' },
    ],
  },
  {
    id: 'suveniry',
    title: 'Сувениры',
    products: [
      { title: 'Сувенирная продукция из дерева' },
      { title: 'Антибактериальные сувениры' },
    ],
  },
]

function slugifyId(sectionId: string, title: string): string {
  const base = `${sectionId}-${title}`
    .toLowerCase()
    .replace(/[ё]/g, 'e')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
  return base
}

export const CATALOG_SECTIONS: CatalogSection[] = SECTIONS_INPUT.map((s, i) => ({
  id: s.id,
  title: s.title,
  sortOrder: i,
}))

function catalogProductId(sectionId: string, product: SectionProductInput): string {
  if (product.slug) return `${sectionId}--${product.slug}`
  return slugifyId(sectionId, product.title)
}

function flattenSectionProducts(
  section: SectionInput,
  sectionIndex: number
): CatalogProduct[] {
  const out: CatalogProduct[] = []
  let productIndex = 0

  for (const p of section.products) {
    const parentSlug = p.slug
    out.push({
      id: catalogProductId(section.id, p),
      title: p.title,
      sectionId: section.id,
      sectionTitle: section.title,
      sortOrder: sectionIndex * 100 + productIndex,
      slug: p.slug,
    })
    productIndex += 1

    for (const child of p.children ?? []) {
      out.push({
        id: catalogProductId(section.id, child),
        title: child.title,
        sectionId: section.id,
        sectionTitle: section.title,
        sortOrder: sectionIndex * 100 + productIndex,
        slug: child.slug,
        parentSlug,
      })
      productIndex += 1
    }
  }

  return out
}

export const CATALOG_PRODUCTS: CatalogProduct[] = SECTIONS_INPUT.flatMap((section, sectionIndex) =>
  flattenSectionProducts(section, sectionIndex)
)

export function getCatalogProductBySlug(slug: string): CatalogProduct | undefined {
  return CATALOG_PRODUCTS.find((p) => p.slug === slug)
}

export function getChildProductsOf(parentSlug: string): CatalogProduct[] {
  return CATALOG_PRODUCTS.filter((p) => p.parentSlug === parentSlug).sort(
    (a, b) => a.sortOrder - b.sortOrder
  )
}

/** Позиции верхнего уровня раздела (без вложенных подразделов). */
export function getRootProductsForSectionTitle(sectionTitle: string): CatalogProduct[] {
  return getProductsForSectionTitle(sectionTitle).filter((p) => !p.parentSlug)
}

export const CATALOG_SECTION_BY_ID = Object.fromEntries(
  CATALOG_SECTIONS.map((s) => [s.id, s])
) as Record<CatalogSectionId, CatalogSection>

export const CATALOG_SECTION_BY_TITLE = Object.fromEntries(
  CATALOG_SECTIONS.map((s) => [s.title, s])
) as Record<string, CatalogSection>

/** Как в исходном Catalog.vue: раздел → список позиций. */
export const CATALOG_ITEMS_BY_SECTION: Record<string, SectionProductInput[]> = Object.fromEntries(
  SECTIONS_INPUT.map((s) => [s.title, s.products])
)

export const DEFAULT_CATALOG_SECTION_ID: CatalogSectionId = 'reklamnaya-poligrafiya'

export const DEFAULT_CATALOG_SECTION_TITLE =
  CATALOG_SECTION_BY_ID[DEFAULT_CATALOG_SECTION_ID].title

/** Режим «Поиск по всему каталогу». */
export const WHOLE_CATALOG_TITLE = 'Весь каталог'

export function getAllCatalogProducts(): CatalogProduct[] {
  return [...CATALOG_PRODUCTS].sort((a, b) => a.sortOrder - b.sortOrder)
}

function titleWords(normalizedTitle: string): string[] {
  return normalizedTitle.split(/[\s\-–—,/]+/).filter(Boolean)
}

/**
 * Совпадение по названию продукции (без учёта регистра):
 * — с начала всего названия («мен» → «Меню…»);
 * — с начала любого слова («календар» → «Настенные календари»);
 * — вхождение подстроки в название.
 */
export function productTitleMatchesSearch(title: string, normalizedQuery: string): boolean {
  if (!normalizedQuery) return true
  const name = normalizeForSearch(title)
  if (name.startsWith(normalizedQuery)) return true
  if (titleWords(name).some((word) => word.startsWith(normalizedQuery))) return true
  return name.includes(normalizedQuery)
}

function productTitleSearchRank(title: string, normalizedQuery: string): number {
  const name = normalizeForSearch(title)
  if (name.startsWith(normalizedQuery)) return 0
  if (titleWords(name).some((word) => word.startsWith(normalizedQuery))) return 1
  if (name.includes(normalizedQuery)) return 2
  return 100
}

/** Поиск по названию продукции в реальном времени. */
export function searchProductsByTitle(query: string): CatalogProduct[] {
  const all = getAllCatalogProducts()
  const q = normalizeSearchQuery(query)
  if (!q) return all

  return all
    .filter((p) => productTitleMatchesSearch(p.title, q))
    .sort((a, b) => {
      const rankDiff =
        productTitleSearchRank(a.title, q) - productTitleSearchRank(b.title, q)
      if (rankDiff !== 0) return rankDiff
      return a.sortOrder - b.sortOrder
    })
}

/** Позиции раздела в исходном порядке (без поиска). */
export function getProductsForSectionTitle(sectionTitle: string): CatalogProduct[] {
  const section = CATALOG_SECTION_BY_TITLE[sectionTitle]
  const items = CATALOG_ITEMS_BY_SECTION[sectionTitle]
  if (!section || !items?.length) return []

  const byTitle = new Map(
    CATALOG_PRODUCTS.filter((p) => p.sectionId === section.id).map((p) => [p.title, p])
  )

  return items
    .map((item) => byTitle.get(item.title))
    .filter((p): p is CatalogProduct => Boolean(p))
}

/** Миниатюры карточек каталога — файлы в `public/catalog/` */
export const catalogProductImages: Record<string, string> = {
  'reklamnaya-poligrafiya--katalogi-buklety-broshyury': '/catalog/katalogi-buklety-broshyury.png',
  'reklamnaya-poligrafiya--sertifikaty-kupony': '/catalog/sertifikaty-kupony.png',
  'reklamnaya-poligrafiya--plakaty-postery-afishi': '/catalog/plakaty-postery-afishi.png',
  'reklamnaya-poligrafiya--listovki': '/catalog/listovki.png',
  'reklamnaya-poligrafiya--katalogi': '/catalog/katalogi.png',
  'reklamnaya-poligrafiya--diskontnye-karty': '/catalog/diskontnye-karty.png',
  'reklamnaya-produkciya-mps--shelftokery': '/catalog/shelftokery.png',
  'reklamnaya-produkciya-mps--tsenniki': '/catalog/tsenniki.png',
  'reklamnaya-produkciya-mps--henhery': '/catalog/henhery.png',
  'reklamnaya-produkciya-mps--kassovye-blyudca-monetnicy': '/catalog/kassovye-blyudca-monetnicy.png',
  'reklamnaya-produkciya-mps--korobki-pod-bumazhnye-cheki': '/catalog/korobki-pod-bumazhnye-cheki.png',
  'reklamnaya-produkciya-mps--voblery': '/catalog/voblery.png',
  'produkciya-dlya-restoranov--menyu-na-boltah': '/catalog/menyu-na-boltah.png',
  'produkciya-dlya-restoranov--menyu-s-razdvizhnymi-koltsami': '/catalog/menyu-s-razdvizhnymi-koltsami.png',
  'produkciya-dlya-restoranov--menyu-v-tverdom-pereplete': '/catalog/menyu-v-tverdom-pereplete.png',
  'produkciya-dlya-restoranov--menyu-domik': '/catalog/menyu-domik.png',
  'produkciya-dlya-restoranov--papki-dlya-scheta': '/catalog/papki-dlya-scheta.png',
  'produkciya-dlya-restoranov--odnolistovoe-menyu': '/catalog/odnolistovoe-menyu.png',
  'produkciya-dlya-restoranov--menyu-podlozhka': '/catalog/menyu-podlozhka.png',
  'produkciya-dlya-restoranov--menyu-papka-iz-dereva': '/catalog/menyu-papka-iz-dereva.png',
  'produkciya-dlya-restoranov--menyu-buklet': '/catalog/menyu-buklet.png',
  'produkciya-dlya-restoranov--menyu-na-pruzhine': '/catalog/menyu-na-pruzhine.png',
  'produkciya-dlya-restoranov--menyu-detskoe': '/catalog/menyu-detskoe.png',
  'produkciya-dlya-restoranov--menyu-vyrubnoe': '/catalog/menyu-vyrubnoe.png',
  'produkciya-dlya-restoranov--birdekeli': '/catalog/birdekeli.png',
  'produkciya-dlya-restoranov--barnoe-menyu': '/catalog/barnoe-menyu.png',
}

/** Дополнительно по slug (если удобнее подключать фото) */
export const catalogProductImagesBySlug: Record<string, string> = {
  'katalogi-buklety-broshyury': '/catalog/katalogi-buklety-broshyury.png',
  'sertifikaty-kupony': '/catalog/sertifikaty-kupony.png',
  'plakaty-postery-afishi': '/catalog/plakaty-postery-afishi.png',
  listovki: '/catalog/listovki.png',
  katalogi: '/catalog/katalogi.png',
  'diskontnye-karty': '/catalog/diskontnye-karty.png',
  shelftokery: '/catalog/shelftokery.png',
  tsenniki: '/catalog/tsenniki.png',
  henhery: '/catalog/henhery.png',
  'kassovye-blyudca-monetnicy': '/catalog/kassovye-blyudca-monetnicy.png',
  'korobki-pod-bumazhnye-cheki': '/catalog/korobki-pod-bumazhnye-cheki.png',
  voblery: '/catalog/voblery.png',
  'menyu-na-boltah': '/catalog/menyu-na-boltah.png',
  'menyu-s-razdvizhnymi-koltsami': '/catalog/menyu-s-razdvizhnymi-koltsami.png',
  'menyu-v-tverdom-pereplete': '/catalog/menyu-v-tverdom-pereplete.png',
  'menyu-domik': '/catalog/menyu-domik.png',
  'papki-dlya-scheta': '/catalog/papki-dlya-scheta.png',
  'odnolistovoe-menyu': '/catalog/odnolistovoe-menyu.png',
  'menyu-podlozhka': '/catalog/menyu-podlozhka.png',
  'menyu-papka-iz-dereva': '/catalog/menyu-papka-iz-dereva.png',
  'menyu-buklet': '/catalog/menyu-buklet.png',
  'menyu-na-pruzhine': '/catalog/menyu-na-pruzhine.png',
  'menyu-detskoe': '/catalog/menyu-detskoe.png',
  'menyu-vyrubnoe': '/catalog/menyu-vyrubnoe.png',
  birdekeli: '/catalog/birdekeli.png',
  'barnoe-menyu': '/catalog/barnoe-menyu.png',
}

export function productDetailPath(product: CatalogProduct): string {
  if (product.slug) return `/catalog/product/${product.slug}`
  return '/contacts'
}

export function productImageUrl(product: CatalogProduct): string | undefined {
  if (product.imageUrl) return product.imageUrl
  if (product.slug && catalogProductImagesBySlug[product.slug]) {
    return catalogProductImagesBySlug[product.slug]
  }
  return catalogProductImages[product.id]
}

export type CatalogSortId = 'section-asc' | 'product-asc' | 'product-desc'

export const CATALOG_SORT_OPTIONS: { id: CatalogSortId; label: string }[] = [
  { id: 'section-asc', label: 'По названию каталога' },
  { id: 'product-asc', label: 'По названию продукции (А–Я)' },
  { id: 'product-desc', label: 'По названию продукции (Я–А)' },
]

export const DEFAULT_CATALOG_SORT: CatalogSortId = 'section-asc'

/** Для поиска: ё→е, без учёта регистра. */
export function normalizeForSearch(text: string): string {
  return text.trim().toLocaleLowerCase('ru').replace(/ё/g, 'е').replace(/\s+/g, ' ')
}

export function normalizeSearchQuery(q: string): string {
  return normalizeForSearch(q)
}

/** Буквы запроса встречаются в тексте по порядку (без учёта регистра). */
function matchesLetterSequence(haystack: string, needle: string): boolean {
  if (needle.length < 2) return false
  let pos = 0
  for (const ch of haystack) {
    if (ch === needle[pos]) pos += 1
    if (pos === needle.length) return true
  }
  return false
}

function sectionMatchesQuery(sectionTitle: string, q: string): boolean {
  const section = normalizeForSearch(sectionTitle)
  return section.includes(q) || matchesLetterSequence(section, q)
}

function titleMatchesQuery(title: string, q: string): boolean {
  const name = normalizeForSearch(title)
  return name.startsWith(q) || name.includes(q) || matchesLetterSequence(name, q)
}

export function productMatchesSearch(product: CatalogProduct, normalizedQuery: string): boolean {
  if (!normalizedQuery) return true
  const q = normalizeForSearch(normalizedQuery)
  if (!q) return true
  return sectionMatchesQuery(product.sectionTitle, q) || titleMatchesQuery(product.title, q)
}

/**
 * Чем меньше число, тем выше в выдаче:
 * сначала совпадение по разделу, затем по названию продукции.
 */
export function getSearchMatchRank(product: CatalogProduct, normalizedQuery: string): number {
  const q = normalizeForSearch(normalizedQuery)
  const section = normalizeForSearch(product.sectionTitle)
  const title = normalizeForSearch(product.title)

  if (section === q) return 0
  if (section.startsWith(q)) return 1
  if (section.includes(q)) return 2
  if (title.startsWith(q)) return 3
  if (title.includes(q)) return 4
  if (matchesLetterSequence(section, q)) return 5
  if (matchesLetterSequence(title, q)) return 6
  return 100
}

function compareBySortId(a: CatalogProduct, b: CatalogProduct, sortId: CatalogSortId): number {
  switch (sortId) {
    case 'product-desc': {
      const byTitle = b.title.localeCompare(a.title, 'ru', { sensitivity: 'base' })
      return byTitle !== 0 ? byTitle : a.sortOrder - b.sortOrder
    }
    case 'product-asc': {
      const byTitle = a.title.localeCompare(b.title, 'ru', { sensitivity: 'base' })
      return byTitle !== 0 ? byTitle : a.sortOrder - b.sortOrder
    }
    case 'section-asc':
    default: {
      const bySection = a.sectionTitle.localeCompare(b.sectionTitle, 'ru', { sensitivity: 'base' })
      if (bySection !== 0) return bySection
      return a.sortOrder - b.sortOrder
    }
  }
}

export function filterCatalogProducts(options: {
  products?: CatalogProduct[]
  sectionId?: CatalogSectionId | 'all'
  search?: string
  sort?: CatalogSortId
}): CatalogProduct[] {
  const {
    products = CATALOG_PRODUCTS,
    sectionId = DEFAULT_CATALOG_SECTION_ID,
    search = '',
    sort = DEFAULT_CATALOG_SORT,
  } = options

  const q = normalizeSearchQuery(search)

  if (!q) {
    const sid = sectionId === 'all' ? DEFAULT_CATALOG_SECTION_ID : sectionId
    return products
      .filter((p) => p.sectionId === sid)
      .sort((a, b) => a.sortOrder - b.sortOrder)
  }

  const matched = products.filter((p) => productMatchesSearch(p, q))

  return [...matched].sort((a, b) => {
    const rankDiff = getSearchMatchRank(a, q) - getSearchMatchRank(b, q)
    if (rankDiff !== 0) return rankDiff
    return compareBySortId(a, b, sort)
  })
}

export function sectionProductCount(sectionId: CatalogSectionId): number {
  const title = CATALOG_SECTION_BY_ID[sectionId]?.title
  if (!title) return 0
  return CATALOG_ITEMS_BY_SECTION[title]?.length ?? 0
}
