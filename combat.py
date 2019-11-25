# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Combat Function

from enum import IntEnum

from global_defines import (logd, DiceRoll, CoverageEnum, body_parts,
                            DamageTypeEnum,
                            SkillEnum, ImpactResult, ImpactActionEnum,
                            ImpactAction, CombatAttack, ANSI)
from dmg_table import dmg_table_melee
from utils import (printCombatAttackActions, printCombatDefenseActions,
                   prompt)
from rooms import rooms
from person import persons
from items import items


class Action(IntEnum):
  IGNORE = 0
  MELEE = 1
  BLOCK = 2
  DODGE = 3
  MISSILE = 5
  GRAPPLE = 6
  ESOTERIC = 7
  FLEE = 8


class Aim(IntEnum):
  HIGH = 0
  MID = 1
  LOW = 2


class Roll(IntEnum):
  NONE = 0
  CS = 1
  MS = 2
  MF = 3
  CF = 4


class ResultEnum(IntEnum):
  MISS = 0
  BLOCK = 1
  FUMBLE = 2
  STUMBLE = 3
  TADV = 4
  DMG = 5


T_ATK = 1 << 0
T_DEF = 1 << 1
T_BOTH = T_ATK | T_DEF


class Result:
  def __init__(self, targets, result, level=0):
    self.TargetFlag = targets
    self.Result = result
    self.Level = level

  def __str__(self):
    ret = "T:"
    if T_ATK & self.TargetFlag > 0:
      ret += "T_ATK"
    if T_DEF & self.TargetFlag > 0:
      if len(ret) > 2:
        ret += "|"
      ret += "T_DEF"
    ret += " %s/%d" % (self.Result, self.Level)
    return ret


class Combatant:
  def Reset(self):
    self.Person = None
    self.Action = Action.IGNORE
    self.Aim = Aim.MID
    self.Roll = Roll.NONE
    self.Attacks = None
    self.TAdvCount = 0

  def __init__(self):
    self.Reset()


def ResolveSkill(c, ml):
  r = DiceRoll(1, 100).Result()
  logd("%s RESOLVE SKILL: %d, ROLL: %d" % (c.Person.Name, ml, r))
  # success
  if r <= ml:
    if r % 5 == 0:
      return Roll.CS
    else:
      return Roll.MS
  # failure
  else:
    if r % 5 == 0:
      return Roll.CF
    else:
      return Roll.MF


hit_table_melee_default = {
    CoverageEnum.SKULL: [15, 5, 0],
    CoverageEnum.FACE: [30, 10, 0],
    CoverageEnum.NECK: [45, 15, 0],
    CoverageEnum.SHOULDERS: [57, 27, 0],
    CoverageEnum.UPPER_ARMS: [69, 33, 0],
    CoverageEnum.ELBOWS: [73, 35, 0],
    CoverageEnum.FOREARMS: [81, 39, 6],
    CoverageEnum.HANDS: [85, 43, 12],
    CoverageEnum.THORAX_FRONT: [95, 60, 19],
    CoverageEnum.ABDOMEN_FRONT: [100, 70, 29],
    CoverageEnum.GROIN: [0, 74, 35],
    CoverageEnum.HIPS: [0, 80, 49],
    CoverageEnum.THIGHS: [0, 88, 70],
    CoverageEnum.KNEES: [0, 90, 78],
    CoverageEnum.CALVES: [0, 96, 92],
    CoverageEnum.FEET: [0, 100, 100],
}


resolve_melee = {
    # ATTACKER
    Roll.CF: {
        # DEFENDER
        Action.BLOCK: {
            Roll.CF: Result(T_BOTH, ResultEnum.FUMBLE, 3),
            Roll.MF: Result(T_ATK, ResultEnum.FUMBLE, 3),
            Roll.MS: Result(T_DEF, ResultEnum.TADV),
            Roll.CS: Result(T_DEF, ResultEnum.TADV),
        },
        Action.MELEE: {
            Roll.CF: Result(T_BOTH, ResultEnum.FUMBLE, 3),
            Roll.MF: Result(T_ATK, ResultEnum.FUMBLE, 3),
            Roll.MS: Result(T_DEF, ResultEnum.DMG, 2),
            Roll.CS: Result(T_DEF, ResultEnum.DMG, 3),
        },
        Action.DODGE: {
            Roll.CF: Result(T_BOTH, ResultEnum.STUMBLE, 3),
            Roll.MF: Result(T_ATK, ResultEnum.STUMBLE, 3),
            Roll.MS: Result(T_DEF, ResultEnum.TADV),
            Roll.CS: Result(T_DEF, ResultEnum.TADV),
        },
        Action.IGNORE: {
            Roll.CF: Result(T_DEF, ResultEnum.TADV),
            Roll.MF: Result(T_DEF, ResultEnum.TADV),
            Roll.MS: Result(T_DEF, ResultEnum.TADV),
            Roll.CS: Result(T_DEF, ResultEnum.TADV),
        },
    },
    Roll.MF: {
        Action.BLOCK: {
            Roll.CF: Result(T_DEF, ResultEnum.FUMBLE, 3),
            Roll.MF: Result(T_BOTH, ResultEnum.MISS),
            Roll.MS: Result(T_BOTH, ResultEnum.MISS),
            Roll.CS: Result(T_DEF, ResultEnum.TADV),
        },
        Action.MELEE: {
            Roll.CF: Result(T_DEF, ResultEnum.FUMBLE, 3),
            Roll.MF: Result(T_BOTH, ResultEnum.MISS),
            Roll.MS: Result(T_DEF, ResultEnum.DMG, 1),
            Roll.CS: Result(T_DEF, ResultEnum.DMG, 2),
        },
        Action.DODGE: {
            Roll.CF: Result(T_DEF, ResultEnum.STUMBLE, 3),
            Roll.MF: Result(T_BOTH, ResultEnum.MISS),
            Roll.MS: Result(T_BOTH, ResultEnum.MISS),
            Roll.CS: Result(T_DEF, ResultEnum.TADV),
        },
        Action.IGNORE: {
            Roll.CF: Result(T_ATK, ResultEnum.DMG, 1),
            Roll.MF: Result(T_ATK, ResultEnum.DMG, 1),
            Roll.MS: Result(T_ATK, ResultEnum.DMG, 1),
            Roll.CS: Result(T_ATK, ResultEnum.DMG, 1),
        },
    },
    Roll.MS: {
        Action.BLOCK: {
            Roll.CF: Result(T_ATK, ResultEnum.DMG, 2),
            Roll.MF: Result(T_ATK, ResultEnum.DMG, 1),
            Roll.MS: Result(T_BOTH, ResultEnum.BLOCK),
            Roll.CS: Result(T_BOTH, ResultEnum.MISS),
        },
        Action.MELEE: {
            Roll.CF: Result(T_ATK, ResultEnum.DMG, 3),
            Roll.MF: Result(T_ATK, ResultEnum.DMG, 2),
            Roll.MS: Result(T_BOTH, ResultEnum.DMG, 1),
            Roll.CS: Result(T_DEF, ResultEnum.DMG, 1),
        },
        Action.DODGE: {
            Roll.CF: Result(T_ATK, ResultEnum.DMG, 2),
            Roll.MF: Result(T_ATK, ResultEnum.DMG, 1),
            Roll.MS: Result(T_BOTH, ResultEnum.MISS),
            Roll.CS: Result(T_BOTH, ResultEnum.MISS),
        },
        Action.IGNORE: {
            Roll.CF: Result(T_ATK, ResultEnum.DMG, 3),
            Roll.MF: Result(T_ATK, ResultEnum.DMG, 3),
            Roll.MS: Result(T_ATK, ResultEnum.DMG, 3),
            Roll.CS: Result(T_ATK, ResultEnum.DMG, 3),
        },
    },
    Roll.CS: {
        Action.BLOCK: {
            Roll.CF: Result(T_ATK, ResultEnum.DMG, 3),
            Roll.MF: Result(T_ATK, ResultEnum.DMG, 2),
            Roll.MS: Result(T_ATK, ResultEnum.DMG, 1),
            Roll.CS: Result(T_BOTH, ResultEnum.BLOCK),
        },
        Action.MELEE: {
            Roll.CF: Result(T_ATK, ResultEnum.DMG, 4),
            Roll.MF: Result(T_ATK, ResultEnum.DMG, 3),
            Roll.MS: Result(T_ATK, ResultEnum.DMG, 1),
            Roll.CS: Result(T_BOTH, ResultEnum.DMG, 2),
        },
        Action.DODGE: {
            Roll.CF: Result(T_ATK, ResultEnum.DMG, 3),
            Roll.MF: Result(T_ATK, ResultEnum.DMG, 2),
            Roll.MS: Result(T_ATK, ResultEnum.DMG, 1),
            Roll.CS: Result(T_BOTH, ResultEnum.MISS),
        },
        Action.IGNORE: {
            Roll.CF: Result(T_ATK, ResultEnum.DMG, 4),
            Roll.MF: Result(T_ATK, ResultEnum.DMG, 4),
            Roll.MS: Result(T_ATK, ResultEnum.DMG, 4),
            Roll.CS: Result(T_ATK, ResultEnum.DMG, 4),
        },
    },
}


# Determine Order via Initiative + 1D100
# Attack Declaration
#   Melee Attack
#   Missile Attack
#   >Weapon Aspect
#   >Aiming Zone: High, Med, Low
# Defense Declaraction
#   Block/Parry
#   Counterstrike
#   Dodge
#   Ignore
#   Grapple Defense
#   Missile Defense
#   Esoteric Defense
def combat(player, enemies):
  # start of combat checks?
  order = dict()
  player.SetCombatWait()
  for x in enemies:
    persons[x.Person].SetCombatWait()
  att = Combatant()
  defe = Combatant()

  while True:
    logd("** START ROUND **")
    order.clear()

    # setup initiative
    for x in enemies:
        init = DiceRoll(1, 100).Result()
        init += persons[x.Person].AttrInitiative(items)
        order.update({init: persons[x.Person]})
    # player
    init = DiceRoll(1, 100).Result()
    init += player.SkillML(SkillEnum.INITIATIVE, items)
    order.update({init: player})

    # TURN loop
    for i in sorted(order, reverse=True):
      # start of combat round
      att.Reset()
      defe.Reset()

      logd("* START TURN: %s *" % order[i].Name)

      if order[i] == player:
        att.Person = player
        # TODO: if len(order) > 2: player choose target
        # HACK: Choose 1st non-player target
        for init, ce in order.items():
          if ce != player:
            defe.Person = ce
            break

        logd("PLAYER ACTION: %s vs. %s" %
             (att.Person.Name, defe.Person.Name))

        # target mob chooses action
        #   block if available (equipment)
        #   dodge if not
        # TODO: counterstrike?
        defe.Action = Action.BLOCK
        defe.Attacks = defe.Person.GenerateCombatAttacks(items, block=True)
        if len(defe.Attacks) < 1:
          defe.Action = Action.DODGE

        att.Person.SetCombatAttacker()
        defe.Person.SetCombatDefender()

        print("\nCombat commands:")
        printCombatAttackActions(att.Person)
        while True:
          prompt(player, rooms)
          if player.Command == "attack":
            att.Action = Action.MELEE
            att.Attacks = att.Person.GenerateCombatAttacks(items)
            # [player choose aiming zone]
            att.Aim = Aim.MID
            break
          elif player.Command == "flee":
            # TODO: implement skill check
            att.Action = Action.FLEE
            break
          else:
            print("\n%sYou cannot do that here.%s" %
                  (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
          # if player == FLEE, choose dodge automatically
      else:
        att.Person = order[i]
        defe.Person = player

        # mob chooses attack action
        #   flee?
        att.Action = Action.MELEE
        att.Attacks = att.Person.GenerateCombatAttacks(items)
        if len(att.Attacks) == 0:
          logd("MOB ERROR! %s no attack!" % (att.Person.Name))
          att.Action = Action.IGNORE

        logd("MOB ACTION: %s vs. %s" %
             (att.Person.Name, defe.Person.Name))
        # TODO: [mob chooses aiming zone]
        att.Aim = Aim.MID

        att.Person.SetCombatAttacker()
        defe.Person.SetCombatDefender()

        print("\nCombat commands:")
        printCombatDefenseActions(player)
        while True:
          prompt(player, rooms)
          if player.Command == "block":
            defe.Action = Action.BLOCK
            defe.Attacks = defe.Person.GenerateCombatAttacks(items,
                                                             block=True)
            if len(defe.Attacks) < 1:
              defe.Action = Action.DODGE
            break
          elif player.Command == "dodge":
            defe.Action = Action.DODGE
            break
          # elif player.Command == "counterstrike":
          #  defe.Action = Action.MELEE
          #  defe.Attacks = defe.Person.GenerateCombatAttacks(items)
          #  break
          else:
            print("\n%sYou cannot do that here.%s" %
                  (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))

      # RESOLUTION PHASE
      if att.Action == Action.FLEE:
        break

      if att.Attacks is not None:
        for at in att.Attacks:
          att.Roll = ResolveSkill(att, at.SkillML)
          logd("ATTACKER %s %s" %
               (att.Person.Name, att.Roll))
          if defe.Action == Action.BLOCK:
            if len(defe.Attacks) < 1:
              defe.Action = Action.DODGE
            else:
              defe.Roll = ResolveSkill(defe, defe.Attacks[0].SkillML)
          if defe.Action == Action.DODGE:
            defe.Roll = ResolveSkill(defe, defe.Person.AttrDodge(items))
          logd("DEFENDER %s %s" %
               (defe.Person.Name, defe.Roll))
          # use resolve_melee for now
          res = resolve_melee[att.Roll][defe.Action][defe.Roll]

          if res.Result == ResultEnum.MISS:
            if att.Person == player:
              print("\nYou MISS [%s] with your [%s]." %
                    (defe.Person.Name, at.Name.lower()))
            else:
              print("\n[%s] MISSES you with [%s]." %
                    (att.Person.Name, at.Name.lower()))
          elif res.Result == ResultEnum.BLOCK:
            if att.Person == player:
              print("\n[%s] BLOCKS your attack with [%s]." %
                    (defe.Person.Name, defe.Attacks[0].Name.lower()))
            else:
              print("\nYou BLOCK [%s] with your [%s]." %
                    (att.Person.Name, defe.Attacks[0].Name.lower()))
          # elif res.Result == ResultEnum.FUMBLE:
            # TODO:
          # elif res.Result == ResultEnum.STUMBLE:
            # TODO:
          # elif res.Result == ResultEnum.TADV:
            # TODO:
          elif res.Result == ResultEnum.DMG:

            if res.TargetFlag & T_ATK > 0:
              # attacker lands impact
              impact = at.Roll.Result()
              for x in range(res.Level):
                impact += DiceRoll(1, 6).Result()
              logd("%s IMPACT CALC: %d" % (att.Person.Name, impact))
              # roll hit location
              loc = CoverageEnum.THORAX_FRONT
              r = DiceRoll(1, 100).Result()
              for l, hit_table in hit_table_melee_default.items():
                if hit_table[att.Aim] > 0 and r <= hit_table[att.Aim]:
                  loc = l
                  break
              logd("%s LOC: %s" % (att.Person.Name, loc))
              # defender applies armor
              impact -= defe.Person.Defense(items, loc, at.DamageType)
              logd("%s ADJ. IMPACT: %d" % (att.Person.Name, impact))
              leftright = ""
              if body_parts[loc].LeftRight:
                if r % 2 == 1:
                  leftright = "left "
                else:
                  leftright = "right "
              if att.Person == player:
                print("\nYou HIT [%s's] %s%s with your [%s]!" %
                      (defe.Person.Name, leftright,
                       body_parts[loc].PartName.lower(), at.Name))
              else:
                print("\n[%s] HITS your %s%s with their [%s]!" %
                      (att.Person.Name, leftright,
                       body_parts[loc].PartName.lower(), at.Name))

              if (impact <= 0):
                if att.Person == player:
                  print("Your [%s] GLANCES off [%s] with no effect!" %
                        (at.Name, defe.Person.Name))
                else:
                  print("[%s's %s] GLANCES off you with no effect!" %
                        (att.Person.Name, at.Name))
              else:

                # check impact effect
                ia_list = None
                for ir in dmg_table_melee[at.DamageType][loc]:
                  if impact <= ir.ImpactMax:
                    ia_list = ir.ImpactActions
                    break
                for ia in ia_list:
                  print("IMPACT_ACTION: %s LEVEL:%d" % (ia.Action, ia.Level))

            if res.TargetFlag & T_DEF > 0:
              # defender lands impact
              impact = defe.Attacks[0].Roll.Result()
              for x in range(res.Level):
                impact += DiceRoll(1, 6).Result()
              print("%s IMPACT CALC: %d" % (defe.Person.Name, impact))

          else:
            print("\n*** %s ***" % res)

      else:
        logd("***%s HAD NO ATTACKS ***\n" % res)

      # check if dead
      att.Person.SetCombatWait()
      defe.Person.SetCombatWait()

    if att.Action == Action.FLEE:
      player.Room = player.LastRoom
      player.ClearCombat()
      for x in enemies:
        persons[x.Person].ClearCombat()
      print("\n%sYou FLEE!%s" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
      break

# vim: set tabstop=2 shiftwidth=2 expandtab:
