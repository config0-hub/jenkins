"""
# Copyright (C) 2025 Gary Leong <gary@config0.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

def _get_public_ip(stack):

    _lookup = {"must_exists": True,
               "must_be_one": True,
               "resource_type": "server",
               "hostname": stack.hostname}

    return list(stack.get_resource(**_lookup))[0]["public_ip"]


def _get_private_key_hash(stack):

    _lookup = {"must_exists": True,
               "resource_type": "ssh_key_pair",
               "name": stack.ssh_key_name}

    try:
        private_key = stack.get_resource(decrypt=True,
                                         **_lookup)[0]["private_key"]
    except:
        _lookup["resource_type"] = "ssh_public_key"
        private_key = stack.get_resource(decrypt=True,
                                         **_lookup)[0]["private_key"]

    return stack.b64_encode(private_key)


def run(stackargs):

    import json

    # instantiate authoring stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="hostname")
    stack.parse.add_required(key="ssh_key_name")
    stack.parse.add_required(key="publish_private_key",
                             default="null")
    stack.parse.add_optional(key="ansible_docker_image",
                             default="config0/ansible-run-env")

    # Add execgroup
    stack.add_execgroup("config0-publish:::jenkins::on_docker")
    stack.add_substack("config0-publish:::config0_core::publish_host_file")

    # Initialize
    stack.init_variables()
    stack.init_execgroups()
    stack.init_substacks()

    public_ip = _get_public_ip(stack)
    _private_key_hash = _get_private_key_hash(stack)

    # generate stateful id
    stateful_id = stack.random_id(size=10)

    env_vars = {
        "STATEFUL_ID": stateful_id,
        "DOCKER_IMAGE": stack.ansible_docker_image,
        "ANSIBLE_DIR": "var/tmp/ansible",
        "ANS_VAR_private_key": _private_key_hash,  # expects base64 string
        "ANS_VAR_hosts": stack.b64_encode(json.dumps({"all": [public_ip]})),
        "ANS_VAR_exec_ymls": "install.yml",
        "ANSIBLE_EXEC_YMLS": "install.yml"
    }

    human_description = "Install Jenkins for Ansible"
    inputargs = {
        "display": True,
        "human_description": human_description,
        "env_vars": json.dumps(env_vars.copy()),
        "stateful_id": stateful_id,
        "automation_phase": "infrastructure",
        "hostname": stack.hostname
    }

    stack.on_docker.insert(**inputargs)

    # publish variables
    _publish_vars = {
        "hostname": stack.hostname,
        "jenkins_ipaddress": public_ip,
        "jenkins_url": f"https://{public_ip}",
        "jenkins_user": "admin"
    }

    if stack.publish_private_key:
        _publish_vars["private_key_b64"] = _private_key_hash

    stack.publish(_publish_vars)

    # fetch and publish jenkins admin password
    arguments = {
        "remote_file": "/var/lib/jenkins/secrets/initialAdminPassword",
        "key": "jenkins_password",
        "hostname": stack.hostname,
        "ssh_key_name": stack.ssh_key_name
    }

    human_description = "Publish jenkins admin init password"
    inputargs = {
        "arguments": arguments,
        "automation_phase": "infrastructure",
        "human_description": human_description
    }

    stack.publish_host_file.insert(display=True, **inputargs)

    return stack.get_results()