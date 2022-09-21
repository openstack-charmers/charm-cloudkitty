# Cloudkitty

Cloudkitty charm - Openstack Rating as a Service

## Description

This charm provides a way to deploy Cloudkitty - Openstack Rating as a Service module - in Openstack

## Usage

Deploy cloudkitty charm along with keystone, mysql and gnocchi

```
juju deploy cloudkitty --channel edge
juju deploy keystone
juju deploy --channel edge mysql
juju deploy gnocchi
```

## Relations

Add cloudkitty charm required relations
```
juju relate cloudkitty keystone
juju relate cloudkitty mysql
juju relate cloudkitty gnocchi
```

## Actions

Action `restart-services`
```
juju run-action --wait restart-services cloudkitty/leader
```

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