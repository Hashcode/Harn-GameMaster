# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Person Definitions

from console import (ANSI)
from global_defines import (DiceRoll, DamageTypeEnum, ItemEnum, AttrEnum,
                            SkillEnum, PersonEnum, ItemLink, Periodic,
                            TargetTypeEnum, ConditionCheckEnum, Condition,
                            TriggerTypeEnum, Trigger, QuestEnum,
                            PersonFlag, Mob, MobTalk, MobAttack,
                            MaterialEnum, AimEnum, DoorEnum, RoomEnum,
                            DirectionEnum)

persons = {
    PersonEnum.MON_RAT:
        Mob(PersonEnum.MON_RAT, "an ugly rat",
            "An ugly rat scurries across the ground.", 35, 4, 25, AimEnum.LOW, PersonFlag.AGGRESSIVE, MaterialEnum.FUR_LT,
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
                MobAttack("Bite", 60, 34, 0, 0, DiceRoll(1, 2), DamageTypeEnum.PIERCE),
                MobAttack("Claws", 100, 24, 0, 0, DiceRoll(1, 1), DamageTypeEnum.EDGE),
            ],
            mob_skills={
                SkillEnum.AWARENESS: 0,
                SkillEnum.STEALTH: 0,
            },
            loot={
                ItemEnum.MISC_RAT_FUR: 100,
            }),
    PersonEnum.MON_RAT_LARGE:
        Mob(PersonEnum.MON_RAT_LARGE, "a large nasty-looking rat",
            "A large nasty-looking rat scrambles across the ground.", 40, 4, 30,
            AimEnum.LOW, PersonFlag.AGGRESSIVE, MaterialEnum.FUR_LT,
            attrs={
                AttrEnum.SEX: 0,
                AttrEnum.STRENGTH: 7,
                AttrEnum.STAMINA: 4,
                AttrEnum.DEXTERITY: 5,
                AttrEnum.AGILITY: 7,
                AttrEnum.EYESIGHT: 8,
                AttrEnum.HEARING: 20,
                AttrEnum.SMELL: 15,
                AttrEnum.INTELLIGENCE: 5,
                AttrEnum.AURA: 6,
                AttrEnum.WILL: 8,
            },
            mob_attacks=[
                MobAttack("Bite", 60, 37, 0, 0, DiceRoll(1, 3), DamageTypeEnum.PIERCE),
                MobAttack("Claws", 100, 27, 0, 0, DiceRoll(1, 2), DamageTypeEnum.EDGE),
            ],
            mob_skills={
                SkillEnum.AWARENESS: 10,
                SkillEnum.STEALTH: 0,
            },
            loot={
                ItemEnum.ARMOR_STAINED_QUILT_COWL: 50,
                ItemEnum.MISC_RAT_FUR: 100,
            }),
    PersonEnum.MON_RAT_GUARD:
        Mob(PersonEnum.MON_RAT_GUARD, "a rat guardian",
            "A rat guardian glares around the room.", 45, 5, 35,
            AimEnum.LOW, PersonFlag.AGGRESSIVE, MaterialEnum.FUR_LT,
            cur=DiceRoll(1, 6, 10),
            attrs={
                AttrEnum.SEX: 0,
                AttrEnum.STRENGTH: 8,
                AttrEnum.STAMINA: 5,
                AttrEnum.DEXTERITY: 7,
                AttrEnum.AGILITY: 8,
                AttrEnum.EYESIGHT: 8,
                AttrEnum.HEARING: 20,
                AttrEnum.SMELL: 15,
                AttrEnum.INTELLIGENCE: 5,
                AttrEnum.AURA: 6,
                AttrEnum.WILL: 9,
            },
            mob_attacks=[
                MobAttack("Bite", 60, 41, 0, 0, DiceRoll(1, 4), DamageTypeEnum.PIERCE),
                MobAttack("Claws", 100, 31, 0, 0, DiceRoll(1, 3), DamageTypeEnum.EDGE),
            ],
            mob_skills={
                SkillEnum.AWARENESS: 10,
                SkillEnum.STEALTH: 0,
            },
            loot={
                ItemEnum.ARMOR_STAINED_QUILT_LEGGINGS: 50,
                ItemEnum.MISC_RAT_FUR: 100,
            }),
    PersonEnum.MON_RAT_NOBLE:
        Mob(PersonEnum.MON_RAT_NOBLE, "a rat noble",
            "A rat noble calmly nibbles some cheese.", 45, 5, 35,
            AimEnum.LOW, PersonFlag.AGGRESSIVE, MaterialEnum.FUR_LT,
            cur=DiceRoll(1, 6, 40),
            attrs={
                AttrEnum.SEX: 0,
                AttrEnum.STRENGTH: 8,
                AttrEnum.STAMINA: 5,
                AttrEnum.DEXTERITY: 8,
                AttrEnum.AGILITY: 8,
                AttrEnum.EYESIGHT: 8,
                AttrEnum.HEARING: 20,
                AttrEnum.SMELL: 15,
                AttrEnum.INTELLIGENCE: 5,
                AttrEnum.AURA: 6,
                AttrEnum.WILL: 9,
            },
            mob_skills={
                SkillEnum.AWARENESS: 10,
                SkillEnum.STEALTH: 0,
            },
            mob_attacks=[
                MobAttack("Bite", 60, 45, 0, 0, DiceRoll(1, 4), DamageTypeEnum.PIERCE),
                MobAttack("Claws", 100, 35, 0, 0, DiceRoll(1, 3), DamageTypeEnum.EDGE),
            ],
            loot={
                ItemEnum.RING_ATTACK_SILVER: 100,
                ItemEnum.MISC_RAT_FUR: 100,
            }),
    PersonEnum.BL_KEEP_GUARD:
        Mob(PersonEnum.BL_KEEP_GUARD, "a gatehouse guard",
            "A gatehouse guard keeps watch over his post.", 60, 17, 50,
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
                        [
                            Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.PLAYER_QUEST, QuestEnum.GUARD_INTRO),
                        ],
                        [
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    [
                                        "@@NAME_CAP@@ in your direction. \"Come TALK to me, Traveller, when you get "
                                        "a moment.\"",
                                        "%s[TIP: Sometimes keywords will be presented in all capitals such as 'TALK'. "
                                        "You can type these keywords to start interactions or talk about different subjects. "
                                        "As the adventure progresses this will happen less and less.]"
                                        "%s" % (ANSI.TEXT_COLOR_CYAN, ANSI.TEXT_NORMAL)
                                    ]),
                        ]),
                MobTalk("~on_exit~",
                        [
                            Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.PLAYER_QUEST, QuestEnum.GUARD_INTRO),
                        ],
                        [
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    [
                                        "@@NAME_CAP@@ moves to block your way. \"I meant you need to TALK to me before entering.\" "
                                        "He taps his foot impatiently.",
                                    ]),
                            Trigger(TriggerTypeEnum.DENY),
                        ]),
                MobTalk("",
                        triggers=[
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    [
                                        "@@NAME_CAP@@ turns to look at you.",
                                        "\"Hello Traveller. Welcome to Stonehaven KEEP. Times are rough, so you may need to forgive "
                                        "the grim faces of our inhabitants. We've seen a recent surge in attacks from the wild men "
                                        "of the forest.\"",
                                        "\"You look rather new to the area, so if you want more INFORMATION let me know.\"",
                                    ]),
                        ]),
                MobTalk("",
                        [
                            Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.PLAYER_QUEST, QuestEnum.GUARD_DELIVERY),
                        ],
                        [
                            Trigger(TriggerTypeEnum.PAUSE, 1),
                            Trigger(TriggerTypeEnum.MESSAGE, ["@@NAME_CAP@@ then looks thoughtful for a moment."]),
                            Trigger(TriggerTypeEnum.PAUSE, 2),
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    [
                                        "\"About an hour ago, a cart of goods from the east came through here.  A package fell off "
                                        "while I was going through the inventory. Alas, I didn't notice until the wagon was gone.\"",
                                    ]),
                            Trigger(TriggerTypeEnum.PAUSE, 1),
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    [
                                        "\"Would you be interested in performing a DELIVERY for me?\"",
                                        "%s[TIP: The guard is offering a quest. To accept the quest type 'DELIVERY'. The 'QUESTS' "
                                        "command displays more information about your current and completed quests.]"
                                        "%s" % (ANSI.TEXT_COLOR_CYAN, ANSI.TEXT_NORMAL),
                                    ]),
                            Trigger(TriggerTypeEnum.QUEST_COMPLETE, QuestEnum.GUARD_INTRO),
                        ]),
                MobTalk("keep",
                        triggers=[
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    [
                                        "\"Ah, Stonehaven Keep, the last bastion of civilization before the wild forests off to "
                                        "the northeast.\"",
                                        "At this @@NAME@@ glances out across the moat towards the forest in the distance.",
                                        "\"Castellan Danly oversees the keep with a firm but fair hand. Mind that you don't go "
                                        "causin' any trouble or you'll see the keep's prison from the inside.\"",
                                        "@@SEX@@ turns and points down the passage leading into the keep.",
                                        "\"Inside we have a bevy of shops and services to choose from.  Just follow the "
                                        "Southern Walk once you're inside.\"",
                                    ]),
                        ]),
                MobTalk("information",
                        triggers=[
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    [
                                        "\"Ah some helpful information, let's see.\"",
                                        "@@NAME_CAP@@ gives you a discerning look.",
                                        "\"These are rough times. If I were you, I would secure better weapons and ARMOR. Of course, "
                                        "you can't just pick up a bastard sword and charge into battle. This ain't no fairy tale. "
                                        "You'll want to train your SKILLS up over time with practice.\"",
                                        "\"To use items like weapons, armor and other things, you'll need to GET, DROP, EQUIP and "
                                        "REMOVE them. Mind you, I wouldn't leave anything on the ground for long.\"",
                                        "\"You should take some time and look at the STATS and INFO about yourself.  Best to know "
                                        "what you're good at.\"",
                                    ]),
                        ]),
                MobTalk("delivery",
                        [
                            Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.PLAYER_QUEST, QuestEnum.GUARD_DELIVERY),
                        ],
                        [
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    ["A gap-toothed smile cracks the face of @@NAME@@."]),
                            Trigger(TriggerTypeEnum.PAUSE, 2),
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    ["\"Glad to here it! Here, take this to the provisioner on the Southern Walk.\""]),
                            Trigger(TriggerTypeEnum.PAUSE, 1),
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    [
                                        "@@NAME_CAP@@ gives you a small weathered package.",
                                        "%s[TIP: You are still in 'TALK' mode with the guard. To stop talking type 'DONE'. Then "
                                        "you can see what's in your inventory with the 'INVENTORY' command (or it's "
                                        "abbreviation 'I'). Also, 'HELP' will display all of the commands for the "
                                        "game.]%s" % (ANSI.TEXT_COLOR_CYAN, ANSI.TEXT_NORMAL),
                                    ]),
                            Trigger(TriggerTypeEnum.ITEM_GIVE, ItemEnum.QUEST_WEATHERED_PACKAGE),
                            Trigger(TriggerTypeEnum.QUEST_GIVE, QuestEnum.GUARD_DELIVERY),
                        ]),
                MobTalk("~",
                        triggers=[
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    [
                                        "\"Stay safe while in the Keep.\"",
                                        "@@NAME_CAP@@ resumes his post.",
                                    ]),
                        ]),
            ]),
    PersonEnum.BL_KEEP_SENTRY:
        Mob(PersonEnum.BL_KEEP_SENTRY, "a sentry",
            "A common sentry stands watch.", 50, 14, 40,
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
                        Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=15),
                    ],
                    [
                        Trigger(TriggerTypeEnum.MESSAGE,
                                ["@@NAME_CAP@@ shuffles his feet looking bored."]),
                    ], 300),
                Periodic(
                    [
                        Condition(ConditionCheckEnum.GREATER_THAN, TargetTypeEnum.HOUR_OF_DAY_CHECK, value=21),
                        Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=15),
                    ],
                    [
                        Trigger(TriggerTypeEnum.MESSAGE, ["@@NAME_CAP@@ yawns."]),
                    ], 300),
                Periodic(
                    [
                        Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.HOUR_OF_DAY_CHECK, value=4),
                        Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=15),
                    ],
                    [
                        Trigger(TriggerTypeEnum.MESSAGE, ["@@NAME_CAP@@ nods off for a moment before jerking upright."]),
                    ], 300),
            ]),
    PersonEnum.BL_KEEP_BEGGAR:
        Mob(PersonEnum.BL_KEEP_BEGGAR, "an unkempt man",
            "An unkempt man sits near the wall mumbling to himself.", 40, 12, 35,
            cur=DiceRoll(1, 2),
            attrs={
                AttrEnum.SEX: 1,
                AttrEnum.STRENGTH: 10,
                AttrEnum.STAMINA: 11,
                AttrEnum.DEXTERITY: 12,
                AttrEnum.AGILITY: 11,
                AttrEnum.EYESIGHT: 10,
                AttrEnum.HEARING: 10,
                AttrEnum.SMELL: 4,
                AttrEnum.INTELLIGENCE: 16,
                AttrEnum.AURA: 10,
                AttrEnum.WILL: 11,
            },
            mob_skills={
                SkillEnum.UNARMED: 40,
            },
            eq={
                ItemEnum.ARMOR_TUNIC_CLOTH: ItemLink(1, True),
            },
            periodics=[
                Periodic(
                    [
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.FLAG_CHECK, PersonFlag.BEHAVIOR_1),
                    ],
                    [
                        Trigger(TriggerTypeEnum.MESSAGE, ["@@NAME_CAP@@ sags visibly and sits back down."]),
                        Trigger(TriggerTypeEnum.PERSON_DESC, "@@NAME_CAP@@ sits near the wall mumbling to himself."),
                        Trigger(TriggerTypeEnum.TAKE_FLAG, PersonFlag.BEHAVIOR_1),
                    ], 300),
            ],
            talk=[
                MobTalk("~on_enter~",
                        [
                            Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=15),
                        ],
                        [
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    ["@@NAME_CAP@@ mumbles, \"He was an unholy abomination ...\""]),
                            Trigger(TriggerTypeEnum.END),
                        ]),
                MobTalk("~on_enter~",
                        [
                            Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.FLAG_CHECK, PersonFlag.BEHAVIOR_1),
                            Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=15),
                        ],
                        [
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    ["@@NAME_CAP@@ jumps to his feet and stares at you."]),
                            Trigger(TriggerTypeEnum.PERSON_DESC,
                                    "@@NAME_CAP@@ is standing here crazily looking in all directions."),
                            Trigger(TriggerTypeEnum.GIVE_FLAG, PersonFlag.BEHAVIOR_1),
                            Trigger(TriggerTypeEnum.END),
                        ]),
                MobTalk("~on_enter~",
                        [
                            Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=15),
                        ],
                        [
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    ["@@NAME_CAP@@ mumbles, \"I told her not to pick it up ...\""]),
                            Trigger(TriggerTypeEnum.END),
                        ]),
            ]),
    PersonEnum.BL_KEEP_CORPORAL_WATCH:
        Mob(PersonEnum.BL_KEEP_CORPORAL_WATCH, "the corporal of the watch",
            "The corporal of the watch stands here grumbling to his scribe.", 65, 18, 50,
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
                SkillEnum.SWORD: 70,
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
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.MOB_IN_ROOM, PersonEnum.BL_KEEP_YARD_SCRIBE),
                        Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=15),
                    ],
                    [
                        Trigger(TriggerTypeEnum.MESSAGE,
                                ["@@NAME_CAP@@ glances at the scribe and grumbles under his breath."]),
                    ], 300),
                Periodic(
                    [
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.LOCATED_IN_ROOM, RoomEnum.BL_ENTRY_YARD),
                        Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.FLAG_CHECK, PersonFlag.BEHAVIOR_1),
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.MOB_IN_ROOM, PersonEnum.BL_KEEP_YARD_SCRIBE),
                        Condition(ConditionCheckEnum.GREATER_THAN, TargetTypeEnum.HOUR_OF_DAY_CHECK, value=19),
                    ],
                    [
                        Trigger(TriggerTypeEnum.PERSON_DESC,
                                "@@NAME_CAP@@ seems to be on his way somewhere."),
                        Trigger(TriggerTypeEnum.MESSAGE,
                                [
                                    "@@NAME_CAP@@ turns to the scribe. \"The hour grows late and I am "
                                    "in need of a good meal. I shall see you in the morn.\"",
                                ]),
                        Trigger(TriggerTypeEnum.PERSON_MOVE, DirectionEnum.SOUTH),
                        Trigger(TriggerTypeEnum.GIVE_FLAG, PersonFlag.BEHAVIOR_1),
                        Trigger(TriggerTypeEnum.END),
                    ], 30),
                Periodic(
                    [
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.FLAG_CHECK, PersonFlag.BEHAVIOR_1),
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.LOCATED_IN_ROOM, RoomEnum.BL_EASTERN_WALK),
                    ],
                    [
                        Trigger(TriggerTypeEnum.PERSON_MOVE, DirectionEnum.SOUTH),
                        Trigger(TriggerTypeEnum.END),
                    ], 30),
                Periodic(
                    [
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.FLAG_CHECK, PersonFlag.BEHAVIOR_1),
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.LOCATED_IN_ROOM, RoomEnum.BL_SOUTHEASTERN_WALK),
                    ],
                    [
                        Trigger(TriggerTypeEnum.PERSON_MOVE, DirectionEnum.WEST),
                        Trigger(TriggerTypeEnum.END),
                    ], 30),
                Periodic(
                    [
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.FLAG_CHECK, PersonFlag.BEHAVIOR_1),
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.LOCATED_IN_ROOM, RoomEnum.BL_SOUTHERN_WALK),
                    ],
                    [
                        Trigger(TriggerTypeEnum.PERSON_DESC, "@@NAME_CAP@@ is resting here."),
                        Trigger(TriggerTypeEnum.MESSAGE,
                                ["@@NAME_CAP@@ unlocks the door to a private apartment with an iron key."]),
                        Trigger(TriggerTypeEnum.DOOR_UNLOCK, DoorEnum.CORPORAL_APPT_DOOR),
                        Trigger(TriggerTypeEnum.PERSON_MOVE, DirectionEnum.SOUTH),
                        Trigger(TriggerTypeEnum.MESSAGE,
                                ["@@NAME_CAP@@ lays down on the bed."]),
                        Trigger(TriggerTypeEnum.END),
                    ], 30),
                Periodic(
                    [
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.FLAG_CHECK, PersonFlag.BEHAVIOR_1),
                        Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.HOUR_OF_DAY_CHECK, value=2),
                    ],
                    [
                        Trigger(TriggerTypeEnum.TAKE_FLAG, PersonFlag.BEHAVIOR_1),
                    ], 30),
                Periodic(
                    [
                        Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.FLAG_CHECK, PersonFlag.BEHAVIOR_1),
                        Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.FLAG_CHECK, PersonFlag.BEHAVIOR_2),
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.LOCATED_IN_ROOM, RoomEnum.BL_APARMENT_1),
                        Condition(ConditionCheckEnum.GREATER_THAN, TargetTypeEnum.HOUR_OF_DAY_CHECK, value=6),
                    ],
                    [
                        Trigger(TriggerTypeEnum.PERSON_DESC,
                                "@@NAME_CAP@@ seems to be on his way somewhere."),
                        Trigger(TriggerTypeEnum.MESSAGE, ["@@NAME_CAP@@ stands up."]),
                        Trigger(TriggerTypeEnum.PERSON_MOVE, DirectionEnum.NORTH),
                        Trigger(TriggerTypeEnum.MESSAGE,
                                ["@@NAME_CAP@@ locks the door to a private apartment with an iron key."]),
                        Trigger(TriggerTypeEnum.DOOR_LOCK, DoorEnum.CORPORAL_APPT_DOOR),
                        Trigger(TriggerTypeEnum.GIVE_FLAG, PersonFlag.BEHAVIOR_2),
                        Trigger(TriggerTypeEnum.END),
                    ], 30),
                Periodic(
                    [
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.FLAG_CHECK, PersonFlag.BEHAVIOR_2),
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.LOCATED_IN_ROOM, RoomEnum.BL_SOUTHERN_WALK),
                    ],
                    [
                        Trigger(TriggerTypeEnum.PERSON_MOVE, DirectionEnum.EAST),
                        Trigger(TriggerTypeEnum.END),
                    ], 30),
                Periodic(
                    [
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.FLAG_CHECK, PersonFlag.BEHAVIOR_2),
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.LOCATED_IN_ROOM, RoomEnum.BL_SOUTHEASTERN_WALK),
                    ],
                    [
                        Trigger(TriggerTypeEnum.PERSON_MOVE, DirectionEnum.NORTH),
                        Trigger(TriggerTypeEnum.END),
                    ], 30),
                Periodic(
                    [
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.FLAG_CHECK, PersonFlag.BEHAVIOR_2),
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.LOCATED_IN_ROOM, RoomEnum.BL_EASTERN_WALK),
                    ],
                    [
                        Trigger(TriggerTypeEnum.PERSON_DESC, "@@NAME_CAP@@ stands here grumbling to his scribe."),
                        Trigger(TriggerTypeEnum.PERSON_MOVE, DirectionEnum.NORTH),
                        Trigger(TriggerTypeEnum.TAKE_FLAG, PersonFlag.BEHAVIOR_2),
                        Trigger(TriggerTypeEnum.END),
                    ], 30),
            ]),
    PersonEnum.BL_KEEP_YARD_SCRIBE:
        Mob(PersonEnum.BL_KEEP_YARD_SCRIBE, "a young scribe",
            "A young scribe is taking notes as traffic moves in and out of the keep.", 40, 12, 35,
            cur=DiceRoll(1, 6, 3),
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
                SkillEnum.UNARMED: 50,
            },
            eq={
                ItemEnum.ARMOR_ROBE_CLOTH: ItemLink(1, True),
            },
            periodics=[
                Periodic(
                    [
                        Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=15),
                    ],
                    [
                        Trigger(TriggerTypeEnum.MESSAGE, ["@@NAME_CAP@@ scribbles something in his notes."]),
                    ], 300),
            ]),
    PersonEnum.BL_SMITHY:
        Mob(PersonEnum.BL_SMITHY, "the smithy",
            "A large ruddy faced man in a leather apron moves about the room.", 60, 17, 50,
            cur=DiceRoll(1, 6, 20),
            attrs={
                AttrEnum.SEX: 1,
                AttrEnum.STRENGTH: 18,
                AttrEnum.STAMINA: 16,
                AttrEnum.DEXTERITY: 16,
                AttrEnum.AGILITY: 12,
                AttrEnum.EYESIGHT: 15,
                AttrEnum.HEARING: 5,
                AttrEnum.SMELL: 7,
                AttrEnum.INTELLIGENCE: 12,
                AttrEnum.AURA: 12,
                AttrEnum.WILL: 16,
            },
            mob_skills={
                SkillEnum.CLUB: 75,
                SkillEnum.METALCRAFT: 50,
            },
            eq={
                ItemEnum.WEAPON_MAUL: ItemLink(1, True),
                ItemEnum.ARMOR_GAMBESON_QUILT: ItemLink(1, True),
                ItemEnum.ARMOR_CAP_LEATHER: ItemLink(1, True),
                ItemEnum.ARMOR_APRON_LEATHER: ItemLink(1, True),
                ItemEnum.ARMOR_SHOES_LEATHER: ItemLink(1, True),
            },
            sell_items={
                ItemEnum.ARMOR_COWL_MAIL: ItemLink(1),
                ItemEnum.ARMOR_BYRNIE_MAIL: ItemLink(1),
                ItemEnum.ARMOR_HAUBERK_MAIL: ItemLink(1),
                ItemEnum.ARMOR_LEGGINGS_MAIL: ItemLink(1),
                ItemEnum.ARMOR_MITTENS_MAIL: ItemLink(1),
                ItemEnum.ARMOR_VEST_SCALE: ItemLink(1),
                ItemEnum.ARMOR_BYRNIE_SCALE: ItemLink(1),
                ItemEnum.ARMOR_HAUBERK_SCALE: ItemLink(1),
            },
            talk=[
                MobTalk("",
                        triggers=[
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    ["The large man turns away from his work. \"Hello citizen. Care to BUY something?\""]),
                        ]),
                MobTalk("shop",
                        triggers=[
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    ["\"If you seek metal armors, you're in the right place to BUY them.\""]),
                        ]),
                MobTalk("buy",
                        triggers=[
                            Trigger(TriggerTypeEnum.MESSAGE, ["\"I sell only the finest made goods:\""]),
                            Trigger(TriggerTypeEnum.ITEM_BUY),
                        ]),
                MobTalk("~",
                        triggers=[
                            Trigger(TriggerTypeEnum.MESSAGE, ["\"It's been a pleasure.\""]),
                        ]),
            ]),
    PersonEnum.BL_PROVISIONER:
        Mob(PersonEnum.BL_PROVISIONER, "the provisioner",
            "A sturdy shop keeper wanders around cleaning supplies.", 60, 17, 50,
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
                SkillEnum.DAGGER: 75,
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
                ItemEnum.WEAPON_CLUB: ItemLink(1),
                ItemEnum.WEAPON_STAFF: ItemLink(1),
                ItemEnum.ARMOR_CAP_CLOTH: ItemLink(1),
                ItemEnum.ARMOR_HOOD_CLOTH: ItemLink(1),
                ItemEnum.ARMOR_VEST_CLOTH: ItemLink(1),
                ItemEnum.ARMOR_TUNIC_CLOTH: ItemLink(1),
                ItemEnum.ARMOR_SURCOAT_CLOTH: ItemLink(1),
                ItemEnum.ARMOR_ROBE_CLOTH: ItemLink(1),
                ItemEnum.ARMOR_LEGGINGS_CLOTH: ItemLink(1),
                ItemEnum.ARMOR_CAP_QUILT: ItemLink(1),
                ItemEnum.ARMOR_COWL_QUILT: ItemLink(1),
                ItemEnum.ARMOR_TUNIC_QUILT: ItemLink(1),
                ItemEnum.ARMOR_GAMBESON_QUILT: ItemLink(1),
                ItemEnum.ARMOR_LEGGINGS_QUILT: ItemLink(1),
                ItemEnum.MISC_TORCH: ItemLink(1),
            },
            buy_items={
                ItemEnum.WEAPON_CLUB: ItemLink(1),
                ItemEnum.MISC_RAT_FUR: ItemLink(1),
                ItemEnum.ARMOR_STAINED_QUILT_COWL: ItemLink(1),
                ItemEnum.ARMOR_STAINED_QUILT_LEGGINGS: ItemLink(1),
            },
            talk=[
                MobTalk("",
                        triggers=[
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    [
                                        "\"Hello! Welcome to my humble SHOP.  Feel free to look around for something to "
                                        "BUY or you can SELL various items to me.\"",
                                    ]),
                        ]),
                MobTalk("",
                        [
                            Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.PLAYER_QUEST_COMPLETE,
                                      QuestEnum.GUARD_DELIVERY),
                        ],
                        [
                            Trigger(TriggerTypeEnum.PAUSE, 2),
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    [
                                        "\"Ah! I see you have a package for me.  I appreciate your help bringing it to "
                                        "the shop.\"",
                                    ]),
                            Trigger(TriggerTypeEnum.PAUSE, 1),
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    [
                                        "You give the weathered package to @@NAME@@.",
                                        "@@SEX_PRONOUN_CAP@@ gently places it on a pile of goods and takes a moment to rummage "
                                        "around behind the counter.  After a moment @@SEX_PRONOUN@@ steps up to you and presses "
                                        "a few coins into your hand.",
                                    ]),
                            Trigger(TriggerTypeEnum.ITEM_TAKE, ItemEnum.QUEST_WEATHERED_PACKAGE),
                            Trigger(TriggerTypeEnum.CURRENCY_GIVE, 5),
                            Trigger(TriggerTypeEnum.QUEST_COMPLETE, QuestEnum.GUARD_DELIVERY),
                        ]),
                MobTalk("",
                        [
                            Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.PLAYER_QUEST,
                                      QuestEnum.WAREHOUSE_RATS),
                        ],
                        [
                            Trigger(TriggerTypeEnum.PAUSE, 2),
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    [
                                        "\"If you're interested, I could use some help in my warehouse. Seemingly "
                                        "overnight rats have infested the place. It doesn't look good for me and worse "
                                        "when they get into the wares we store for traveling folks.\"",
                                    ]),
                            Trigger(TriggerTypeEnum.PAUSE, 2),
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    ["@@SEX_PRONOUN_CAP@@ pauses to shiver slightly."]),
                            Trigger(TriggerTypeEnum.PAUSE, 2),
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    [
                                        "\"Care to clear out a few rats as you have time? You could bring me their "
                                        "fur as PROOF of your efforts?\"",
                                    ]),
                        ]),
                MobTalk("proof",
                        [
                            Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.PLAYER_QUEST, QuestEnum.WAREHOUSE_RATS),
                        ],
                        [
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    [
                                        "\"Great! The warehouse is back down the Southern Walk and then north on Eastern "
                                        "Walk. It's there on the left. Return to me and I'll pay you for each fur you "
                                        "collect.\"",
                                    ]),
                            Trigger(TriggerTypeEnum.PAUSE, 1),
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    ["@@NAME_CAP@@ trails off as @@SEX_PRONOUN@@ takes a closer look at you ..."]),
                            Trigger(TriggerTypeEnum.PAUSE, 1),
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    [
                                        "\"Oh my, you are quite unprepared to go rat hunting. Perhaps I have something to "
                                        "help.\"",
                                        "@@NAME_CAP@@ starts searching around @@SEX_POSSESSIVE_PRONOUN@@ shop."
                                    ]),
                            Trigger(TriggerTypeEnum.PAUSE, 3),
                            Trigger(TriggerTypeEnum.MESSAGE, ["@@NAME_CAP@@ finds a wooden club lying in a corner."]),
                            Trigger(TriggerTypeEnum.PAUSE, 2),
                            Trigger(TriggerTypeEnum.MESSAGE, ["@@NAME_CAP@@ digs a stained quilt tunic out of a chest."]),
                            Trigger(TriggerTypeEnum.PAUSE, 2),
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    ["@@NAME_CAP@@ pulls a key from a pocket in @@SEX_POSSESSIVE_PRONOUN@@ surcoat."]),
                            Trigger(TriggerTypeEnum.PAUSE, 2),
                            Trigger(TriggerTypeEnum.MESSAGE, ["\"Yes yes. This will do. Here take these.\""]),
                            Trigger(TriggerTypeEnum.PAUSE, 1),
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    [
                                        "@@NAME_CAP@@ gives you a stained quilt tunic.",
                                        "@@NAME_CAP@@ gives you a wooden club.",
                                        "@@NAME_CAP@@ gives you a large bronze key.",
                                    ]),
                            Trigger(TriggerTypeEnum.ITEM_GIVE, ItemEnum.WEAPON_CLUB),
                            Trigger(TriggerTypeEnum.ITEM_GIVE, ItemEnum.ARMOR_STAINED_QUILT_TUNIC),
                            Trigger(TriggerTypeEnum.ITEM_GIVE, ItemEnum.KEY_WAREHOUSE_DBL_DOOR),
                            Trigger(TriggerTypeEnum.QUEST_GIVE, QuestEnum.WAREHOUSE_RATS),
                            Trigger(TriggerTypeEnum.PAUSE, 1),
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    ["\"Don't forget you'll need to EQUIP the club and tunic. Good luck!"]),
                        ]),
                MobTalk("~on_enter~",
                        [
                            Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.PLAYER_QUEST_COMPLETE,
                                      QuestEnum.WAREHOUSE_RATS),
                            Condition(ConditionCheckEnum.HAS, TargetTypeEnum.PLAYER_INVEN, ItemEnum.MISC_RAT_FUR),
                        ],
                        [
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    [
                                        "\"Ah, I see you've been clearing out the varmin in the warehouse! "
                                        "I'll pay you 1 SP per fur as I agreed. And in the future you can SELL them "
                                        "to me.\"",
                                    ]),
                            Trigger(TriggerTypeEnum.QUEST_COMPLETE, QuestEnum.WAREHOUSE_RATS),
                            Trigger(TriggerTypeEnum.ITEM_SELL),
                        ]),
                MobTalk("shop",
                        triggers=[
                            Trigger(TriggerTypeEnum.MESSAGE, ["\"Ah a customer! Are you here to BUY or SELL?\""]),
                        ]),
                MobTalk("buy",
                        triggers=[
                            Trigger(TriggerTypeEnum.MESSAGE, ["\"Excellent! Here's what I have:\""]),
                            Trigger(TriggerTypeEnum.ITEM_BUY),
                        ]),
                MobTalk("sell",
                        triggers=[
                            Trigger(TriggerTypeEnum.MESSAGE, ["\"Let's see if you have anything I need ...\""]),
                            Trigger(TriggerTypeEnum.ITEM_SELL),
                        ]),
                MobTalk("~",
                        triggers=[
                            Trigger(TriggerTypeEnum.MESSAGE, ["\"Fare thee well.\""]),
                        ]),
            ]),
    PersonEnum.BL_TANNER:
        Mob(PersonEnum.BL_TANNER, "the tanner",
            "A short muscular woman strides purposefully around the shop.", 60, 17, 50,
            cur=DiceRoll(1, 6, 20),
            attrs={
                AttrEnum.SEX: 2,
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
                SkillEnum.DAGGER: 75,
                SkillEnum.HIDEWORK: 50,
            },
            eq={
                ItemEnum.WEAPON_DAGGER: ItemLink(1, True),
                ItemEnum.ARMOR_GAMBESON_QUILT: ItemLink(1, True),
                ItemEnum.ARMOR_CAP_LEATHER: ItemLink(1, True),
                ItemEnum.ARMOR_SURCOAT_LEATHER: ItemLink(1, True),
                ItemEnum.ARMOR_SHOES_LEATHER: ItemLink(1, True),
            },
            sell_items={
                ItemEnum.ARMOR_CAP_LEATHER: ItemLink(1),
                ItemEnum.ARMOR_COWL_LEATHER: ItemLink(1),
                ItemEnum.ARMOR_VEST_LEATHER: ItemLink(1),
                ItemEnum.ARMOR_TUNIC_LEATHER: ItemLink(1),
                ItemEnum.ARMOR_SURCOAT_LEATHER: ItemLink(1),
                ItemEnum.ARMOR_LEGGINGS_LEATHER: ItemLink(1),
                ItemEnum.ARMOR_SHOES_LEATHER: ItemLink(1),
                ItemEnum.ARMOR_CALF_BOOTS_LEATHER: ItemLink(1),
                ItemEnum.ARMOR_KNEE_BOOTS_LEATHER: ItemLink(1),
                ItemEnum.ARMOR_GAUNTLETS_LEATHER: ItemLink(1),
                ItemEnum.ARMOR_HALFHELM_KURBUL: ItemLink(1),
                ItemEnum.ARMOR_BREASTPLATE_KURBUL: ItemLink(1),
                ItemEnum.ARMOR_BACKPLATE_KURBUL: ItemLink(1),
                ItemEnum.ARMOR_AILETTES_KURBUL: ItemLink(1),
                ItemEnum.ARMOR_REREBRACES_KURBUL: ItemLink(1),
                ItemEnum.ARMOR_COUDES_KURBUL: ItemLink(1),
                ItemEnum.ARMOR_VAMBRACES_KURBUL: ItemLink(1),
                ItemEnum.ARMOR_KNEECOPS_KURBUL: ItemLink(1),
                ItemEnum.ARMOR_GREAVES_KURBUL: ItemLink(1),
            },
            talk=[
                MobTalk("",
                        triggers=[
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    [
                                        "@@NAME_CAP@@ puts down @@SEX_POSSESSIVE_PRONOUN@@ tools.",
                                        "\"Ah, a customer ... What would you like to BUY?\"",
                                    ]),
                        ]),
                MobTalk("shop",
                        triggers=[
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    ["\"Have a look around and let me know if you would care to BUY an item?\""]),
                        ]),
                MobTalk("buy",
                        triggers=[
                            Trigger(TriggerTypeEnum.MESSAGE, ["\"See anything you like?\""]),
                            Trigger(TriggerTypeEnum.ITEM_BUY),
                        ]),
                MobTalk("~",
                        triggers=[
                            Trigger(TriggerTypeEnum.MESSAGE, ["\"The pleasure was mine.\""]),
                        ]),
            ]),
    PersonEnum.BL_ARMS_DEALER:
        Mob(PersonEnum.BL_ARMS_DEALER, "the arms dealer",
            "A thin pale man sits behind a counter.", 60, 17, 50,
            cur=DiceRoll(1, 6, 20),
            attrs={
                AttrEnum.SEX: 1,
                AttrEnum.STRENGTH: 10,
                AttrEnum.STAMINA: 12,
                AttrEnum.DEXTERITY: 13,
                AttrEnum.AGILITY: 10,
                AttrEnum.EYESIGHT: 15,
                AttrEnum.HEARING: 12,
                AttrEnum.SMELL: 13,
                AttrEnum.INTELLIGENCE: 15,
                AttrEnum.AURA: 12,
                AttrEnum.WILL: 13,
            },
            mob_skills={
                SkillEnum.DAGGER: 75,
                SkillEnum.SURVIVAL: 50,
            },
            eq={
                ItemEnum.WEAPON_DAGGER: ItemLink(1, True),
                ItemEnum.ARMOR_VEST_CLOTH: ItemLink(1, True),
                ItemEnum.ARMOR_COWL_LEATHER: ItemLink(1, True),
                ItemEnum.ARMOR_SURCOAT_LEATHER: ItemLink(1, True),
                ItemEnum.ARMOR_LEGGINGS_CLOTH: ItemLink(1, True),
                ItemEnum.ARMOR_KNEE_BOOTS_LEATHER: ItemLink(1, True),
            },
            sell_items={
                ItemEnum.WEAPON_DAGGER: ItemLink(1),
                ItemEnum.WEAPON_MAIN_GAUCHE: ItemLink(1),
                ItemEnum.WEAPON_SHORTSWORD: ItemLink(1),
                ItemEnum.WEAPON_BROADSWORD: ItemLink(1),
                ItemEnum.WEAPON_BASTARD_SWORD: ItemLink(1),
                ItemEnum.WEAPON_MACE: ItemLink(1),
                ItemEnum.WEAPON_MORNINGSTAR: ItemLink(1),
                ItemEnum.WEAPON_HANDAXE: ItemLink(1),
                ItemEnum.WEAPON_WARHAMMER: ItemLink(1),
                ItemEnum.WEAPON_BALL_AND_CHAIN: ItemLink(1),
                ItemEnum.WEAPON_STAFF: ItemLink(1),
                ItemEnum.WEAPON_SPEAR: ItemLink(1),
                ItemEnum.WEAPON_POLEAXE: ItemLink(1),
            },
            talk=[
                MobTalk("",
                        triggers=[
                            Trigger(TriggerTypeEnum.MESSAGE,
                                    [
                                        "Glancing warily around, the man sits up straighter.",
                                        "\"If you see something you want to BUY, just say the word.\"",
                                    ]),
                        ]),
                MobTalk("shop",
                        triggers=[
                            Trigger(TriggerTypeEnum.MESSAGE, ["\"What would you like to BUY?\""]),
                        ]),
                MobTalk("buy",
                        triggers=[
                            Trigger(TriggerTypeEnum.MESSAGE, ["\"All hand made arms of the finest quality:\""]),
                            Trigger(TriggerTypeEnum.ITEM_BUY),
                        ]),
                MobTalk("~",
                        triggers=[
                            Trigger(TriggerTypeEnum.MESSAGE, ["\"Entertaining ... as always.\""]),
                        ]),
            ]),
}

# vim: tabstop=2 shiftwidth=2 expandtab:
