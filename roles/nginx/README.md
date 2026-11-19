# Nginx

  Ansible роль для гибкой настройки веб-сервера Nginx (HTTP и Stream модули) через переменные хоста.

## Возможности

* Управление сетевыми портами контейнера и хоста.
* Динамическая генерация HTTP-сайтов, локаций и правил `if`.
* Поддержка HTTP-маппинга (`map`) и балансировки (`upstream`).
* Поддержка конфигурации Stream-модуля (TCP/UDP, proxy, upstream, map).

---

## Переменные роли

Ниже представлены основные структуры данных для настройки параметров Nginx.

### 1. Сетевые порты (`nginx_ports_vars`)
Определяет проброс портов между хостом и контейнером Nginx.

```yaml
nginx_ports_vars:
  - name: http_port
    host: 80
    container: 80
    protocol: tcp
```

### 2. Настройки HTTP (`nginx_http_*`)

#### Виртуальные хосты (`nginx_http_sites`)
Конфигурация серверов, локаций, правил перенаправления и блокировок.

```yaml
nginx_http_sites:
  example.com:
    - access_log: /var/log/nginx/access.log combined
      listen: $HTTP_PORT_CONTAINER
      server_name: example.com
      locations:
        /:
          modifier: "="
          if:
            - rule: "$bad_bot != 0"
              action: "return 444"
          return: 301 https://google.com/
```

#### Маппинг HTTP переменных (`nginx_http_map`)
Позволяет создавать переменные на основе значений других переменных (например, блокировка ботов по User-Agent).

```yaml
nginx_http_map:
  bad_bot:
    source: "$http_user_agent"
    mappings:
      default: 0
      "~*badbot": 1
      "~*curl": 1
```

#### Балансировка HTTP (`nginx_http_upstream`)
Настройка бэкенд-серверов для HTTP проксирования.

```yaml
nginx_http_upstream:
  example:
    servers:
      - server: 127.0.0.1:9091
        max_fails: 1
        max_conns: 30
    resolver: "127.0.0.1 ipv6=off valid=300s"
    resolver_timeout: 5s
```

---

### 3. Настройки Stream (`nginx_stream_*`)

#### Общие параметры (`nginx_stream_common`)
Логирование и глобальные включения файлов для Stream-модуля.

```yaml
nginx_stream_common:
  log_format:
    basic: "'$remote_addr [$time_local] $protocol $status $bytes_sent $bytes_received $session_time'"
  access_log: "/var/log/nginx/access.log basic"
  include:
    - "example.conf"
```

#### Проксирование Stream (`nginx_stream_sites`)
Перенаправление трафика на уровне TCP/UDP (например, VPN или DNS).

```yaml
nginx_stream_sites:
  example:
    listen: "50157 udp"
    proxy_pass: "example_server"
    proxy_timeout: "30s"
    proxy_connect_timeout: "3s"
```

#### Балансировка Stream (`nginx_stream_upstream`)
Группы бэкендов для распределения TCP/UDP трафика.

```yaml
nginx_stream_upstream:
  example_server:
    servers:
      - server: "127.0.0.1:9091"
        max_conns: 20
```

#### Маппинг Stream переменных (`nginx_stream_map`)
Маршрутизация трафика на основе SNI (`$ssl_preread_server_name`) или других параметров.

```yaml
nginx_stream_map:
  backend:
    source: "$ssl_preread_server_name"
    mappings:
      "cloudflare.com": "172.17.0.1:8444"
      "example.com": "example_server"
      default: '""'
```

### 4. Другие переменные

* nginx_user (string) - Имя пользователя от которого запускается/разворачивается модуль
* nginx_enabled (bool) - Включает/отключает nginx в docker
* nginx_env_vars_extra (map) - Позволяет задавать переменные для файла **.env**

---

## Пример использования в Playbook

Можно использовать готовый playbook nginx.yaml либо добавить в свой playbook.

```yaml
- hosts: webservers
  gather_facts: true
  tasks:
    - name: Import nginx role
      import_role:
        name: nginx
```
