# This file is part of ubuntu-cloud-image. See LICENSE for license information.
"""Ubuntu Cloud Image main module."""

import argparse
import logging
import sys

from . import image

CLOUDS = {
    "azure": image.Azure,
    "aws": image.AWS,
    "aws-cn": image.AWSChina,
    "aws-govcloud": image.AWSGovCloud,
    "gce": image.GCE,
    "kvm": image.KVM,
    "lxc": image.LXC,
    "maasv2": image.MAASv2,
    "maas": image.MAASv3,
}


def parse_args():  # pylint: disable=too-many-statements
    """Set up command-line arguments."""
    parser = argparse.ArgumentParser("ubuntu-cloud-image")
    parser.add_argument("--debug", action="store_true", help="additional debug output")

    subparsers = parser.add_subparsers()
    subparsers.required = True
    subparsers.dest = "command"

    aws = subparsers.add_parser("aws", help="Amazon Web Services")
    aws.add_argument("release", help="Ubuntu release codename (e.g. Bionic)")
    aws.add_argument("region", help="cloud region (e.g. us-west-2)")
    aws.add_argument("--daily", action="store_true", help="daily image")
    aws.add_argument("--minimal", action="store_true", help="minimal image")
    aws.add_argument(
        "--arch",
        default="amd64",
        choices=["amd64", "arm64"],
        help="architecture (default: amd64)",
    )
    aws.add_argument(
        "--root-store",
        default="ssd",
        choices=["ssd", "instance"],
        help="image root store",
    )

    aws_cn = subparsers.add_parser("aws-cn", help="Amazon Web Services China")
    aws_cn.add_argument("release", help="Ubuntu release codename (e.g. Bionic)")
    aws_cn.add_argument("region", help="cloud region (e.g. cn-north-1)")
    aws_cn.add_argument(
        "--arch",
        default="amd64",
        choices=["amd64", "arm64"],
        help="architecture (default: amd64)",
    )
    aws_cn.add_argument(
        "--root-store",
        default="ssd",
        choices=["ssd", "instance"],
        help="image root store",
    )

    aws_govcloud = subparsers.add_parser(
        "aws-govcloud", help="Amazon Web Services GovCloud"
    )
    aws_govcloud.add_argument("release", help="Ubuntu release codename (e.g. Bionic)")
    aws_govcloud.add_argument("region", help="cloud region (e.g. us-gov-west-1)")
    aws_govcloud.add_argument(
        "--arch",
        default="amd64",
        choices=["amd64", "arm64"],
        help="architecture (default: amd64)",
    )
    aws_govcloud.add_argument(
        "--root-store",
        default="ssd",
        choices=["ssd", "instance"],
        help="image root store",
    )

    azure = subparsers.add_parser("azure", help="Microsoft Azure")
    azure.add_argument("release", help="Ubuntu release codename (e.g. Bionic)")
    azure.add_argument("region", help="cloud region (e.g. 'West US')")
    azure.add_argument("--daily", action="store_true", help="daily image")
    azure.add_argument(
        "--arch",
        default="amd64",
        choices=["amd64"],
        help="architecture (default: amd64)",
    )

    gce = subparsers.add_parser("gce", help="Google Compute Engine")
    gce.add_argument("release", help="Ubuntu release codename (e.g. Bionic)")
    gce.add_argument("region", help="cloud region (e.g. us-west1)")
    gce.add_argument("--daily", action="store_true", help="daily image")
    gce.add_argument("--minimal", action="store_true", help="minimal image")
    gce.add_argument(
        "--arch",
        default="amd64",
        choices=["amd64"],
        help="architecture (default: amd64)",
    )

    kvm = subparsers.add_parser("kvm", help="Kernel-based Virtual Machine")
    kvm.add_argument("release", help="Ubuntu release codename (e.g. Bionic)")
    kvm.add_argument("--daily", action="store_true", help="daily image")
    kvm.add_argument("--minimal", action="store_true", help="minimal image")
    kvm.add_argument(
        "--arch",
        default="amd64",
        choices=["amd64", "arm64", "ppc64el", "s390x", "armhf", "i386"],
        help="architecture (default: amd64)",
    )

    lxc = subparsers.add_parser("lxc", help="Linux Containers")
    lxc.add_argument("release", help="Ubuntu release codename (e.g. Bionic)")
    lxc.add_argument("--daily", action="store_true", help="daily image")
    lxc.add_argument("--minimal", action="store_true", help="minimal image")
    lxc.add_argument(
        "--arch",
        default="amd64",
        choices=["amd64", "arm64", "ppc64el", "s390x", "armhf", "i386"],
        help="architecture (default: amd64)",
    )

    maasv2 = subparsers.add_parser("maasv2", help="Metal as a Service (MAAS) Version 2")
    maasv2.add_argument("release", help="Ubuntu release codename (e.g. Bionic)")
    maasv2.add_argument("--daily", action="store_true", help="daily image")
    maasv2.add_argument(
        "--arch",
        default="amd64",
        choices=["amd64", "arm64", "ppc64el", "s390x", "armhf", "i386"],
        help="architecture (default: amd64)",
    )
    maasv2.add_argument(
        "--kernel", default="generic", help="kernel flavor (default: generic)"
    )

    maasv3 = subparsers.add_parser("maas", help="Metal as a Service (MAAS) Version 3")
    maasv3.add_argument("release", help="Ubuntu release codename (e.g. Bionic)")
    maasv3.add_argument(
        "--arch",
        default="amd64",
        choices=["amd64", "arm64", "ppc64el", "s390x", "armhf", "i386"],
        help="architecture (default: amd64)",
    )
    maasv3.add_argument(
        "--kernel", default="generic", help="kernel flavor (default: generic)"
    )

    return parser.parse_args()


def setup_logging(debug):
    """Config logging mechanism."""
    logging.basicConfig(
        stream=sys.stdout,
        format="%(message)s",
        level=logging.DEBUG if debug else logging.INFO,
    )

    return logging.getLogger(__name__)


def launch():
    """Launch ubuntu-cloud-image."""
    cli = vars(parse_args())
    log = setup_logging(cli.pop("debug"))

    cloud = CLOUDS[cli.pop("command")](**cli)
    log.debug(cloud)
    cloud.search()


if __name__ == "__main__":
    sys.exit(launch())
