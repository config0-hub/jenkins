# Jenkins Installation Stack

## Description
This stack automates the installation of Jenkins on a pre-existing server using Ansible in a Docker container. It configures the server, publishes the Jenkins credentials, and makes them available for future use.

## Variables

### Required
| Name | Description | Default |
|------|-------------|---------|
| hostname | Server hostname | &nbsp; |
| ssh_key_name | Name label for SSH key | &nbsp; |
| publish_private_key | Flag to determine whether to publish the private key | "null" |

### Optional
| Name | Description | Default |
|------|-------------|---------|
| ansible_docker_image | Ansible container image | "config0/ansible-run-env" |

## Dependencies

### Substacks
- [config0-publish:::config0_core::publish_host_file](http://config0.http.redirects.s3-website-us-east-1.amazonaws.com/assets/stacks/config0-publish/config0_core/publish_host_file/default)

### Execgroups
- [config0-publish:::jenkins::on_docker](http://config0.http.redirects.s3-website-us-east-1.amazonaws.com/assets/exec/groups/config0-publish/jenkins/on_docker/default)

### Shelloutconfigs
- [config0-publish:::terraform::resource_wrapper](http://config0.http.redirects.s3-website-us-east-1.amazonaws.com/assets/shelloutconfigs/config0-publish/terraform/resource_wrapper/default)

## License
<pre>
Copyright (C) 2025 Gary Leong <gary@config0.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the License.
</pre>