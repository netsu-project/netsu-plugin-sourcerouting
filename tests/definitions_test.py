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

import jsonschema
import pytest

from netsu_plugin_sourcerouting import definitions


_definitions = {'Config': {'type': 'object', 'properties': {}}}
definitions.update(_definitions)
schema = {'$ref': '#/definitions/Config', 'definitions': _definitions}


@pytest.mark.unit
class TestValidConfig(object):

    def test_empty(self):
        DATA = {'sourcerouting': {'static': [], 'dynamic': []}}
        jsonschema.validate(DATA, schema)

    def test_filled(self):
        DATA = {'sourcerouting': {
            'static': [
                {
                    'device': 'br0',
                    'subnet': '192.168.1.0/24',
                    'gateway': '192.168.1.1',
                    'label': 'foo'
                }
            ],
            'dynamic': [
                {
                    'device': 'br1',
                    'label': 'bar'
                }
            ]
        }}
        jsonschema.validate(DATA, schema)

    def test_empty_label(self):
        DATA = {'sourcerouting': {
            'dynamic': [
                {
                    'device': 'br1',
                    'label': None
                }
            ]
        }}
        jsonschema.validate(DATA, schema)

    def test_no_label(self):
        DATA = {'sourcerouting': {
            'dynamic': [
                {
                    'device': 'br1'
                }
            ]
        }}
        jsonschema.validate(DATA, schema)


@pytest.mark.unit
class TestInvalidConfig(object):

    def test_missing_device(self):
        DATA = {'sourcerouting': {
            'static': [
                {
                    'subnet': '192.168.1.0/24',
                    'gateway': '192.168.1.1',
                    'label': 'foo'
                }
            ]
        }}
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(DATA, schema)

    def test_invalid_subnet(self):
        DATA = {'sourcerouting': {
            'static': [
                {
                    'subnet': '192.168.1.0',
                    'gateway': '192.168.1.1',
                    'label': 'foo'
                }
            ]
        }}
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(DATA, schema)

    def test_invalid_gateway(self):
        DATA = {'sourcerouting': {
            'static': [
                {
                    'subnet': '192.168.1.0/24',
                    'gateway': '192.168.1.300',
                    'label': 'foo'
                }
            ]
        }}
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(DATA, schema)
