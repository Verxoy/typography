# Graphics Module (оригинальный код)

Источник: [Nagibator2999/Graphics_Module](https://github.com/Nagibator2999/Graphics_Module)

## Структура

| Путь | Назначение |
|------|------------|
| `color-converter-backend/app.py` | Flask API (RGB→CMYK, ICC) — **без изменений** |
| `color-converter-backend/profiles/` | ICC-профили `coated.icc`, `uncoated.icc` |
| `vue-project/public/graphics-module/` | Фронтенд (`index.html`, `style.css`) — **без изменений** |

Сайт открывает модуль в iframe: `/graphic-module` → `/graphics-module/index.html`.

## Запуск (2 терминала)

### 1. Flask-модуль (порт 5000)

```powershell
.\scripts\run-graphics-module.ps1
```

### 2. Сайт

```powershell
# Терминал A — Django
cd backend
.\venv\Scripts\python.exe manage.py runserver

# Терминал B — Vue
cd vue-project
npm run dev
```

Страница: `http://localhost:5173/graphic-module`

## Проверка

- `http://127.0.0.1:5000/health` — JSON со статусом и ICC
- В конвертере при выборе цвета статус «ICC активен»
