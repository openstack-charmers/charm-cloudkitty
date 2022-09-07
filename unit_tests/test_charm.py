# Copyright 2021 OpenStack Charmers
# See LICENSE file for licensing details.
#
# Learn more about testing at: https://juju.is/docs/sdk/testing

import logging
import unittest
import sys
import pwd
import grp
import os
import tempfile

sys.path.append('lib')  # noqa
sys.path.append('src')  # noqa

from pathlib import Path
from unittest import mock
import charm

from ops.testing import Harness
from charmhelpers.fetch import apt_install


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
        super().setUp()

        self.harness = Harness(TestCloudkittyCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()

    @mock.patch('os.fchown')
    @mock.patch('os.chown')
    @mock.patch('pwd.getpwnam', mock.Mock(auto_spec=True))
    @mock.patch('grp.getgrnam', mock.Mock(auto_spec=True))
    def test_config_changed(self, chown, fchown):
        self.harness.set_leader(True)
        self.harness.enable_hooks()

        with tempfile.TemporaryDirectory() as tmpdir:
            with mock.patch("charm.CloudkittyCharm.CONFIG_DIR",
                            new_callable=mock.PropertyMock,
                            return_value=Path(tmpdir)):
                fpath = Path(tmpdir) / 'cloudkitty.conf'

                self.harness.update_config({'debug': True})

                # test config file got created
                self.assertTrue(os.path.isfile(fpath))

                # test file got rendered
                with open(fpath) as f:
                    content = f.read()
                    self.assertIn('debug = True', content)

    # @mock.patch('charmhelpers.fetch.apt_install')
    # @mock.patch('charmhelpers.fetch.apt_update')
    # def test_on_install(self, apt_install, apt_update):
    #     self.harness.charm.on_install(mock.Mock(auto_spec=True))
    #     apt_update.assert_called()
    #     apt_install.assert_called_with(['cloudkitty-api',
    #         'cloudkitty-processor',
    #         'cloudkitty-common',
    #         'python3-cloudkitty'])

    def test_identity_service_relation(self):
        self.harness.enable_hooks()
        rid = self.harness.add_relation('identity-service', 'keystone')
        self.harness.add_relation_unit(rid, 'keystone/0')
        self.harness.update_relation_data(
            rid,
            'keystone/0',
            {
                'auth_protocol': 'http',
                'auth_host': '10.0.0.1',
                'service_port': '5000',
                'api_version': 'v3',
                'service_user_name': 'test_user',
                'service_password': 'test_password'
            }
        )
        import ripdb; ripdb.set_trace()

    def test_database_relation(self):
        rid = self.harness.add_relation('database', 'mysql')
        self.harness.add_relation_unit(rid, 'mysql/0')
