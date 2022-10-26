#
# RT63365E Profiles
#

define Device/asus_dsl-n14u
  DEVICE_VENDOR := Asus
  DEVICE_MODEL := DSL-N14U
  SUPPORTED_DEVICES += dsl-n14u
  SOC := rt63365e
  IMAGES := trx
  IMAGE/trx := trx
  IMAGE_SIZE := 16000k
endef
TARGET_DEVICES += asus_dsl-n14u
