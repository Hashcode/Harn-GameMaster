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

import random
import time
import calendar

from global_defines import (roll, ItemEnum, ItemLink, Player,
                            PERS_COMBAT, PERS_AGGRESSIVE,
                            RoomEnum, RoomFuncResponse, ANSI)
from utils import (ResetPlayerStats, printRoomDescription, printRoomObjects,
                   prompt)
from rooms import rooms
from person import persons
from combat import combat

TestMode = True

ROOM_RESPAWN = RoomEnum.BL_PRIEST_CHAMBER

random.seed()
print(ANSI.CLEAR + ANSI.RESET_CURSOR, end='')

player = Player("Unknown")
player.SetRoom(RoomEnum.GAME_START)

if TestMode:
  ResetPlayerStats(player)
  player.AddItem(ItemEnum.WEAPON_DAGGER, ItemLink(1))

  player.AddItem(ItemEnum.ARMOR_HALFHELM_LEATHER_RING, ItemLink(1))
  player.AddItem(ItemEnum.ARMOR_TUNIC_CLOTH, ItemLink(1))
  player.AddItem(ItemEnum.ARMOR_LEGGINGS_CLOTH, ItemLink(1))
  player.AddItem(ItemEnum.ARMOR_SHOES_LEATHER, ItemLink(1))
  player.AddItem(ItemEnum.ARMOR_COWL_MAIL, ItemLink(1))

  player.AddItem(ItemEnum.RING_ATTACK_SILVER, ItemLink(1))
  player.AddItem(ItemEnum.MISC_STONE, ItemLink(2))

while True:
  combat_flag = False
  res = RoomFuncResponse.NONE
  printRoomDescription(player.Room, rooms)

  # Call Room Function
  if not rooms[player.Room].Function is None:
    # Return value means: True == Print Prompt, False == Skip Prompt
    res = rooms[player.Room].Function(player)

  if res == RoomFuncResponse.SKIP:
    continue

  # Check for room spawns
  if not rooms[player.Room].Spawns is None:
    for s in rooms[player.Room].Spawns:
      seconds = calendar.timegm(time.gmtime())
      if s.LastSpawnCheck + s.SpawnDelaySeconds >= seconds:
        continue
      s.LastSpawnCheck = seconds
      count = 0
      for p in rooms[player.Room].Persons:
        if p.Person == s.Person:
          count += 1
      if count < s.MaxQuantity:
        if roll(1, 100) <= s.Chance:
          rooms[player.Room].AddPerson(s.Person)

  printRoomObjects(player.Room, rooms)

  # Check if the room persons need to attack
  for x in rooms[player.Room].Persons:
    if persons[x.Person].Flags & PERS_COMBAT == 0 and \
       persons[x.Person].Flags & PERS_AGGRESSIVE > 0:
      combat_flag = True
      x.CombatEnemy = player
      player.Flags |= PERS_COMBAT
      print("[%s] attacks you!" % persons[x.Person].Name)

  if player.Flags & PERS_COMBAT > 0:
     combat_flag = True

  if combat_flag:
    combat(player, persons, rooms)
    if player.HitPoints_Cur <= 0:
      print("\nThe last of your strength slips away, and your vision\n"
            "fades to black...")
      print("\n%sYou have died!%s" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
      time.sleep(2)
      print("\nYou slow come back to your senses ...\n")
      time.sleep(2)
      player.SetRoom(ROOM_RESPAWN)
    continue

  # Handle Commands
  if res != RoomFuncResponse.NO_PROMPT:
    prompt(player, rooms)
    if player.Command != "":
      print("\n%sYou cannot do that here.%s" %
            (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))

# vim: set tabstop=2 shiftwidth=2 expandtab:
