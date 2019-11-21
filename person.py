# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Person Definitions

from global_defines import *
from utils import *

persons = {
  PersonEnum.RAT:
    Monster("ugly rat", 10, MaterialEnum.QUILT_FUR, PERS_AGGRESSIVE,
      attacks={
        ItemEnum.WEAPON_BITE_SMALL: Attack(50),
        ItemEnum.WEAPON_CLAW_SMALL: Attack(50),
      }),
}

# vim: tabstop=2 shiftwidth=2 expandtab:
