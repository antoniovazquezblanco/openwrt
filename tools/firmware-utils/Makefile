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
PKG_SOURCE_DATE:=2023-06-05
PKG_SOURCE_VERSION:=a2e9dd6d5af5a36d915325a1505a87956cd96ab5
PKG_MIRROR_HASH:=2cfd36e749b51d539cffe22c77a4c3ccd3bac2eca482affe23e1cab539e8bd16

include $(INCLUDE_DIR)/host-build.mk
include $(INCLUDE_DIR)/cmake.mk

$(eval $(call HostBuild))
