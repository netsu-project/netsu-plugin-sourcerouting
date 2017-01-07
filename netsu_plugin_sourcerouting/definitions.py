# Copyright (C) 2016 Petr Horacek <phoracek@redhat.com>
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


ADDRESS_PATTERN = ('^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}'
                   '([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$')
SUBNET_PATTERN = ('^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}'
                  '([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'
                  '(\/([0-9]|[1-2][0-9]|3[0-2]))$')
LABEL_PATTERN = '^[0-9a-zA-Z _-]{0,254}$'


STATIC_SR = {
    'SourceRoutingStatic': {
        'type': 'object',
        'required': ['device', 'subnet', 'gateway'],
        'properties': {
            'device': {
                'type': 'string'
            },
            'subnet': {
                'type': 'string',
                'pattern': SUBNET_PATTERN
            },
            'gateway': {
                'type': 'string',
                'pattern': ADDRESS_PATTERN
            },
            'label': {
                'default': None,
                'anyOf': [
                    {'type': 'string', 'pattern': LABEL_PATTERN},
                    {'type': 'null'}
                ]
            }
        }
    }
}

DYNAMIC_SR = {
    'SourceRoutingDynamic': {
        'type': 'object',
        'required': ['device'],
        'properties': {
            'device': {
                'type': 'string'
            },
            'label': {
                'default': None,
                'anyOf': [
                    {'type': 'string', 'pattern': LABEL_PATTERN},
                    {'type': 'null'}
                ]
            }
        }
    }
}

SOURCE_ROUTES = {
    'SourceRouting': {
        'type': 'object',
        'default': {},
        'properties': {
            'static': {
                'type': 'array',
                'default': [],
                'items': {'$ref': '#/definitions/SourceRoutingStatic'}
            },
            'dynamic': {
                'type': 'array',
                'default': [],
                'items': {'$ref': '#/definitions/SourceRoutingDynamic'}
            }
        }
    }
}


def update(api_definitions):
    api_definitions.update(STATIC_SR)
    api_definitions.update(DYNAMIC_SR)
    api_definitions.update(SOURCE_ROUTES)
    api_definitions['Config']['properties']['sourcerouting'] = {
        '$ref': '#/definitions/SourceRouting'
    }
