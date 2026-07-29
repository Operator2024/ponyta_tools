
# Wireguard Easy
>
> Ansible role for configuration wireguard. Or wrapper for project [wg-easy](https://github.com/wg-easy/wg-easy)

## Settings

Для конфигурации роли доступны следующие переменные

| Name                         | Description                                                                            | Default                                   |
|:-----------------------------|:---------------------------------------------------------------------------------------|:------------------------------------------|
| **`wg_user`**                | System user account under which the environment is configured                          | `root`                                    |
| **`wg_easy_enabled`**        | Toggle switch to control whether the WireGuard Docker services should be running       | `false`                                   |
| **`wg_default_dir`**         | Base installation directory on the remote host for application files                   | `/opt/docker_apps/wg_easy`                |
| **`wg_compose_file`**        | Absolute path to the targeted `docker-compose.yml` configuration file                  | `{{ wg_default_dir }}/docker-compose.yml` |
| **`git_repo_url`**           | URL of the official wg-easy Git repository to source files from                        | `https://github.com`                      |
| **`git_clone_path`**         | Destination directory on the host where the Git repository will be cloned              | `{{ wg_default_dir }}`                    |
| **`git_branch`**             | Specific branch, tag, or version release to checkout from Git                          | `v14`                                     |
| **`service_name`**           | Designated identifier for the core service inside Docker Compose                       | `wg_easy`                                 |
| **`image_version`**          | Tag version of the Docker image used to build the container                            | `14`                                      |
| **`wg_network_name`**        | Name of the primary dedicated Docker network created for the VPN                       | `wg-easy-net`                             |
| **`wg_network_subnet`**      | Total IP subnet allocated for the Docker network infrastructure                        | `172.20.0.0/16`                           |
| **`wg_network_range`**       | IP range scope assigned specifically for routing VPN client connections                | `172.20.5.0/24`                           |
| **`wg_network_gateway`**     | Assigned gateway IP address for the internal container network                         | `172.20.5.254`                            |
| **`wg_shared_network`**      | Toggle to link the container to an external shared proxy network                       | `false`                                   |
| **`wg_shared_network_name`** | Name of the external shared network (the missing dependency causing the earlier error) | `shared-net`                              |
| **`wg_env_vars_extra`**      | Dictionary block for declaring custom container environment variables                  | `{}`                                      |
| **`port`**                         | TCP port for Web UI inside container container                                                               | 51821                                     |
| **`port_ext`**                     | TCP port for Web UI outside container container                                                               | 51821                                     |
| **`wg_port`**                      | UDP port for 'wireguard' inside containercontainer                                                               | 51820                                     |
| **`wg_port_ext`**                  | UDP port for 'wireguard' outside container container                                                               | 51820                                     |
| **`password_hash`**                | Clear password for web UI                                                              | wg_easy_default_PSWD                      |

The full list of parameters that can be specified (depending on the version of wg-easy) in wg_env_vars_extra -> <https://github.com/wg-easy/wg-easy/blob/v14.0.0/README.md#options>

Some parameters have a default value, eg.

* lang - en
* wh_host - vpn.example.com
* port - 51821
* port_ext - 51821
* wg_port - 51820
* wg_port_ext - 51820
* password_hash - wg_easy_default_PSWD
