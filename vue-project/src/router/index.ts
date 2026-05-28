import { createRouter, createWebHistory } from 'vue-router'
import { CATALOG_PRODUCT_SLUGS } from '../data/catalogProductDetails'
import { useAuth } from '../composables/useAuth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/catalog/product/:slug',
    name: 'CatalogProduct',
    component: () => import('../views/CatalogProductDetail.vue'),
    beforeEnter: (to) => {
      const slug = String(to.params.slug ?? '')
      if (!CATALOG_PRODUCT_SLUGS.includes(slug)) {
        return { path: '/catalog' }
      }
    }
  },  {
    path: '/catalog',
    name: 'Catalog',
    component: () => import('../views/Catalog.vue')
  },
  {
    path: '/contacts',
    name: 'Contacts',
    component: () => import('../views/Contacts.vue')
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue'),
  },
  {
    path: '/about/clients',
    name: 'AboutClients',
    component: () => import('../views/about/AboutSubpage.vue'),
  },
  {
    path: '/about/partners',
    name: 'AboutPartners',
    component: () => import('../views/about/AboutSubpage.vue'),
  },
  {
    path: '/about/advantages',
    name: 'AboutAdvantages',
    component: () => import('../views/about/AboutSubpage.vue'),
  },
  {
    path: '/vacancies',
    name: 'Vacancies',
    component: () => import('../views/Vacancies.vue')
  },
  {
    path: '/resume',
    name: 'Resume',
    component: () => import('../views/Resume.vue')
  },
  {
    path: '/technologies',
    name: 'Technologies',
    component: () => import('../views/Technologies.vue')
  },
  {
    path: '/graphic-module',
    name: 'GraphicModule',
    component: () => import('../views/GraphicModule.vue'),
  },
  {
    path: '/graphic-module/maket',
    name: 'GraphicModuleMaket',
    component: () => import('../views/GraphicModuleStudio.vue'),
  },
  {
    path: '/quick-quote',
    name: 'QuickQuote',
    component: () => import('../views/QuickQuote.vue'),
  },
  {
    path: '/staff/login',
    name: 'StaffLogin',
    component: () => import('../views/staff/StaffLogin.vue'),
    meta: { guestOnly: true },
  },
  {
    path: '/staff/inbox',
    name: 'StaffInbox',
    component: () => import('../views/staff/StaffInbox.vue'),
    meta: { requiresStaff: true },
  },
  {
    path: '/staff/quotes',
    redirect: { name: 'StaffInbox', query: { type: 'quote' } },
  },
  {
    path: '/staff/quotes/:ref',
    name: 'StaffQuoteDetail',
    component: () => import('../views/staff/StaffQuoteDetail.vue'),
    meta: { requiresStaff: true },
  },
  {
    path: '/staff/callbacks/:ref',
    name: 'StaffCallbackDetail',
    component: () => import('../views/staff/StaffCallbackDetail.vue'),
    meta: { requiresStaff: true },
  },
  {
    path: '/staff/chats/:ref',
    name: 'StaffChatDetail',
    component: () => import('../views/staff/StaffChatDetail.vue'),
    meta: { requiresStaff: true },
  },
  {
    path: '/staff/admin',
    redirect: { path: '/staff/admin/catalog' },
  },
  {
    path: '/staff/admin/catalog',
    name: 'StaffAdminCatalog',
    component: () => import('../views/staff/admin/StaffAdminCatalog.vue'),
    meta: { requiresStaff: true },
  },
  {
    path: '/staff/admin/portfolio',
    name: 'StaffAdminPortfolio',
    component: () => import('../views/staff/admin/StaffAdminPortfolio.vue'),
    meta: { requiresStaff: true },
  },
  {
    path: '/staff/admin/chat',
    name: 'StaffAdminChat',
    component: () => import('../views/staff/admin/StaffAdminChat.vue'),
    meta: { requiresStaff: true },
  },
  {
    path: '/staff/admin/graphic',
    name: 'StaffAdminGraphic',
    component: () => import('../views/staff/admin/StaffAdminGraphic.vue'),
    meta: { requiresStaff: true, requiresAdmin: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to) => {
  const { checked, isStaff, isAdministrator, fetchMe } = useAuth()

  if (to.meta.requiresStaff || to.meta.requiresAdmin) {
    if (!checked.value) await fetchMe()
    if (!isStaff.value) {
      return { name: 'StaffLogin', query: { redirect: to.fullPath } }
    }
  }

  if (to.meta.requiresAdmin) {
    if (!isAdministrator.value) {
      return { path: '/staff/admin/chat' }
    }
  }

  if (to.meta.guestOnly && to.name === 'StaffLogin') {
    if (!checked.value) await fetchMe()
    if (isStaff.value) {
      return { name: 'StaffInbox' }
    }
  }
})

export default router