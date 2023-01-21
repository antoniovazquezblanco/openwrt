#
# RT63365E Profiles
#

define Device/asus_dsl-n14u
  DEVICE_VENDOR := Asus
  DEVICE_MODEL := DSL-N14U
  SUPPORTED_DEVICES += dsl-n14u
  SOC := rt63365e
  LOADER_TYPE := bin
  LZMA_TEXT_START := 0x80020000
  KERNEL := kernel-bin | lzma | check-size 6160384 | loader-kernel | lzma-no-dict | check-size 1572608
  IMAGES := DSL-N14U.trx
  IMAGE/DSL-N14U.trx := append-kernel | append-rootfs | tctrx
endef
TARGET_DEVICES += asus_dsl-n14u

define Build/tctrx
  mv $@ "`dirname $@`/tclinux"
	$(STAGING_DIR_HOST)/bin/tctrx -k `stat -c%s "$(IMAGE_KERNEL)"` -r `stat -c%s "$(IMAGE_ROOTFS)"` -f "`dirname $@`/tclinux" -o "`dirname $@`/tclinux.bin"
  mv "`dirname $@`/tclinux.bin" $@
endef
