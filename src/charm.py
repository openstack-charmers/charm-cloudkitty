#!/usr/bin/env python3

"""Charm the service.

Refer to the following post for a quick-start guide that will help you
develop a new k8s charm using the Operator Framework:

    https://discourse.charmhub.io/t/4208
"""

import logging

import ops_openstack.core

from ops.framework import StoredState
from ops.main import main
from ops.model import (
    ActiveStatus,
    WaitingStatus
)

from charmhelpers.core import templating
from charmhelpers.contrib.openstack import templating as os_templating

from charmhelpers.contrib.openstack.ip import (
    resolve_address
)

from charmhelpers.core.hookenv import (
    relation_set
)

from ops_openstack.adapters import (
    ConfigurationAdapter,
)

from charms.sunbeam_keystone_operator.v0.identity_service import (
    IdentityServiceRequires
)

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
    config_dir = '/etc/cloudkitty/'

    port = '8889'
    release = 'yoga'

    def __init__(self, *args):
        super().__init__(*args)

        self.options = CharmCloudkittyOptions(self)

        base_url = 'http://' + self.host + ':' + self.port

        self.identity_service = IdentityServiceRequires(
            charm=self,
            relation_name="identity-service",
            service_endpoints={
                "service_name": "cloudkitty",
                "type": "rating",
                "description": "Rating as a Service",
                "internal_url": base_url,
                "public_url": base_url,
                "admin_url": base_url,
            },
            region=self.options.region
        )

        self.framework.observe(self.on.install,
                               self._on_install)
        self.framework.observe(self.on.config_changed,
                               self._on_config_changed)
        self.framework.observe(self.on.shared_db_relation_joined,
                               self._on_shared_db_relation_joined)

    @property
    def host(self) -> str:
        return '127.0.0.1'

    @property
    def port(self) -> str:
        return self.options.port

    @property
    def db_data(self):
        relation = self.model.get_relation('shared-db')
        if relation is None:
            return None
        unit = list(relation.units)[0]
        data = relation.data[unit]
        return {
            'db': {
                'user': self.options.db_user,
                'password': data.get('password'),
                'host': data.get('private-address'),
                'name': self.options.db_name,
            }
        }

    def build_context(self):
        context = {}

        db = self.db_data
        if db is not None:
            context.update(db)

        context.update({
            'options': self.options,
            'identity_service': self.identity_service
        })

        return context

    def _on_install(self, event):
        super().on_install(event)

    def _on_config_changed(self, _):
        self.options = CharmCloudkittyOptions(self)

        # if self.options.debug:
        #     import ripdb; ripdb.set_trace()

        templating.render(
            source='cloudkitty.conf',
            template_loader=os_templating.get_loader(
                'templates/',
                self.release
            ),
            target=self.config_dir + 'cloudkitty.conf',
            context=self.build_context(),
            owner=self.CONFIG_FILE_OWNER,
            group=self.CONFIG_FILE_GROUP,
            perms=0o640
        )
        self.unit.status = ActiveStatus()

    def _on_shared_db_relation_joined(self, _):
        relation_set(
            database=self.options.db_name,
            username=self.options.db_user,
            hostname=resolve_address()
        )
        self.unit.status = WaitingStatus()


if __name__ == "__main__":
    main(CharmCloudkittyCharm)
