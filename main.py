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

from global_defines import *
from utils import *
from rooms import rooms
from person import persons
from combat import combat

TestMode = True

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

  # Check if the room persons need to attack
  for x in rooms[player.Room].Persons:
    if x.Flags & PERS_COMBAT == 0 and x.Flags & PERS_AGGRESSIVE > 0:
      combat_flag = True
      x.CombatEnemy == player
      x.Flags |= PERS_COMBAT
      player.Flags |= PERS_COMBAT
      print("%s attacks you!" % x.Name)

  if player.CombatEnemy != None:
     combat_flag = True

  if combat_flag:
    combat(player, persons, rooms)
    if player.HitPoints_Cur <= 0:
      print("\nThe last of your strength slips away, and your vision fades to black...")
      print("\n%sYou have died!%s" % (ANSI.TEXT_BOLD, ANSI_TEXT_NORMAL))
      time.sleep(2)
      print("\nYou slow come back to your senses ...\n")
      time.sleep(2)
      player.SetRoom(ROOM_RESPAWN)
      continue

  # Handle Commands
  if res != RoomFuncResponse.NO_PROMPT:
    prompt(player, rooms)
    if player.Command == "q" or player.Command == "quit":
      break
    if player.Command != "":
      print("You cannot do that here.")

# vim: set tabstop=2 shiftwidth=2 expandtab: