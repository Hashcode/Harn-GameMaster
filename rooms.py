# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Room Functions

import time
import copy

from global_defines import *
from utils import *
from db import *

ROOM_START = RoomEnum.BL_KEEP_GATEHOUSE
ROOM_RESPAWN = RoomEnum.BL_PRIEST_CHAMBER

def room_StartGame(player):
  while True:
    desc = ANSI.TEXT_BOLD + "CREATE" + ANSI.TEXT_NORMAL + " a new character " \
      "or " + ANSI.TEXT_BOLD + "RESTORE" + ANSI.TEXT_NORMAL + " a saved game"
    Player.Command = input("\n%s? " % desc).lower()
    if Player.Command == "restore":
      player.SetRoom(RoomEnum.GAME_RESTORE_SAVE)
      break
    elif Player.Command == "create":
      player.SetRoom(RoomEnum.GAME_CREATE_CHARACTER)
      break
  return RoomFuncResponse.SKIP

def room_RestoreSave(player):
  name = input("\nCharacter name: ")
  pwd = input("Password: ")
  
  print("\nPlease wait while saved data is loaded ...")
  ret = LoadPlayer(player, name, pwd)
  if not ret:
    print("Unable to find save data for %s." % name)
    player.SetRoom(RoomEnum.GAME_START)
    return RoomFuncResponse.SKIP

  print("Loaded.")
  ResetPlayerStats(player)
  player.SetRoom(player.Room)
  return RoomFuncResponse.SKIP

def room_CreateCharacter(player):
  player.Name = input("\nChoose a character name: ")
  if len(player.Name) < 3 or len(player.Name) > 20:
    print("\nCharacter name needs between 3 and 20 characters long.")
    return RoomFuncResponse.SKIP

  if ExistsDB(player.Name):
    print("\nCharacter aready exists.")
    player.SetRoom(RoomEnum.GAME_START)
    return RoomFuncResponse.SKIP

  print("\nYour password is used to encrypt your SAVE data.")
  print("It should NOT be a password used for anything important.")
  player.Password = input("\nEnter a password: ").upper()
  if len(player.Password) < 3 or len(player.Password) > 10:
    print("\nPassword needs to be between 3 and 10 characters long.")
    return RoomFuncResponse.SKIP

  player.SetRoom(ROOM_START)
  if not actionSave(player, rooms):
    return RoomFuncResponse.SKIP

  ResetPlayerStats(player)

  print("\nGood luck, %s!" % (player.Name))
  return RoomFuncResponse.SKIP

rooms = {
  # GAME ROOMS
  RoomEnum.GAME_START:
    Room("Welcome to Hashcode's Gameshop!", "",
      "Take your characters on exciting journeys in the gritty world of the\n" \
      "HârnMaster Game System in classic Dungeon's & Dragons(tm) modules.\n" \
      "\n" \
      "During your adventures you will accumulate skills, items and wealth.\n" \
      "Make sure to SAVE along the way to ensure your progress won't be lost.",
      room_StartGame),
  RoomEnum.GAME_RESTORE_SAVE:
    Room("Restore Saved Progress", "",
      "", room_RestoreSave),
  RoomEnum.GAME_CREATE_CHARACTER:
    Room("Create a New Character", "",
      "", room_CreateCharacter),

  # KEEP ON THE BORDERLANDS
  RoomEnum.BL_KEEP_GATEHOUSE:
    Room("The Main Gatehouse to Stonehaven Keep",
      "the main gatehouse",
      "Two 30' high towers complete with battlements, flank a 20' high\n" \
      "gatehouse. All have holes for bow and crossbow fire. A deep crevice\n" \
      "in front of the place is spanned by a drawbridge.\n" \
      "\n" \
      "There is a portcullis at the entry way to the gatehouse, inside of\n" \
      "which a passage leads to large gates.  The passage is about 10' wide\n" \
      "and 10' high.\n" \
      "\n" \
      "It is obvious that the building is constructed of great blocks of\n" \
      "solid granite, undoubtedly common throughout the entire fortress.",
      exits={
        DirectionEnum.WEST: Exit(RoomEnum.BL_GATEHOUSE_PASSAGE),
      }),
  RoomEnum.BL_PRIEST_CHAMBER:
    Room("The Priest's Chamber",
      "the priest's chamber",
      "The well-appointed chamber you are standing in radiates warmth from\n" \
      "a cozy fire roaring in a small western alcove.  While spartan in\n" \
      "furnishings, a well-made armoire sits in a corner as well as a tidy\n" \
      "bed along one wall. Several religious paintings are hung on the walls.",
      exits=None),
  RoomEnum.BL_GATEHOUSE_PASSAGE:
    Room("Gatehouse Passage",
      "a gatehouse passage",
      "This 10' wide and 10' high passage leads from the main gatehouse of\n" \
      "Stonehaven Keep to the entry yard.  The ceiling above is pierced with\n" \
      "murder holes, and the walls to either side contain arrow slits for\n" \
      "archery.",
      exits={
        DirectionEnum.WEST: Exit(RoomEnum.BL_ENTRY_YARD),
        DirectionEnum.EAST: Exit(RoomEnum.BL_KEEP_GATEHOUSE),
      }),
  RoomEnum.BL_ENTRY_YARD:
    Room("Entry Yard",
      "an entry yard",
      "This is a small area that is paved with cobblestones.  It forms a road\n" \
      "of sorts along the southern edge of the keep interior.",
      exits={
        DirectionEnum.NORTHEAST: Exit(RoomEnum.BL_NORTH_GATEHOUSE_TOWER),
        DirectionEnum.EAST: Exit(RoomEnum.BL_GATEHOUSE_PASSAGE),
        DirectionEnum.SOUTH: Exit(RoomEnum.BL_EASTERN_WALK),
        DirectionEnum.WEST: Exit(RoomEnum.BL_STABLE),
      }),
  RoomEnum.BL_NORTH_GATEHOUSE_TOWER:
    Room("North Gatehouse Tower",
      "the north gatehouse tower",
      "** TODO **",
      exits={
        DirectionEnum.SOUTHWEST: Exit(RoomEnum.BL_ENTRY_YARD),
      }),
  RoomEnum.BL_STABLE:
    Room("Common Stable",
      "a common stable",
      "** TODO **",
      exits={
        DirectionEnum.EAST: Exit(RoomEnum.BL_ENTRY_YARD),
      }),
  RoomEnum.BL_EASTERN_WALK:
    Room("Eastern Walk",
      "the eastern walk",
      "You stand on a cobblestone paved walk which follows the interior wall\n" \
      "of the keep.",
      exits={
        DirectionEnum.NORTH: Exit(RoomEnum.BL_ENTRY_YARD),
        DirectionEnum.EAST: Exit(RoomEnum.BL_SOUTH_GATEHOUSE_TOWER),
        DirectionEnum.SOUTH: Exit(RoomEnum.BL_SOUTHEASTERN_WALK),
        DirectionEnum.WEST: Exit(RoomEnum.BL_WAREHOUSE),
      }),
  RoomEnum.BL_SOUTH_GATEHOUSE_TOWER:
    Room("South Gatehouse Tower",
      "the south gatehouse tower",
      "** TODO **",
      exits={
        DirectionEnum.WEST: Exit(RoomEnum.BL_EASTERN_WALK),
      }),
  RoomEnum.BL_WAREHOUSE:
    Room("Common Warehouse",
      "a common warehouse",
      "** TODO **",
      exits={
        DirectionEnum.EAST: Exit(RoomEnum.BL_EASTERN_WALK),
      }),
  RoomEnum.BL_SOUTHEASTERN_WALK:
    Room("South-Eastern Walk",
      "the south-eastern walk",
      "You stand on a cobblestone paved walk which follows the interior wall\n" \
      "of the keep.",
      exits={
        DirectionEnum.NORTH: Exit(RoomEnum.BL_EASTERN_WALK),
        DirectionEnum.SOUTHEAST: Exit(RoomEnum.BL_BAILIFF_TOWER),
      }),
  RoomEnum.BL_BAILIFF_TOWER:
    Room("Bailiff's Tower",
      "the Bailiff's tower",
      "** TODO **",
      exits={
        DirectionEnum.NORTHWEST: Exit(RoomEnum.BL_SOUTHEASTERN_WALK),
      }),
}

# vim: tabstop=2 shiftwidth=2 expandtab:
