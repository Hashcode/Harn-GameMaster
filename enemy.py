# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Enemy Definitions

from global_defines import *
from utils import *

# Rat

def rat_StartRound(raction, player, enemy):
    if raction >= 1 and raction <= 49:
      print("\n%s eyes you suspiciously, waiting for you to make a move ..." % (enemy.Name))
      enemy.Action = CombatActionEnum.DODGE
    elif raction >= 50 and raction <= 89:
      print("\n%s gets ready to attack ..." % (enemy.Name))
      enemy.Action = CombatActionEnum.MELEE_ATTACK
    elif raction >= 90 and raction <= 100:
      print("\n%s backs up in a defensive position ..." % (enemy.Name))
      enemy.Action = CombatActionEnum.BLOCK

def rat_EndRound(player, enemy):
  if enemy.Action == CombatActionEnum.MELEE_ATTACK:
    if player.Action == CombatActionEnum.BLOCK:
      userDmg = roll(enemy.DamageRolls, enemy.DamageDice) - (CalcDefense(player) * 1.5)
    else:
      userDmg = roll(enemy.DamageRolls, enemy.DamageDice) - CalcDefense(player)
    if userDmg > 0:
      player.HitPoints_Cur -= userDmg
      print("%s hits you for %d damage." % (enemy.Name, userDmg))
    else:
      print("Your armor blocks the damage from %s" % (enemy.Name))

enemies = {
  EnemyEnum.RAT:
    Enemy("an ugly rat", 10,
          1, 4, DamageTypeEnum.EDGE, 3,
          rat_StartRound, rat_EndRound),
}

# vim: tabstop=2 shiftwidth=2 expandtab:
