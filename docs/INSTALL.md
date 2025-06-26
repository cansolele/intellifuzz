# Установка InteliFuzz

## Системные требования

- **Python**: 3.6 или выше
- **ffuf**: установлен и доступен в PATH
- **Git**: для клонирования репозитория
- **Интернет**: для работы с облачными AI-провайдерами

## Пошаговая установка

### 1. Клонирование репозитория
```bash
git clone https://github.com/cansolele/intellifuzz
cd intellifuzz
```

### 2. Установка зависимостей

#### Автоматическая установка
```bash
pip install -r requirements.txt
```

#### Ручная установка зависимостей
```bash
pip install requests openai anthropic ollama PyYAML
```

### 3. Проверка ffuf
```bash
ffuf -version
```
Если ffuf не установлен:
```bash
# Ubuntu/Debian
apt install ffuf

# macOS
brew install ffuf

# Из исходников
go install github.com/ffuf/ffuf@latest
```

### 4. Настройка AI-провайдеров

#### Интерактивная настройка (рекомендуется)
```bash
python intellifuzz.py --setup
```

#### Переменные окружения
```bash
export OPENAI_API_KEY="ваш-ключ"
export ANTHROPIC_API_KEY="ваш-ключ"
export OPENROUTER_API_KEY="ваш-ключ"
```

### 5. Проверка установки
```bash
python intellifuzz.py --help
```

## Альтернативные способы установки

### Установка в виртуальное окружение
```bash
python -m venv intellifuzz-env
source intellifuzz-env/bin/activate  # Linux/Mac
# или
intellifuzz-env\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Создание символической ссылки

Для использования из любой директории:
```bash
sudo ln -s $(pwd)/intellifuzz.py /usr/local/bin/intellifuzz
chmod +x /usr/local/bin/intellifuzz
```

Теперь можно использовать:
```bash
intellifuzz -u https://target.com/FUZZ -w wordlist.txt
```

## Проверка установки

Убедитесь что всё работает:
```bash
python intellifuzz.py --provider ollama https://httpbin.org/FUZZ
```

## Структура проекта

После установки вы получите следующую структуру:
```
intellifuzz/
├── intellifuzz.py     # Основной исполняемый файл
├── config.yaml        # Конфигурация (создаётся при первом запуске)
├── requirements.txt   # Зависимости Python
├── src/               # Модули проекта
│   ├── __init__.py
│   ├── config.py      # Управление конфигурацией
│   ├── providers.py   # AI-провайдеры
│   └── utils.py       # Утилиты
└── docs/              # Документация
    ├── INSTALL.md
    ├── CONFIG.md
    └── EXAMPLES.md
``` 