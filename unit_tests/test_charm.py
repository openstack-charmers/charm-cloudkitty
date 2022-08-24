import unittest
# from unittest.mock import Mock

from charm import CharmCloudkittyCharm
# from ops.model import ActiveStatus
from ops.testing import Harness


class TestCharm(unittest.TestCase):
    def setUp(self):
        self.harness = Harness(CharmCloudkittyCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()

    def test_config_changed(self):
        self.harness.update_config({"debug": True})
        pass
