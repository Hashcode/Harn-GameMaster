# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Combat Function

from global_defines import ANSI, CombatActionEnum, PERS_COMBAT
from utils import printCombatActions, prompt


def combat(player, persons, rooms):
  # start of combat checks?

  while True:
    # start of round checks
    player.Action = CombatActionEnum.NONE
    for x in rooms[player.Room].Persons:
      if x.CombatEnemy == player:
        x.Action = CombatActionEnum.NONE

    # TODO Determine Initiative

    # First Attack vs. Defense
    # Seciond Attack vs. Defense

    # enemy.StartRound(enemyAttNum, player, enemy)

    print("\nYour HP: %d\nYour Mana: %d\n" %
          (player.HitPoints_Cur, player.MagicPoints_Cur))
    print("\nChoose a combat command:")
    printCombatActions()

    while True:
      prompt(player, rooms)
      if player.Command == "attack":
        print("Coming soon!")
        break
      elif player.Command == "dodge":
        print("Coming soon!")
        break
      elif player.Command == "block":
        print("Coming soon!")
        break
      elif player.Command == "status":
        print("Coming soon!")
        break
      elif player.Command == "flee":
        # TODO: implement skill check
        player.Action = CombatActionEnum.FLEE
        for x in rooms[player.Room].Persons:
          x.CombatEnemy = None
        player.Room = player.LastRoom
        player.Flags &= ~PERS_COMBAT
        print("\n%sYou FLEE!%s" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
        break
      else:
        print("\n%sYou cannot do that here.%s" %
              (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))

    if player.HitPoints_Cur < 1 or player.Action == CombatActionEnum.FLEE:
      break

# vim: set tabstop=2 shiftwidth=2 expandtab:
