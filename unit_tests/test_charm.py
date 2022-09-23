# Copyright 2021 OpenStack Charmers
# See LICENSE file for licensing details.
#
# Learn more about testing at: https://juju.is/docs/sdk/testing


import sys

sys.path.append('lib')  # noqa
sys.path.append('src')  # noqa

import charm
import unittest
import test_utils

from unittest.mock import (
    patch,
    call
)
from ops.testing import Harness


class TestCloudkittyCharm(charm.CloudkittyCharm):
    """
    Workaround until 'network-get' call gets mocked
    See https://github.com/canonical/operator/issues/456
    See https://github.com/canonical/operator/issues/222
    """
    @property
    def host(self):
        return '10.0.0.10'


class TestCharm(unittest.TestCase):
    def setUp(self):
        self.harness = Harness(TestCloudkittyCharm)

        self.harness.set_leader(True)
        self.harness.disable_hooks()

        self.addCleanup(self.harness.cleanup)
        self.harness.begin()

    @patch('ops_openstack.core.apt_update')
    @patch('ops_openstack.core.apt_install')
    def test_on_install(self, _install, _update):
        self.harness.charm.on_install('An event')
        _update.assert_called_with(fatal=True)
        _install.assert_called_with(TestCloudkittyCharm.PACKAGES, fatal=True)

    @patch('charmhelpers.core.host.mkdir')
    @patch('charmhelpers.core.host.write_file')
    def test_config_changed(self, _write_file, _mkdir):
        # change application config
        self.harness.update_config({'debug': True})

        # check rendered content
        content = self.harness.charm._render_config('An event')
        self.assertIn('debug = True', content)

    @patch('charmhelpers.core.host.mkdir')
    @patch('charmhelpers.core.host.write_file')
    def test_identity_service_relation(self, _write_file, _mkdir):
        # add identity-service relation
        test_utils.add_complete_identity_relation(self.harness)

        # check rendered content
        expect_entries = [
            'auth_protocol = http',
            'auth_uri = http://keystone.local:5000/v3',
            'auth_url = http://keystone.local:12345/v3',
            'project_domain_name = servicedom',
            'user_domain_name = servicedom',
            'identity_uri = http://keystone.local:5000/v3',
            'project_name = svcproj1',
            'username = svcuser1',
            'password = svcpass1',
            'region_name = RegionOne'
        ]

        content = self.harness.charm._render_config('An event')
        for entry in expect_entries:
            self.assertIn(entry, content)

    @patch('charmhelpers.core.host.mkdir')
    @patch('charmhelpers.core.host.write_file')
    def test_database_relation(self, _write_file, _mkdir):
        # add database relation
        test_utils.add_complete_database_relation(self.harness)

        # check rendered content
        expect_entries = [
            'mysql+pymysql://dbuser:strongpass@juju-unit-1:3306/cloudkitty'
        ]

        content = self.harness.charm._render_config('An event')
        for entry in expect_entries:
            self.assertIn(entry, content)

    @patch('charmhelpers.core.host.mkdir')
    @patch('charmhelpers.core.host.write_file')
    @patch('subprocess.run')
    def test_database_migration(self, _subprocess_run, _write_file, _mkdir):
        # enable hooks
        self.harness.enable_hooks()

        # add database relation
        test_utils.add_complete_database_relation(self.harness)

        calls = [
            call(['cloudkitty-storage-init'], capture_output=True),
            call(['cloudkitty-dbsync', 'upgrade'], capture_output=True)
        ]
        _subprocess_run.assert_has_calls(calls, any_order=True)
