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
from enemy import enemies
from combat import combat

TestMode = True

random.seed()
print(ANSI.CLEAR + ANSI.RESET_CURSOR, end='')

player = Player("Unknown")
player.SetRoom(RoomEnum.START_GAME)

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
  res = RoomFuncResponse.NONE
  printRoomDescription(player.Room, rooms)

  # Call Room Function
  if not rooms[player.Room].Function is None:
    # Return value means: True == Print Prompt, False == Skip Prompt
    res = rooms[player.Room].Function(player)

  if res == RoomFuncResponse.SKIP:
    continue

  # Fighting Check
  if player.CombatEnemy == EnemyEnum.NONE:
    # Check if the room has an enemy
    if rooms[player.Room].Enemy != EnemyEnum.NONE:
      if enemies[rooms[player.Room].Enemy].Alive:
        player.CombatEnemy = rooms[player.Room].Enemy

  if player.CombatEnemy != EnemyEnum.NONE:
    combat(player, enemies[player.CombatEnemy], rooms)
    player.CombatEnemy = EnemyEnum.NONE
    if player.HitPoints_Cur < 1:
      print("\nThe last of your strength slips away, and your vision fades to black...")
      print("\nYou have been defeated by %s." % (enemies[player.CombatEnemy].Name))
      time.sleep(2)
      player.SetRoom(RoomEnum.DEATH)
    elif not enemies[player.CombatEnemy].Alive:
      if not enemies[player.CombatEnemy].Alive:
        print("\nCongratulations! You have defeated %s!" % (enemies[player.CombatEnemy].Name))

  # Handle Commands
  if res != RoomFuncResponse.NO_PROMPT:
    prompt(player, rooms)
    if player.Command == "quit":
      print("\nGoodbye!\n")
      break
    if player.Command != "":
      print("You cannot do that here.")

# vim: set tabstop=2 shiftwidth=2 expandtab:
