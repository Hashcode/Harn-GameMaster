# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Room Functions

from enum import IntEnum

from console import (ANSI, InputFlag)
from db import (ExistsDB, LoadPlayer)
from gamedata import (GameData)
from global_defines import (PersonEnum, Player, ItemEnum, DoorEnum, Door,
                            DoorState, DirectionEnum,
                            ConditionCheckEnum, TargetTypeEnum, Condition,
                            TriggerTypeEnum, Trigger, Periodic,
                            RoomFuncResponse, RoomEnum, Exit, RoomFlag, Room)
from utils import (actionSave)


def room_StartGame():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  while True:
    desc = ANSI.TEXT_BOLD + "CREATE" + ANSI.TEXT_NORMAL + \
        " a new character or " + ANSI.TEXT_BOLD + "RESTORE" + \
        ANSI.TEXT_NORMAL + " a saved game"
    Player.Command = cm.Input("%s?" % desc, line_length=10).lower()
    if Player.Command == "restore":
      player.SetRoom(RoomEnum.GAME_RESTORE_SAVE)
      break
    elif Player.Command == "create":
      player.SetRoom(RoomEnum.GAME_CREATE_CHARACTER)
      break
  return RoomFuncResponse.SKIP


def room_RestoreSave():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  name = cm.Input("Character name:", line_length=20)
  pwd = cm.Input("Password:", line_length=10, input_flags=InputFlag.PASSWORD)

  cm.Print("\nPlease wait while saved data is loaded ...")
  ret = LoadPlayer(player, name, pwd)
  if not ret:
    cm.Print("%sUnable to find save data for %s!%s" %
             (ANSI.TEXT_BOLD, name, ANSI.TEXT_NORMAL))
    player.SetRoom(RoomEnum.GAME_START)
    return RoomFuncResponse.SKIP

  cm.Print("Loaded.")
  player.ResetStats()
  player.SetRoom(player.Room)
  return RoomFuncResponse.SKIP


def room_CreateCharacter():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  player.Name = cm.Input("Choose a character name:", line_length=20)
  if len(player.Name) < 3 or len(player.Name) > 20:
    cm.Print("\nCharacter name needs between 3 and 20 characters long.")
    return RoomFuncResponse.SKIP

  cm.Print("\nA password is used to encrypt your SAVE data.")
  cm.Print("It should NOT be a password used for anything important.")
  player.Password = cm.Input("Enter a password:", line_length=10,
                             input_flags=InputFlag.PASSWORD).upper()
  if len(player.Password) < 3 or len(player.Password) > 10:
    cm.Print("\nPassword needs to be between 3 and 10 characters long.")
    return RoomFuncResponse.SKIP

  if ExistsDB(player.Name, player.Password):
    cm.Print("\nCharacter aready exists.")
    player.SetRoom(RoomEnum.GAME_START)
    return RoomFuncResponse.SKIP

  player.GenAttr()
  player.GenSkills()
  player.ResetStats()
  player.SetRoom(GameData.ROOM_START)

  #  cm.Print("\nSaving character ...")
  #  if not actionSave():
  #    return RoomFuncResponse.SKIP
  #  cm.Print("Done.")

  cm.Print("\nGood luck, %s!" % (player.Name))
  return RoomFuncResponse.SKIP


# ZONES
class ZoneEnum(IntEnum):
  NONE = 0
  KEEP = 1
  FOREST = 2


doors = {
    DoorEnum.KEEP_DRAWBRIDGE:
        Door("drawbridge", DoorState(True, True), ItemEnum.NONE),
    DoorEnum.WAREHOUSE_DBL_DOOR:
        Door("double doors", DoorState(True, False),
             ItemEnum.KEY_WAREHOUSE_DBL_DOOR),
}

rooms = {
    # GAME ROOMS
    RoomEnum.GAME_START:
        Room(ZoneEnum.NONE,
             "Welcome to Harn GameMaster!", "",
             [
                 "Take your characters on exciting journeys in the gritty "
                 "world of the HârnMaster Game System in classic Dungeon's "
                 "and Dragons(tm) modules.",
                 "During your adventures you will accumulate skills, items "
                 "and wealth. Make sure to SAVE along the way to ensure "
                 "your progress won't be lost."
             ],
             func=room_StartGame),
    RoomEnum.GAME_RESTORE_SAVE:
        Room(ZoneEnum.NONE,
             "Restore Saved Progress", func=room_RestoreSave),
    RoomEnum.GAME_CREATE_CHARACTER:
        Room(ZoneEnum.NONE,
             "Create a New Character", func=room_CreateCharacter),

    # KEEP ON THE BORDERLANDS
    RoomEnum.BL_KEEP_GATEHOUSE:
        Room(ZoneEnum.KEEP,
             "The Main Gatehouse to Stonehaven Keep", "the main gatehouse",
             [
                 "Two 30' high towers complete with battlements, flank a 20' "
                 "high gatehouse. All have holes for bow and crossbow fire. "
                 "A deep crevice in front of the place can be spanned by a "
                 "drawbridge.",
                 "There is a portcullis at the entry way to the gatehouse, "
                 "inside of which a passage leads to large gates. The passage "
                 "is about 10' wide and 10' high.",
                 "It is obvious that the building is constructed of great "
                 "blocks of solid granite, undoubtedly common throughout the "
                 "entire fortress."
             ],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.WEST: Exit(RoomEnum.BL_GATEHOUSE_PASSAGE),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_ROAD_TO_KEEP,
                                          DoorEnum.KEEP_DRAWBRIDGE),
             },
             room_pers=[
                 PersonEnum.BL_KEEP_GUARD,
                 PersonEnum.BL_KEEP_SENTRY,
             ]),
    RoomEnum.BL_PRIEST_CHAMBER:
        Room(ZoneEnum.KEEP,
             "The Priest's Chamber", "the priest's chamber",
             [
                 "The well-appointed chamber you are standing in radiates "
                 "warmth from a cozy fire roaring in a small western alcove. "
                 "While spartan in furnishings, a well-made armoire sits in "
                 "a corner as well as a tidy bed along one wall. Several "
                 "religious paintings are hung on the walls."
             ],
             flags=RoomFlag.LIGHT,
             exits=None),
    RoomEnum.BL_GATEHOUSE_PASSAGE:
        Room(ZoneEnum.KEEP,
             "Gatehouse Passage", "a gatehouse passage",
             [
                 "This 10' wide and 10' high passage leads from the main "
                 "gatehouse of Stonehaven Keep to the entry yard.  The "
                 "ceiling above is pierced with murder holes, and the walls "
                 "to either side contain arrow slits for archery."
             ],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.WEST: Exit(RoomEnum.BL_ENTRY_YARD),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_KEEP_GATEHOUSE),
             }),
    RoomEnum.BL_ENTRY_YARD:
        Room(ZoneEnum.KEEP,
             "Entry Yard", "an entry yard",
             [
                 "This is a small area that is paved with cobblestones.  It "
                 "forms a road of sorts along the southern edge of the keep "
                 "interior."
             ],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.NORTHEAST: Exit(RoomEnum.BL_N_GATEHOUSE_TOWER),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_GATEHOUSE_PASSAGE),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_EASTERN_WALK),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_STABLE),
             },
             room_pers=[
                 PersonEnum.BL_KEEP_CORPORAL_WATCH,
                 PersonEnum.BL_KEEP_YARD_SCRIBE,
                 PersonEnum.BL_KEEP_SENTRY,
             ],
             periodics=[
                 Periodic(
                     [
                         Condition(ConditionCheckEnum.LESS_THAN,
                                   TargetTypeEnum.PERCENT_CHANCE,
                                   value=15),
                     ],
                     [
                         Trigger(TriggerTypeEnum.ROOM_MESSAGE,
                                 "A woman bumps into you as she crosses "
                                 "the yard."),
                     ], 300),
                 Periodic(
                     [
                         Condition(ConditionCheckEnum.HAS,
                                   TargetTypeEnum.MOB_IN_ROOM,
                                   PersonEnum.BL_KEEP_CORPORAL_WATCH),
                         Condition(ConditionCheckEnum.LESS_THAN,
                                   TargetTypeEnum.PERCENT_CHANCE,
                                   value=25),
                     ],
                     [
                         Trigger(TriggerTypeEnum.ROOM_MESSAGE,
                                 "A lackey runs up and delivers a message "
                                 "to the corporal of the watch."),
                     ], 450),
             ]),
    RoomEnum.BL_N_GATEHOUSE_TOWER:
        Room(ZoneEnum.KEEP,
             "North Gatehouse Tower", "the north gatehouse tower",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.SOUTHWEST: Exit(RoomEnum.BL_ENTRY_YARD),
             }),
    RoomEnum.BL_STABLE:
        Room(ZoneEnum.KEEP,
             "Common Stable", "a common stable",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.EAST: Exit(RoomEnum.BL_ENTRY_YARD),
             }),
    RoomEnum.BL_EASTERN_WALK:
        Room(ZoneEnum.KEEP,
             "Eastern Walk", "the eastern walk",
             [
                 "You stand on a cobblestone paved walk which follows the "
                 "interior wall of the keep."
             ],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_ENTRY_YARD),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_S_GATEHOUSE_TOWER),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_SOUTHEASTERN_WALK),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_WAREHOUSE,
                                          DoorEnum.WAREHOUSE_DBL_DOOR),
             }),
    RoomEnum.BL_S_GATEHOUSE_TOWER:
        Room(ZoneEnum.KEEP,
             "South Gatehouse Tower", "the south gatehouse tower",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.WEST: Exit(RoomEnum.BL_EASTERN_WALK),
             }),
    RoomEnum.BL_WAREHOUSE:
        Room(ZoneEnum.KEEP,
             "Common Warehouse", "a common warehouse",
             [
                 "Visiting merchants and other travelers who have "
                 "quantities of goods are required to keep their materials "
                 "here until they are either sold to the persons at the "
                 "keep or taken elsewhere.  Stored here are several covered "
                 "carts, many boxes, barrels, and bales."
                 "Large rat droppings can be seen in several corners."
             ],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.EAST: Exit(RoomEnum.BL_EASTERN_WALK,
                                          DoorEnum.WAREHOUSE_DBL_DOOR),
             },
             periodics=[
                 Periodic(
                     [
                         Condition(ConditionCheckEnum.LESS_THAN,
                                   TargetTypeEnum.MOB_IN_ROOM,
                                   PersonEnum.MON_RAT, 1),
                         Condition(ConditionCheckEnum.LESS_THAN,
                                   TargetTypeEnum.PERCENT_CHANCE,
                                   value=100),
                     ],
                     [
                         Trigger(TriggerTypeEnum.ROOM_SPAWN,
                                 PersonEnum.MON_RAT),
                     ], 360),
             ]),
    RoomEnum.BL_SOUTHEASTERN_WALK:
        Room(ZoneEnum.KEEP,
             "South-Eastern Walk", "the south-eastern walk",
             [
                 "You stand on a cobblestone paved walk which follows the "
                 "interior wall of the keep."
             ],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_EASTERN_WALK),
                 DirectionEnum.SOUTHEAST: Exit(RoomEnum.BL_BAILIFF_TOWER),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_SOUTHERN_WALK),
             }),
    RoomEnum.BL_BAILIFF_TOWER:
        Room(ZoneEnum.KEEP,
             "Bailiff's Tower", "the Bailiff's tower",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.NORTHWEST: Exit(RoomEnum.BL_SOUTHEASTERN_WALK),
             }),
    RoomEnum.BL_SOUTHERN_WALK:
        Room(ZoneEnum.KEEP,
             "Southern Walk", "the southern walk",
             ["** TODO **"],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_SMITHY),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_SOUTHEASTERN_WALK),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_APARMENT_1),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_SOUTHERN_WALK_2),
             }),
    RoomEnum.BL_SMITHY:
        Room(ZoneEnum.KEEP,
             "The Smithy", "the smithy",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_SOUTHERN_WALK),
             }),
    RoomEnum.BL_APARMENT_1:
        Room(ZoneEnum.KEEP,
             "A Private Apartment", "a private apartment",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_SOUTHERN_WALK),
             }),
    RoomEnum.BL_SOUTHERN_WALK_2:
        Room(ZoneEnum.KEEP,
             "Southern Walk", "the southern walk",
             ["** TODO **"],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_MAIN_WALK),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_SOUTHERN_WALK),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_APARMENT_2),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_SOUTHERN_WALK_3),
             }),
    RoomEnum.BL_APARMENT_2:
        Room(ZoneEnum.KEEP,
             "A Private Apartment", "a private apartment",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_SOUTHERN_WALK_2),
             }),
    RoomEnum.BL_SOUTHERN_WALK_3:
        Room(ZoneEnum.KEEP,
             "Southern Walk", "the southern walk",
             ["** TODO **"],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.NORTHWEST: Exit(RoomEnum.BL_WEAPONSMITH),
                 DirectionEnum.NORTHEAST: Exit(RoomEnum.BL_PROVISIONS),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_SOUTHERN_WALK_2),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_APARMENT_3),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_SOUTHWESTERN_WALK),
             }),
    RoomEnum.BL_WEAPONSMITH:
        Room(ZoneEnum.KEEP,
             "The Weaponsmith", "the weaponsmith",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.SOUTHEAST: Exit(RoomEnum.BL_SOUTHERN_WALK_3),
             }),
    RoomEnum.BL_PROVISIONS:
        Room(ZoneEnum.KEEP,
             "Provisions Shop", "a provisions shop",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.SOUTHWEST: Exit(RoomEnum.BL_SOUTHERN_WALK_3),
             },
             room_pers=[
                 PersonEnum.BL_PROVISIONER,
             ]),
    RoomEnum.BL_APARMENT_3:
        Room(ZoneEnum.KEEP,
             "A Private Apartment", "a private apartment",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_SOUTHERN_WALK_3),
             }),
    RoomEnum.BL_SOUTHWESTERN_WALK:
        Room(ZoneEnum.KEEP,
             "South-Western Walk", "the south-western walk",
             ["** TODO **"],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.NORTHWEST: Exit(RoomEnum.BL_FOUNTAIN_SQUARE),
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_APARMENT_4),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_SOUTHERN_WALK_3),
                 DirectionEnum.SOUTHEAST: Exit(RoomEnum.BL_BANK),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_WATCH_TOWER),
             }),
    RoomEnum.BL_APARMENT_4:
        Room(ZoneEnum.KEEP,
             "A Private Apartment", "a private apartment",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_SOUTHWESTERN_WALK),
             }),
    RoomEnum.BL_BANK:
        Room(ZoneEnum.KEEP,
             "The Bank & Loan", "the bank & loan",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.NORTHWEST: Exit(RoomEnum.BL_SOUTHWESTERN_WALK),
             }),
    RoomEnum.BL_WATCH_TOWER:
        Room(ZoneEnum.KEEP,
             "Southwest Watch Tower", "the southwest watch tower",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_SOUTHWESTERN_WALK),
             }),
    RoomEnum.BL_FOUNTAIN_SQUARE:
        Room(ZoneEnum.KEEP,
             "Fountain Square", "fountain square",
             ["** TODO **"],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_TAVERN_MAINROOM),
                 DirectionEnum.SOUTHEAST: Exit(RoomEnum.BL_SOUTHWESTERN_WALK),
             }),
    RoomEnum.BL_TAVERN_MAINROOM:
        Room(ZoneEnum.KEEP,
             "The Tavern", "the tavern",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_FOUNTAIN_SQUARE),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_TAVERN_KITCHEN),
             }),
    RoomEnum.BL_TAVERN_KITCHEN:
        Room("Tavern Kitchen", "the tavern kitchen",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.WEST: Exit(RoomEnum.BL_TAVERN_MAINROOM),
                 DirectionEnum.UP: Exit(RoomEnum.BL_TAVERN_LOFT),
             }),
    RoomEnum.BL_TAVERN_LOFT:
        Room(ZoneEnum.KEEP,
             "Tavern Loft", "a loft above the tavern",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.DOWN: Exit(RoomEnum.BL_TAVERN_KITCHEN),
             }),
    RoomEnum.BL_MAIN_WALK:
        Room(ZoneEnum.KEEP,
             "Main Walk", "a main thorough fair",
             ["** TODO **"],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_SOUTHERN_WALK_2),
             }),


    # OUTSIDE KEEP
    RoomEnum.BL_ROAD_TO_KEEP:
        Room(ZoneEnum.FOREST,
             "Road to the Keep", "on a steep road",
             ["** TODO **"],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.WEST: Exit(RoomEnum.BL_KEEP_GATEHOUSE,
                                          DoorEnum.KEEP_DRAWBRIDGE),
             }),
}

# vim: tabstop=2 shiftwidth=2 expandtab:
