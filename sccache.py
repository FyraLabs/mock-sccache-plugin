# -*- coding: utf-8 -*-
# vim:expandtab:autoindent:tabstop=4:shiftwidth=4:filetype=python:textwidth=0:
# License: GPL2 or later see COPYING
# Written by Michael Brown
# Copyright (C) 2007 Michael E Brown <mebrown@michaels-house.net>

# python library imports

# our imports
from mockbuild.mounts import BindMountPoint
from mockbuild.trace_decorator import getLog, traceLog
from mockbuild import file_util

requires_api_version = "1.1"
run_in_bootstrap = False

# plugin entry point
@traceLog()
def init(plugins, conf, buildroot):
    SCCache(plugins, conf, buildroot)


class SCCache(object):
    """enables sccache in buildroot/rpmbuild"""
    # pylint: disable=too-few-public-methods
    @traceLog()
    def __init__(self, plugins, conf, buildroot):
        self.buildroot = buildroot
        self.config = buildroot.config
        self.state = buildroot.state
        self.sccache_opts = conf
        tmpdict = self.sccache_opts.copy()
        tmpdict.update({'chrootuid': self.buildroot.chrootuid})
        self.sccachePath = self.sccache_opts['dir'] % tmpdict
        buildroot.preexisting_deps.append("sccache")
        plugins.add_hook("prebuild", self._sccachePreBuildHook)
        plugins.add_hook("preinit", self._sccachePreInitHook)
        buildroot.mounts.add(
            BindMountPoint(srcpath=self.sccachePath, bindpath=buildroot.make_chroot_path("/var/tmp/sccache")))

    # =============
    # 'Private' API
    # =============
    # start the sccache server before build
    @traceLog()
    def _sccachePreBuildHook(self):
        self.buildroot.doChroot(["sccache", "--start-server"], shell=False)

    # set up the sccache dir.
    # we also set a few variables used by sccache to find the shared cache.
    @traceLog()
    def _sccachePreInitHook(self):
        getLog().info("enabled sccache")
        envupd = {"SCCACHE_DIR": "/var/tmp/sccache",
            "SCCACHE_CACHE_SIZE": self.sccache_opts['max_cache_size'],
            "RUSTC_WRAPPER": "/usr/bin/sccache"}
        self.buildroot.env.update(envupd)

        file_util.mkdirIfAbsent(self.buildroot.make_chroot_path('/var/tmp/sccache'))
        file_util.mkdirIfAbsent(self.sccachePath)
        self.buildroot.uid_manager.changeOwner(self.sccachePath, recursive=True)
