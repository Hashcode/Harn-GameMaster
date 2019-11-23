# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Person Definitions

from global_defines import (DiceRoll, DamageTypeEnum, ItemEnum, AttrEnum,
                            SkillEnum, PersonEnum, ItemLink, Mob, MobAttack,
                            MaterialEnum, PERS_AGGRESSIVE)

persons = {
    PersonEnum.MON_RAT:
        Mob("ugly rat", "An ugly rat scurries across the ground.", 45, 6, 80,
            PERS_AGGRESSIVE,
            MaterialEnum.FUR_LT,
            attrs={
                AttrEnum.STRENGTH: 5,
                AttrEnum.STAMINA: 8,
                AttrEnum.DEXTERITY: 4,
                AttrEnum.AGILITY: 16,
                AttrEnum.EYESIGHT: 12,
                AttrEnum.HEARING: 20,
                AttrEnum.SMELL: 15,
                AttrEnum.INTELLIGENCE: 4,
                AttrEnum.AURA: 5,
                AttrEnum.WILL: 8,
            },
            mob_attacks=[
                MobAttack("Bite", 60, 65, DiceRoll(1, 2),
                          DamageTypeEnum.PIERCE),
                MobAttack("Claws", 100, 50, DiceRoll(1, 1),
                          DamageTypeEnum.EDGE),
            ],
            mob_skills={
                SkillEnum.AWARENESS: 0,
                SkillEnum.STEALTH: 0,
            },
            loot={
                ItemEnum.MISC_RAT_FUR: 75,
            }),
    PersonEnum.BL_KEEP_GUARD:
        Mob("gatehouse guard", "An impassive guard stares ahead.", 60, 17, 50,
            cur=DiceRoll(1, 6, 40),
            attrs={
                AttrEnum.STRENGTH: 14,
                AttrEnum.STAMINA: 14,
                AttrEnum.DEXTERITY: 12,
                AttrEnum.AGILITY: 10,
                AttrEnum.EYESIGHT: 14,
                AttrEnum.HEARING: 12,
                AttrEnum.SMELL: 10,
                AttrEnum.INTELLIGENCE: 12,
                AttrEnum.AURA: 12,
                AttrEnum.WILL: 13,
            },
            mob_attacks=[
                MobAttack("Bastard Sword", 80, 65, DiceRoll(1, 6, 2),
                          DamageTypeEnum.EDGE),
                MobAttack("Kite Shield", 100, 50, DiceRoll(1, 1),
                          DamageTypeEnum.BLUNT),
            ],
            eq={
                ItemEnum.WEAPON_BASTARD_SWORD: ItemLink(1, True),
                ItemEnum.SHIELD_KITE_STEEL: ItemLink(1, True),
                ItemEnum.ARMOR_COWL_QUILT: ItemLink(1, True),
                ItemEnum.ARMOR_TUNIC_QUILT: ItemLink(1, True),
                ItemEnum.ARMOR_LEGGINGS_QUILT: ItemLink(1, True),
                ItemEnum.ARMOR_HALFHELM_LEATHER_RING: ItemLink(1, True),
                ItemEnum.ARMOR_HAUBERK_LEATHER_RING: ItemLink(1, True),
                ItemEnum.ARMOR_LEGGINGS_LEATHER_RING: ItemLink(1, True),
                ItemEnum.ARMOR_GAUNTLETS_LEATHER_RING: ItemLink(1, True),
            },
            loot={
                ItemEnum.MISC_STONE: 50,
            }),
}

# vim: tabstop=2 shiftwidth=2 expandtab:
