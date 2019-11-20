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

# Charlock

def char_StartRound(raction, player, enemy):
    if raction >= 1 and raction <= 19:
      print("\n%s eyes you suspiciously, waiting for you to make a move ..." % (enemy.Name))
      enemy.Action = CombatActionEnum.DODGE
    elif raction >= 20 and raction <= 69:
      print("\n%s raises his razor-sharp wings to strike you ..." % (enemy.Name))
      enemy.Action = CombatActionEnum.MELEE_ATTACK
    elif raction >= 70 and raction <= 84:
      print("\n%s backs up in a defensive position ..." % (enemy.Name))
      enemy.Action = CombatActionEnum.BLOCK
    elif raction >= 85 and raction <= 96:
      if enemy.HitPoints_Cur < enemy.HitPoints_Max:
        print("\n%s raises his head, and is surrounded by a glowing green aura ..." % (enemy.Name))
        enemy.Action = CombatActionEnum.SPELL
      else:
        enemy.Action = CombatActionEnum.DODGE
        print("\n%s eyes you suspiciously, waiting for you to make a move ..." % (enemy.Name))
    elif raction >= 97 and raction <= 100:
      print("\n%s rears back onto his hind legs, drawing in breath for a devastating torrent of fire ..." % (enemy.Name))
      enemy.Action = CombatActionEnum.ABILITY

def char_EndRound(player, enemy):
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
  if enemy.Action == CombatActionEnum.SPELL: # HEAL
    healthAdd = 5
    if enemy.HitPoints_Cur + healthAdd > enemy.HitPoints_Max:
      enemy.HitPoints_Cur = enemy.HitPoints_Max
    else:
      enemy.HitPoints_Cur += healthAdd
    print("%s heals some of his damage." % (enemy.Name))
  if enemy.Action == CombatActionEnum.ABILITY: # Fireball
    player.HitPoints_Cur -= 1000
    print("%s's massive attack hits you for 1000 damage." % (enemy.Name))

enemies = {
  EnemyEnum.RAT:
    Enemy("an ugly rat", 10,
          1, 4, DamageTypeEnum.EDGE, 3,
          rat_StartRound, rat_EndRound),

  EnemyEnum.CHARLOK:
    Enemy("Charlock", 20,
          2, 6, DamageTypeEnum.EDGE, 12,
          char_StartRound, char_EndRound),
}