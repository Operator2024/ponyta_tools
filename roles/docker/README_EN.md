# Docker

  Ansible role for automatic installation and configuration of Docker CE, including rootless mode support, user/group creation, and Docker network management.

## Features

* Docker CE installation from the official repository (apt/yum).
* Package version pinning via APT pinning.
* Creation of a system user and groups for Docker.
* Rootless mode support (linger, `dockerd-rootless-setuptool.sh`).
* Creation of Docker networks with a custom subnet and gateway.

---

## ⚠️ Breaking changes

Starting with this version, the **`docker_users` variable has been removed** and replaced by `docker_user` / `docker_group`.

| Before | After |
|--------|-------|
| `docker_users: ["user1", "user2"]` | `docker_user: docker` + `docker_group: ["docker", "sudo"]` |

Existing inventories that still define `docker_users` will **silently stop working** — override the variables according to the table below.

---

## Role Variables

| Variable | Description | Default |
|:---------|:------------|:--------|
| **`docker_ensure`** | Docker package state: `latest` or `absent` (removal) | `latest` |
| **`docker_user`** | Name of the system user for Docker services. Empty string — do not create a user | `docker` |
| **`docker_group`** | List of groups the user is added to. On RHEL-family systems use `wheel` instead of `sudo` | `["docker", "sudo"]` |
| **`docker_rootless`** | Enable Docker rootless mode | `false` |
| **`use_apt_pin_version`** | Use APT pinning to lock package versions | `true` |
| **`docker_networks`** | List of Docker networks to create (see below) | `[]` |
| **`docker_packages_extra`** | Extra packages merged into the main list (per OS release) | — |

## Rootless mode

When `docker_rootless: true`, the role:

1. Stops and disables the `docker.service` and `docker.socket` system services and removes `/var/run/docker.sock`.
2. Renames the user: a `_rootless` suffix is appended to `docker_user` (e.g. `docker` → `docker_rootless`).
3. Enables linger for the user (`loginctl enable-linger`).
4. Installs rootless Docker on behalf of the user (`dockerd-rootless-setuptool.sh install`).

> **Note:** for rootless mode the `uidmap` package is automatically added to the dependencies.

## Docker networks

The role can create networks with a custom subnet and gateway (uses `community.docker.docker_network`):

```yaml
docker_networks:
  - name: local-network
    driver: bridge
    state: present
    ipam_config:
      subnet: 172.16.248.248/30
      gateway: 172.16.248.249
```

If network creation fails, the playbook stops with a message containing the network name and the reason.

## APT pinning

Package versions are defined in `vars/<OS>.yml` per release (e.g. `jammy`, `noble` for Ubuntu).
When `use_apt_pin_version: true`, a file is created in `/etc/apt/preferences.d/` for each package with priority `1001`.

## Usage example

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

## Supported OS

| OS | Versions |
|----|----------|
| Debian | 12 |
| Ubuntu | 22.04, 24.04 |
| CentOS / RHEL | dependencies are described in `vars/main.yml` (installed via yum) |
