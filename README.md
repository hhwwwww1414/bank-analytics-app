
# Bank Analytics App



> **Статус CI**: этот бейдж показывает результаты выполнения автотестов (pytest) и линтинга (ruff) в GitHub Actions.
![CI](https://github.com/hhwwwww1414/bank-analytics-app/actions/workflows/ci.yml/badge.svg)


**Полное решение для визуализации и анализа банковских данных с реальным и синтетическим источником**

---

## 📋 Описание проекта

Bank Analytics App — это настольное приложение на Python/Tkinter, которое позволяет:

- **Импортировать** реальные данные маркетингового опроса клиентов банка (UCI Bank Marketing #222)
- **Генерировать** синтетические справочники клиентов и счетов с настраиваемыми параметрами
- **Просматривать** и редактировать CRUD-справочники «Клиенты» и «Счета»
- **Формировать 7 типов отчётов**:
  1. Текстовая проекция
  2. Статистический анализ (числовые и категориальные метрики)
  3. Сводная таблица (pivot)
  4. Кластеризованная столбчатая диаграмма
  5. Категоризированная гистограмма
  6. Диаграмма Box-Plot
  7. Диаграмма рассеивания
- **Экспортировать** результаты в Excel (для статистики) и CSV (для таблиц)
- **Настраивать** цветовую тему, шрифты и пути через окно «Настройки»
- **Переключать режим** работы с данными (REAL / SYNTH) без перезапуска

Проект структурирован по модулям, снабжён утилитами загрузки/сохранения, логированием, автотестами и CI.

---

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/hhwwwww1414/bank-analytics-app.git
cd bank-analytics-app
```

### 2. Установка и активация виртуального окружения

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Генерация данных или загрузка реальных

При первом запуске автоматически качаются реальные данные UCI Bank Marketing. Синтетические данные можно генерировать в приложении через диалог выбора источника.

### 5. Запуск приложения

```bash
python -m scripts.main
```

или, при наличии в `dist/BankApp.exe` (сборка PyInstaller):

```bash
./dist/BankApp.exe
```

---

## 🗂 Структура проекта

```
bank-analytics-app/
├── data/                # .pkl-файлы клиентов и счетов (real/synth)
├── graphics/            # Сохранённые изображения отчётов
├── library/             # Общие утилиты (common_funcs.py)
├── notes/               # User_Guide.pdf и Developer_Guide.pdf
├── output/              # Экспортированные CSV/Excel
├── requirements.txt     # Pip-зависимости
├── README.md            # Этот файл
├── scripts/
│   ├── app_state.py     # Переключатель REAL/SYNTH
│   ├── data_ingestion.py# Скачивание и разбиение UCI-данных
│   ├── data_management.py
│   ├── generator_synth.py
│   ├── generate_initial_data.py
│   ├── main.py          # Точка входа (Tkinter GUI)
│   ├── reporting.py     # Функции для отчётов
│   └── gui/             # Окна Tkinter
│       ├── main_window.py
│       ├── clients_window.py
│       ├── accounts_window.py
│       ├── report_*.py
│       └── settings_window.py
└── tests/               # Pytest-автотесты
    ├── test_data_management.py
    └── test_reporting.py
```

---

## ⚙️ Конфигурация

Файл `scripts/app_config.ini` содержит разделы:

```ini
[DATA]
data_mode = real        ; real или synth

[PATHS]
data_dir     = data
graphics_dir = graphics
output_dir   = output

[GUI]
font_family = Cambria
font_size   = 14
base_fg     = #000000
base_bg     = #D7E1C5
```

Изменение `data_mode` отражается сразу, без перезапуска.

---

## ✅ Тестирование и линтинг

- **Pytest**:
  ```bash
  pytest -q
  ```
- **Ruff (lint)**:
  ```bash
  python -m ruff check . --fix
  ```
- CI запускает и `pytest`, и `ruff` на GitHub Actions.

---

## 📦 Сборка в одиночный exe (опционально)

```bash
pip install pyinstaller
pyinstaller scripts/main.py --onefile --noconsole -n BankApp
```

Получится `dist/BankApp.exe`, которое можно запускать без установки Python.

---

## 🔒 Архивирование проекта

```bash
# Windows PowerShell:
Compress-Archive -Path work -DestinationPath 191_01_003.zip
```

или под UNIX:

```bash
zip -r -P YOUR_PASSWORD 191_01_003.zip work
```

