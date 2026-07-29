# 🔥 Ponyta Tools

> Полный комплект Ansible-ролей и плейбуков для быстрой настройки сервисов

---

## 📦 Что внутри?

### 🛠️ **Роли (Roles)**

| Роль | Назначение | Поддерживаемые ОС |
|------|------------|-------------------|
| 🐳 **`docker`** | Автоматическая установка и настройка Docker CE | Debian 12, Ubuntu 22.04/24.04 |
| 🔥 **`ponyta`** | Развертывание и конфигурация сервиса Ponyta | Debian, Ubuntu |
| 🔥 **`oricorio`** | Развертывание и конфигурация сервиса Oricorio | Debian, Ubuntu |
| 🔥 **`nginx`** | Развертывание/конфигурацию Nginx в Docker | - |

### 📋 **Плейбуки (Playbooks)**

| Плейбук | Описание | Теги |
|---------|----------|------|
| **`ponyta_setup.yaml`** | ⚡ **Основной плейбук**<br>Полный цикл установки: Docker → Ponyta | `always, create_dirs, create_user, debug, docker, force_update_git_repo, git, htpasswd, ponyta, docker_restart_services`|
|**`nginx.yaml`**| Плейбук для деплоя nginx| `always, debug, docker, nginx_dirs, nginx_docker_down, nginx_docker_generate, nginx_docker_restart, nginx_docker_up, nginx_generate` |

---

## 🚀 Быстрый старт

Для работы необходимы следующие пакеты:

- ansible версии 10.0.1 и выше
- ansible-core версии 2.17.14 и выше

Для установки их в отдельный venv выполните команду

```bash
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

Для проверки наличия пакетов выполните команду

```bash
pip list
```

Вывод должен быть подобный

```bash
Package      Version
------------ -------
ansible      10.0.1
ansible-core 2.17.14
cffi         2.0.0
cryptography 46.0.3
Jinja2       3.1.6
MarkupSafe   3.0.3
packaging    25.0
pip          24.0
pycparser    2.23
PyYAML       6.0.3
resolvelib   1.0.1
```

### Клонирование репозитория

```bash
git clone https://github.com/operator2024/ponyta-tools.git
cd ponyta-tools
```

### Запуск ansible

```bash
ansible-playbook -i <path_to_your_inventory> playbooks/<any_playybok_from_dir>
```
