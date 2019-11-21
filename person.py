# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Person Definitions

from global_defines import *
from utils import *

persons = {
  PersonEnum.MON_RAT:
    Monster("ugly rat", "An ugly rat scurries across the ground.", 10,
      MaterialEnum.QUILT_FUR, PERS_AGGRESSIVE,
      attacks={
        ItemEnum.WEAPON_BITE_SMALL: Attack(50),
        ItemEnum.WEAPON_CLAW_SMALL: Attack(50),
      }),
  PersonEnum.BL_KEEP_GUARD:
    NPC("gatehouse guard", "An impassive guard stares ahead.", 90,
      eq={
        ItemEnum.WEAPON_BASTARD_SWORD: ItemLink(equip=True),
        ItemEnum.SHIELD_KNIGHT_STEEL: ItemLink(equip=True),
        ItemEnum.ARMOR_CAP_QUILT: ItemLink(equip=True),
        ItemEnum.ARMOR_GAMBESON_QUILT: ItemLink(equip=True),
        ItemEnum.ARMOR_LEGGINGS_QUILT: ItemLink(equip=True),
        ItemEnum.ARMOR_HALFHELM_LEATHER_RING: ItemLink(equip=True),
        ItemEnum.ARMOR_HAUBERK_LEATHER_RING: ItemLink(equip=True),
        ItemEnum.ARMOR_LEGGINGS_LEATHER_RING: ItemLink(equip=True),
        ItemEnum.ARMOR_GAUNTLETS_LEATHER_RING: ItemLink(equip=True),
        ItemEnum.ARMOR_KNEE_BOOTS_LEATHER: ItemLink(equip=True),
      }),
}

# vim: tabstop=2 shiftwidth=2 expandtab:
