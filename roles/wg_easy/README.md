# WireGuard Easy

> Ansible-роль для деплоя [wg-easy](https://github.com/wg-easy/wg-easy) — простого веб-интерфейса для управления WireGuard VPN в Docker.

> 🇬🇧 **English version:** [README_EN.md](README_EN.md)

## Quick Start

Минимальный набор переменных для деплоя (`host_vars/<host>.yaml`):

```yaml
# Включить сервис
wg_easy_enabled: true

# Версия образа wg-easy: latest, 14, 15, 15.4.0
image_version: "14"

# Основные переменные окружения (v14)
wg_env_vars_extra:
  wg_host: vpn.example.com        # домен или IP сервера, на котором деплоится VPN
  password_hash: <your_password>  # пароль от веб-интерфейса
  lang: ru
```

Запуск:

```bash
ansible-playbook -i <path_to_your_inventory> playbooks/<playbook>.yaml
```

После деплоя веб-интерфейс будет доступен на порту `51821` (TCP), WireGuard — на порту `51820` (UDP).

## Основные переменные роли

| Name | Description | Default |
|:-----|:------------|:--------|
| **`wg_easy_enabled`** | Включить/выключить сервис WireGuard (Docker Compose) | `false` |
| **`image_version`** | Версия Docker-образа wg-easy. Доступны: `latest`, `14`, `15`, `15.4.0` | `14` |
| **`wg_user`** | Системный пользователь, от которого деплоится сервис | `root` |
| **`wg_default_dir`** | Каталог установки на удалённом хосте | `/opt/docker_apps/wg_easy` |
| **`wg_compose_file`** | Путь до итогового `docker-compose.yml` | `{{ wg_default_dir }}/docker-compose.yml` |
| **`service_name`** | Имя сервиса в Docker Compose | `wg-easy` |
| **`wg_shared_network`** | Подключить контейнер к внешней общей Docker-сети | `false` |
| **`wg_shared_network_name`** | Имя внешней общей сети (используется при `wg_shared_network: true`) | `shared-net` |

> **Примечание:** переменную `wg_network_name` задавать не нужно — она вычисляется динамически как `{{ service_name }}-net` (по умолчанию `wg-easy-net`).

## Переменные окружения wg-easy

Значения по умолчанию (v14, словарь `wg_env_vars`):

| Name | Default |
|:-----|:--------|
| `lang` | `en` |
| `wg_host` | `vpn.example.com` |
| `port` | `51821` |
| `port_ext` | `51821` |
| `wg_port` | `51820` |
| `wg_port_ext` | `51820` |
| `password_hash` | `wg_easy_default_PSWD` |

Свои значения передаются через `wg_env_vars_extra` (см. Quick Start).

> Полный список доступных переменных и их описание — в официальной документации
> [wg-easy (секция Options)](https://github.com/wg-easy/wg-easy/blob/v14.0.0/README.md#options).

### Версии 15+

Для `image_version: 15` / `15.4.0` используются словари:

* **`wg_env_vars_15`** — переменные окружения wg-easy v15 (`experimental_awg`, `insecure`, `disable_ipv6`, `disable_password_auth` и др.);
* **`wg_env_vars_init`** / **`wg_env_vars_init_extra`** — переменные первичной инициализации (выполняется один раз при первом запуске): `init_enabled`, `init_username`, `init_password`, `init_host`, `init_port`, `init_dns`, `init_ipv4_cidr`, `init_allowed_ips`.

Пример:

```yaml
image_version: "15.4.0"

wg_env_vars_init_extra:
  init_enabled: true
  init_username: admin
  init_password: <your_password>
  init_host: vpn.example.com
  init_dns: 1.1.1.1,8.8.8.8
```

## Полезные теги

| Tag | Description |
|:----|:------------|
| `wg_easy_docker_restart` | Перезапустить сервис (вместо идемпотентного up) |
| `force_update_git_repo` | Принудительно обновить git-репозиторий wg-easy |
| `wg_easy_generate` | Перегенерировать compose-файл |
| `debug` | Вывод статуса сервисов Docker Compose |
