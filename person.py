# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Person Definitions

from global_defines import (DiceRoll, DamageTypeEnum, ItemEnum, AttrEnum,
                            SkillEnum, PersonEnum, ItemLink,
                            Mob, MobTalk, MobAttack,
                            MaterialEnum, AimEnum, PERS_AGGRESSIVE)

persons = {
    PersonEnum.MON_RAT:
        Mob(PersonEnum.MON_RAT, "an ugly rat",
            "An ugly rat scurries across the ground.", 35, 4, 25, AimEnum.LOW,
            PERS_AGGRESSIVE,
            MaterialEnum.FUR_LT,
            attrs={
                AttrEnum.SEX: 0,
                AttrEnum.STRENGTH: 5,
                AttrEnum.STAMINA: 4,
                AttrEnum.DEXTERITY: 4,
                AttrEnum.AGILITY: 7,
                AttrEnum.EYESIGHT: 8,
                AttrEnum.HEARING: 20,
                AttrEnum.SMELL: 15,
                AttrEnum.INTELLIGENCE: 4,
                AttrEnum.AURA: 5,
                AttrEnum.WILL: 7,
            },
            mob_attacks=[
                MobAttack("Bite", 60, 34, 0, 0, DiceRoll(1, 2),
                          DamageTypeEnum.PIERCE),
                MobAttack("Claws", 100, 24, 0, 0, DiceRoll(1, 1),
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
        Mob(PersonEnum.BL_KEEP_GUARD, "a gatehouse guard",
            "An impassive guard stares ahead.", 60, 17, 50,
            cur=DiceRoll(1, 6, 40),
            attrs={
                AttrEnum.SEX: 1,
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
            },
            talk=[
                MobTalk("",
                        text=[
                            "The guard turns to look at you. "
                            "\"Oh ... Hello Traveller. I didn't notice you "
                            "there. Welcome to Stonehaven KEEP. If you need "
                            "to know where to STAY or EAT, let me know.\""
                        ]),
                MobTalk("keep",
                        text=[
                            "\"Ah, Stonehaven Keep, the last bastion of "
                            "civilization before the wild forests off to the "
                            "northeast.\"  At this the guard glances out "
                            "across the great crevice towards the forest in "
                            "the distance.", "\"Castellan Danly oversees the "
                            "Keep with a firm but fair hand.  Mind that you "
                            "don't go causing any trouble or you'll see the "
                            "keep's prison from the inside.\"", "He turns "
                            "and points down the passage leading into the "
                            "Keep. \"Inside we have a bevy of shops and "
                            "services to choose from.  Just follow the "
                            "Southern Walk once you're inside.\""
                        ]),
                MobTalk("~",
                        text=[
                            "\"Stay safe while in the Keep.\" The guard "
                            "resumes his post."
                        ]),
            ]),
}

# vim: tabstop=2 shiftwidth=2 expandtab:
