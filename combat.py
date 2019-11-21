# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Combat Function

import time
import random

from global_defines import *
from utils import *

def combat(player, persons, rooms):
  # start of combat checks?

  while True:
    # start of round checks
    player.Action = CombatActionEnum.NONE
    for x in rooms[player.Room].Persons:
      if x.CombatEnemy == player:
        x.Action = CombatActionEnum.NONE

    initiative_list = []
    # TODO Determine Initiative

    # First Attack vs. Defense
    # Seciond Attack vs. Defense

    enemyAttNum = random.randint(1,100)
    #enemy.StartRound(enemyAttNum, player, enemy)

    print("\nYour HP: %d\nYour Mana: %d\n" % (player.HitPoints_Cur, player.MagicPoints_Cur))
    print("\nChoose a combat command:")
    printCombatActions()
    prompt(player, rooms)

    if player.HitPoints_Cur < 1 or player.Action == CombatActionEnum.FLEE:
      break

# vim: set tabstop=2 shiftwidth=2 expandtab:
