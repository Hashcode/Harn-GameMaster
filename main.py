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

TestMode = True

ROOM_START = RoomEnum.BL_KEEP_GATEHOUSE
ROOM_RESPAWN = RoomEnum.BL_PRIEST_CHAMBER

seed()
print(ANSI.CLEAR + ANSI.RESET_CURSOR, end='')

player = Player("Unknown")
player.SetRoom(RoomEnum.GAME_START)
GameData.SetPlayer(player)

from items import items
GameData.SetItems(items)
from person import persons
GameData.SetPersons(persons)
from rooms import rooms
GameData.SetRooms(rooms)
GameData.ROOM_START = ROOM_START
GameData.ROOM_RESPAWN = ROOM_RESPAWN

from utils import (printRoomDescription, printRoomObjects, prompt)
from combat import combat


if TestMode:
  player.AddItem(ItemEnum.WEAPON_CLUB, ItemLink(1, equip=True))

  player.AddItem(ItemEnum.ARMOR_TUNIC_CLOTH, ItemLink(1, equip=True))
  player.AddItem(ItemEnum.ARMOR_LEGGINGS_CLOTH, ItemLink(1, equip=True))

while True:
  res = RoomFuncResponse.NONE
  printRoomDescription(player.Room)

  # Call Room Function
  if rooms[player.Room].Function is not None:
    # Return value means: True == Print Prompt, False == Skip Prompt
    res = rooms[player.Room].Function()

  if res == RoomFuncResponse.SKIP:
    continue

  # Check for room events
  GameData.ProcessRoomEvents()

  printRoomObjects(player.Room)

  # Check if the room persons need to attack
  enemies = GameData.ProcessRoomCombat()
  if len(enemies) > 0:
    combat(player, enemies)
    continue

  # Handle Commands
  if res != RoomFuncResponse.NO_PROMPT:
    prompt()
    if player.Command != "":
      print("\n%sYou cannot do that here.%s" %
            (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))

# vim: set tabstop=2 shiftwidth=2 expandtab:
