# Примеры использования InteliFuzz

## Быстрый старт

### Базовое использование
```bash
python intellifuzz.py https://target.com/FUZZ
```

### С выбором провайдера
```bash
python intellifuzz.py --provider ollama https://target.com/FUZZ
```

## Примеры по типам приложений

### Web-приложения

#### PHP-сайты
```bash
# Поиск PHP файлов
python intellifuzz.py https://phpsite.com/FUZZ

# С дополнительными параметрами ffuf
python intellifuzz.py https://phpsite.com/FUZZ -w custom-wordlist.txt -mc 200,301,302 -fs 1024
```

#### ASP.NET приложения
```bash
# Microsoft технологии
python intellifuzz.py https://aspnet-site.com/FUZZ -H "User-Agent: Mozilla/5.0"
```

#### Java приложения
```bash
# Java веб-приложения
python intellifuzz.py https://java-app.com/api/FUZZ
```

### API тестирование

#### REST API
```bash
# API endpoints
python intellifuzz.py https://api.example.com/v1/FUZZ -H "Authorization: Bearer token"

# С фильтрацией по статус-кодам
python intellifuzz.py https://api.example.com/FUZZ -mc 200,404,500
```

#### GraphQL
```bash
# GraphQL endpoints
python intellifuzz.py https://graphql.example.com/FUZZ -H "Content-Type: application/json"
```

### Поиск файлов и директорий

#### Документы
```bash
# Поиск документов в презентационной директории
python intellifuzz.py https://company.com/presentations/FUZZ
```

#### Backup файлы
```bash
# Поиск бэкапов
python intellifuzz.py https://target.com/backups/FUZZ
```

#### Конфигурационные файлы
```bash
# Конфиги
python intellifuzz.py https://target.com/config/FUZZ
```

## Продвинутые примеры

### Использование разных провайдеров

#### Ollama для быстрого тестирования
```bash
# Быстро и бесплатно
python intellifuzz.py --provider ollama https://target.com/FUZZ -t 50
```

#### OpenAI для точности
```bash
# Максимальная точность
python intellifuzz.py --provider openai https://complex-app.com/FUZZ
```

#### OpenRouter для разнообразия моделей
```bash
# Доступ к разным моделям
python intellifuzz.py --provider openrouter https://target.com/FUZZ
```

### Кастомные конфигурации

#### Пентест конфиг
```yaml
# pentest.yaml
providers:
  ollama:
    model: "llama3.2"
    base_url: "http://localhost:11434"

default_provider: "ollama"

ffuf:
  max_extensions: 6

ai:
  temperature: 0
  max_tokens: 1500
```

```bash
python intellifuzz.py --provider ollama https://target.com/FUZZ --max-extensions 6
```

#### Bug Bounty конфиг
```yaml
# bugbounty.yaml
providers:
  openai:
    model: "gpt-4o"
    
default_provider: "openai"

ffuf:
  max_extensions: 8

ai:
  temperature: 0.2
  max_tokens: 2000
```

```bash
python intellifuzz.py --provider openai https://bugbounty-target.com/FUZZ --max-extensions 8
```

## Интеграция с другими инструментами

### С Burp Suite
```bash
# Использование Burp как прокси
python intellifuzz.py https://target.com/FUZZ -x http://127.0.0.1:8080
```

### С Nuclei
```bash
# Сначала InteliFuzz для обнаружения файлов
python intellifuzz.py https://target.com/FUZZ -o found-files.txt

# Затем Nuclei для проверки уязвимостей
nuclei -list found-files.txt -t ~/nuclei-templates/
```

### Скриптинг и автоматизация

#### Bash скрипт
```bash
#!/bin/bash
# auto-fuzz.sh

TARGETS=("https://target1.com" "https://target2.com")
WORDLISTS=("common.txt" "api.txt" "files.txt")

for target in "${TARGETS[@]}"; do
    echo "Fuzzing $target"
    python intellifuzz.py "$target/FUZZ" -o "results_$(basename $target).txt"
done
```

#### Python скрипт
```python
#!/usr/bin/env python3
# mass-fuzz.py

import subprocess
import sys

targets = [
    "https://target1.com",
    "https://target2.com", 
    "https://target3.com"
]

wordlists = ["common.txt", "api.txt", "admin.txt"]

for target in targets:
    for wordlist in wordlists:
        cmd = [
            "python", "intellifuzz.py",
            "-u", f"{target}/FUZZ",
            "-w", wordlist,
            "-o", f"results_{target.replace('https://', '').replace('.', '_')}_{wordlist}.txt"
        ]
        
        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd)
```

## Специальные случаи

### Медленные целевые системы
```bash
# Увеличенные таймауты
python intellifuzz.py \
  --config slow-target.yaml \
  -u https://slow-target.com/FUZZ \
  -w wordlist.txt \
  -p 0.5 \
  -t 10
```

### Высокая нагрузка
```bash
# Максимальная скорость
python intellifuzz.py \
  --provider ollama \
  -u https://fast-target.com/FUZZ \
  -w wordlist.txt \
  -t 100 \
  -p 0.1
```

### Обход WAF
```bash
# Случайные User-Agent'ы и задержки
python intellifuzz.py \
  -u https://protected-site.com/FUZZ \
  -w wordlist.txt \
  -H "User-Agent: FUZZ" \
  -w user-agents.txt \
  -p 2 \
  -t 5
```

## Анализ результатов

### Фильтрация результатов
```bash
# Только успешные ответы
python intellifuzz.py -u https://target.com/FUZZ -w wordlist.txt -mc 200

# Исключение определённых размеров
python intellifuzz.py -u https://target.com/FUZZ -w wordlist.txt -fs 1024,2048

# Фильтрация по словам в ответе
python intellifuzz.py -u https://target.com/FUZZ -w wordlist.txt -fw 50
```

### Сохранение результатов
```bash
# В файл
python intellifuzz.py -u https://target.com/FUZZ -w wordlist.txt -o results.txt

# В JSON формате
python intellifuzz.py -u https://target.com/FUZZ -w wordlist.txt -of json -o results.json
```

## Troubleshooting примеры

### Проверка подключения к Ollama
```bash
# Проверка доступности
curl http://localhost:11434/api/tags

# Если Ollama не отвечает
ollama serve &
sleep 5
python intellifuzz.py --provider ollama -u https://httpbin.org/FUZZ -w test.txt
```

### Тестирование API ключей
```bash
# Тест OpenAI
OPENAI_API_KEY="your-key" python intellifuzz.py --provider openai -u https://httpbin.org/FUZZ -w test.txt

# Тест Anthropic
ANTHROPIC_API_KEY="your-key" python intellifuzz.py --provider anthropic -u https://httpbin.org/FUZZ -w test.txt
```

### Debug режим
```bash
# Подробный вывод
python intellifuzz.py -u https://target.com/FUZZ -w wordlist.txt -v

# С отладочной информацией
python -u intellifuzz.py -u https://target.com/FUZZ -w wordlist.txt 2>&1 | tee debug.log
``` 