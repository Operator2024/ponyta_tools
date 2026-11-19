# Docker

  Ansible-роль для автоматической установки и настройки Docker CE, включая поддержку rootless-режима, создание пользователя/групп и управление Docker-сетями.

## Возможности

* Установка Docker CE из официального репозитория (apt/yum).
* Фиксация версий пакетов через APT pinning.
* Создание системного пользователя и групп для работы с Docker.
* Поддержка rootless-режима (linger, `dockerd-rootless-setuptool.sh`).
* Создание Docker-сетей с заданной подсетью и шлюзом.

---

## ⚠️ Breaking changes

Начиная с этой версии переменная **`docker_users` удалена** и заменена на `docker_user` / `docker_group`.

| Было | Стало |
|------|-------|
| `docker_users: ["user1", "user2"]` | `docker_user: docker` + `docker_group: ["docker", "sudo"]` |

Существующие инвентари, в которых задана `docker_users`, **молча перестанут работать** — переопределите переменные согласно таблице ниже.

---

## Переменные роли

| Переменная | Описание | Значение по умолчанию |
|:-----------|:---------|:----------------------|
| **`docker_ensure`** | Состояние пакетов Docker: `latest` или `absent` (удаление) | `latest` |
| **`docker_user`** | Имя системного пользователя для сервисов Docker. Пустая строка — не создавать пользователя | `docker` |
| **`docker_group`** | Список групп, в которые добавляется пользователь. На RHEL-семействе используйте `wheel` вместо `sudo` | `["docker", "sudo"]` |
| **`docker_rootless`** | Включить rootless-режим Docker | `false` |
| **`use_apt_pin_version`** | Использовать APT pinning для фиксации версий пакетов | `true` |
| **`docker_networks`** | Список Docker-сетей для создания (см. ниже) | `[]` |
| **`docker_packages_extra`** | Дополнительные пакеты, добавляемые к основному списку (по релизу ОС) | — |

## Rootless-режим

При `docker_rootless: true` роль:

1. Останавливает и отключает системные службы `docker.service` и `docker.socket`, удаляет `/var/run/docker.sock`.
2. Переименовывает пользователя: к `docker_user` добавляется суффикс `_rootless` (например, `docker` → `docker_rootless`).
3. Включает linger для пользователя (`loginctl enable-linger`).
4. Устанавливает rootless Docker от имени пользователя (`dockerd-rootless-setuptool.sh install`).

> **Примечание:** для rootless-режима в список зависимостей автоматически добавляется пакет `uidmap`.

## Создание Docker-сетей

Роль может создавать сети с заданной подсетью и шлюзом (используется `community.docker.docker_network`):

```yaml
docker_networks:
  - name: local-network
    driver: bridge
    state: present
    ipam_config:
      subnet: 172.16.248.248/30
      gateway: 172.16.248.249
```

При ошибке создания сети плейбук упадёт с сообщением, содержащим имя сети и причину.

## APT pinning

Версии пакетов задаются в `vars/<ОС>.yml` по релизам (например, `jammy`, `noble` для Ubuntu).
При `use_apt_pin_version: true` для каждого пакета создаётся файл в `/etc/apt/preferences.d/` с приоритетом `1001`.

## Пример использования

```yaml
- hosts: all
  roles:
    - role: docker
      vars:
        docker_user: docker
        docker_group: ["docker", "sudo"]
        docker_rootless: false
        docker_networks:
          - name: local-network
            driver: bridge
            state: present
            ipam_config:
              subnet: 172.16.248.248/30
              gateway: 172.16.248.249
```

## Поддерживаемые ОС

| ОС | Версии |
|----|--------|
| Debian | 12 |
| Ubuntu | 22.04, 24.04 |
| CentOS / RHEL | зависимости описаны в `vars/main.yml` (установка через yum) |
