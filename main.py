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

from console import (ANSI, ConsoleManager)
from gamedata import (GameData)
from global_defines import (quests, Player, RoomEnum, RoomFuncResponse)

TestMode = True

ROOM_START = RoomEnum.BL_KEEP_GATEHOUSE
ROOM_RESPAWN = RoomEnum.BL_PRIEST_CHAMBER

seed()
print(ANSI.CLEAR + ANSI.RESET_CURSOR, end='')

cm = ConsoleManager()
cm.start()
GameData.SetConsole(cm)

player = Player("Unknown")
player.SetRoom(RoomEnum.GAME_START)
GameData.SetPlayer(player)

from items import items
GameData.SetItems(items)
GameData.SetQuests(quests)
from person import persons
GameData.SetPersons(persons)
from rooms import (doors, rooms)
GameData.SetDoors(doors)
GameData.SetRooms(rooms)
GameData.ROOM_START = ROOM_START
GameData.ROOM_RESPAWN = ROOM_RESPAWN

from utils import (processWeather, processTime, processConditions, processTriggers,
                   printRoomDescription, printRoomObjects, roomTalkTrigger,
                   prompt)

GameData.SetProcessConditions(processConditions)
GameData.SetProcessTriggers(processTriggers)
GameData.SetProcessTime(processTime)
GameData.SetProcessWeather(processWeather)

from combat import combat

while True:
  res = RoomFuncResponse.NONE
  printRoomDescription(player.Room)

  # Call Room Function
  if rooms[player.Room].Function is not None:
    # Return value means: True == Print Prompt, False == Skip Prompt
    res = rooms[player.Room].Function()

  if res == RoomFuncResponse.SKIP:
    continue

  # Check for events
  GameData.ProcessEvents()

  printRoomObjects(player.Room)
  roomTalkTrigger("on_enter")

  # Check if the room persons need to attack
  enemies = GameData.ProcessRoomCombat()
  if len(enemies) > 0:
    combat(player, enemies)
    continue

  # Handle Commands
  if res != RoomFuncResponse.NO_PROMPT:
    prompt()

cm.SetNormalTerm()


# vim: set tabstop=2 shiftwidth=2 expandtab:
