<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const vacancies = ref([
  {
    id: 1,
    title: 'Менеджер по продажам',
    department: 'Отдел продаж',
    salary: 'от 60 000 ₽',
    type: 'Полная занятость',
    description: 'Поиск и привлечение новых клиентов, ведение переговоров, заключение договоров',
    requirements: [
      'Опыт работы в продажах от 1 года',
      'Умение вести переговоры',
      'Уверенный пользователь ПК',
      'Грамотная устная и письменная речь'
    ],
    conditions: [
      'Официальное трудоустройство',
      'Обучение за счёт компании',
      'Процент от продаж',
      'Дружный коллектив'
    ]
  },
  {
    id: 2,
    title: 'Дизайнер полиграфии',
    department: 'Производственный отдел',
    salary: 'от 70 000 ₽',
    type: 'Полная занятость',
    description: 'Разработка макетов полиграфической продукции, работа с клиентами по техническим заданиям',
    requirements: [
      'Знание Adobe Photoshop, Illustrator, InDesign',
      'Опыт работы в полиграфии от 2 лет',
      'Понимание допечатной подготовки',
      'Портфолио работ'
    ],
    conditions: [
      'Современное рабочее место',
      'Гибкий график',
      'Профессиональный рост',
      'Бонусы за выполнение плана'
    ]
  },
  {
    id: 3,
    title: 'Оператор печатной машины',
    department: 'Производство',
    salary: 'от 80 000 ₽',
    type: 'Полная занятость',
    description: 'Настройка и обслуживание печатного оборудования, контроль качества печати',
    requirements: [
      'Опыт работы на цифровых или офсетных машинах',
      'Техническое образование',
      'Внимательность и аккуратность',
      'Готовность к сменной работе'
    ],
    conditions: [
      'Стабильная заработная плата',
      'Предоставление спецодежды',
      'Питание за счёт компании',
      'Карьерный рост'
    ]
  }
])

const benefits = [
  {
    icon: 'salary',
    title: 'Конкурентная зарплата',
    description: 'Выплачивается 2 раза в месяц без задержек'
  },
  {
    icon: 'growth',
    title: 'Профессиональный рост',
    description: 'Обучение и развитие за счёт компании'
  },
  {
    icon: 'team',
    title: 'Дружный коллектив',
    description: 'Поддержка и взаимопомощь в команде'
  },
  {
    icon: 'schedule',
    title: 'Гибкий график',
    description: 'Возможность совмещать с учёбой'
  }
]

const selectedVacancy = ref<number | null>(null)

const toggleVacancy = (id: number) => {
  selectedVacancy.value = selectedVacancy.value === id ? null : id
}

const applyForVacancy = (title: string) => {
  router.push('/resume')
}
</script>

<template>
  <div class="app">
    <main class="main-content">
      <div class="container">
        <!-- Заголовок страницы -->
        <h1 class="page-title">Вакансии</h1>
        <p class="page-subtitle">Присоединяйтесь к нашей команде профессионалов</p>

        <!-- Изображение -->
        <div class="vacancies-image-wrapper">
          <img src="/images/qqq1.png" alt="Наша команда" class="vacancies-image" />
        </div>

        <!-- Преимущества работы у нас -->
        <div class="benefits-section">
          <h2 class="section-title">Почему стоит работать у нас</h2>
          <div class="benefits-grid">
            <div v-for="benefit in benefits" :key="benefit.title" class="benefit-card">
              <div class="benefit-icon">
                <svg v-if="benefit.icon === 'salary'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="2" y="6" width="20" height="12" rx="2"/>
                  <circle cx="12" cy="12" r="2"/>
                  <path d="M6 12h.01M18 12h.01"/>
                </svg>
                <svg v-else-if="benefit.icon === 'growth'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>
                  <polyline points="17 6 23 6 23 12"/>
                </svg>
                <svg v-else-if="benefit.icon === 'team'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                  <circle cx="9" cy="7" r="4"/>
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                </svg>
                <svg v-else-if="benefit.icon === 'schedule'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                  <line x1="16" y1="2" x2="16" y2="6"/>
                  <line x1="8" y1="2" x2="8" y2="6"/>
                  <line x1="3" y1="10" x2="21" y2="10"/>
                </svg>
              </div>
              <h3 class="benefit-title">{{ benefit.title }}</h3>
              <p class="benefit-description">{{ benefit.description }}</p>
            </div>
          </div>
        </div>

        <!-- Список вакансий -->
        <div class="vacancies-section">
          <h2 class="section-title">Открытые вакансии</h2>
          <div class="vacancies-list">
            <div 
              v-for="vacancy in vacancies" 
              :key="vacancy.id"
              class="vacancy-card"
              :class="{ active: selectedVacancy === vacancy.id }"
            >
              <div class="vacancy-header" @click="toggleVacancy(vacancy.id)">
                <div class="vacancy-main">
                  <h3 class="vacancy-title">{{ vacancy.title }}</h3>
                  <div class="vacancy-meta">
                    <span class="vacancy-department">{{ vacancy.department }}</span>
                    <span class="vacancy-type">{{ vacancy.type }}</span>
                  </div>
                </div>
                <div class="vacancy-salary">
                  {{ vacancy.salary }}
                </div>
                <div class="vacancy-toggle">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline :points="selectedVacancy === vacancy.id ? '6 9 12 15 18 9' : '6 9 12 15 18 9'" 
                              :class="{ rotated: selectedVacancy === vacancy.id }"/>
                  </svg>
                </div>
              </div>

              <div class="vacancy-content" v-show="selectedVacancy === vacancy.id">
                <p class="vacancy-description">{{ vacancy.description }}</p>
                
                <div class="vacancy-details">
                  <div class="detail-column">
                    <h4 class="detail-title">Требования:</h4>
                    <ul class="detail-list">
                      <li v-for="(req, index) in vacancy.requirements" :key="index">{{ req }}</li>
                    </ul>
                  </div>
                  
                  <div class="detail-column">
                    <h4 class="detail-title">Условия:</h4>
                    <ul class="detail-list">
                      <li v-for="(cond, index) in vacancy.conditions" :key="index">{{ cond }}</li>
                    </ul>
                  </div>
                </div>

                <router-link to="/resume" class="apply-btn">
                  Откликнуться на вакансию
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="22" y1="2" x2="11" y2="13"/>
                    <polygon points="22 2 15 22 11 13 2 9 22 2"/>
                  </svg>
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- Призыв к действию -->
        <div class="cta-section">
          <div class="cta-content">
            <h2 class="cta-title">Не нашли подходящую вакансию?</h2>
            <p class="cta-text">Отправьте нам своё резюме, и мы рассмотрим вашу кандидатуру для будущих позиций</p>
            <router-link to="/resume" class="cta-button">
              Отправить резюме
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                <polyline points="22,6 12,13 2,6"/>
              </svg>
            </router-link>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
/* (Все стили из предыдущего сообщения остаются без изменений) */
.page-title {
  font-size: 42px;
  color: #008000;
  text-align: center;
  margin-bottom: 10px;
  font-family: var(--font-heading);
}

.page-subtitle {
  font-size: 18px;
  color: #666;
  text-align: center;
  margin-bottom: 40px;
}

.vacancies-image-wrapper {
  margin-bottom: 50px;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.vacancies-image {
  width: 100%;
  height: 400px;
  object-fit: cover;
  display: block;
}

.benefits-section {
  margin-bottom: 60px;
}

.section-title {
  font-size: 32px;
  color: #333;
  text-align: center;
  margin-bottom: 40px;
  font-family: var(--font-heading);
}

.benefits-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 25px;
}

.benefit-card {
  background: #f5f5f5;
  border-radius: 15px;
  padding: 30px 20px;
  text-align: center;
  transition: all 0.3s;
  border-bottom: 3px solid #ff7722;
}

.benefit-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.benefit-icon {
  width: 60px;
  height: 60px;
  background: #ff7722;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.benefit-icon svg {
  width: 30px;
  height: 30px;
  color: white;
}

.benefit-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
}

.benefit-description {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
}

.vacancies-section {
  margin-bottom: 60px;
}

.vacancies-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.vacancy-card {
  background: white;
  border-radius: 15px;
  border: 2px solid #e8e8e8;
  overflow: hidden;
  transition: all 0.3s;
}

.vacancy-card:hover {
  border-color: #ff7722;
  box-shadow: 0 5px 20px rgba(255, 119, 34, 0.15);
}

.vacancy-card.active {
  border-color: #ff7722;
  box-shadow: 0 5px 20px rgba(255, 119, 34, 0.2);
}

.vacancy-header {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 25px 30px;
  cursor: pointer;
  transition: background 0.3s;
}

.vacancy-header:hover {
  background: #f9f9f9;
}

.vacancy-main {
  flex: 1;
}

.vacancy-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
  font-family: var(--font-heading);
}

.vacancy-meta {
  display: flex;
  gap: 15px;
}

.vacancy-department,
.vacancy-type {
  font-size: 13px;
  color: #666;
  background: #e8e8e8;
  padding: 5px 12px;
  border-radius: 15px;
}

.vacancy-salary {
  font-size: 18px;
  font-weight: 600;
  color: #008000;
  white-space: nowrap;
}

.vacancy-toggle {
  width: 40px;
  height: 40px;
  background: #f5f5f5;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.vacancy-toggle svg {
  width: 20px;
  height: 20px;
  color: #666;
  transition: transform 0.3s;
}

.vacancy-toggle svg.rotated {
  transform: rotate(180deg);
}

.vacancy-content {
  padding: 0 30px 30px;
}

.vacancy-description {
  font-size: 15px;
  color: #666;
  line-height: 1.7;
  margin-bottom: 25px;
  padding-bottom: 25px;
  border-bottom: 1px solid #e8e8e8;
}

.vacancy-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-bottom: 25px;
}

.detail-column {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.detail-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.detail-list li {
  font-size: 14px;
  color: #666;
  padding-left: 20px;
  position: relative;
  line-height: 1.6;
}

.detail-list li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #008000;
  font-weight: bold;
}

.apply-btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: #ff7722;
  color: white;
  padding: 14px 30px;
  border-radius: 25px;
  border: none;
  cursor: pointer;
  font-size: 15px;
  font-weight: 500;
  transition: all 0.3s;
  text-decoration: none;
}

.apply-btn:hover {
  background: #e66611;
  transform: translateX(5px);
}

.apply-btn svg {
  width: 18px;
  height: 18px;
}

.cta-section {
  background: linear-gradient(135deg, #ff7722 0%, #ff9955 100%);
  border-radius: 20px;
  padding: 50px;
  text-align: center;
  margin-bottom: 40px;
}

.cta-title {
  font-size: 28px;
  color: white;
  margin-bottom: 15px;
  font-family: var(--font-heading);
}

.cta-text {
  font-size: 16px;
  color: white;
  opacity: 0.95;
  margin-bottom: 30px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.cta-button {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: white;
  color: #ff7722;
  padding: 15px 35px;
  border-radius: 25px;
  text-decoration: none;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s;
}

.cta-button:hover {
  background: #f5f5f5;
  transform: translateY(-3px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
}

.cta-button svg {
  width: 20px;
  height: 20px;
}

@media (max-width: 1024px) {
  .benefits-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .page-title {
    font-size: 32px;
  }
  
  .vacancies-image {
    height: 250px;
  }
  
  .benefits-grid {
    grid-template-columns: 1fr;
  }
  
  .vacancy-header {
    flex-wrap: wrap;
    gap: 15px;
  }
  
  .vacancy-salary {
    order: 3;
    width: 100%;
    text-align: center;
    padding-top: 15px;
    border-top: 1px solid #e8e8e8;
  }
  
  .vacancy-toggle {
    order: 2;
  }
  
  .vacancy-main {
    order: 1;
    flex: 1;
  }
  
  .vacancy-details {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .cta-section {
    padding: 30px 20px;
  }
  
  .cta-title {
    font-size: 24px;
  }
}

@media (max-width: 640px) {
  .vacancy-title {
    font-size: 18px;
  }
  
  .vacancy-salary {
    font-size: 16px;
  }
  
  .benefit-card {
    padding: 25px 20px;
  }
}
</style>