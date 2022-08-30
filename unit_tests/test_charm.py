# Copyright 2021 OpenStack Charmers
# See LICENSE file for licensing details.
#
# Learn more about testing at: https://juju.is/docs/sdk/testing

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
from charm import CharmCloudkittyCharm
from ops.testing import Harness


class TestCharm(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.harness = Harness(CharmCloudkittyCharm)
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
            with mock.patch("charm.CharmCloudkittyCharm.config_dir",
                            new_callable=mock.PropertyMock,
                            return_value=tmpdir):
                temp_dir = Path(tmpdir)
                fpath = temp_dir / 'cloudkitty.conf'

                self.harness.update_config({'debug': True})

                # test config file got created
                self.assertTrue(os.path.isfile(fpath))

                # test file got rendered
                with open(fpath) as f:
                    content = f.read()
                    self.assertIn('debug = True', content)

    def test_on_install(self):
        pass

    def test_keystone_relation(self):
        rid = self.harness.add_relation('identity-service', 'keystone')
        self.harness.add_relation_unit(rid, 'keystone/0')
        self.harness.update_relation_data(
            rid,
            'keystone/0',
            {
                'port': '5000',
                'hostname': '10.0.0.1'
            }
        )
        self.assertEqual(
            self.harness.get_relation_data(rid, 'keystone/0'),
            {
                'port': '5000',
                'hostname': '10.0.0.1'
            }
        )
