# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Room Functions

from global_defines import (PersonEnum, Player, ItemEnum, DoorEnum, Door,
                            DoorState, DirectionEnum,
                            RoomFuncResponse, RoomEnum, Exit, Room, RoomSpawn,
                            ANSI, GameData)
from utils import (actionSave)
from db import (ExistsDB, LoadPlayer)


def room_StartGame():
  player = GameData.GetPlayer()
  while True:
    desc = ANSI.TEXT_BOLD + "CREATE" + ANSI.TEXT_NORMAL + \
        " a new character or " + ANSI.TEXT_BOLD + "RESTORE" + \
        ANSI.TEXT_NORMAL + " a saved game"
    Player.Command = input("\n%s? " % desc).lower()
    if Player.Command == "restore":
      player.SetRoom(RoomEnum.GAME_RESTORE_SAVE)
      break
    elif Player.Command == "create":
      player.SetRoom(RoomEnum.GAME_CREATE_CHARACTER)
      break
  return RoomFuncResponse.SKIP


def room_RestoreSave():
  player = GameData.GetPlayer()
  name = input("\nCharacter name: ")
  pwd = input("Password: ")

  print("\nPlease wait while saved data is loaded ...")
  ret = LoadPlayer(player, name, pwd)
  if not ret:
    print("%sUnable to find save data for %s!%s" %
          (ANSI.TEXT_BOLD, name, ANSI.TEXT_NORMAL))
    player.SetRoom(RoomEnum.GAME_START)
    return RoomFuncResponse.SKIP

  print("Loaded.")
  player.ResetStats()
  player.SetRoom(player.Room)
  return RoomFuncResponse.SKIP


def room_CreateCharacter():
  player = GameData.GetPlayer()
  player.Name = input("\nChoose a character name: ")
  if len(player.Name) < 3 or len(player.Name) > 20:
    print("\nCharacter name needs between 3 and 20 characters long.")
    return RoomFuncResponse.SKIP

  print("\nA password is used to encrypt your SAVE data.")
  print("It should NOT be a password used for anything important.")
  player.Password = input("\nEnter a password: ").upper()
  if len(player.Password) < 3 or len(player.Password) > 10:
    print("\nPassword needs to be between 3 and 10 characters long.")
    return RoomFuncResponse.SKIP

  if ExistsDB(player.Name, player.Password):
    print("\nCharacter aready exists.")
    player.SetRoom(RoomEnum.GAME_START)
    return RoomFuncResponse.SKIP

  player.GenAttr()
  player.GenSkills()
  player.ResetStats()
  player.SetRoom(GameData.ROOM_START)

  print("\nSaving character ...")
  if not actionSave():
    return RoomFuncResponse.SKIP
  print("Done.")

  print("\nGood luck, %s!" % (player.Name))
  return RoomFuncResponse.SKIP


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
        Room("Welcome to Harn GameMaster!", "",
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
        Room("Restore Saved Progress", func=room_RestoreSave),
    RoomEnum.GAME_CREATE_CHARACTER:
        Room("Create a New Character", func=room_CreateCharacter),

    # KEEP ON THE BORDERLANDS
    RoomEnum.BL_KEEP_GATEHOUSE:
        Room("The Main Gatehouse to Stonehaven Keep", "the main gatehouse",
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
             exits={
                 DirectionEnum.WEST: Exit(RoomEnum.BL_GATEHOUSE_PASSAGE),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_ROAD_TO_KEEP,
                                          DoorEnum.KEEP_DRAWBRIDGE),
             },
             room_pers=[
                 PersonEnum.BL_KEEP_GUARD,
             ]),
    RoomEnum.BL_PRIEST_CHAMBER:
        Room("The Priest's Chamber", "the priest's chamber",
             [
                 "The well-appointed chamber you are standing in radiates "
                 "warmth from a cozy fire roaring in a small western alcove. "
                 "While spartan in furnishings, a well-made armoire sits in "
                 "a corner as well as a tidy bed along one wall. Several "
                 "religious paintings are hung on the walls."
             ],
             exits=None),
    RoomEnum.BL_GATEHOUSE_PASSAGE:
        Room("Gatehouse Passage", "a gatehouse passage",
             [
                 "This 10' wide and 10' high passage leads from the main "
                 "gatehouse of Stonehaven Keep to the entry yard.  The "
                 "ceiling above is pierced with murder holes, and the walls "
                 "to either side contain arrow slits for archery."
             ],
             exits={
                 DirectionEnum.WEST: Exit(RoomEnum.BL_ENTRY_YARD),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_KEEP_GATEHOUSE),
             }),
    RoomEnum.BL_ENTRY_YARD:
        Room("Entry Yard", "an entry yard",
             [
                 "This is a small area that is paved with cobblestones.  It "
                 "forms a road of sorts along the southern edge of the keep "
                 "interior."
             ],
             exits={
                 DirectionEnum.NORTHEAST: Exit(RoomEnum.BL_N_GATEHOUSE_TOWER),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_GATEHOUSE_PASSAGE),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_EASTERN_WALK),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_STABLE),
             }),
    RoomEnum.BL_N_GATEHOUSE_TOWER:
        Room("North Gatehouse Tower", "the north gatehouse tower",
             ["** TODO **"],
             exits={
                 DirectionEnum.SOUTHWEST: Exit(RoomEnum.BL_ENTRY_YARD),
             }),
    RoomEnum.BL_STABLE:
        Room("Common Stable", "a common stable",
             ["** TODO **"],
             exits={
                 DirectionEnum.EAST: Exit(RoomEnum.BL_ENTRY_YARD),
             }),
    RoomEnum.BL_EASTERN_WALK:
        Room("Eastern Walk", "the eastern walk",
             [
                 "You stand on a cobblestone paved walk which follows the "
                 "interior wall of the keep."
             ],
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_ENTRY_YARD),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_S_GATEHOUSE_TOWER),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_SOUTHEASTERN_WALK),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_WAREHOUSE,
                                          DoorEnum.WAREHOUSE_DBL_DOOR),
             }),
    RoomEnum.BL_S_GATEHOUSE_TOWER:
        Room("South Gatehouse Tower", "the south gatehouse tower",
             ["** TODO **"],
             exits={
                 DirectionEnum.WEST: Exit(RoomEnum.BL_EASTERN_WALK),
             }),
    RoomEnum.BL_WAREHOUSE:
        Room("Common Warehouse", "a common warehouse",
             [
                 "Visiting merchants and other travelers who have "
                 "quantities of goods are required to keep their materials "
                 "here until they are either sold to the persons at the "
                 "keep or taken elsewhere.  Stored here are several covered "
                 "carts, many boxes, barrels, and bales."
                 "Large rat droppings can be seen in several corners."
             ],
             exits={
                 DirectionEnum.EAST: Exit(RoomEnum.BL_EASTERN_WALK,
                                          DoorEnum.WAREHOUSE_DBL_DOOR),
             },
             spawns=[
                 RoomSpawn(PersonEnum.MON_RAT, 100, 1, 360),
             ]),
    RoomEnum.BL_SOUTHEASTERN_WALK:
        Room("South-Eastern Walk", "the south-eastern walk",
             [
                 "You stand on a cobblestone paved walk which follows the "
                 "interior wall of the keep."
             ],
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_EASTERN_WALK),
                 DirectionEnum.SOUTHEAST: Exit(RoomEnum.BL_BAILIFF_TOWER),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_SOUTHERN_WALK),
             }),
    RoomEnum.BL_BAILIFF_TOWER:
        Room("Bailiff's Tower", "the Bailiff's tower",
             ["** TODO **"],
             exits={
                 DirectionEnum.NORTHWEST: Exit(RoomEnum.BL_SOUTHEASTERN_WALK),
             }),
    RoomEnum.BL_SOUTHERN_WALK:
        Room("Southern Walk", "the southern walk",
             ["** TODO **"],
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_SMITHY),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_SOUTHEASTERN_WALK),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_APARMENT_1),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_SOUTHERN_WALK_2),
             }),
    RoomEnum.BL_SMITHY:
        Room("The Smithy", "the smithy",
             ["** TODO **"],
             exits={
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_SOUTHERN_WALK),
             }),
    RoomEnum.BL_APARMENT_1:
        Room("A Private Apartment", "a private apartment",
             ["** TODO **"],
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_SOUTHERN_WALK),
             }),
    RoomEnum.BL_SOUTHERN_WALK_2:
        Room("Southern Walk", "the southern walk",
             ["** TODO **"],
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_MAIN_WALK),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_SOUTHERN_WALK),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_APARMENT_2),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_SOUTHERN_WALK_3),
             }),
    RoomEnum.BL_APARMENT_2:
        Room("A Private Apartment", "a private apartment",
             ["** TODO **"],
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_SOUTHERN_WALK_2),
             }),
    RoomEnum.BL_SOUTHERN_WALK_3:
        Room("Southern Walk", "the southern walk",
             ["** TODO **"],
             exits={
                 DirectionEnum.NORTHWEST: Exit(RoomEnum.BL_WEAPONSMITH),
                 DirectionEnum.NORTHEAST: Exit(RoomEnum.BL_PROVISIONS),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_SOUTHERN_WALK_2),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_APARMENT_3),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_SOUTHWESTERN_WALK),
             }),
    RoomEnum.BL_WEAPONSMITH:
        Room("The Weaponsmith", "the weaponsmith",
             ["** TODO **"],
             exits={
                 DirectionEnum.SOUTHEAST: Exit(RoomEnum.BL_SOUTHERN_WALK_3),
             }),
    RoomEnum.BL_PROVISIONS:
        Room("Provisions Shop", "a provisions shop",
             ["** TODO **"],
             exits={
                 DirectionEnum.SOUTHWEST: Exit(RoomEnum.BL_SOUTHERN_WALK_3),
             },
             room_pers=[
                 PersonEnum.BL_PROVISIONER,
             ]),
    RoomEnum.BL_APARMENT_3:
        Room("A Private Apartment", "a private apartment",
             ["** TODO **"],
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_SOUTHERN_WALK_3),
             }),
    RoomEnum.BL_SOUTHWESTERN_WALK:
        Room("South-Western Walk", "the south-western walk",
             ["** TODO **"],
             exits={
                 DirectionEnum.NORTHWEST: Exit(RoomEnum.BL_FOUNTAIN_SQUARE),
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_APARMENT_4),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_SOUTHERN_WALK_3),
                 DirectionEnum.SOUTHEAST: Exit(RoomEnum.BL_BANK),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_WATCH_TOWER),
             }),
    RoomEnum.BL_APARMENT_4:
        Room("A Private Apartment", "a private apartment",
             ["** TODO **"],
             exits={
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_SOUTHWESTERN_WALK),
             }),
    RoomEnum.BL_BANK:
        Room("The Bank & Loan", "the bank & loan",
             ["** TODO **"],
             exits={
                 DirectionEnum.NORTHWEST: Exit(RoomEnum.BL_SOUTHWESTERN_WALK),
             }),
    RoomEnum.BL_WATCH_TOWER:
        Room("Southwest Watch Tower", "the southwest watch tower",
             ["** TODO **"],
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_SOUTHWESTERN_WALK),
             }),
    RoomEnum.BL_FOUNTAIN_SQUARE:
        Room("Fountain Square", "fountain square",
             ["** TODO **"],
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_TAVERN_MAINROOM),
                 DirectionEnum.SOUTHEAST: Exit(RoomEnum.BL_SOUTHWESTERN_WALK),
             }),
    RoomEnum.BL_TAVERN_MAINROOM:
        Room("The Tavern", "the tavern",
             ["** TODO **"],
             exits={
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_FOUNTAIN_SQUARE),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_TAVERN_KITCHEN),
             }),
    RoomEnum.BL_TAVERN_KITCHEN:
        Room("Tavern Kitchen", "the tavern kitchen",
             ["** TODO **"],
             exits={
                 DirectionEnum.WEST: Exit(RoomEnum.BL_TAVERN_MAINROOM),
                 DirectionEnum.UP: Exit(RoomEnum.BL_TAVERN_LOFT),
             }),
    RoomEnum.BL_TAVERN_LOFT:
        Room("Tavern Loft", "a loft above the tavern",
             ["** TODO **"],
             exits={
                 DirectionEnum.DOWN: Exit(RoomEnum.BL_TAVERN_KITCHEN),
             }),
    RoomEnum.BL_MAIN_WALK:
        Room("Main Walk", "a main thorough fair",
             ["** TODO **"],
             exits={
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_SOUTHERN_WALK_2),
             }),


    # OUTSIDE KEEP
    RoomEnum.BL_ROAD_TO_KEEP:
        Room("Road to the Keep", "on a steep road",
             ["** TODO **"],
             exits={
                 DirectionEnum.WEST: Exit(RoomEnum.BL_KEEP_GATEHOUSE,
                                          DoorEnum.KEEP_DRAWBRIDGE),
             }),
}

# vim: tabstop=2 shiftwidth=2 expandtab:
