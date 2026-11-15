# WireGuard Easy

> Ansible role for deploying [wg-easy](https://github.com/wg-easy/wg-easy) — a simple web UI for managing WireGuard VPN in Docker.

## Quick Start

Minimal set of variables for deployment (`host_vars/<host>.yaml`):

```yaml
# Enable the service
wg_easy_enabled: true

# wg-easy image version: latest, 14, 15, 15.4.0
image_version: "14"

# Core environment variables (v14)
wg_env_vars_extra:
  wg_host: vpn.example.com        # domain or IP of the server hosting the VPN
  password_hash: <your_password>  # web UI password
  lang: en
```

Run:

```bash
ansible-playbook -i <path_to_your_inventory> playbooks/<playbook>.yaml
```

After deployment, the web UI will be available on port `51821` (TCP), and WireGuard on port `51820` (UDP).

## Main Role Variables

| Name | Description | Default |
|:-----|:------------|:--------|
| **`wg_easy_enabled`** | Enable/disable the WireGuard service (Docker Compose) | `false` |
| **`image_version`** | wg-easy Docker image version. Available: `latest`, `14`, `15`, `15.4.0` | `14` |
| **`wg_user`** | System user under which the service is deployed | `root` |
| **`wg_default_dir`** | Installation directory on the remote host | `/opt/docker_apps/wg_easy` |
| **`wg_compose_file`** | Path to the resulting `docker-compose.yml` | `{{ wg_default_dir }}/docker-compose.yml` |
| **`service_name`** | Service name in Docker Compose | `wg-easy` |
| **`wg_shared_network`** | Attach the container to an external shared Docker network | `false` |
| **`wg_shared_network_name`** | Name of the external shared network (used when `wg_shared_network: true`) | `shared-net` |

> **Note:** there is no need to set `wg_network_name` — it is computed dynamically as `{{ service_name }}-net` (`wg-easy-net` by default).

## wg-easy Environment Variables

Default values (v14, the `wg_env_vars` dictionary):

| Name | Default |
|:-----|:--------|
| `lang` | `en` |
| `wg_host` | `vpn.example.com` |
| `port` | `51821` |
| `port_ext` | `51821` |
| `wg_port` | `51820` |
| `wg_port_ext` | `51820` |
| `password_hash` | `wg_easy_default_PSWD` |

Custom values are passed via `wg_env_vars_extra` (see Quick Start).

> For the full list of available variables and their descriptions, see the official
> [wg-easy documentation (Options section)](https://github.com/wg-easy/wg-easy/blob/v14.0.0/README.md#options).

### Versions 15+

For `image_version: 15` / `15.4.0` the following dictionaries are used:

* **`wg_env_vars_15`** — wg-easy v15 environment variables (`experimental_awg`, `insecure`, `disable_ipv6`, `disable_password_auth`, etc.);
* **`wg_env_vars_init`** / **`wg_env_vars_init_extra`** — one-time initialization variables (applied once on first start): `init_enabled`, `init_username`, `init_password`, `init_host`, `init_port`, `init_dns`, `init_ipv4_cidr`, `init_allowed_ips`.

Example:

```yaml
image_version: "15.4.0"

wg_env_vars_init_extra:
  init_enabled: true
  init_username: admin
  init_password: <your_password>
  init_host: vpn.example.com
  init_dns: 1.1.1.1,8.8.8.8
```

## Useful Tags

| Tag | Description |
|:----|:------------|
| `wg_easy_docker_restart` | Restart the service (instead of an idempotent up) |
| `force_update_git_repo` | Force-update the wg-easy Git repository |
| `wg_easy_generate` | Re-render the compose file |
| `debug` | Show Docker Compose service status |
