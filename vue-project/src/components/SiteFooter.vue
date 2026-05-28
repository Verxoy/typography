<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="container">
        <div class="footer-grid">
          <div class="footer-brand">
            <router-link to="/">
              <img src="/logo.png" alt="Типография Андрея Христюбова" class="footer-logo" />
            </router-link>
            <div class="footer-info">
              <p>© 2022 ООО Типография Андрея Христюбова</p>
              <p>630083, г. Новосибирск</p>
              <p>ул. Большевистская, 131, корпус 6</p>
              <p>Пн–Пт: 9:00–18:00</p>
            </div>
          </div>

          <div class="footer-block">
            <h3 class="footer-block-title">Разделы сайта</h3>
            <nav class="footer-menu" aria-label="Навигация в подвале">
              <div class="footer-menu-col">
                <router-link to="/" class="footer-link">Главная</router-link>
                <router-link to="/catalog" class="footer-link">Каталог</router-link>
                <router-link to="/technologies" class="footer-link">Технологии</router-link>
              </div>
              <div class="footer-menu-col">
                <router-link to="/contacts" class="footer-link">Контакты</router-link>
                <router-link to="/about" class="footer-link">О нас</router-link>
                <router-link to="/vacancies" class="footer-link">Вакансии</router-link>
                <router-link to="/graphic-module" class="footer-link">Графический модуль</router-link>
              </div>
            </nav>
          </div>

          <div class="footer-block">
            <h3 class="footer-block-title">Контакты</h3>
            <div class="footer-contacts">
              <a href="tel:+73832091247" class="footer-contact">
                <svg class="footer-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
                  <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
                </svg>
                <span>+7 (383) 209-12-47</span>
              </a>
              <a href="tel:+79039345111" class="footer-contact">
                <svg class="footer-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
                  <rect x="5" y="2" width="14" height="20" rx="2" ry="2"/>
                  <line x1="12" y1="18" x2="12.01" y2="18"/>
                </svg>
                <span>+7 (903) 934-51-11</span>
              </a>
              <a href="mailto:info@tahh.ru" class="footer-contact">
                <svg class="footer-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                  <polyline points="22,6 12,13 2,6"/>
                </svg>
                <span>info@tahh.ru</span>
              </a>
            </div>
          </div>

          <div class="footer-block footer-block--social">
            <h3 class="footer-block-title">Мы в соцсетях</h3>
            <div class="footer-social">
              <a href="https://vk.com" target="_blank" rel="noopener noreferrer" class="social-icon social-icon--vk" aria-label="ВКонтакте">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                  <rect width="24" height="24" rx="5.5" fill="currentColor" />
                  <path
                    fill="#fff"
                    d="M6.79 7.3H4.05c.13 6.24 3.25 9.99 8.72 9.99h.31v-3.57c2.01.2 3.53 1.67 4.14 3.57h2.84c-.78-2.84-2.83-4.41-4.11-5.01 1.28-.74 3.08-2.54 3.51-4.98h-2.58c-.56 1.98-2.22 3.78-3.8 3.95V7.3H10.5v6.92c-1.6-.4-3.62-2.34-3.71-6.92Z"
                  />
                </svg>
              </a>
              <a href="https://t.me" target="_blank" rel="noopener noreferrer" class="social-icon" aria-label="Telegram">
                <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                  <path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/>
                </svg>
              </a>
              <a href="https://youtube.com" target="_blank" rel="noopener noreferrer" class="social-icon" aria-label="YouTube">
                <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                  <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                </svg>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="footer-bottom">
      <div class="container">
        <div class="footer-line" />
      </div>
    </div>
  </footer>
</template>
