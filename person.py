# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Person Definitions

from global_defines import (DiceRoll, DamageTypeEnum, ItemEnum, AttrEnum,
                            SkillEnum, PersonEnum, ItemLink,
                            TargetTypeEnum, ConditionCheckEnum, Condition,
                            TriggerTypeEnum, Trigger, QuestEnum,
                            Mob, MobTalk, MobAttack,
                            MaterialEnum, AimEnum,
                            PERS_AGGRESSIVE, PERS_SHOPKEEP)

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
            mob_skills={
                SkillEnum.POLEARM: 50, # 21 Based + 50 Train
            },
            eq={
                ItemEnum.WEAPON_PIKE: ItemLink(1, True),
                ItemEnum.ARMOR_COWL_QUILT: ItemLink(1, True),
                ItemEnum.ARMOR_TUNIC_QUILT: ItemLink(1, True),
                ItemEnum.ARMOR_LEGGINGS_QUILT: ItemLink(1, True),
                ItemEnum.ARMOR_HALFHELM_LEATHER_RING: ItemLink(1, True),
                ItemEnum.ARMOR_HAUBERK_LEATHER_RING: ItemLink(1, True),
                ItemEnum.ARMOR_LEGGINGS_LEATHER_RING: ItemLink(1, True),
                ItemEnum.ARMOR_GAUNTLETS_LEATHER_RING: ItemLink(1, True),
            },
            talk=[
                MobTalk("",
                        text=[
                            "The guard turns to look at you. "
                            "\"Oh ... Hello Traveller. I didn't notice you "
                            "there. Welcome to Stonehaven KEEP. If you need "
                            "to know where to STAY or EAT, let me know.\""
                        ]),
                MobTalk("",
                        condition=[
                            Condition(ConditionCheckEnum.HAS_NOT,
                                      TargetTypeEnum.PLAYER_QUEST,
                                      QuestEnum.GUARD_DELIVERY),
                        ],
                        text=[
                            "The guard then looks thoughtful for a moment.",
                            "\"About an hour ago, a cart of goods from "
                            "the east came through here.  A package fell "
                            "off while I was going through the inventory. "
                            "Alas, I didn't notice until the wagon was "
                            "gone.\"",
                            "\"Would you be interested in performing a "
                            "DELIVERY for me?\""
                        ]),
                MobTalk("keep",
                        text=[
                            "\"Ah, Stonehaven Keep, the last bastion of "
                            "civilization before the wild forests off to the "
                            "northeast.\"  At this the guard glances out "
                            "across the great crevice towards the forest in "
                            "the distance.",
                            "\"Castellan Danly oversees the keep with a firm "
                            "but fair hand.  Mind that you don't go causin' "
                            "any trouble or you'll see the keep's prison "
                            "from the inside.\"",
                            "He turns and points down the passage leading "
                            "into the keep. \"Inside we have a bevy of "
                            "shops and services to choose from.  Just "
                            "follow the Southern Walk once you're inside.\""
                        ]),
                MobTalk("delivery",
                        condition=[
                            Condition(ConditionCheckEnum.HAS_NOT,
                                      TargetTypeEnum.PLAYER_QUEST,
                                      QuestEnum.GUARD_DELIVERY),
                        ],
                        text=[
                            "A gap-toothed smile cracks the face of the "
                            "stoic guard.",
                            "\"Glad to here it! Here, take this to the "
                            "provisioner on the Southern Walk.\"",
                            "A gatehouse guard gives you a small "
                            "weathered package."
                        ],
                        triggers=[
                            Trigger(TriggerTypeEnum.ITEM_GIVE,
                                    ItemEnum.QUEST_WEATHERED_PACKAGE),
                            Trigger(TriggerTypeEnum.QUEST_GIVE,
                                    QuestEnum.GUARD_DELIVERY),
                        ]),
                MobTalk("~",
                        text=[
                            "\"Stay safe while in the Keep.\" The guard "
                            "resumes his post."
                        ]),
            ]),
    PersonEnum.BL_PROVISIONER:
        Mob(PersonEnum.BL_PROVISIONER, "the provisioner",
            "A sturdy shop keeper wanders around cleaning supplies.",
            60, 17, 50,
            flags=PERS_SHOPKEEP,
            cur=DiceRoll(1, 6, 20),
            attrs={
                AttrEnum.SEX: 1,
                AttrEnum.STRENGTH: 14,
                AttrEnum.STAMINA: 14,
                AttrEnum.DEXTERITY: 16,
                AttrEnum.AGILITY: 14,
                AttrEnum.EYESIGHT: 15,
                AttrEnum.HEARING: 12,
                AttrEnum.SMELL: 10,
                AttrEnum.INTELLIGENCE: 12,
                AttrEnum.AURA: 12,
                AttrEnum.WILL: 13,
            },
            mob_skills={
                SkillEnum.DAGGER: 45,
            },
            eq={
                ItemEnum.WEAPON_DAGGER: ItemLink(1, True),
                ItemEnum.ARMOR_GAMBESON_QUILT: ItemLink(1, True),
                ItemEnum.ARMOR_CAP_LEATHER: ItemLink(1, True),
                ItemEnum.ARMOR_SURCOAT_LEATHER: ItemLink(1, True),
                ItemEnum.ARMOR_SHOES_LEATHER: ItemLink(1, True),
            },
            talk=[
                MobTalk("",
                        text=[
                            "\"Hello! Welcome to my humble shop.\""
                        ]),
                MobTalk("",
                        condition=[
                            Condition(ConditionCheckEnum.HAS,
                                      TargetTypeEnum.PLAYER_QUEST,
                                      QuestEnum.GUARD_DELIVERY),
                        ],
                        text=[
                            "\"Ah! I see you have a package for me.  I "
                            "appreciate your help brining it to the shop.\"",
                            "You give the weathered package to the shop "
                            "keeper.",
                            "He gently places it on a pile of goods and "
                            "takes a moment to rummage around behind the "
                            "counter.  After a moment he steps up to you "
                            "and presses a few coins into your hand."
                        ],
                        triggers=[
                            Trigger(TriggerTypeEnum.ITEM_TAKE,
                                    ItemEnum.QUEST_WEATHERED_PACKAGE),
                            Trigger(TriggerTypeEnum.CURRENCY_GIVE, 5),
                            Trigger(TriggerTypeEnum.QUEST_COMPLETE,
                                    QuestEnum.GUARD_DELIVERY),
                        ]),
                MobTalk("~",
                        text=[
                            "\"Fare thee well.\""
                        ]),
            ]),
}

# vim: tabstop=2 shiftwidth=2 expandtab:
