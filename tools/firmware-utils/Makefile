#
# Copyright (C) 2006-2020 OpenWrt.org
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#
include $(TOPDIR)/rules.mk

PKG_NAME:=firmware-utils
PKG_RELEASE:=1

PKG_SOURCE_PROTO:=git
PKG_SOURCE_URL=https://github.com/antoniovazquezblanco/firmware-utils.git
PKG_SOURCE_DATE:=2024-01-24
PKG_SOURCE_VERSION:=8ab532096efc9fdd9d16df82a8f2ca291d410065
PKG_MIRROR_HASH:=2cfd36e749b51d539cffe22c77a4c3ccd3bac2eca482affe23e1cab539e8bd16

include $(INCLUDE_DIR)/host-build.mk
include $(INCLUDE_DIR)/cmake.mk

$(eval $(call HostBuild))
