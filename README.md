# GoMatrixHosting AWX Setup - An AWX setup for managing multiple Matrix servers.

## Purpose

This playbook spawns an AWX system that can create and manage multiple [Matrix](http://matrix.org/) servers. You can issue users an AWX login to their own 'organisation', which they can use to manage/configure 1 to N servers through.

Users can be assigned a server from DigitalOcean at the creation of the account, or they can be prompted to connect their own server in the 2nd 'provision' stage. This script is free to use in a commercial context with the MemberPress addon, we've published a seperate webhook resolver for it that allows the creation and deletion of 'members' and their 'subscriptions'.

Ideally this system can manage the updates, configuration, backups and monitoring on it's own. It is an extension of the popular deploy script [spantaleev/matrix-docker-ansible-deploy](https://github.com/spantaleev/matrix-docker-ansible-deploy).


## Installation

To configure and install this AWX setup on your own server, follow the [Installation.md in the docs/ directory](docs/Installation.md).


## Docker images used by this playbook


This playbook sets up your server using the following Docker images:

- [matrixdotorg/synapse](https://hub.docker.com/r/matrixdotorg/synapse/) - the official [Synapse](https://github.com/matrix-org/synapse) Matrix homeserver (optional)

- [instrumentisto/coturn](https://hub.docker.com/r/instrumentisto/coturn/) - the [Coturn](https://github.com/coturn/coturn) STUN/TURN server (optional)

- [vectorim/riot-web](https://hub.docker.com/r/vectorim/riot-web/) - the [Element](https://element.io/) web client (optional)


## Deficiencies

This Ansible playbook can be improved in the following ways:

- Someone should fork it! :)


## Support

- Matrix room: [#gomatrixhosting:perthchat.org](https://matrix.to/#/#gomatrixhosting:perthchat.org)

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
