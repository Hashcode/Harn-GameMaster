# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Game System:
# Based on "HârnMaster Third Edition"
# Copyright (c) 1986 - 2003 N. Robin Crossby & Columbia Games, Inc.
# By N. Robin Crossby and Tom Dalgliesh

# Adventure Setting:
# Based on "The Keep on the Borderlands"
# Copyright (c) 1980, 1981 - TSR Hobbies, Inc.
# By Gary Gygax

# Main setup

from random import seed

from global_defines import (ItemEnum, ItemLink, Player,
                            RoomEnum, RoomFuncResponse, ANSI, GameData)
from utils import (printRoomDescription, printRoomObjects, prompt)
from items import items
from person import persons
from rooms import rooms
from combat import combat

TestMode = True

ROOM_START = RoomEnum.BL_KEEP_GATEHOUSE
ROOM_RESPAWN = RoomEnum.BL_PRIEST_CHAMBER

seed()
print(ANSI.CLEAR + ANSI.RESET_CURSOR, end='')

player = Player("Unknown")
player.SetRoom(RoomEnum.GAME_START)

GameData.SetItems(items)
GameData.SetPersons(persons)
GameData.SetRooms(rooms)
GameData.ROOM_START = ROOM_START
GameData.ROOM_RESPAWN = ROOM_RESPAWN


if TestMode:
  player.AddItem(ItemEnum.WEAPON_CLUB, ItemLink(1, equip=True))

  player.AddItem(ItemEnum.ARMOR_TUNIC_CLOTH, ItemLink(1, equip=True))
  player.AddItem(ItemEnum.ARMOR_LEGGINGS_CLOTH, ItemLink(1, equip=True))

while True:
  enemies = []
  res = RoomFuncResponse.NONE
  printRoomDescription(player.Room, rooms)

  # Call Room Function
  if rooms[player.Room].Function is not None:
    # Return value means: True == Print Prompt, False == Skip Prompt
    res = rooms[player.Room].Function(player)

  if res == RoomFuncResponse.SKIP:
    continue

  # Check for room events
  GameData.ProcessRoomEvents()

  printRoomObjects(player.Room, rooms)

  # Check if the room persons need to attack
  count = 0
  for x in rooms[player.Room].Persons:
    if x.IsAggressive():
      count += 1
      if count == 1:
        print("")
      enemies.append(x)
      print("%s%s attacks you!%s" %
            (ANSI.TEXT_BOLD, x.Name.capitalize(),
             ANSI.TEXT_NORMAL))
    if player.CombatTarget is not None:
      if player.CombatTarget == x.UUID:
        print("\nYou attack %s!" % x.Name)
        enemies.append(x)
        player.CombatTarget = None

  if len(enemies) > 0:
    combat(player, enemies)
    continue

  # Handle Commands
  if res != RoomFuncResponse.NO_PROMPT:
    prompt(player, rooms)
    if player.Command != "":
      print("\n%sYou cannot do that here.%s" %
            (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))

# vim: set tabstop=2 shiftwidth=2 expandtab:
