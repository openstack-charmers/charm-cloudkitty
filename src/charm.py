#!/usr/bin/env python3

"""Charm the service.

Refer to the following post for a quick-start guide that will help you
develop a new k8s charm using the Operator Framework:

    https://discourse.charmhub.io/t/4208
"""

import logging

import ops_openstack.core

from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus

from charmhelpers.core import templating
from charmhelpers.contrib.openstack import templating as os_templating

from ops_openstack.adapters import (
    ConfigurationAdapter,
)

logger = logging.getLogger(__name__)

class CharmCloudkittyOptions(ConfigurationAdapter):
    pass

class CharmCloudkittyCharm(ops_openstack.core.OSBaseCharm):
    """Charm the service."""

    PACKAGES = ['cloudkitty-api', 'cloudkitty-processor', 'cloudkitty-common', 'python3-cloudkitty']

    _stored = StoredState()

    CONFIG_FILE_OWNER = 'cloudkitty'
    CONFIG_FILE_GROUP = 'cloudkitty'

    release = 'yoga'

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.config_changed, self._on_config_changed)

    def _on_config_changed(self, event):
         templating.render(
            source='cloudkitty.conf',
            template_loader=os_templating.get_loader('templates/',
                                                     self.release),
            target='/etc/cloudkitty/cloudkitty.conf',
            context={'options': CharmCloudkittyOptions(self)},
            owner=self.CONFIG_FILE_OWNER,
            group=self.CONFIG_FILE_GROUP,
            perms=0o440
        )

    def _on_install(self, event):
        super().on_install(event)

if __name__ == "__main__":
    main(CharmCloudkittyCharm)
