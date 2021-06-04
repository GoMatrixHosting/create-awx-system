# GoMatrixHosting AWX Setup - An AWX setup for managing multiple Matrix servers.

## Purpose

This playbook spawns an AWX system that can create and manage multiple [Matrix](http://matrix.org/) servers. You can issue members an AWX login to their own 'organisation', which they can use to manage/configure 1 to N servers.

Members can be assigned a server from Digitalocean, or they can connect their own on-premises server. This script is free to use in a commercial context with the 'MemberPress Plus' and 'WP Oauth Sever' addons. It can also be run in a non-commercial context.

The AWX system is arranged into 'members' each with their own 'subscriptions'. After creating a subscription the user enters the 'provision stage' where they defined the URLs they will use, the servers location and whether or not there's already a website at the base domain. They then proceed onto the 'deploy stage' where they can configure their Matrix server.

Ideally this system can manage the updates, configuration, backups and monitoring on it's own. It is an extension of the popular deploy script [spantaleev/matrix-docker-ansible-deploy](https://github.com/spantaleev/matrix-docker-ansible-deploy).

This project is currently beta quality and we encourage you to try it.


## Installation

To configure and install this AWX setup on your own server, follow the [Installation_AWX.md in the docs/ directory](docs/Installation_AWX.md).

For a simpler installation guide that's perfect for first time users see [Installation_Minimal_AWX.md in the docs/ directory](docs/Installation_Minimal_AWX.md).


## Deficiencies

This Ansible playbook can be improved in the following ways:

- Can be expanded to include other sections of the original playbook, like bridges.
- Someone should fork it! :)


## Contact Us

- General room: [#general:gomatrixhosting.com](https://matrix.to/#/#general:gomatrixhosting.com)
- Support room: [#support:gomatrixhosting.com](https://matrix.to/#/#support:gomatrixhosting.com)


## License

    Copyright (C) 2021 GoMatrixHosting.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
    
