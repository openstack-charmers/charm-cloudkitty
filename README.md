# Cloudkitty

Cloudkitty charm - Openstack Rating as a Service

## Description

This charm provides a way to deploy Cloudkitty Rating as a Service (RaaS) module for Openstack

Cloudkitty is a service that provides



## Usage

Deploy cloudkitty charm along with keystone, mysql and gnocchi

```
juju deploy cloudkitty --channel edge

juju deploy keystone
juju relate cloudkitty keystone

juju deploy --channel edge mysql
juju relate cloudkitty mysql

juju deploy gnocchi
juju relate cloudkitty gnocchi

juju deploy rabbitmq-server
juju relate cloudkitty rabbitmq-server
```

## Relations



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