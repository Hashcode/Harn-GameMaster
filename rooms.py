# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Room Functions

import time
import copy

from global_defines import *
from utils import *
from db import *

def room_StartGame(player):
  while True:
    desc = ANSI.TEXT_BOLD + "CREATE" + ANSI.TEXT_NORMAL + " a new character " \
      "or " + ANSI.TEXT_BOLD + "RESTORE" + ANSI.TEXT_NORMAL + " a saved game"
    Player.Command = input("\n%s? " % desc).lower()
    if Player.Command == "restore":
      player.SetRoom(RoomEnum.RESTORE_SAVE)
      break
    elif Player.Command == "create":
      player.SetRoom(RoomEnum.CREATE_CHARACTER)
      break
  return RoomFuncResponse.SKIP

def room_RestoreSave(player):
  name = input("\nCharacter name: ")
  pwd = input("Password: ")
  
  print("\nPlease wait while saved data is loaded ...")
  ret = LoadPlayer(player, name, pwd)
  if not ret:
    print("Unable to find save data for %s." % name)
    player.SetRoom(RoomEnum.START_GAME)
    return RoomFuncResponse.SKIP

  print("Loaded.")
  ResetPlayerStats(player)
  player.SetRoom(player.Room)
  return RoomFuncResponse.SKIP

def room_CreateCharacter(player):
  player.Name = input("\nCharacter name: ")
  if len(player.Name) > 30:
    print("\nCharacter name needs to be less than 30 characters.")
    return RoomFuncResponse.SKIP

  if ExistsDB(player.Name):
    print("\nCharacter aready exists.")
    player.SetRoom(RoomEnum.START_GAME)
    return RoomFuncResponse.SKIP

  ResetPlayerStats(player)

  print("\nGood luck, %s!" % (player.Name))
  player.SetRoom(RoomEnum.BL_BEGIN)
  return RoomFuncResponse.SKIP

def room_UserDeath(player):
  if player.Lives > 0:
    plural = ""
    if player.Lives > 1:
      plural = "s"

    print("You have %s live%s left.\nWould you like to RESPAWN, or END the game?"
          % (player.Lives, plural))
    while True:
      player.Command = input("\nType your command: ").lower()
      if player.Command == "respawn":
        print("\nYou have been revived.")
        player.SetRoom(RoomEnum.BL_RESPAWN)
        return RoomFuncResponse.SKIP
      elif player.Command == "end":
        print("\nVery well. Until next time, %s" % (player.Name))
        exit()
  else:
    print("You have lost your last life!")
    print("\nDeleting saved progress ...")
    DeleteDB(player.Name)
    print("Done.")
    print("\nFarewell, %s." % (player.Name))
    exit()

rooms = {
  # GAME ROOMS
  RoomEnum.DEAD:
    Room("", "",
      "", room_UserDeath),
  RoomEnum.START_GAME:
    Room("Welcome to Hashcode's Gameshop!", "",
      "Take your characters on exciting journeys in the gritty world of the\n" \
      "HârnMaster Game System in classic Dungeon's & Dragons(tm) modules.\n" \
      "\n" \
      "During your adventures you will accumulate skills, items and wealth.\n" \
      "Make sure to SAVE along the way to ensure your progress won't be lost.",
      room_StartGame),
  RoomEnum.RESTORE_SAVE:
    Room("Restore Saved Progress", "",
      "", room_RestoreSave),
  RoomEnum.CREATE_CHARACTER:
    Room("Create a New Character", "",
      "", room_CreateCharacter),

  # KEEP ON THE BORDERLANDS
  RoomEnum.BL_BEGIN:
    Room("The Main Gatehouse to Stonehaven Keep",
      "gatehouse to Stonehaven Keep",
      "Two 30' high towers complete with battlements, flank a 20' high\n" \
      "gatehouse. All have holes for bow and crossbow fire. A deep crevice\n" \
      "in front of the place is spanned by a drawbridge.\n" \
      "\n" \
      "There is a portcullis at the entry way to the gatehouse, inside of\n" \
      "which a passage leads to large gates.  The passage is about 10' wide\n" \
      "and 10' high. The ceiling above is pierced with murder holes, and\n" \
      "the walls to either side contain arrow slits for archers.\n" \
      "\n" \
      "It is obvious that the building is constructed of great blocks of\n" \
      "solid granite, undoubtedly common throughout the entire fortress.",
      exits=None),
  RoomEnum.BL_RESPAWN:
    Room("The Priest's Chamber",
      "priest's chamber",
      "The well-appointed chamber you are standing in radiates warmth from\n" \
      "a cozy fire roaring in a small western alcove.  While spartan in\n" \
      "furnishings, a well-made armoire sits in a corner as well as a tidy\n" \
      "bed along one wall. Several religious paintings are hung on the walls.",
      exits=None),
}

# vim: tabstop=2 shiftwidth=2 expandtab:
