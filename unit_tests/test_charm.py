# Copyright 2021 OpenStack Charmers
# See LICENSE file for licensing details.
#
# Learn more about testing at: https://juju.is/docs/sdk/testing


import unittest
import sys

sys.path.append('lib')  # noqa
sys.path.append('src')  # noqa

import tempfile

from unittest import mock
import pwd
import grp
import os

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
                            return_value=tmpdir+'/'):
                self.harness.update_config({'debug': True})
                fpath = tmpdir + '/' + 'cloudkitty.conf'
                self.assertTrue(os.path.isfile(fpath))

                # need to test if _on_config_changed function got called

                with open(fpath) as f:
                    content = f.read()
                    self.assertIn('debug = True', content)

    def test_on_install(self):
        pass
