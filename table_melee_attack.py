# Copyright (c) 2019-2020 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Melee Hit Table

from enum import IntEnum

from global_defines import (Roll)


class Action(IntEnum):
  IGNORE = 0
  MELEE = 1
  BLOCK = 2
  DODGE = 3
  MISSILE = 5
  GRAPPLE = 6
  ESOTERIC = 7
  FLEE = 8


class ResultEnum(IntEnum):
  MISS = 0
  BLOCK = 1
  FUMBLE = 2
  STUMBLE = 3
  TADV = 4
  DMG = 5
  DODGE = 6


T_ATK = 1 << 0
T_DEF = 1 << 1
T_BOTH = T_ATK | T_DEF


class Result:
  def __init__(self, targets, result, level=0):
    self.TargetFlag = targets
    self.Result = result
    self.Level = level

  def __str__(self):
    ret = "T:"
    if T_ATK & self.TargetFlag > 0:
      ret += "T_ATK"
    if T_DEF & self.TargetFlag > 0:
      if len(ret) > 2:
        ret += "|"
      ret += "T_DEF"
    ret += " %s/%d" % (self.Result, self.Level)
    return ret


resolve_melee = {
    # ATTACKER
    Roll.CF: {
        # DEFENDER
        Action.BLOCK: {
            Roll.CF: Result(T_BOTH, ResultEnum.FUMBLE, 3),
            Roll.MF: Result(T_ATK, ResultEnum.FUMBLE, 3),
            Roll.MS: Result(T_DEF, ResultEnum.TADV),
            Roll.CS: Result(T_DEF, ResultEnum.TADV),
        },
        Action.DODGE: {
            Roll.CF: Result(T_BOTH, ResultEnum.STUMBLE, 3),
            Roll.MF: Result(T_ATK, ResultEnum.STUMBLE, 3),
            Roll.MS: Result(T_DEF, ResultEnum.TADV),
            Roll.CS: Result(T_DEF, ResultEnum.TADV),
        },
        Action.IGNORE: {
            Roll.CF: Result(T_DEF, ResultEnum.TADV),
            Roll.MF: Result(T_DEF, ResultEnum.TADV),
            Roll.MS: Result(T_DEF, ResultEnum.TADV),
            Roll.CS: Result(T_DEF, ResultEnum.TADV),
        },
    },
    Roll.MF: {
        Action.BLOCK: {
            Roll.CF: Result(T_DEF, ResultEnum.FUMBLE, 3),
            Roll.MF: Result(T_BOTH, ResultEnum.MISS),
            Roll.MS: Result(T_BOTH, ResultEnum.MISS),
            Roll.CS: Result(T_DEF, ResultEnum.TADV),
        },
        Action.DODGE: {
            Roll.CF: Result(T_DEF, ResultEnum.STUMBLE, 3),
            Roll.MF: Result(T_BOTH, ResultEnum.MISS),
            Roll.MS: Result(T_BOTH, ResultEnum.DODGE),
            Roll.CS: Result(T_DEF, ResultEnum.TADV),
        },
        Action.IGNORE: {
            Roll.CF: Result(T_ATK, ResultEnum.DMG, 1),
            Roll.MF: Result(T_ATK, ResultEnum.DMG, 1),
            Roll.MS: Result(T_ATK, ResultEnum.DMG, 1),
            Roll.CS: Result(T_ATK, ResultEnum.DMG, 1),
        },
    },
    Roll.MS: {
        Action.BLOCK: {
            Roll.CF: Result(T_ATK, ResultEnum.DMG, 2),
            Roll.MF: Result(T_ATK, ResultEnum.DMG, 1),
            Roll.MS: Result(T_BOTH, ResultEnum.BLOCK),
            Roll.CS: Result(T_BOTH, ResultEnum.MISS),
        },
        Action.DODGE: {
            Roll.CF: Result(T_ATK, ResultEnum.DMG, 2),
            Roll.MF: Result(T_ATK, ResultEnum.DMG, 1),
            Roll.MS: Result(T_BOTH, ResultEnum.DODGE),
            Roll.CS: Result(T_BOTH, ResultEnum.DODGE),
        },
        Action.IGNORE: {
            Roll.CF: Result(T_ATK, ResultEnum.DMG, 3),
            Roll.MF: Result(T_ATK, ResultEnum.DMG, 3),
            Roll.MS: Result(T_ATK, ResultEnum.DMG, 3),
            Roll.CS: Result(T_ATK, ResultEnum.DMG, 3),
        },
    },
    Roll.CS: {
        Action.BLOCK: {
            Roll.CF: Result(T_ATK, ResultEnum.DMG, 3),
            Roll.MF: Result(T_ATK, ResultEnum.DMG, 2),
            Roll.MS: Result(T_ATK, ResultEnum.DMG, 1),
            Roll.CS: Result(T_BOTH, ResultEnum.BLOCK),
        },
        Action.DODGE: {
            Roll.CF: Result(T_ATK, ResultEnum.DMG, 3),
            Roll.MF: Result(T_ATK, ResultEnum.DMG, 2),
            Roll.MS: Result(T_ATK, ResultEnum.DMG, 1),
            Roll.CS: Result(T_BOTH, ResultEnum.DODGE),
        },
        Action.IGNORE: {
            Roll.CF: Result(T_ATK, ResultEnum.DMG, 4),
            Roll.MF: Result(T_ATK, ResultEnum.DMG, 4),
            Roll.MS: Result(T_ATK, ResultEnum.DMG, 4),
            Roll.CS: Result(T_ATK, ResultEnum.DMG, 4),
        },
    },
}

# vim: tabstop=2 shiftwidth=2 expandtab:
