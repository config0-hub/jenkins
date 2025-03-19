# Jenkins Installation Stack

## Description
This stack automates the installation of Jenkins on a pre-existing server using Ansible in a Docker container. It configures the server, publishes the Jenkins credentials, and makes them available for future use.

## Variables

### Required
| Name | Description | Default |
|------|-------------|---------|
| hostname | Server hostname | |
| ssh_key_name | Name label for SSH key | |
| publish_private_key | 99checkme99 Flag to determine whether to publish the private key | "null" |

### Optional
| Name | Description | Default |
|------|-------------|---------|
| ansible_docker_image | Ansible container image | "config0/ansible-run-env" |

## Features
- Automatically retrieves server public IP
- Securely handles SSH keys
- Installs and configures Jenkins using Ansible
- Publishes Jenkins access credentials including admin password
- Provides access URL for the Jenkins instance

## Dependencies

### Substacks
- [config0-publish:::config0_core::publish_host_file](https://api-app.config0.com/web_api/v1.0/stacks/config0-publish/config0_core/publish_host_file)

### Execgroups
- [config0-publish:::jenkins::on_docker](https://api-app.config0.com/web_api/v1.0/exec/groups/config0-publish/jenkins/on_docker)

## License
Copyright (C) 2025 Gary Leong <gary@config0.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the License.