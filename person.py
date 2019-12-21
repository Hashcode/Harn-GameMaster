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
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE,
                                "The corporal of the watch glances at the scribe and grumbles under his breath."),
                    ], 300),
                Periodic(
                    [
                        Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.FLAG_CHECK, PersonFlag.BEHAVIOR_1),
                        Condition(ConditionCheckEnum.HAS, TargetTypeEnum.MOB_IN_ROOM, PersonEnum.BL_KEEP_YARD_SCRIBE),
                        Condition(ConditionCheckEnum.GREATER_THAN, TargetTypeEnum.HOUR_OF_DAY_CHECK, value=19),
                    ],
                    [
                        Trigger(TriggerTypeEnum.PERSON_DESC,
                                "The corporal of the watch seems to be on his way somewhere."),
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE,
                                "The corporal of the watch turns to the scribe. \"The hour grows late and I am "
                                "in need of a good meal. I shall see you in the morn.\""),
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
                        Trigger(TriggerTypeEnum.PERSON_DESC, "The corporal of the watch is resting here."),
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE,
                                "The corporal of the watch unlocks the door to a private apartment with an iron key."),
                        Trigger(TriggerTypeEnum.DOOR_UNLOCK, DoorEnum.CORPORAL_APPT_DOOR),
                        Trigger(TriggerTypeEnum.PERSON_MOVE, DirectionEnum.SOUTH),
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE,
                                "The corporal of the watch lays down on the bed."),
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
                                "The corporal of the watch seems to be on his way somewhere."),
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE, "The corporal of the watch stands up."),
                        Trigger(TriggerTypeEnum.PERSON_MOVE, DirectionEnum.NORTH),
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE,
                                "The corporal of the watch locks the door to a private apartment with an iron key."),
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
                        Trigger(TriggerTypeEnum.PERSON_DESC, "The corporal of the watch stands here grumbling to his scribe."),
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
                        Trigger(TriggerTypeEnum.ROOM_MESSAGE, "The scribe scribbles something in his notes."),
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
                        text=[
                            "The large man turns away from his work. \"Hello citizen. Care to BUY something?\"",
                        ]),
                MobTalk("shop",
                        text=[
                            "\"If you seek metal armors, you're in the right place to BUY them.\"",
                        ]),
                MobTalk("buy",
                        text=[
                            "\"I sell only the finest made goods:\"",
                        ],
                        triggers=[
                            Trigger(TriggerTypeEnum.ITEM_BUY),
                        ]),
                MobTalk("~",
                        text=[
                            "\"It's been a pleasure.\""
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
                ItemEnum.WEAPON_STAFF: ItemLink(1),
                ItemEnum.MISC_TORCH: ItemLink(1),
            },
            buy_items={
                ItemEnum.MISC_RAT_FUR: ItemLink(1),
            },
            talk=[
                MobTalk("",
                        text=[
                            "\"Hello! Welcome to my humble SHOP.  Feel free to look around for something to BUY or you can "
                            "SELL various items to me.\"",
                        ]),
                MobTalk("",
                        condition=[
                            Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.PLAYER_QUEST_COMPLETE,
                                      QuestEnum.GUARD_DELIVERY),
                        ],
                        text=[
                            "\"Ah! I see you have a package for me.  I appreciate your help bringing it to the shop.\"",
                            "You give the weathered package to the shop keeper.",
                            "He gently places it on a pile of goods and takes a moment to rummage around behind the "
                            "counter.  After a moment he steps up to you and presses a few coins into your hand.",
                        ],
                        triggers=[
                            Trigger(TriggerTypeEnum.ITEM_TAKE, ItemEnum.QUEST_WEATHERED_PACKAGE),
                            Trigger(TriggerTypeEnum.CURRENCY_GIVE, 1),
                            Trigger(TriggerTypeEnum.QUEST_COMPLETE, QuestEnum.GUARD_DELIVERY),
                        ]),
                MobTalk("",
                        condition=[
                            Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.PLAYER_QUEST,
                                      QuestEnum.WAREHOUSE_RATS),
                        ],
                        text=[
                            "\"If you're interested, I could use some help in my warehouse. Seemingly overnight "
                            "rats have infested the place. It doesn't look good for me and worse when they get "
                            "into the wares we store for traveling folks.\"",
                            "He pauses to shiver slightly.",
                            "\"Care to clear out a few rats as you have time? You could bring me their fur as "
                            "PROOF of your efforts?\"",
                        ]),
                MobTalk("proof",
                        condition=[
                            Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.PLAYER_QUEST,
                                      QuestEnum.WAREHOUSE_RATS),
                        ],
                        text=[
                            "\"Great! The warehouse is back down the Southern Walk and then north on Eastern "
                            "Walk. It's there on the left.\"",
                            "The provisioner starts patting his surcoat and checking his pockets.",
                            "\"Return to me and I'll pay you for each fur you collect. You'll need this key for "
                            "the double doors.\"",
                            "The provisioner gives you a large bronze key.",
                        ],
                        triggers=[
                            Trigger(TriggerTypeEnum.QUEST_GIVE, QuestEnum.WAREHOUSE_RATS),
                            Trigger(TriggerTypeEnum.ITEM_GIVE, ItemEnum.KEY_WAREHOUSE_DBL_DOOR),
                        ]),
                MobTalk("~on_enter~",
                        condition=[
                            Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.PLAYER_QUEST_COMPLETE,
                                      QuestEnum.WAREHOUSE_RATS),
                            Condition(ConditionCheckEnum.HAS, TargetTypeEnum.PLAYER_INVEN, ItemEnum.MISC_RAT_FUR),
                        ],
                        text=[
                            "\"Ah, I see you've been clearing out the varmin in the warehouse! I'll pay you "
                            "1 SP per fur as I agreed.\""
                        ],
                        triggers=[
                            Trigger(TriggerTypeEnum.QUEST_COMPLETE, QuestEnum.WAREHOUSE_RATS),
                            Trigger(TriggerTypeEnum.ITEM_SELL),
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
            },
            talk=[
                MobTalk("",
                        text=[
                            "The study woman puts down her tools. \"Ah, a customer ... What would you like to BUY?\"",
                        ]),
                MobTalk("shop",
                        text=[
                            "\"Have a look around and let me know if you would care to BUY an item?\"",
                        ]),
                MobTalk("buy",
                        text=[
                            "\"See anything you like?\"",
                        ],
                        triggers=[
                            Trigger(TriggerTypeEnum.ITEM_BUY),
                        ]),
                MobTalk("~",
                        text=[
                            "\"The pleasure was mine.\""
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
                        text=[
                            "Glancing warily around, the man sits up straighter. \"If you see something you want to BUY, "
                            "just say the word.\"",
                        ]),
                MobTalk("shop",
                        text=[
                            "\"What would you like to BUY?\"",
                        ]),
                MobTalk("buy",
                        text=[
                            "\"All hand made arms of the finest quality:\"",
                        ],
                        triggers=[
                            Trigger(TriggerTypeEnum.ITEM_BUY),
                        ]),
                MobTalk("~",
                        text=[
                            "\"Entertaining ... as always.\""
                        ]),
            ]),
}

# vim: tabstop=2 shiftwidth=2 expandtab:
