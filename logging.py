# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Logging

LOG_OFF = 0
LOG_ERR = 1
LOG_WRN = 2
LOG_INF = 3
LOG_DBG = 4

LogLevel = LOG_INF


def log(ll, line):
  if LogLevel >= ll:
    print(line)


def loge(line):
  log(LOG_ERR, "> [error] %s" % line)


def logw(line):
  log(LOG_WRN, "> [warn] %s" % line)


def logi(line):
  log(LOG_INF, "> [info] %s" % line)


def logd(line):
  log(LOG_DBG, "> [debug] %s" % line)

