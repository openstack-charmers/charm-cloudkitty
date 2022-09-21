# Cloudkitty

Cloudkitty charm - Openstack Rating as a Service

## Description

This charm provides a way to deploy Cloudkitty - Openstack Rating as a Service module - in Openstack

**What is CloudKitty ?**

CloudKitty is a generic solution for the chargeback and rating of a cloud. Provides a metric-based rating for cloud administrators allowing them to create rating rules to the collected data.


**CloudKitty usage**

With Cloudkitty, it is possible to:

* Collect metrics from OpenStack (through Gnocchi).
* Apply rating rules to the previous metrics.
* Retrieve the rated information, grouped by scope and/or by metric type.

However, it is not possible to:

* Limit resources in other OpenStack services.
* Add taxes, convert between currencies, etc...

CloudKitty associates a price to a metric for a given period, the price is mapped according to end-user needs.

## Usage

Deploy cloudkitty charm

```
juju deploy cloudkitty --channel edge
```

Or in a bundle
```
applications:
  cloudkitty:
    charm: ch:cloudkitty
    channel: edge
    num_units: 1
    series: jammy
```

## Relations

Cloudkitty charm supports the following relations.

MySQL relation - provides database storage for the cloudkitty service.

```
juju deploy mysql --channel edge
juju relate cloudkitty mysql
```

Keystone relation - provides identity management.

```
juju deploy keystone
juju relate cloudkitty keystone
```

Gnocchi relation - provides metrics collector service.
```
juju deploy gnocchi
juju relate cloudkitty gnocchi
```

RabbitMQ relation - provides messages queue service.
```
juju deploy rabbitmq-server
juju relate cloudkitty rabbitmq-server
```

## Actions
This section lists Juju [actions](https://jaas.ai/docs/actions) supported by the charm. Actions allow specific operations to be performed on a per-unit basis.

* `restart-services`\
restarts `cloudkitty-{api,processor}` services in the unit.

    ```
    juju run-action --wait cloudkitty/leader restart-services
    ```

## TO-DO

This charm is under development not yet stable, the following list provides pending features

* TLS support using [[TLS interface]](https://opendev.org/openstack/charm-ops-interface-tls-certificates/src/branch/master/interface_tls_certificates/ca_client.py)

* InfluxDB relation required for storage v2 [[link]](https://docs.openstack.org/cloudkitty/latest/admin/configuration/storage.html#influxdb-v2)

* Cloudkitty dashboard relation


## TO-DO

* TLS with vault
*
*

## Contributing

Please see the [Juju SDK docs](https://juju.is/docs/sdk) for guidelines
on enhancements to this charm following best practice guidelines, and
`CONTRIBUTING.md` for developer guidance.


# Bugs

Please report bugs on [Launchpad][lp-bugs-charm-cloudkitty].

For general charm questions refer to the [OpenStack Charm Guide][cg].

<!-- LINKS -->
[cg]: https://docs.openstack.org/charm-guide
[lp-bugs-charm-cloudkitty]: https://bugs.launchpad.net/charm-cloudkitty/+filebug