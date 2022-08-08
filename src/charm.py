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

from charms.sunbeam_keystone_operator.v0.identity_service import IdentityServiceRequires

logger = logging.getLogger(__name__)

class CharmCloudkittyOptions(ConfigurationAdapter):
    pass

class CharmCloudkittyCharm(ops_openstack.core.OSBaseCharm):
    """Charm the service."""

    PACKAGES = [
        'cloudkitty-api',
        'cloudkitty-processor',
        'cloudkitty-common',
        'python3-cloudkitty'
    ]

    _stored = StoredState()

    CONFIG_FILE_OWNER = 'cloudkitty'
    CONFIG_FILE_GROUP = 'cloudkitty'

    release = 'yoga'

    def __init__(self, *args):
        super().__init__(*args)

        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.config_changed, self._on_config_changed)

        self.identity_service = IdentityServiceRequires(
            charm = self,
            relation_name = "identity-service",
            service_endpoints = {
              "service_name": "cloudkitty",
              "type": "rating",
              "description": "Rating as a Service",
              "internal_url": "http://10.5.1.152:8889",
              "public_url": "http://10.5.1.152:8889",
              "admin_url": "http://10.5.1.152:8889",
            },
            region = "RegionOne"

            # self, "cloudkitty",
            # service = "rating",
            # internal_url = "http://10.5.1.152:8889",
            # public_url = "http://10.5.1.152:8889",
            # admin_url = "http://10.5.1.152:8889",
            # region = "RegionOne"
        )

        self.framework.observe(
            self.identity_service.on.connected, self._on_identity_service_connected)
        self.framework.observe(
            self.identity_service.on.ready, self._on_identity_service_ready)
        self.framework.observe(
            self.identity_service.on.goneaway, self._on_identity_service_goneaway)

    def _on_install(self, event):
        super().on_install(event)

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

    def _on_identity_service_connected(self, _):
        '''React to the IdentityService connected event.

        This event happens when n IdentityService relation is added to the
        model before credentials etc have been provided.
        '''
        # Do something before the relation is complete
        pass

    def _on_identity_service_ready(self, _):
        '''React to the IdentityService ready event.

        The IdentityService interface will use the provided config for the
        request to the identity server.
        '''
        # IdentityService Relation is ready. Do something with the completed relation.
        pass

    def _on_identity_service_goneaway(self, _):
        '''React to the IdentityService goneaway event.

        This event happens when an IdentityService relation is removed.
        '''
        # IdentityService Relation has goneaway. shutdown services or suchlike
        pass

if __name__ == "__main__":
    main(CharmCloudkittyCharm)
