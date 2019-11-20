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
    Player.Command = input("CREATE a new character or RESTORE a saved game? ").lower()
    if Player.Command == "restore":
      player.SetRoom(RoomEnum.RESTORE_SAVE)
      break
    elif Player.Command == "create":
      player.SetRoom(RoomEnum.CREATE_CHARACTER)
      break
  return RoomFuncResponse.SKIP

def room_RestoreSave(player):
  name = input("Character name: ")
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
  player.Name = input("Character name: ")
  if len(player.Name) > 30:
    print("\nCharacter name needs to be less than 30 characters.")
    return RoomFuncResponse.SKIP

  if ExistsDB(player.Name):
    print("\nCharacter aready exists.")
    player.SetRoom(RoomEnum.START_GAME)
    return RoomFuncResponse.SKIP

  ResetPlayerStats(player)

  print("\nGood luck, %s!" % (player.Name))
  player.SetRoom(RoomEnum.OUTSIDE_HUT)
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
        player.SetRoom(room_HutOut)
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
  RoomEnum.DEAD:
    Room("", "", room_UserDeath),
  RoomEnum.START_GAME:
    Room("", "Welcome to Legend of the Red Dragon!", room_StartGame),
  RoomEnum.RESTORE_SAVE:
    Room("", "Restore saved progress", room_RestoreSave),
  RoomEnum.CREATE_CHARACTER:
    Room("", "Create a new character", room_CreateCharacter),
  RoomEnum.OUTSIDE_HUT:
    Room("the outside of a small hut",
        "You are standing outside the door to the High Chronicler's hut, to the north. It is snowing.",
        exits={
          DirectionEnum.SOUTH: Exit(RoomEnum.CLEARING),
          DirectionEnum.WEST: Exit(RoomEnum.ICY_MOUNTAINS),
        }),
  RoomEnum.CLEARING:
    Room("a small clearing",
        "The trees rustle as a gentle wind blows through this small clearing in the forest.",
        exits={
          DirectionEnum.NORTH: Exit(RoomEnum.OUTSIDE_HUT),
        }),
  RoomEnum.ICY_MOUNTAINS:
    Room("the edge of icy mountains",
        "You stand at the edge of an icy mountain range.",
        enemy=EnemyEnum.RAT,
        exits={
          DirectionEnum.WEST: Exit(RoomEnum.DARK_CAVE),
          DirectionEnum.EAST: Exit(RoomEnum.OUTSIDE_HUT),
        }),
  RoomEnum.DARK_CAVE:
    Room("the entrance to a dark cave",
        "The darkness closes in around you as you enter the cave.  The air smells of ash and burnt stone.",
        exits={
          DirectionEnum.WEST: Exit(RoomEnum.CHARLOK_PIT),
          DirectionEnum.EAST: Exit(RoomEnum.ICY_MOUNTAINS),
        }),
  RoomEnum.CHARLOK_PIT:
    Room("the center of a circular pit",
        "You are standing in the middle of a circular pit.",
        enemy=EnemyEnum.CHARLOK,
        exits={
          DirectionEnum.EAST: Exit(RoomEnum.DARK_CAVE),
        }),
}

# vim: tabstop=2 shiftwidth=2 expandtab:
