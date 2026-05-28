import { ref } from 'vue'
import { apiFetch } from '@/api/http'
import type { CatalogProduct, CatalogSectionId } from '@/data/catalog'

type ApiCatalogResponse = {
  sections: { id: string; title: string; sortOrder: number; homeImageUrl?: string | null }[]
  products: {
    id: string
    title: string
    sectionId: string
    sectionTitle: string
    sortOrder: number
    slug?: string | null
    imageUrl?: string | null
  }[]
}

const loaded = ref(false)
const apiProducts = ref<CatalogProduct[] | null>(null)
const apiSections = ref<
  { id: CatalogSectionId; title: string; sortOrder: number; homeImageUrl?: string }[] | null
>(null)

export function usePublicCatalog() {
  async function loadCatalogFromApi() {
    if (loaded.value) return
    try {
      const data = await apiFetch<ApiCatalogResponse>('/catalog/')
      apiSections.value = data.sections.map((s) => ({
        id: s.id as CatalogSectionId,
        title: s.title,
        sortOrder: s.sortOrder,
        homeImageUrl: s.homeImageUrl ?? undefined,
      }))
      apiProducts.value = data.products.map((p) => ({
        id: p.id,
        title: p.title,
        sectionId: p.sectionId as CatalogSectionId,
        sectionTitle: p.sectionTitle,
        sortOrder: p.sortOrder,
        slug: p.slug ?? undefined,
        imageUrl: p.imageUrl ?? undefined,
      }))
    } catch {
      apiProducts.value = null
      apiSections.value = null
    } finally {
      loaded.value = true
    }
  }

  return { loaded, apiProducts, apiSections, loadCatalogFromApi }
}
