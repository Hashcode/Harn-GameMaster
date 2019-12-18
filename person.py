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
                            MaterialEnum, AimEnum, RoomEnum)

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
                ItemEnum.MISC_RAT_FUR: 75,
            }),
    PersonEnum.BL_KEEP_GUARD:
        Mob(PersonEnum.BL_KEEP_GUARD, "a gatehouse guard",
            "A mild-mannered guard keeps watch over the gatehouse.", 60, 17, 50,
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
                            Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.PLAYER_QUEST, QuestEnum.GUARD_INTRO),
                        ],
                        text=[
                            "The guard glances in your direction. \"Come TALK to me, Traveller, when you get a moment.\"",
                            "%s[TIP: Sometimes keywords will be presented in all capitals such as 'TALK'.  You can type "
                            "these keywords to start interactions or talk about different subjects.  As the adventure "
                            "progresses this will happen less and less.]%s" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL),
                        ]),
                MobTalk("~on_exit~",
                        condition=[
                            Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.PLAYER_QUEST, QuestEnum.GUARD_INTRO),
                        ],
                        text=[
                            "The guard moves to block your way. \"I meant you need to TALK to me before entering.\" "
                            "He taps his foot impatiently.",
                        ],
                        triggers=[
                            Trigger(TriggerTypeEnum.DENY),
                        ]),
                MobTalk("",
                        text=[
                            "The guard turns to look at you.",
                            "\"Hello Traveller. Welcome to Stonehaven KEEP. Times are rough, so you may need to forgive the grim "
                            "faces of our inhabitants. We've seen a recent surge in attacks from the wild men of the forest.\"",
                            "\"You look rather new to the area, so if you want more INFORMATION let me know.\"",
                        ]),
                MobTalk("",
                        condition=[
                            Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.PLAYER_QUEST, QuestEnum.GUARD_DELIVERY),
                        ],
                        text=[
                            "The guard then looks thoughtful for a moment.",
                            "\"About an hour ago, a cart of goods from the east came through here.  A package fell off "
                            "while I was going through the inventory. Alas, I didn't notice until the wagon was gone.\"",
                            "\"Would you be interested in performing a DELIVERY for me?\"",
                            "%s[TIP: The guard is offering a quest. To accept the quest type 'DELIVERY'. The 'QUESTS' command "
                            "displays more information about your current and completed quests.]%s" % (ANSI.TEXT_BOLD,
                                                                                                       ANSI.TEXT_NORMAL),
                        ],
                        triggers=[
                            Trigger(TriggerTypeEnum.QUEST_COMPLETE, QuestEnum.GUARD_INTRO),
                        ]),
                MobTalk("keep",
                        text=[
                            "\"Ah, Stonehaven Keep, the last bastion of civilization before the wild forests off to the "
                            "northeast.\"  At this the guard glances out across the moat towards the forest in the distance.",
                            "\"Castellan Danly oversees the keep with a firm but fair hand.  Mind that you don't go causin' "
                            "any trouble or you'll see the keep's prison from the inside.\"",
                            "He turns and points down the passage leading into the keep. \"Inside we have a bevy of "
                            "shops and services to choose from.  Just follow the Southern Walk once you're inside.\"",
                        ]),
                MobTalk("information",
                        text=[
                            "\"Ah some helpful information, let's see.\"",
                            "The guard gives you a discerning look.",
                            "\"These are rough times. If I were you, I would secure better weapons and ARMOR. Of course, "
                            "you can't just pick up a bastard sword and charge into battle. This ain't no fairy tale. "
                            "You'll want to TRAIN your SKILLS up over time with practice.\"",
                            "\"To use items like weapons, armor and other things, you'll need to GET, DROP, EQUIP and "
                            "REMOVE them. Mind you, I wouldn't leave anything on the ground for long.\"",
                            "\"You should take some time and look at the STATS and INFO about yourself.  Best to know "
                            "what you're good at.\"",
                        ]),
                MobTalk("delivery",
                        condition=[
                            Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.PLAYER_QUEST, QuestEnum.GUARD_DELIVERY),
                        ],
                        text=[
                            "A gap-toothed smile cracks the face of the stoic guard.",
                            "\"Glad to here it! Here, take this to the provisioner on the Southern Walk.\"",
                            "A gatehouse guard gives you a small weathered package.",
                            "%s[TIP: You are still in 'TALK' mode with the guard. To stop talking type 'DONE'. Then you "
                            "can see what's in your inventory with the 'INVENTORY' command (or it's abbreviation 'I'). "
                            "Also, 'HELP' will display all of the commands for the game.]%s" % (ANSI.TEXT_BOLD,
                                                                                                ANSI.TEXT_NORMAL),
                        ],
                        triggers=[
                            Trigger(TriggerTypeEnum.ITEM_GIVE, ItemEnum.QUEST_WEATHERED_PACKAGE),
                            Trigger(TriggerTypeEnum.QUEST_GIVE, QuestEnum.GUARD_DELIVERY),
                        ]),
                MobTalk("~",
                        text=[
                            "\"Stay safe while in the Keep.\" The guard resumes his post.",
                        ]),
            ]),
    PersonEnum.BL_KEEP_SENTRY:
        Mob(PersonEnum.BL_KEEP_SENTRY, "a common sentry",
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
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE, "A sentry shuffles his feet looking bored."),
                    ], 300),
                Periodic(
                    [
                        Condition(ConditionCheckEnum.GREATER_THAN, TargetTypeEnum.HOUR_OF_DAY_CHECK, value=21),
                        Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=15),
                    ],
                    [
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE, "A sentry yawns."),
                    ], 300),
                Periodic(
                    [
                        Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.HOUR_OF_DAY_CHECK, value=4),
                        Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=15),
                    ],
                    [
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE, "A sentry nods off for a moment before jerking upright."),
                    ], 300),
            ]),
    PersonEnum.BL_KEEP_BEGGAR:
        Mob(PersonEnum.BL_KEEP_BEGGAR, "an unkempt beggar",
            "An unkempt man sits near the wall mumbling to himself.", 40, 12, 35,
            cur=DiceRoll(1, 6, 60),
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
                SkillEnum.UNARMED: 20,
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
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE, "An unkempt man sags visibly and sits back down."),
                        Trigger(TriggerTypeEnum.PERSON_DESC, "An unkempt man sits near the wall mumbling to himself."),
                        Trigger(TriggerTypeEnum.TAKE_FLAG, PersonFlag.BEHAVIOR_1),
                    ], 300),
            ],
            talk=[
                MobTalk("~on_enter~",
                        condition=[
                            Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=15),
                        ],
                        text=[
                            "An unkempt man mumbles, \"He was an unholy abomination ...\"",
                        ],
                        triggers=[
                            Trigger(TriggerTypeEnum.END),
                        ]),
                MobTalk("~on_enter~",
                        condition=[
                            Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.FLAG_CHECK, PersonFlag.BEHAVIOR_1),
                            Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=15),
                        ],
                        text=[
                            "An unkempt man jumps to his feet and stares at you.",
                        ],
                        triggers=[
                            Trigger(TriggerTypeEnum.PERSON_DESC,
                                    "An unkempt man is standing here crazily looking in all directions."),
                            Trigger(TriggerTypeEnum.GIVE_FLAG, PersonFlag.BEHAVIOR_1),
                            Trigger(TriggerTypeEnum.END),
                        ]),
                MobTalk("~on_enter~",
                        condition=[
                            Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=15),
                        ],
                        text=[
                            "An unkempt man mumbles, \"I told her not to pick it up ...\"",
                        ],
                        triggers=[
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
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.MOB_IN_ROOM, PersonEnum.BL_KEEP_YARD_SCRIBE),
                        Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=15),
                    ],
                    [
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE,
                                "The corporal of the watch glances at the scribe and grumbles under his breath."),
                    ], 300),
                Periodic(
                    [
                        Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.FLAG_CHECK, PersonFlag.BEHAVIOR_1),
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.MOB_IN_ROOM, PersonEnum.BL_KEEP_YARD_SCRIBE),
                        Condition(ConditionCheckEnum.GREATER_THAN, TargetTypeEnum.HOUR_OF_DAY_CHECK, value=19),
                        Trigger(TriggerTypeEnum.END),
                    ],
                    [
                        Trigger(TriggerTypeEnum.PERSON_DESC,
                                "The corporal of the watch seems to be on his way somewhere."),
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE,
                                "The corporal of the watch turns to the scribe. \"The hour grows late and I am "
                                "in need of a good meal. I shall see you in the morn.\""),
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE, "The corporal of the watch moves to the south."),
                        Trigger(TriggerTypeEnum.GIVE_FLAG, PersonFlag.BEHAVIOR_1),
                        Trigger(TriggerTypeEnum.PERSON_MOVE, RoomEnum.BL_EASTERN_WALK),
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE, "The corporal of the watch enters from the north."),
                        Trigger(TriggerTypeEnum.END),
                    ], 30),
                Periodic(
                    [
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.FLAG_CHECK, PersonFlag.BEHAVIOR_1),
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.LOCATED_IN_ROOM, RoomEnum.BL_EASTERN_WALK),
                        Trigger(TriggerTypeEnum.END),
                    ],
                    [
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE, "The corporal of the watch moves to the south."),
                        Trigger(TriggerTypeEnum.PERSON_MOVE, RoomEnum.BL_SOUTHEASTERN_WALK),
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE, "The corporal of the watch enters from the north."),
                        Trigger(TriggerTypeEnum.END),
                    ], 30),
                Periodic(
                    [
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.FLAG_CHECK, PersonFlag.BEHAVIOR_1),
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.LOCATED_IN_ROOM, RoomEnum.BL_SOUTHEASTERN_WALK),
                        Trigger(TriggerTypeEnum.END),
                    ],
                    [
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE, "The corporal of the watch moves to the west."),
                        Trigger(TriggerTypeEnum.PERSON_MOVE, RoomEnum.BL_SOUTHERN_WALK),
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE, "The corporal of the watch enters from the east."),
                        Trigger(TriggerTypeEnum.END),
                    ], 30),
                Periodic(
                    [
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.FLAG_CHECK, PersonFlag.BEHAVIOR_1),
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.LOCATED_IN_ROOM, RoomEnum.BL_SOUTHERN_WALK),
                    ],
                    [
                        Trigger(TriggerTypeEnum.PERSON_DESC, "The corporal of the watch is resting here."),
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE,
                                "The corporal of the watch enters a private apartment to the south."),
                        Trigger(TriggerTypeEnum.PERSON_MOVE, RoomEnum.BL_APARMENT_1),
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE,
                                "The corporal of the watch enters the private apartment from the north."),
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE,
                                "The corporal of the watch lays down on the bed."),
                        Trigger(TriggerTypeEnum.TAKE_FLAG, PersonFlag.BEHAVIOR_1),
                        Trigger(TriggerTypeEnum.END),
                    ], 30),
                Periodic(
                    [
                        Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.FLAG_CHECK, PersonFlag.BEHAVIOR_2),
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.LOCATED_IN_ROOM, RoomEnum.BL_APARMENT_1),
                        Condition(ConditionCheckEnum.GREATER_THAN, TargetTypeEnum.HOUR_OF_DAY_CHECK, value=6),
                    ],
                    [
                        Trigger(TriggerTypeEnum.PERSON_DESC,
                                "The corporal of the watch seems to be on his way somewhere."),
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE, "The corporal of the watch stands up."),
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE,
                                "The corporal of the watch leaves the private apartment to the north."),
                        Trigger(TriggerTypeEnum.GIVE_FLAG, PersonFlag.BEHAVIOR_2),
                        Trigger(TriggerTypeEnum.PERSON_MOVE, RoomEnum.BL_SOUTHERN_WALK),
                        Trigger(TriggerTypeEnum.END),
                    ], 30),
                Periodic(
                    [
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.FLAG_CHECK, PersonFlag.BEHAVIOR_2),
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.LOCATED_IN_ROOM, RoomEnum.BL_SOUTHERN_WALK),
                    ],
                    [
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE, "The corporal of the watch moves to the east."),
                        Trigger(TriggerTypeEnum.PERSON_MOVE, RoomEnum.BL_SOUTHEASTERN_WALK),
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE, "The corporal of the watch enters from the west."),
                        Trigger(TriggerTypeEnum.END),
                    ], 30),
                Periodic(
                    [
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.FLAG_CHECK, PersonFlag.BEHAVIOR_2),
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.LOCATED_IN_ROOM, RoomEnum.BL_SOUTHEASTERN_WALK),
                    ],
                    [
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE, "The corporal of the watch moves to the north."),
                        Trigger(TriggerTypeEnum.PERSON_MOVE, RoomEnum.BL_EASTERN_WALK),
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE, "The corporal of the watch enters from the south."),
                        Trigger(TriggerTypeEnum.END),
                    ], 30),
                Periodic(
                    [
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.FLAG_CHECK, PersonFlag.BEHAVIOR_2),
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.LOCATED_IN_ROOM, RoomEnum.BL_EASTERN_WALK),
                    ],
                    [
                        Trigger(TriggerTypeEnum.PERSON_DESC, "The corporal of the watch stands here grumbling to his scribe."),
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE, "The corporal of the watch moves to the north."),
                        Trigger(TriggerTypeEnum.PERSON_MOVE, RoomEnum.BL_ENTRY_YARD),
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE, "The corporal of the watch enters from the south."),
                        Trigger(TriggerTypeEnum.TAKE_FLAG, PersonFlag.BEHAVIOR_2),
                        Trigger(TriggerTypeEnum.END),
                    ], 30),
            ]),
    PersonEnum.BL_KEEP_YARD_SCRIBE:
        Mob(PersonEnum.BL_KEEP_YARD_SCRIBE, "a young scribe",
            "A young scribe is taking notes as traffic moves in and out of the keep.", 40, 12, 35,
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
                        Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=15),
                    ],
                    [
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE, "The scribe scribbles something in his notes."),
                    ], 300),
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
                ItemEnum.MISC_TORCH: ItemLink(1),
            },
            talk=[
                MobTalk("",
                        text=[
                            "\"Hello! Welcome to my humble SHOP.  Feel free to look around for something to BUY or you can "
                            "SELL various items to me.\"",
                        ]),
                MobTalk("",
                        condition=[
                            Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.PLAYER_QUEST_COMPLETE, QuestEnum.GUARD_DELIVERY),
                        ],
                        text=[
                            "\"Ah! I see you have a package for me.  I appreciate your help bringing it to the shop.\"",
                            "You give the weathered package to the shop keeper.",
                            "He gently places it on a pile of goods and takes a moment to rummage around behind the "
                            "counter.  After a moment he steps up to you and presses a few coins into your hand.",
                        ],
                        triggers=[
                            Trigger(TriggerTypeEnum.ITEM_TAKE, ItemEnum.QUEST_WEATHERED_PACKAGE),
                            Trigger(TriggerTypeEnum.CURRENCY_GIVE, 5),
                            Trigger(TriggerTypeEnum.QUEST_COMPLETE, QuestEnum.GUARD_DELIVERY),
                        ]),
                MobTalk("shop",
                        text=[
                            "\"Ah a customer! Are you here to BUY or SELL?\"",
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
