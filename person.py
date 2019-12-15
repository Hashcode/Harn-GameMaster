# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Person Definitions

from global_defines import (DiceRoll, DamageTypeEnum, ItemEnum, AttrEnum,
                            SkillEnum, PersonEnum, ItemLink, Periodic,
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
            "A mild-mannered guard keeps watch over the gatehouse.",
            60, 17, 50,
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
                SkillEnum.POLEARM: 50,  # 21 Based + 50 Train
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
                MobTalk("~on_enter~",
                        condition=[
                            Condition(ConditionCheckEnum.HAS_NOT,
                                      TargetTypeEnum.PLAYER_QUEST,
                                      QuestEnum.GUARD_INTRO),
                        ],
                        text=[
                            "The guard glances in your direction. "
                            "\"Come TALK to me Traveller, when you get "
                            "a moment.\""
                        ]),
                MobTalk("~on_exit~",
                        condition=[
                            Condition(ConditionCheckEnum.HAS_NOT,
                                      TargetTypeEnum.PLAYER_QUEST,
                                      QuestEnum.GUARD_INTRO),
                        ],
                        text=[
                            "The guard moves to block your way. "
                            "\"I meant you need to TALK to me, when you get "
                            "a chance.\"  He taps his foot impatiently,"
                        ],
                        triggers=[
                            Trigger(TriggerTypeEnum.DENY),
                        ]),
                MobTalk("",
                        text=[
                            "The guard turns to look at you. "
                            "\"Hello Traveller. Welcome to Stonehaven KEEP. "
                            "If you need to know where to STAY or EAT, let "
                            "me know.\""
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
                        ],
                        triggers=[
                            Trigger(TriggerTypeEnum.QUEST_COMPLETE,
                                    QuestEnum.GUARD_INTRO),
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
    PersonEnum.BL_KEEP_SENTRY:
        Mob(PersonEnum.BL_KEEP_SENTRY, "a common sentry",
            "A common sentry stands watch.",
            50, 14, 40,
            cur=DiceRoll(1, 6, 10),
            attrs={
                AttrEnum.SEX: 1,
                AttrEnum.STRENGTH: 12,
                AttrEnum.STAMINA: 12,
                AttrEnum.DEXTERITY: 12,
                AttrEnum.AGILITY: 10,
                AttrEnum.EYESIGHT: 12,
                AttrEnum.HEARING: 11,
                AttrEnum.SMELL: 9,
                AttrEnum.INTELLIGENCE: 10,
                AttrEnum.AURA: 10,
                AttrEnum.WILL: 11,
            },
            mob_skills={
                SkillEnum.POLEARM: 40,
            },
            eq={
                ItemEnum.WEAPON_POLEAXE: ItemLink(1, True),
                ItemEnum.ARMOR_COWL_QUILT: ItemLink(1, True),
                ItemEnum.ARMOR_TUNIC_QUILT: ItemLink(1, True),
                ItemEnum.ARMOR_LEGGINGS_QUILT: ItemLink(1, True),
                ItemEnum.ARMOR_HALFHELM_KURBUL: ItemLink(1, True),
                ItemEnum.ARMOR_BYRNIE_LEATHER_RING: ItemLink(1, True),
                ItemEnum.ARMOR_LEGGINGS_LEATHER: ItemLink(1, True),
                ItemEnum.ARMOR_GAUNTLETS_LEATHER_RING: ItemLink(1, True),
            },
            periodics=[
                Periodic(
                    [
                        Condition(ConditionCheckEnum.LESS_THAN,
                                  TargetTypeEnum.PERCENT_CHANCE,
                                  value=15),
                    ],
                    [
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE,
                                "A sentry shuffles his feet looking bored."),
                    ], 300),
            ]),
    PersonEnum.BL_KEEP_CORPORAL_WATCH:
        Mob(PersonEnum.BL_KEEP_CORPORAL_WATCH, "the corporal of the watch",
            "The corporal of the watch stands here grumbling to his scribe.",
            65, 18, 50,
            cur=DiceRoll(1, 6, 60),
            attrs={
                AttrEnum.SEX: 1,
                AttrEnum.STRENGTH: 15,
                AttrEnum.STAMINA: 15,
                AttrEnum.DEXTERITY: 13,
                AttrEnum.AGILITY: 12,
                AttrEnum.EYESIGHT: 12,
                AttrEnum.HEARING: 13,
                AttrEnum.SMELL: 10,
                AttrEnum.INTELLIGENCE: 13,
                AttrEnum.AURA: 11,
                AttrEnum.WILL: 12,
            },
            mob_skills={
                SkillEnum.POLEARM: 50,
            },
            eq={
                ItemEnum.WEAPON_BASTARD_SWORD: ItemLink(1, True),
                ItemEnum.SHIELD_ROUND_BANDED: ItemLink(1, True),
                ItemEnum.ARMOR_COWL_QUILT: ItemLink(1, True),
                ItemEnum.ARMOR_TUNIC_QUILT: ItemLink(1, True),
                ItemEnum.ARMOR_LEGGINGS_QUILT: ItemLink(1, True),
                ItemEnum.ARMOR_COWL_MAIL: ItemLink(1, True),
                ItemEnum.ARMOR_BYRNIE_MAIL: ItemLink(1, True),
                ItemEnum.ARMOR_LEGGINGS_MAIL: ItemLink(1, True),
                ItemEnum.ARMOR_MITTENS_MAIL: ItemLink(1, True),
            },
            periodics=[
                Periodic(
                    [
                        Condition(ConditionCheckEnum.HAS,
                                  TargetTypeEnum.MOB_IN_ROOM,
                                  PersonEnum.BL_KEEP_YARD_SCRIBE),
                        Condition(ConditionCheckEnum.LESS_THAN,
                                  TargetTypeEnum.PERCENT_CHANCE,
                                  value=15),
                    ],
                    [
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE,
                                "The corporal of the watch glances at the "
                                "scribe and grumbles under his breath."),
                    ], 300),
            ]),
    PersonEnum.BL_KEEP_YARD_SCRIBE:
        Mob(PersonEnum.BL_KEEP_YARD_SCRIBE, "a young scribe",
            "A young scribe is taking notes as traffic moves in and out of "
            "the keep.",
            40, 12, 35,
            cur=DiceRoll(1, 6, 60),
            attrs={
                AttrEnum.SEX: 1,
                AttrEnum.STRENGTH: 10,
                AttrEnum.STAMINA: 11,
                AttrEnum.DEXTERITY: 14,
                AttrEnum.AGILITY: 11,
                AttrEnum.EYESIGHT: 15,
                AttrEnum.HEARING: 14,
                AttrEnum.SMELL: 10,
                AttrEnum.INTELLIGENCE: 13,
                AttrEnum.AURA: 10,
                AttrEnum.WILL: 11,
            },
            mob_skills={
                SkillEnum.UNARMED: 20,
            },
            eq={
                ItemEnum.ARMOR_ROBE_CLOTH: ItemLink(1, True),
            },
            periodics=[
                Periodic(
                    [
                        Condition(ConditionCheckEnum.LESS_THAN,
                                  TargetTypeEnum.PERCENT_CHANCE,
                                  value=15),
                    ],
                    [
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE,
                                "The scribe scribbles something in his "
                                "notes."),
                    ], 300),
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
            sell_items={
                ItemEnum.WEAPON_KNIFE: ItemLink(1),
                ItemEnum.WEAPON_SICKLE: ItemLink(1),
                ItemEnum.WEAPON_STAFF: ItemLink(1),
            },
            talk=[
                MobTalk("",
                        text=[
                            "\"Hello! Welcome to my humble SHOP.  Feel free "
                            "to look around for something to BUY or you can "
                            "SELL various items to me.\""
                        ]),
                MobTalk("",
                        condition=[
                            Condition(ConditionCheckEnum.HAS_NOT,
                                      TargetTypeEnum.PLAYER_QUEST_COMPLETE,
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
                MobTalk("shop",
                        text=[
                            "\"Ah a customer! Are you here to BUY or "
                            "SELL?\"",
                        ]),
                MobTalk("buy",
                        text=[
                            "\"Excellent!  Here's what I have:\"",
                        ],
                        triggers=[
                            Trigger(TriggerTypeEnum.ITEM_BUY),
                        ]),
                MobTalk("sell",
                        text=[
                            "\"Let's see if you have anything I need ...\"",
                        ],
                        triggers=[
                            Trigger(TriggerTypeEnum.ITEM_SELL),
                        ]),
                MobTalk("~",
                        text=[
                            "\"Fare thee well.\""
                        ]),
            ]),
}

# vim: tabstop=2 shiftwidth=2 expandtab:
