# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Combat Function

import time
import random

from global_defines import *
from utils import *

def playerStartRound(player, rooms):
  player.Action = CombatActionEnum.NONE
  while True:
    prompt(player, rooms)
    if player.Command == "attack":
        player.Action = CombatActionEnum.MELEE_ATTACK
        break
    elif player.Command == "block":
        player.Action = CombatActionEnum.BLOCK
        break
    elif player.Command == "dodge":
        player.Action = CombatActionEnum.DODGE
        break
    elif player.Command == "flee":
      player.Action = CombatActionEnum.FLEE
      break
    else:
      print("\nYou are unable to use that ability.")
      break

def playerApplyAction(player, enemy):
  if player.Action == CombatActionEnum.MELEE_ATTACK:
    # TODO calc attack options
    print("attack!")
  elif player.Action == CombatActionEnum.BLOCK:
    print("\nA glowing purple shield appears around you shielding you from some damage.")
  elif player.Action == CombatActionEnum.FLEE:
    print("\nYou turn around and flee!")
    player.SetRoom(player.LastRoom)

def combat(player, enemy, rooms):
  ResetPlayerStats(player)
  enemy.ResetStats()

  while enemy.HitPoints_Cur > 0 and player.Action != CombatActionEnum.FLEE:
    if player.HitPoints_Cur < 1:
      return

    # TODO Determine Initiative

    # First Attack vs. Defense
    # Seciond Attack vs. Defense

    enemy.Action = CombatActionEnum.NONE
    enemyAttNum = random.randint(1,100)

    enemy.StartRound(enemyAttNum, player, enemy)

    print("\n%s HP: %d" %(enemy.Name.upper(), enemy.HitPoints_Cur))
    print("\nYour HP: %d\nYour Mana: %d\n\nYour combat command:" % (player.HitPoints_Cur, player.MagicPoints_Cur))
    printCombatActions()

    playerStartRound(player, rooms)
    enemy.LastAction = enemy.Action
    playerApplyAction(player, enemy)
    if enemy.HitPoints_Cur > 0 and player.Action != CombatActionEnum.FLEE:
      enemy.EndRound(player, enemy)

  if enemy.HitPoints_Cur <= 0:
    enemy.Alive = False