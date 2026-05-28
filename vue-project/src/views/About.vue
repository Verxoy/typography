<script setup lang="ts">
import AboutSubnav from '@/components/about/AboutSubnav.vue'
import { ABOUT_COMPANY_PARAGRAPHS } from '@/data/about'
</script>

<template>
  <div class="app about-company-page">
    <main class="main-content about-company-page__main">
      <div class="container">
        <h1 class="page-title about-company-page__title">О нас</h1>
        <p class="page-subtitle about-company-page__subtitle">
          Типография Андрея Христюбова — полиграфия с 2000 года
        </p>

        <AboutSubnav />

        <section class="about-hero" aria-labelledby="about-company-heading">
          <p class="about-kicker">О компании</p>

          <figure class="about-hero__media">
            <img
              src="/images/about-founder.png"
              alt="Андрей Христюбов — основатель типографии"
              class="about-hero__image"
              width="640"
              height="400"
            />
          </figure>

          <h2 id="about-company-heading" class="about-section-title">Наша история и ценности</h2>

          <p
            v-for="(paragraph, index) in ABOUT_COMPANY_PARAGRAPHS"
            :key="index"
            class="about-hero__p"
          >
            {{ paragraph }}
          </p>
        </section>

        <div class="about-cta">
          <p class="about-cta__text">Нужна консультация или расчёт тиража?</p>
          <div class="about-cta__actions">
            <router-link to="/contacts" class="submit-button">Связаться с нами</router-link>
            <router-link to="/quick-quote" class="page-back-link">Быстрый расчёт</router-link>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.about-company-page__main {
  padding-top: 28px;
  padding-bottom: 32px;
}

.about-company-page__title {
  margin-bottom: 6px;
}

.about-company-page__subtitle {
  margin-bottom: 20px;
}

.about-hero {
  margin-bottom: 28px;
}

.about-hero::after {
  content: '';
  display: table;
  clear: both;
}

.about-hero__media {
  float: left;
  width: min(36%, 340px);
  margin: 0 24px 12px 0;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.08);
  background: #fafafa;
  line-height: 0;
}

.about-hero__image {
  display: block;
  width: 100%;
  height: auto;
}

.about-kicker {
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: #ff7722;
  margin: 0 0 10px;
}

.about-section-title {
  font-size: 26px;
  color: #333;
  margin: 0 0 14px;
  font-family: var(--font-heading);
  line-height: 1.25;
}

.about-hero__p {
  font-size: 15px;
  line-height: 1.7;
  color: #555;
  margin: 0 0 12px;
  text-align: justify;
}

.about-cta {
  background: linear-gradient(135deg, #fff8f2 0%, #f5f5f5 100%);
  border: 1px solid rgba(255, 119, 34, 0.2);
  border-radius: 16px;
  padding: 24px 28px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 0;
  clear: both;
}

.about-cta__text {
  font-size: 17px;
  font-weight: 500;
  color: #333;
  margin: 0;
}

.about-cta__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}

.about-cta .page-back-link {
  margin-bottom: 0;
}

@media (max-width: 900px) {
  .about-hero__media {
    float: none;
    width: 100%;
    max-width: 400px;
    margin: 0 auto 16px;
  }

  .about-section-title {
    font-size: 22px;
  }

  .about-hero__p {
    text-align: left;
  }
}

@media (max-width: 600px) {
  .about-cta {
    flex-direction: column;
    align-items: stretch;
    padding: 20px 18px;
  }

  .about-cta__actions {
    flex-direction: column;
  }

  .about-cta .submit-button,
  .about-cta .page-back-link {
    width: 100%;
    justify-content: center;
    text-align: center;
  }
}
</style>
