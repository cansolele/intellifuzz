# Конфигурация InteliFuzz

## Структура конфигурационного файла

InteliFuzz использует YAML-файл для хранения настроек. По умолчанию это `config.yaml`.

```yaml
providers:
  openai:
    api_key: ""
    model: "gpt-4o"
    base_url: "https://api.openai.com/v1"
    
  anthropic:
    api_key: ""
    model: "claude-3-5-sonnet-20241022"
    
  ollama:
    base_url: "http://localhost:11434"
    model: "llama3.2"
    
  openrouter:
    api_key: ""
    model: "openai/gpt-4o"
    base_url: "https://openrouter.ai/api/v1"
    site_url: ""
    site_name: ""

default_provider: "openai"

ffuf:
  path: "ffuf"
  max_extensions: 4
  
ai:
  temperature: 0
  max_tokens: 1000
  timeout: 30
```

## Настройка провайдеров

### OpenAI
```yaml
openai:
  api_key: "sk-..."              # Ваш API ключ
  model: "gpt-4o"                # Модель для использования
  base_url: "https://api.openai.com/v1"  # Базовый URL API
```

Поддерживает актуальные модели GPT-4 и GPT-3.5.

### Anthropic Claude
```yaml
anthropic:
  api_key: "sk-ant-..."          # Ваш API ключ
  model: "claude-3-5-sonnet-20241022"  # Модель для использования
```

Поддерживает модели Claude 3.5 (Sonnet, Haiku) и Claude 3 Opus.

### Ollama (локально)
```yaml
ollama:
  base_url: "http://localhost:11434"  # URL вашего Ollama сервера
  model: "llama3.2"                   # Локальная модель
```

Поддерживает любые локально установленные модели Ollama.

**Установка моделей:**
```bash
ollama pull llama3.2    # или любую другую модель
ollama list             # просмотр установленных моделей
```

### OpenRouter
```yaml
openrouter:
  api_key: "sk-or-..."           # Ваш API ключ
  model: "openai/gpt-4o"         # Модель в формате provider/model
  base_url: "https://openrouter.ai/api/v1"
  site_url: "https://ваш-сайт.com"    # Опционально для рейтинга
  site_name: "Название вашего сайта"  # Опционально для рейтинга
```

Предоставляет доступ к 200+ моделям от разных провайдеров в едином API.

## Настройки AI

```yaml
ai:
  temperature: 0        # Креативность (0-1, 0 = детерминистично)
  max_tokens: 1000      # Максимальное количество токенов в ответе
  timeout: 30           # Таймаут запроса в секундах
```

### Объяснение параметров:

- **temperature**: Контролирует случайность ответов
  - `0` - детерминистичные, повторяемые ответы
  - `0.3` - слегка креативные
  - `0.7` - баланс креативности и логики
  - `1.0` - максимальная креативность

- **max_tokens**: Ограничение длины ответа
  - `500` - короткие ответы
  - `1000` - стандартные ответы (рекомендуется)
  - `2000` - длинные ответы

- **timeout**: Время ожидания ответа
  - `15` - быстрый таймаут
  - `30` - стандартный (рекомендуется)
  - `60` - длительный для медленных провайдеров

## Настройки ffuf

```yaml
ffuf:
  path: "ffuf"         # Путь к исполняемому файлу ffuf
  max_extensions: 4    # Максимальное количество предлагаемых расширений
```

## Интерактивная настройка

Запустите мастер настройки:
```bash
python intellifuzz.py --setup
```

Мастер поможет:
1. Выбрать основной провайдер
2. Настроить API-ключи
3. Выбрать модели
4. Настроить параметры ffuf
5. Сохранить конфигурацию

## Переменные окружения

Переменные окружения имеют приоритет над конфигурационным файлом:

```bash
export OPENAI_API_KEY="ваш-ключ"
export ANTHROPIC_API_KEY="ваш-ключ"
export OPENROUTER_API_KEY="ваш-ключ"
export OLLAMA_BASE_URL="http://localhost:11434"
```

## Множественные конфигурации

Создавайте разные конфиги для разных задач:

```bash
# Конфиг для пентеста
python intellifuzz.py --config pentest.yaml

# Конфиг для Bug Bounty
python intellifuzz.py --config bugbounty.yaml

# Конфиг для разработки
python intellifuzz.py --config dev.yaml
```

## Приоритет настроек

1. Аргументы командной строки (высший)
2. Переменные окружения
3. Конфигурационный файл
4. Значения по умолчанию (низший)

Пример:
```bash
# Переопределяет провайдера из конфига
python intellifuzz.py --provider ollama --config my-config.yaml
``` 