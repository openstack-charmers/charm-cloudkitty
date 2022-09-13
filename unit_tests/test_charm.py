# Copyright 2021 OpenStack Charmers
# See LICENSE file for licensing details.
#
# Learn more about testing at: https://juju.is/docs/sdk/testing


import sys

sys.path.append('lib')  # noqa
sys.path.append('src')  # noqa

import charm
import unittest
import pwd
import grp
import os

from tempfile import TemporaryDirectory
from pathlib import Path
from unittest.mock import (
    Mock,
    PropertyMock,
    patch
)

from ops.testing import Harness
import ops_sunbeam.test_utils as test_utils


class TestCloudkittyCharm(charm.CloudkittyCharm):
    """
    Workaround until 'network-get' call gets mocked
    See https://github.com/canonical/operator/issues/456
    See https://github.com/canonical/operator/issues/222
    """
    @property
    def host(self):
        return '10.0.0.10'


tmpdir = Path(TemporaryDirectory().name)


class TestCharm(unittest.TestCase):
    def setUp(self):
        self.harness = Harness(TestCloudkittyCharm)

        self.harness.set_leader(True)
        self.harness.enable_hooks()

        self.addCleanup(self.harness.cleanup)
        self.harness.begin()

    def test_on_install(self):
        pass

    @patch('charm.CloudkittyCharm.CONFIG_DIR',
       new_callable=PropertyMock,
       return_value=tmpdir)
    @patch('os.fchown')
    @patch('os.chown')
    @patch('pwd.getpwnam', Mock(auto_spec=True))
    @patch('grp.getgrnam', Mock(auto_spec=True))
    def test_config_changed(self, fchown, chown, getpwnam):
        self.harness.update_config({'debug': True})

        fpath = tmpdir / TestCloudkittyCharm.CONFIG_FILE
        self.assertTrue(os.path.isfile(fpath))

        with open(fpath) as f:
            content = f.read()
            self.assertIn('debug = True', content)

    @patch('charm.CloudkittyCharm.CONFIG_DIR',
       new_callable=PropertyMock,
       return_value=tmpdir)
    @patch('os.fchown')
    @patch('os.chown')
    @patch('pwd.getpwnam', Mock(auto_spec=True))
    @patch('grp.getgrnam', Mock(auto_spec=True))
    def test_identity_service_relation(self, fchown, chown, getpwnam):
        # add identity-service relation
        test_utils.add_complete_identity_relation(self.harness)

        fpath = tmpdir / TestCloudkittyCharm.CONFIG_FILE
        self.assertTrue(os.path.isfile(fpath))

        # test file got rendered
        with open(fpath) as f:
            content = f.read()
            self.assertIn(
                'identity_uri = http://keystone.local:5000/v3',
                content)

    @patch('charm.CloudkittyCharm.CONFIG_DIR',
        new_callable=PropertyMock,
        return_value=tmpdir)
    @patch('os.fchown')
    @patch('os.chown')
    @patch('pwd.getpwnam', Mock(auto_spec=True))
    @patch('grp.getgrnam', Mock(auto_spec=True))
    def test_database_relation(self, fchown, chown, getpwnam):
        rid = self.harness.add_relation('database', 'mysql')
        self.harness.add_relation_unit(rid, 'mysql/0')
        self.harness.update_relation_data(
            rid, "mysql/0", {"ingress-address": "10.0.0.33"}
        )
