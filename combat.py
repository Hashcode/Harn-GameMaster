# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Combat Function

from time import sleep
from enum import IntEnum

from global_defines import (DiceRoll, CoverageEnum, body_parts,
                            AimEnum, aims,
                            PlayerCombatState, wounds, PersonWound,
                            AttrEnum, PersonTypeEnum, ItemLink,
                            ImpactActionEnum, ANSI, GameData)
from logging import (logd)
from dmg_table import dmg_table_melee
from utils import prompt
from rooms import rooms
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


# Combat Flags
FLAG_DEAD = 1 << 0


class Combatant:
  def __init__(self, person, uid, items):
    self.Person = person
    self.UUID = uid
    self.Init = 0
    self.TAdvCount = 0
    self.Flags = 0
    self.StunLevel = 0
    self.Action = Action.IGNORE
    self.Aim = AimEnum.MID
    self.Target = None
    self.Roll = Roll.NONE
    self.Attacks = None
    self.TurnTaken = False

  def Refresh(self, items):
    if self.StunLevel > 0:
      self.Init = 0
    else:
      self.Init = DiceRoll(1, 100).Result()
      self.Init += self.Person.AttrInitiative(items)
    self.Action = Action.IGNORE
    self.Aim = AimEnum.MID
    self.TurnTaken = False

  def __eq__(self, other):
    if self.Init == other.Init:
      return True
    else:
      return False

  def __lt__(self, other):
    if self.Init < other.Init:
      return True
    else:
      return False

  def __gt__(self, other):
    if self.Init > other.Init:
      return True
    else:
      return False


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


# COMBAT COMMANDS

def printCombatAttackActions(combatant, target, items):
  att = combatant.Person.GenerateCombatAttacks(items)
  if len(att) > 0:
    att_name = "%s: %s ML" % (att[0].Name, att[0].SkillML)
  else:
    att_name = "no weapon!"
  if combatant.Target is not None:
    target_name = combatant.Target.Person.Name
  else:
    target_name = "[NO TARGET]"
  print("\nOFFENSE COMMANDS:\n")
  print("%-10s %-3s : %s" % ("AIM", "", aims[combatant.Aim].Name))
  print("%-10s %-3s : %s" % ("ATTACK", "[A]", att_name))
  print("%-10s %-3s :" % ("CAST", "[C]"))
  print("%-10s %-3s : %d ML" % ("FLEE", "[F]",
                                combatant.Person.AttrDodge(items)))
  # print("  GRAPPLE")
  # print("  MISSILE")
  print("%-10s %-3s :" % ("PASS", "[P]"))
  print("%-10s %-3s : %s" %
        ("TARGET", "[T]", target_name))


def printCombatDefenseActions(combatant, items):
  block = combatant.Person.GenerateCombatAttacks(items, block=True)
  if len(block) > 0:
    block_name = "%s: %s ML" % (block[0].Name, block[0].SkillML)
  else:
    block_name = "no weapon / shield!"
  print("\nDEFENSE COMMANDS:\n")
  print("%-10s %-3s : %s" % ("BLOCK", "[B]", block_name))
  print("%-10s %-3s : %d ML" % ("DODGE", "",
                                combatant.Person.AttrDodge(items)))
  # print("  MISSILE")
  # print("  GRAPPLE")
  # print("  ESOTERIC")


def chooseTarget(player, enemies):
  ret = None
  print("\nChoose a target:\n")
  count = 0
  for c in enemies:
    if c.Person.PersonType == PersonTypeEnum.NPC:
      if c.Flags & FLAG_DEAD == 0:
        count += 1
        print("%d. %s" % (count, c.Person.Name))
  if count < 1:
    print("[NONE]")
    return ret
  x = input("\nWhich # to attack: ").lower()
  if not x.isnumeric():
    print("\nInvalid target.")
    return ret
  personNum = int(x)
  if personNum < 1 or personNum > count:
    print("\nInvalid target.")
    return ret
  count = 0
  for c in enemies:
    if c.Person.PersonType == PersonTypeEnum.NPC:
      if c.Flags & FLAG_DEAD == 0:
        count += 1
        if count == personNum:
          ret = c.Person.UUID
          break
  return ret


def combat(player, enemies):
  # start of combat checks?
  order = []

  # setup combatants
  player_combatant = Combatant(player, 0, items)
  order.append(player_combatant)
  for x in enemies:
      order.append(Combatant(x, x.UUID, items))

  while True:
    logd("** START ROUND **")

    # Check for end of combat and reduce stun levels
    all_dead = True
    for x in order:
      if x is not player_combatant and x.Flags & FLAG_DEAD == 0:
        all_dead = False
      if x.StunLevel > 0 and x.Flags & FLAG_DEAD == 0:
        x.StunLevel -= 1
        logd("%s STUN_LEVEL %d" %
             (x.Person.Name, x.StunLevel))
        if x.StunLevel < 1:
          if x.Person is player:
            print("%sYour stun WEARS OFF!%s" %
                  (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
          else:
            print("%s%s's stun WEARS OFF!%s" %
                  (ANSI.TEXT_BOLD, x.Person.Name.capitalize(),
                   ANSI.TEXT_NORMAL))
    if all_dead:
      player.CombatState = PlayerCombatState.NONE
      return

    player.CombatState = PlayerCombatState.WAIT
    for x in order:
        x.Refresh(items)
        logd("%s init %d" % (x.Person.Name, x.Init))

    # TURN loop
    for att in sorted(order, reverse=True):
      logd("** TURN %s **" % att.Person.Name)
      att.TurnTaken = True

      if att.Flags & FLAG_DEAD > 0:
        logd("skip %s == DEAD" % att.Person.Name)
        continue

      if att.StunLevel > 0:
        continue

      elif att.Person == player:
        player.CombatState = PlayerCombatState.ATTACK

        if att.Target is None:
          count = 0
          m = None
          for x in order:
            if x.Person.PersonType == PersonTypeEnum.NPC and \
               x.Flags & FLAG_DEAD == 0:
              count += 1
              m = x
              if player.CombatTarget == x.Person.UUID:
                att.Target = x
                break
          if att.Target is None and count == 1:
            att.Target = m
          else:
            while True:
              uid = chooseTarget(player, order)
              if uid is not None:
                for c in order:
                  if c.Person.PersonType == PersonTypeEnum.NPC:
                    if c.Flags & FLAG_DEAD == 0 and c.UUID == uid:
                      att.Target = c
                      break
                if att.Target is not None:
                  break
        defe = att.Target

        logd("PLAYER ACTION: %s vs. %s" %
             (att.Person.Name, defe.Person.Name))

        # target mob chooses action
        #   ignore if stunned
        #   block if available (equipment)
        #   dodge if not
        if defe.StunLevel > 0:
          defe.Action = Action.IGNORE
        else:
          defe.Action = Action.BLOCK
          defe.Attacks = defe.Person.GenerateCombatAttacks(items, block=True)
          if len(defe.Attacks) < 1:
            defe.Action = Action.DODGE

        while True:
          printCombatAttackActions(att, defe, items)
          prompt(player, rooms, func_break=True)
          if player.Command == "aim":
            print("\nComing soon!")
          elif player.Command == "attack" or player.Command == "a":
            if att.Target is None:
              print("\nYou have no target!")
            else:
              att.Action = Action.MELEE
              att.Attacks = att.Person.GenerateCombatAttacks(items)
              break
          elif player.Command == "cast" or player.Command == "c":
            print("\nComing soon!")
          elif player.Command == "flee" or player.Command == "f":
            # TODO: implement skill check
            att.Action = Action.FLEE
            break
          elif player.Command == "pass" or player.Command == "p":
            print("\nYou choose to skip your action.")
            att.Action = Action.IGNORE
            break
          elif player.Command == "target" or player.Command == "t":
            uid = chooseTarget(player, order)
            if uid is not None:
              for c in order:
                if c.Person.PersonType == PersonTypeEnum.NPC:
                  if c.Flags & FLAG_DEAD == 0 and c.UUID == uid:
                    att.Target = c
                    break
          elif player.Command != "help" and player.Command != "?":
            print("\n%sYou cannot do that here.%s" %
                  (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
          # if player == FLEE, choose dodge automatically

      else:
        player.CombatState = PlayerCombatState.DEFEND
        defe = player_combatant

        # mob chooses attack action
        #   flee?
        att.Action = Action.MELEE
        logd("%s: Generate Attack" % (att.Person.Name))
        att.Attacks = att.Person.GenerateCombatAttacks(items)
        if len(att.Attacks) == 0:
          logd("MOB ERROR! %s no attack!" % (att.Person.Name))
          att.Action = Action.IGNORE
        else:
          logd("%s attack: %s" % (att.Person.Name, att.Attacks[0].Name))
        # use default Aim zone
        att.Aim = att.Person.DefaultAim

        # pause scroll momentarily
        sleep(1)

        # determine player defense
        if defe.StunLevel > 0:
          defe.Action = Action.IGNORE
        else:
          defe.Attacks = defe.Person.GenerateCombatAttacks(items, block=True)
          if len(defe.Attacks) < 1:
            defe.Action = Action.DODGE
          elif defe.Person.AttrDodge(items) > defe.Attacks[0].SkillML:
            defe.Action = Action.DODGE
          else:
            defe.Action = Action.BLOCK

      # RESOLUTION PHASE
      if att.Action == Action.FLEE:
        break

      if att.Action == Action.IGNORE:
        continue

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
              print("\nYou MISS %s with your %s." %
                    (defe.Person.Name, at.Name.lower()))
            else:
              print("\n%s MISSES you with %s %s." %
                    (att.Person.Name.capitalize(),
                     att.Person.AttrSexPossessivePronounStr().lower(),
                     at.Name.lower()))
          elif res.Result == ResultEnum.BLOCK:
            if att.Person == player:
              print("\n%s BLOCKS your attack with %s %s." %
                    (defe.Person.Name.capitalize(),
                     defe.Person.AttrSexPossessivePronounStr().lower(),
                     defe.Attacks[0].Name.lower()))
            else:
              print("\nYou BLOCK %s with your %s." %
                    (att.Person.Name, defe.Attacks[0].Name.lower()))
          # elif res.Result == ResultEnum.FUMBLE:
            # TODO:
          # elif res.Result == ResultEnum.STUMBLE:
            # TODO:
          # elif res.Result == ResultEnum.TADV:
            # TODO:
          # Only the current attacker can do damage
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
                print("\nYou HIT %s's %s%s with your %s!" %
                      (defe.Person.Name, leftright,
                       body_parts[loc].PartName.lower(), at.Name.lower()))
              else:
                print("\n%s HITS your %s%s with %s %s!" %
                      (att.Person.Name.capitalize(), leftright,
                       body_parts[loc].PartName.lower(),
                       att.Person.AttrSexPossessivePronounStr().lower(),
                       at.Name.lower()))

              if (impact <= 0):
                s = "S"
                if at.Name.lower().endswith("s"):
                  s = ""
                if att.Person == player:
                  print("Your %s GLANCE%s off %s with no effect!" %
                        (at.Name.lower(), s, defe.Person.Name))
                else:
                  print("%s's %s GLANCE%s off you with no effect!" %
                        (att.Person.Name.capitalize(), at.Name.lower(), s))
              else:

                # check impact effect
                ia_list = None
                for ir in dmg_table_melee[at.DamageType][loc]:
                  if impact <= ir.ImpactMax:
                    ia_list = ir.ImpactActions
                    break
                for ia in ia_list:
                  if ia.Action in [ImpactActionEnum.WOUND_MLD,
                                   ImpactActionEnum.WOUND_SRS,
                                   ImpactActionEnum.WOUND_GRV]:
                    if att.Person == player:
                      print("%s%s suffers a %s wound!%s" %
                            (ANSI.TEXT_BOLD, defe.Person.Name.capitalize(),
                             wounds[ia.Action].Name.lower(),
                             ANSI.TEXT_NORMAL))
                    else:
                      print("%sYou suffer a %s wound!%s" %
                            (ANSI.TEXT_BOLD, wounds[ia.Action].Name.lower(),
                             ANSI.TEXT_NORMAL))
                    w = PersonWound(ia.Action, at.DamageType, loc,
                                    impact + wounds[ia.Action].IPBonus)
                    defe.Person.Wounds.append(w)

                    # determine if the Injury Point Index is > END == DEATH
                    logd("%s WOUND DEATH check: %d vs. %d STA" %
                         (defe.Person.Name, defe.Person.IPIndex(),
                          defe.Person.Attr[AttrEnum.STAMINA]))
                    if defe.Person.IPIndex() > \
                       defe.Person.Attr[AttrEnum.STAMINA]:
                      if att.Person == player:
                        print("%s%s DIES from %s wounds!%s" %
                              (ANSI.TEXT_BOLD, defe.Person.Name.capitalize(),
                               defe.Person.AttrSexPossessivePronounStr(),
                               ANSI.TEXT_NORMAL))
                      else:
                        print("%sYou DIE from your wounds!%s" %
                              (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
                      defe.Flags |= FLAG_DEAD
                      break
                  elif ia.Action == ImpactActionEnum.KILL_CHECK:
                    r = DiceRoll(ia.Level, 6).Result()
                    logd("%s DEATH check: %d vs. %d STA" %
                         (defe.Person.Name, r,
                          defe.Person.Attr[AttrEnum.STAMINA]))
                    if r > defe.Person.Attr[AttrEnum.STAMINA]:
                      # DEATH!
                      if att.Person == player:
                        print("%s%s DIES instantly!%s" %
                              (ANSI.TEXT_BOLD, defe.Person.Name.capitalize(),
                               ANSI.TEXT_NORMAL))
                      else:
                        print("%sYou DIE instantly!%s" %
                              (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
                      defe.Flags |= FLAG_DEAD
                      break
                  # elif ia.Action == ImpactActionEnum.AMPUTATE_CHECK:
                    # TODO
                  elif ia.Action == ImpactActionEnum.SHOCK:
                    num = ia.Level + defe.Person.UniversalPenaltyIndex()
                    r = DiceRoll(num, 6).Result()
                    logd("%s SHOCK check: %d vs. %d END" %
                         (defe.Person.Name, r,
                          defe.Person.AttrEndurance(items)))
                    if r > defe.Person.AttrEndurance(items):
                      if att.Person == player:
                        print("%s%s is STUNNED!%s" %
                              (ANSI.TEXT_BOLD, defe.Person.Name.capitalize(),
                               ANSI.TEXT_NORMAL))
                      else:
                        print("%sYou are STUNNED!%s" %
                              (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
                      defe.StunLevel += 2
                      logd("%s STUN_LEVEL %d" %
                           (defe.Person.Name, defe.StunLevel))
                  else:
                    print("IMPACT_ACTION: %s LEVEL:%d" %
                          (ia.Action, ia.Level))

                if defe.Flags & FLAG_DEAD > 0:
                  break

          else:
            print("\n*** %s ***" % res)

        if defe.Flags & FLAG_DEAD > 0 and defe.Person is not player:
          if defe.Person.CurrencyGen is not None:
            # currency
            r = defe.Person.CurrencyGen.Result()
            print("\nYou collect %d SP!" % (r))
            att.Person.Currency += r
          # handle loot
          if defe.Person.Loot is not None:
            logd("%s LOOT handling" % (defe.Person.Name))
            for item_id, chance in defe.Person.Loot.items():
              r = DiceRoll(1, 100).Result()
              logd("%s LOOT_CHECK %s: %d vs. %d" %
                   (defe.Person.Name, items[item_id].ItemName,
                    r, chance))
              if r <= chance:
                rooms[player.Room].AddItem(item_id, ItemLink(1))
          # remove enemy from room
          rooms[player.Room].RemovePerson(defe.UUID)
          att.Target = None

      else:
        logd("\n***%s HAD NO ATTACKS ***\n" % res)

      # check if dead
      if player_combatant.Flags & FLAG_DEAD > 0:
        break

    if player_combatant.Flags & FLAG_DEAD > 0:
      # penalties?
      sleep(2)
      print("\nYou slowly come back to your senses ...")
      sleep(2)
      player.CombatState = PlayerCombatState.NONE
      player.SetRoom(GameData.ROOM_RESPAWN)
      break

    if att.Action == Action.FLEE:
      player.Room = player.LastRoom
      player.CombatState = PlayerCombatState.NONE
      print("\n%sYou FLEE!%s" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
      break

# vim: set tabstop=2 shiftwidth=2 expandtab:
