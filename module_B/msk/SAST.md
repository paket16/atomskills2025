# Настройка SAST-проверки на MSK-GITLAB

Для подключения SAST (Static Application Security Testing) к репозиторию в GitLab под пользователем root выполните следующие шаги:


## 1. Установка необходимых компонентов

```bash
# Обновление пакетов
apt update && apt upgrade -y

# Установка Docker (если не установлен)
apt install -y docker.io docker-compose
systemctl enable --now docker

# Установка GitLab Runner
curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh" | bash
apt install -y gitlab-runner

# Регистрация runner в GitLab
gitlab-runner register \
  --non-interactive \
  --url "https://gitlab.example.com/" \
  --registration-token "YOUR_REGISTRATION_TOKEN" \
  --executor "docker" \
  --docker-image "alpine:latest" \
  --description "docker-runner" \
  --tag-list "sast" \
  --run-untagged="true" \
  --locked="false"
```

## 3. Настройка SAST в репозитории

### Вариант 1: Через файл .gitlab-ci.yml

1. Создайте/измените файл `.gitlab-ci.yml` в корне репозитория:

```yaml
include:
  - template: Security/SAST.gitlab-ci.yml

variables:
  SAST_DISABLE_DIND: "true"  # Отключить Docker-in-Docker если не требуется
  SAST_ANALYZER_IMAGES: "registry.gitlab.com/gitlab-org/security-products/analyzers"

stages:
  - test

sast:
  stage: test
  tags:
    - sast
```

### Вариант 2: Через UI GitLab

1. Перейдите в репозиторий в веб-интерфейсе GitLab
2. Настройки → CI/CD → Editor
3. Добавьте шаблон SAST как показано выше
4. Сохраните изменения

## 4. Проверка работы SAST

```bash
# Запустите pipeline вручную или сделайте push в репозиторий
git commit --allow-empty -m "Trigger SAST scan"
git push origin master
```

## 5. Просмотр результатов

1. В веб-интерфейсе GitLab перейдите в:
   - CI/CD → Pipelines (просмотр статуса)
   - Security & Compliance → Vulnerability Report (просмотр результатов)

## 6. Дополнительные настройки (опционально)

Для кастомизации SAST можно добавить в `.gitlab-ci.yml`:

```yaml
variables:
  SAST_EXCLUDED_PATHS: "spec, test, tests"  # Исключить определенные пути
  SAST_BRAKEMAN_LEVEL: "1"                  # Уровень проверки для Brakeman
  SEARCH_MAX_DEPTH: "4"                     # Глубина проверки
```

## 7. Устранение неполадок

Если SAST не запускается:
```bash
# Проверьте статус runner
gitlab-runner list

# Проверьте логи runner
journalctl -u gitlab-runner -f

# Проверьте docker контейнеры
docker ps -a
```

## 8. Безопасность

После настройки рекомендуется:
```bash
# Сменить пароль root
passwd
# Введите новый пароль (лучше сложнее чем P@ssw0rd)
```

Теперь в вашем репозитории будет автоматически выполняться статический анализ безопасности кода при каждом push в репозиторий.