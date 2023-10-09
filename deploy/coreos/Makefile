SHELL := /bin/bash
BUTANE_BIN := $(shell which butane)
CONFIG :=
FILES_DIR := ./files
CONFIG_DIR := ./config
FCOS_INSTALLER_BIN := $(shell which coreos-installer)
FCOS_ARCH := x86_64
FCOS_STREAM := stable
FCOS_DEV :=

.PHONY: butane
butane:
	${BUTANE_BIN} \
		-d ${FILES_DIR} \
		-o ${CONFIG_DIR}/${CONFIG}/config.json \
		-p ${CONFIG_DIR}/${CONFIG}/config.yml


.PHONY: install
install: install
	${FCOS_INSTALLER_BIN} \
	 	install \
		-a ${FCOS_ARCH} \
		-s ${FCOS_STREAM} \
		-i ${CONFIG_DIR}/${CONFIG}/config.json \
		${FCOS_DEV}
