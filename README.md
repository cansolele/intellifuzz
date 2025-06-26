# InteliFuzz

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

InteliFuzz - умная AI-powered обёртка для веб-фаззера ffuf. Автоматически анализирует цель и предлагает оптимальные расширения файлов для фаззинга, используя силу искусственного интеллекта от ведущих провайдеров.

## 🚀 Отличия от оригинала

Этот проект является форком [jthack/ffufai](https://github.com/jthack/ffufai) с существенными улучшениями:

- **🎯 Поддержка 4 AI-провайдеров** вместо 2 (добавлены Ollama и OpenRouter)
- **⚙️ YAML-конфигурация** с интерактивной настройкой
- **🏠 Локальные модели** через Ollama (бесплатно)
- **🌐 200+ моделей** через OpenRouter
- **🔧 Гибкие настройки** (temperature, tokens, timeout)
- **📝 Интерактивный мастер** настройки (`--setup`)
- **🔄 Переключение провайдеров** на лету
- **📊 Улучшенная обработка ошибок** и логирование
- **🧩 Модульная архитектура** для легкого расширения

## Особенности

- **Множественные AI-провайдеры**: OpenAI, Anthropic Claude, Ollama (локально), OpenRouter
- **Управление конфигурацией**: YAML-конфиг с интерактивной настройкой
- **Интеграция с ffuf**: Пропускает все параметры ffuf без изменений
- **Умные предложения**: Контекстно-зависимые рекомендации расширений файлов
- **Гибкая аутентификация**: API-ключи, переменные окружения, локальные модели

## Требования

- Python 3.6+
- ffuf (установлен и доступен в PATH)
- Хотя бы один настроенный AI-провайдер:
  - API-ключ OpenAI
  - API-ключ Anthropic
  - Ollama, запущенная локально
  - API-ключ OpenRouter

## Быстрый старт

```bash
# 1. Клонируйте и установите
git clone https://github.com/cansolele/intellifuzz
cd intellifuzz
pip install -r requirements.txt

# 2. Настройте провайдеры
python intellifuzz.py --setup

# 3. Начните фаззинг
python intellifuzz.py https://target.com/FUZZ
```

📖 **Документация:**
- [🔧 Установка](docs/INSTALL.md) - детальная инструкция по установке
- [⚙️ Конфигурация](docs/CONFIG.md) - настройка провайдеров и параметров  
- [💡 Примеры](docs/EXAMPLES.md) - практические примеры использования

## Использование

```bash
# Базовое использование
python intellifuzz.py https://target.com/FUZZ

# Выбор AI-провайдера
python intellifuzz.py --provider ollama https://target.com/FUZZ

# Ограничение количества расширений
python intellifuzz.py --max-extensions 3 https://target.com/FUZZ

# Передача параметров ffuf
python intellifuzz.py https://target.com/FUZZ -w custom-wordlist.txt -H "Authorization: Bearer token"
```

## Поддерживаемые провайдеры

- **OpenAI** - API-ключ, платно
- **Anthropic Claude** - API-ключ, платно  
- **Ollama** - локально, бесплатно
- **OpenRouter** - API-ключ, доступ к 200+ моделям

## Параметры

**Специфичные для InteliFuzz:**
- `--setup`: Запуск интерактивной конфигурации
- `--provider`: Выбор AI-провайдера (openai|anthropic|ollama|openrouter)
- `--max-extensions`: Максимальное количество предлагаемых расширений

**Стандартные параметры ffuf:**
Все остальные параметры передаются напрямую в ffuf (-w, -H, -mc, -fc, -t и др.)

## Примеры

### Примеры применения

**🏠 Локальный AI (Ollama):**
```bash
ollama pull llama3.2  # установка модели
python intellifuzz.py --provider ollama https://target.com/FUZZ
```

**🌐 Множество моделей (OpenRouter):**
```bash
python intellifuzz.py --provider openrouter https://api.target.com/FUZZ
```

**🔧 Интеграция с ffuf:**
```bash
python intellifuzz.py https://target.com/FUZZ -w custom-wordlist.txt -H "Authorization: Bearer token" -mc 200,301,302
```

## Заметки

- Ключевое слово FUZZ должно быть в конце пути URL для лучших результатов
- Переменные окружения (OPENAI_API_KEY и др.) переопределяют конфигурационный файл
- Ollama требует локальной установки и запущенного сервиса
- OpenRouter предоставляет доступ к 200+ моделям через один API


## Благодарности

Форк [jthack/ffufai](https://github.com/jthack/ffufai). Улучшено с поддержкой множественных провайдеров и управлением конфигурацией.
