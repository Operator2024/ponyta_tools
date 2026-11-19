
# Ponyta

⚠️ **Важно:** По умолчанию включен только `prometheus`.
Для включения и задания своих значений встроенным экспортерам/датасоурсам необходимо переопределить ряд переменных перед запуском плейбука.
Полный список переменных будет приведен далее.

## Настройка переменных

Для плейбука `ponyta_setup.yaml` могут быть переопределены следующие переменные:

### 🐳 Включение/выключение экспортеров/сервисов в Docker

- `prometheus_enabled` - включение Prometheus (включен по умолчанию)
- `grafana_enabled` - включение Grafana
- `ping_exporter_enabled` - включение Ping Exporter
- `node_exporter_enabled` - включение Node Exporter
- `blackbox_exporter_enabled` - включение Blackbox Exporter
- `snmp_exporter_enabled` - включение SNMP Exporter

### Настройка .env для docker-compose

Значения файла .env по умолчанию можно переопределить через переменную `env_vars_extra`.
Переменная содержит словарь ключ-значение. Список переменных (ключей) можно найти в пунктах [Настройка Grafana](#основные-параметры), [Настройка Prometheus](#📈-настройка-prometheus) и [Настройка SNMP Exporter](#🔍-настройка-snmp-exporter).

### 📊 Настройка Grafana

#### Основные параметры

| Переменная                   | Описание                           | Значение по умолчанию          |
|------------------------------|------------------------------------|--------------------------------|
| `gf_external_port`           | Порт для доступа к Grafana извне   | `"3000"`                       |
| `gf_security_admin_user`     | Имя пользователя администратора    | `"admin"`                      |
| `gf_security_admin_password` | Пароль администратора              | `"defaultpassword"`            |
| `gf_server_name`             | Имя сервера Grafana                | `"{{ default_domain }}"`       |
| `gf_server_protocol`         | Протокол доступа (http/https)      | `"http"`                       |
| `gf_server_cert_file`        | Путь к SSL сертификату             | `"/etc/grafana/certs/tls.crt"` |
| `gf_server_cert_key`         | Путь к приватному ключу SSL        | `"/etc/grafana/certs/tls.key"` |
| `gf_server_root_url`         | Корневой URL для доступа к Grafana | `"/grafana"`                   |
| `gf_server_domain`           | Домен сервера Grafana              | `"{{ default_domain }}"`       |

#### Настройка SMTP

| Переменная                | Описание                                   | Значение по умолчанию |
|---------------------------|--------------------------------------------|-----------------------|
| `gf_smtp_enabled`         | Включить/выключить SMTP                    | `"false"`             |
| `gf_smtp_host`            | SMTP сервер (например: smtp.gmail.com:587) | `""`                  |
| `gf_smtp_user`            | Пользователь SMTP                          | `""`                  |
| `gf_smtp_password`        | Пароль SMTP                                | `""`                  |
| `gf_smtp_from_address`    | Email адрес отправителя                    | `""`                  |
| `gf_smtp_from_name`       | Имя отправителя                            | `"Grafana"`           |
| `gf_smtp_skip_verify`     | Пропустить проверку сертификата            | `"false"`             |
| `gf_smtp_smarttls_policy` | Политика TLS для SMTP                      | `"MandatoryStartTLS"` |

**Важно:** Измените значения по умолчанию для `gf_security_admin_user`, `gf_security_admin_password` в продакшен среде для обеспечения безопасности.

#### 📈 Настройка Prometheus

| Переменная | Описание | Значение по умолчанию |
|------------|----------|----------------------|
| `prom_url` | URL для доступа к Prometheus (если пусто - используется внутренний адрес) | `""` |
| `prom_port` | Порт для доступа к Prometheus | `9090` |

**Примечание:** Если `prom_url` не задан, будет использоваться внутренний адрес контейнера Prometheus.

#### 🔍 Настройка SNMP Exporter

| Переменная | Описание | Значение по умолчанию |
|------------|----------|----------------------|
| `snmp_secret` | Секретный ключ/пароль для SNMP экспортера | `"defaultpassword"` |
| `snmp_user` | Пользователь для SNMP экспортера | `"admin"` |

**Важно:** Измените значения по умолчанию для `snmp_secret` в продакшен среде для обеспечения безопасности.

## Переменные не относящиеся к `env_vars_extra`

**Важно:** С помощью переменных описанных ниже можно изменять некоторые параметры у некоторых экспортеров, а также добавлять свои `prometheus job` и изменять параметры у существующих.

### Prometheus

- `prometheus_jobs_extra` - позволяет добавить свои задания и/или переопределить значения у уже существующих по умолчанию в Ponyta.
  Список параметров, для которых поддерживается возможность задавать собственное значение можно посмотреть в шаблонах для роли [**Ponyta**](roles/ponyta/templates)

- `prometheus_job_templates_extra` - позволяет связать Prometheus задания (job) с шаблоном в формате **.j2**.
  Например, может быть полезно, когда необходимо добавить собственный шаблон, который предоставит возможность изменения параметров, которой нет у шаблона по умолчанию.
  В этом случае необходимо добавить как ключ-значение запись в переменную, где
  - ключ - название экспортера (job_name) используемое в переменной `prometheus_jobs_extra`
  - значение - имя вашего шаблона в формате **.j2**.

- `prometheus_force_password_regenerate` - позволяет принудительно перегенерировать пароль для файла авторизации [**web.yml**](roles/ponyta/defaults/main.yml#L14)

- `prometheus_users` - позволяет задавать пользователей для basic_auth в Prometheus (ключ-значение: имя-пароль). Может быть более одного пользователя.
- `prometheus_job_basic_auth_username` - позволяет переопределить имя пользователя по умолчанию (admin). Используется экспортером метрик при походе за метриками в сам Prometheus.

### 🎯 Ping Exporter

- `ping_targets` - цели для мониторинга ping
- `ping_dns_nameserver` - DNS сервер для разрешения имен
- `ping_ping_interval` - интервал между пингами
- `ping_ping_timeout` - таймаут ожидания ответа
- `ping_ping_history_size` - размер истории пингов
- `ping_ping_payload_size` - размер полезной нагрузки пинга
- `ping_options_disableIPv6` - отключение IPv6

### ⚙️ Другие переменные

- `git_branch` - ветка для разворачивания сервиса Ponyta
- `ponyta_user` - пользователь для запуска Ponyta
- `docker_packages_extra` - кастомные пакеты/версии Docker
- `blackbox_targets` - кастомные таргеты для Blackbox
- `env_vars_extra` - дополнительные переменные окружения (про неё описано выше)
- `default_domain` - домен по умолчанию

## Пример #1

Необходимо развернуть Ponyta:

- С измененным паролем для пользователя **admin** в Grafana/Promethes ✔️
- С новым пользователем в Prometheus ✔️
- С измененным портом для доступа из вне в Grafana ✔️

### Решение

Для этого необходимо в инвентарном файле переопределить некоторые переменные.

```yaml
---
# Переопределяем пользователя от имени которого экспортер будет ходить за метриками.
# Описываем пользователей для Prometheus
prometheus_job_basic_auth_username: prometheus_metrics
prometheus_users:
  admin: PeSpCHe4mpS5TCf3cULv
  grafana: e8PFSpS5TCf3cULvsGX2j
  prometheus_metrics: j7TwQ5vasiBAzsnK9X6g

# Указываем пользователя, пароль и внешний порт для Grafana
env_vars_extra:
  gf_security_admin_user: bender
  gf_security_admin_password: sGX2je8PFShJMpE4kb2A
  gf_external_port: 8081

# Переопределяем имя и пароль стандартного Datasource для Prometheus
# Имя пользователя и пароль были добавлены выше.
grafana_datasources_extra:
  datasource:
    basicAuthUser: grafana
    secureJsonData:
      basicAuthPassword: "{{ prometheus_users['grafana'] }}"

# Изменяем имя и пароль для стандартного задания с именем 'grafana'
# По умолчанию используется 'password_file', который хранит единый пароль для заданий 'grafana' и 'prometheus'
prometheus_jobs_extra:
  grafana:
    job_name: grafana
    basic_auth:
      username: "{{ env_vars_extra.gf_security_admin_user }}"
      password: "{{ env_vars_extra.gf_security_admin_password }}"
      password_file: null

prometheus_enabled: true
grafana_enabled: true

```

После добавления данных параметров в свой инвентарный файл и запуска плейбука будет развернута Ponyta в docker-compose с двумя включенными сервисами Prometheus и Grafana.
Сервис Grafana будет доступна по адресу вашего сервера на порту 8081.
