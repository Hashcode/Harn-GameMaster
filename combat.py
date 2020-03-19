# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Combat Function

from time import sleep

from console import (TEXT_COLOR, ANSI, InputFlag)
from global_defines import (DiceRoll, Roll, CoverageEnum, body_parts,
                            AimEnum, SkillEnum, ItemTypeEnum,
                            PlayerCombatState, wounds, PersonWound,
                            AttrEnum, PersonTypeEnum, ImpactActionEnum)
from gamedata import (GameData)
from logger import (logd, loge)
from table_melee_attack import (Action, ResultEnum, T_ATK, T_DEF,
                                resolve_melee)
from table_dmg import dmg_table_melee
from utils import (printPaginate, actionPrintCombatHelp, chooseNPC, prompt)


# Combat Flags
FLAG_DEAD = 1 << 0


class Combatant:
  def __init__(self, person, uid):
    self.Person = person
    self.UUID = uid
    self.Init = 0
    self.TAdvCount = 0
    self.Flags = 0
    self.StunLevel = 0
    self.Bleed = 0
    self.Bloodloss = 0
    self.Prone = False
    self.Action = Action.IGNORE
    self.Aim = AimEnum.MID
    self.Target = None
    self.Roll = Roll.NONE
    self.Attacks = None
    self.TurnTaken = False
    self.FumbleItem = None
    self.DefAction = Action.IGNORE

  def Refresh(self):
    if self.StunLevel > 0:
      self.Init = 0
    else:
      self.Init = DiceRoll(1, 100).Result()
      self.Init += self.Person.AttrInitiative()
      if self.Prone:
        self.Init -= 50
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


# COMBAT COMMANDS

def chooseDefense(combatant):
  cm = GameData.GetConsole()
  count = 1
  cm.Print("\nChoose a defense:\n")
  cm.Print("1. DODGE [%d ML]" % combatant.Person.AttrDodge())
  defe_att = combatant.Person.GenerateCombatAttacks(block=True)
  if len(defe_att) > 0:
    count = 2
    cm.Print("2. BLOCK with %s [%d ML]" %
             (defe_att[0].Name.lower(), defe_att[0].SkillML))
  x = cm.Input("Which defense #:", line_length=3,
               input_flags=InputFlag.NUMERIC)
  if not x.isnumeric():
    cm.Print("\nInvalid defense.")
    return
  defeNum = int(x)
  if defeNum < 1 or defeNum > count:
    cm.Print("\nInvalid defense.")
    return
  if defeNum == 1:
    combatant.DefAction = Action.DODGE
  elif count > 1 and defeNum == 2:
    combatant.DefAction = Action.BLOCK


def chooseTarget(att, combatants):
  cm = GameData.GetConsole()
  npcs = []
  for c in combatants:
    if c.Person.PersonType == PersonTypeEnum.NPC:
      if c.Flags & FLAG_DEAD == 0:
        npcs.append(c.Person)
  if len(npcs) < 1:
    cm.Print("\nThere is nothing to attack nearby!")
    return
  p = chooseNPC(npcs, "attack", stats=True)
  if p is not None:
    for c in combatants:
      if c.Person.PersonType == PersonTypeEnum.NPC:
        if c.Flags & FLAG_DEAD == 0:
          if c.UUID == p.UUID:
            att.Target = c
            break


def HandlePlayerDeath(player):
  cm = GameData.GetConsole()
  # penalties?
  sleep(2)
  cm.Print("\nYou slowly come back to your senses ...")
  sleep(2)
  player.CombatState = PlayerCombatState.NONE
  player.SetRoom(GameData.ROOM_RESPAWN)


def HandleMobDeath(att, defe):
  cm = GameData.GetConsole()
  rooms = GameData.GetRooms()
  if defe.Person.CurrencyGen is not None:
    # currency
    r = defe.Person.CurrencyGen.Result()
    cm.Print("\nYou collect %d SP!" % (r))
    att.Person.Currency += r
  # handle loot
  if defe.Person.Loot is not None:
    logd("%s LOOT handling" % (defe.Person.Name))
    for item, chance in defe.Person.Loot.items():
      r = DiceRoll(1, 100).Result()
      logd("%s LOOT_CHECK %s: %d vs. %d" %
           (defe.Person.Name, item.ItemName, r, chance))
      if r <= chance:
        rooms[att.Person.Room].AddItem(item)
  # remove enemy from room
  rooms[att.Person.Room].RemovePerson(defe.UUID)
  del defe.Person
  defe.Person = None
  att.Target = None


def CombatantFumble(combatant, att_item):
  cm = GameData.GetConsole()
  if combatant.Person is GameData.GetPlayer():
    cm.Print("\nYou FUMBLE your %s!" %
             (combatant.Attacks[0].Name.lower()),
             attr=ANSI.TEXT_BOLD)
  else:
    cm.Print("\n%s FUMBLES %s %s!" %
             (combatant.Person.Name.capitalize(),
              combatant.Person.AttrSexPossessivePronounStr().lower(),
              combatant.Attacks[0].Name.lower()),
             attr=ANSI.TEXT_BOLD)
  # unequip weapon
  for item in combatant.Person.Items:
    if att_item.UUID == item.UUID and item.Equipped:
      combatant.FumbleItem = item
      item.Equipped = False
      break


def CombatantStumble(combatant):
  cm = GameData.GetConsole()
  if combatant.Person is GameData.GetPlayer():
    cm.Print("You STUMBLE to the ground!",
             attr=cm.ColorPair(TEXT_COLOR.BRIGHT_YELLOW))
  else:
    cm.Print("%s STUMBLES to the ground!" %
             (combatant.Person.Name.capitalize()),
             attr=cm.ColorPair(TEXT_COLOR.BRIGHT_YELLOW))
  combatant.Prone = True


def HandleImpactDMG(player, att, defe, at, res_level):
  cm = GameData.GetConsole()
  break_loop = False

  # attacker lands impact
  impact = at.Roll.Result()
  for x in range(res_level):
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
  impact -= defe.Person.Defense(loc, at.DamageType)
  logd("%s ADJ. IMPACT: %d" % (att.Person.Name, impact))
  leftright = ""
  if body_parts[loc].LeftRight:
    if r % 2 == 1:
      leftright = "left "
    else:
      leftright = "right "
  if att.Person == player:
    cm.Print("\nYou HIT %s's %s%s with your %s!" %
             (defe.Person.Name, leftright,
              body_parts[loc].PartName.lower(), at.Name.lower()))
  else:
    cm.Print("\n%s HITS your %s%s with %s %s!" %
             (att.Person.Name.capitalize(), leftright,
              body_parts[loc].PartName.lower(),
              att.Person.AttrSexPossessivePronounStr().lower(),
              at.Name.lower()))

  if (impact <= 0):
    s = "S"
    if at.Name.lower().endswith("s"):
      s = ""
    if att.Person == player:
      cm.Print("Your %s GLANCE%s off %s with no effect!" %
               (at.Name.lower(), s, defe.Person.Name))
    else:
      cm.Print("%s's %s GLANCE%s off you with no effect!" %
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
          cm.Print("%s suffers a %s wound!" %
                   (defe.Person.Name.capitalize(),
                    wounds[ia.Action].Name.lower()),
                   attr=ANSI.TEXT_BOLD)
        else:
          cm.Print("You suffer a %s wound!" % (wounds[ia.Action].Name.lower()),
                   attr=ANSI.TEXT_BOLD)
        w = PersonWound(ia.Action, at.DamageType, loc,
                        impact + wounds[ia.Action].IPBonus)
        defe.Person.Wounds.append(w)

        # determine if the Injury Point Index is > STA == DEATH
        logd("%s WOUND DEATH check: %d vs. %d STA" %
             (defe.Person.Name, defe.Person.IPIndex(),
              defe.Person.Attr[AttrEnum.STAMINA]))
        if defe.Person.IPIndex() > \
           defe.Person.Attr[AttrEnum.STAMINA]:
          if att.Person == player:
            cm.Print("%s DIES from %s wounds!" %
                     (defe.Person.Name.capitalize(),
                      defe.Person.AttrSexPossessivePronounStr()),
                     attr=cm.ColorPair(TEXT_COLOR.BRIGHT_RED))
          else:
            cm.Print("You DIE from your wounds!",
                     attr=ANSI.TEXT_BLINK | cm.ColorPair(TEXT_COLOR.BRIGHT_RED))
          defe.Flags |= FLAG_DEAD
          return True

      elif ia.Action == ImpactActionEnum.KILL_CHECK:
        r = DiceRoll(ia.Level, 6).Result()
        logd("%s DEATH check: %d vs. %d STA" %
             (defe.Person.Name, r,
              defe.Person.Attr[AttrEnum.STAMINA]))
        if r > defe.Person.Attr[AttrEnum.STAMINA]:
          # DEATH!
          if att.Person == player:
            cm.Print("%s DIES instantly!" % (defe.Person.Name.capitalize()),
                     attr=cm.ColorPair(TEXT_COLOR.BRIGHT_RED))
          else:
            cm.Print("You DIE instantly!",
                     attr=ANSI.TEXT_BLINK | cm.ColorPair(TEXT_COLOR.BRIGHT_RED))
          defe.Flags |= FLAG_DEAD
          return True

      # elif ia.Action == ImpactActionEnum.AMPUTATE_CHECK:

      elif ia.Action == ImpactActionEnum.SHOCK:
        num = ia.Level + defe.Person.UniversalPenaltyIndex()
        r = DiceRoll(num, 6).Result()
        logd("%s SHOCK check: %d vs. %d END" %
             (defe.Person.Name, r,
              defe.Person.AttrEndurance()))
        if r > defe.Person.AttrEndurance():
          if att.Person == player:
            cm.Print("%s is STUNNED!" % (defe.Person.Name.capitalize()),
                     attr=cm.ColorPair(TEXT_COLOR.BRIGHT_YELLOW))
          else:
            cm.Print("You are STUNNED!",
                     attr=cm.ColorPair(TEXT_COLOR.BRIGHT_YELLOW))
          defe.StunLevel += 2
          logd("%s STUN_LEVEL %d" % (defe.Person.Name, defe.StunLevel))

      if ia.Action == ImpactActionEnum.FUMBLE:
        # treat unarmed fumble as stumble
        if len(defe.Attacks) < 1:
          ia.Action = ImpactActionEnum.STUMBLE
        elif defe.Attacks[0].SkillID == SkillEnum.UNARMED:
          ia.Action = ImpactActionEnum.STUMBLE
        else:
          r = DiceRoll(ia.Level, 6).Result() + defe.Person.PhysicalPenalty()
          if r > defe.Person.Attr[AttrEnum.DEXTERITY]:
            CombatantFumble(defe, defe.Attacks[0].Item)
      if ia.Action == ImpactActionEnum.STUMBLE:
        r = DiceRoll(ia.Level, 6).Result() + defe.Person.PhysicalPenalty()
        if r > defe.Person.Attr[AttrEnum.AGILITY]:
          CombatantStumble(defe)
      if ia.Action == ImpactActionEnum.BLEED:
        if att.Person == player:
          cm.Print("%s's wound is BLEEDING!" % (defe.Person.Name.capitalize()),
                   attr=cm.ColorPair(TEXT_COLOR.BRIGHT_RED))
        else:
          cm.Print("Your wound is BLEEDING!",
                   attr=cm.ColorPair(TEXT_COLOR.BRIGHT_RED))
        defe.Bleed += ia.Level
        logd("%s BLEED %d" % (defe.Person.Name, defe.Bleed))

  if defe.Flags & FLAG_DEAD > 0:
    break_loop = True

  return break_loop


def DetermineDefense(combatant):
  if combatant.StunLevel > 0:
    combatant.Action = Action.IGNORE
  else:
    combatant.Attacks = combatant.Person.GenerateCombatAttacks(block=True)
    if len(combatant.Attacks) < 1:
      combatant.Action = Action.DODGE
    # check player defense preference
    elif combatant.DefAction != Action.IGNORE:
      combatant.Action = combatant.DefAction
    elif combatant.Person.AttrDodge() > combatant.Attacks[0].SkillML:
      combatant.Action = Action.DODGE
    else:
      combatant.Action = Action.BLOCK


def commandHandler(command, data):
  cm = GameData.GetConsole()
  order = data[0]
  att = data[1]
  if command == "stand":
    if att.Prone:
      cm.Print("\nYou stand up.")
      att.Prone = False
      att.Action = Action.IGNORE
      return True
    else:
      cm.Print("\nYou are already standing.")
  elif command == "attack" or command == "a":
    if att.Prone:
      cm.Print("\nYou can't attack while on the ground!")
    else:
      if att.Target is None:
        cm.Print("\nYou have no target!")
      else:
        att.Action = Action.MELEE
        att.Attacks = att.Person.GenerateCombatAttacks()
        return True
  elif command == "defense" or command == "def":
    chooseDefense(att)
  elif command == "equip" or command == "eq":
    # equipped an item == lose a turn
    att.Action = Action.IGNORE
    return True
  elif command == "aim":
    cm.Print("\nComing soon!")
  elif command == "cast" or command == "c":
    cm.Print("\nComing soon!")
  elif command == "flee" or command == "f":
    # TODO: implement skill check
    # if player == FLEE, choose dodge automatically
    # check for a valid exit
    att.Action = Action.FLEE
    return True
  elif command == "pass" or command == "p":
    cm.Print("\nYou choose to skip your action.")
    att.Action = Action.IGNORE
    return True
  elif command == "target" or command == "t":
    chooseTarget(att, order)
  else:
    return False


def HandleAttack(att, order, player_combatant, TAdv=False):
  cm = GameData.GetConsole()

  # will return a combatant who gets Tactical Advantage if needed
  ret = None

  player = GameData.GetPlayer()
  defe = None

  if att.Flags & FLAG_DEAD > 0:
    return ret

  if att.StunLevel > 0:
    return ret

  if att.Person == player:
    player.CombatState = PlayerCombatState.ATTACK

    # auto select a single attacker for player, or let choose
    if att.Target is None:
      count = 0
      m = None
      for x in order:
        if x.Person is None:
          continue
        if x.Person.PersonType == PersonTypeEnum.NPC and \
           x.Flags & FLAG_DEAD == 0:
          count += 1
          m = x
          if player.CombatTarget == x.Person.UUID:
            att.Target = x
            break
      if att.Target is None and count == 1:
        att.Target = m
      elif count > 1:
        while True:
          chooseTarget(att, order)
          if att.Target is not None:
            break
      else:
        return ret
    defe = att.Target

    logd("PLAYER ACTION: %s vs. %s" %
         (att.Person.Name, defe.Person.Name))

    DetermineDefense(defe)

    if TAdv:
      cm.Print("\nTACTICAL ADVANTAGE!",
               attr=ANSI.TEXT_BOLD | cm.ColorPair(TEXT_COLOR.GREEN))
    lines = []
    actionPrintCombatHelp(lines, [None, att, defe])
    printPaginate(lines)
    prompt(commandHandler, [order, att, defe])

  else:
    player.CombatState = PlayerCombatState.DEFEND
    defe = player_combatant

    # mob chooses attack action
    #   flee?
    if att.Prone:
      att.Prone = False
      att.Action = Action.IGNORE
      cm.Print("\n%s gets up." % (att.Person.Name.capitalize()),
               attr=cm.ColorPair(TEXT_COLOR.YELLOW))
    # check for weapon to equip (FUMBLE)
    elif att.FumbleItem is not None:
      cm.Print("\n%s takes a moment to equip %s." %
               (att.Person.Name.capitalize(), att.FumbleItem.ItemName),
               attr=cm.ColorPair(TEXT_COLOR.YELLOW))
      for item in att.Person.Items:
        if item.UUID == att.FumbleItem.UUID and not item.Equipped:
          item.Equipped = True
          break
      att.Action = Action.IGNORE
      att.FumbleItem = None
    else:
      att.Action = Action.MELEE
      logd("%s: Generate Attack" % (att.Person.Name))
      att.Attacks = att.Person.GenerateCombatAttacks()
      if len(att.Attacks) == 0:
        loge("MOB ERROR! %s no attack!" % (att.Person.Name))
        att.Action = Action.IGNORE
      else:
        logd("%s attack: %s" % (att.Person.Name, att.Attacks[0].Name))
      # use default Aim zone
      att.Aim = att.Person.DefaultAim

      # pause scroll momentarily
      sleep(1)
      DetermineDefense(defe)

  # RESOLUTION PHASE

  if att.Action == Action.FLEE:
    return ret

  if att.Action == Action.IGNORE:
    return ret

  if att.Attacks is not None:
    for at in att.Attacks:
      att.Roll = att.Person.ResolveSkill(at.SkillML, at.SkillID)
      if defe.Action == Action.BLOCK:
        if len(defe.Attacks) < 1:
          defe.Action = Action.DODGE
        else:
          defe.Roll = defe.Person.ResolveSkill(defe.Attacks[0].SkillML,
                                               defe.Attacks[0].SkillID)
      if defe.Action == Action.DODGE:
        defe.Roll = defe.Person.ResolveSkill(defe.Person.AttrDodge(),
                                             SkillEnum.DODGE)
      # use resolve_melee for now
      res = resolve_melee[att.Roll][defe.Action][defe.Roll]

      if res.Result == ResultEnum.DODGE:
        if att.Person == player:
          cm.Print("\n%s DODGES you." % defe.Person.Name.capitalize())
        else:
          cm.Print("\nYou DODGE %s." % att.Person.Name)

      if res.Result == ResultEnum.BLOCK:
        if att.Person == player:
          cm.Print("\n%s BLOCKS your attack with %s %s." %
                   (defe.Person.Name.capitalize(),
                    defe.Person.AttrSexPossessivePronounStr().lower(),
                    defe.Attacks[0].Name.lower()))
        else:
          cm.Print("\nYou BLOCK %s with your %s." %
                   (att.Person.Name, defe.Attacks[0].Name.lower()))

      origTargetFlag = res.TargetFlag
      if res.Result == ResultEnum.FUMBLE:
        if T_ATK & res.TargetFlag > 0:
          if at.SkillID == SkillEnum.UNARMED:
            res.Result = ResultEnum.STUMBLE
          else:
            # handled attacker flag
            res.TargetFlag &= ~T_ATK
            r = DiceRoll(res.Level, 6).Result()
            r += att.Person.PhysicalPenalty()
            # account for strapped on shield
            if at.Item.ItemType == ItemTypeEnum.SHIELD:
              r -= 5
            if r > att.Person.Attr[AttrEnum.DEXTERITY]:
              CombatantFumble(att, at.Item)
            else:
              res.Result = ResultEnum.MISS
        if T_DEF & res.TargetFlag > 0:
          if defe.Attacks[0].SkillID == SkillEnum.UNARMED:
            res.Result = ResultEnum.STUMBLE
          else:
            # handled defender flag
            res.TargetFlag &= ~T_DEF
            r = DiceRoll(res.Level, 6).Result()
            r += defe.Person.PhysicalPenalty()
            # account for strapped on shield
            if defe.Attacks[0].Item.ItemType == ItemTypeEnum.SHIELD:
              r -= 5
            if r > defe.Person.Attr[AttrEnum.DEXTERITY]:
              CombatantFumble(defe, defe.Attacks[0].Item)
          # T_ATK is not in targets, reset this to also show attacker missed
          if T_ATK & origTargetFlag == 0:
            res.Result = ResultEnum.MISS

      # handle outside if/elif blocks in case FUMBLE -> STUMBLE
      if res.Result == ResultEnum.STUMBLE:
        if T_ATK & res.TargetFlag > 0:
          r = DiceRoll(res.Level, 6).Result() + att.Person.PhysicalPenalty()
          if r > att.Person.Attr[AttrEnum.AGILITY]:
            CombatantStumble(att)
          else:
            res.Result = ResultEnum.MISS
        if T_DEF & res.TargetFlag > 0:
          r = DiceRoll(res.Level, 6).Result() + defe.Person.PhysicalPenalty()
          if r > defe.Person.Attr[AttrEnum.AGILITY]:
            CombatantStumble(defe)
          # T_ATK is not in targets, reset this to also show attacker missed
          if T_ATK & origTargetFlag == 0:
            res.Result = ResultEnum.MISS

      if res.Result == ResultEnum.TADV:
        # Only the current defender can get a Tactical Advantage
        if res.TargetFlag & T_DEF > 0 and defe.TAdvCount < 1:
          defe.TAdvCount += 1
          if defe.Person == player:
            cm.Print("\nAttacker FAILURE! You get a free action!",
                     attr=ANSI.TEXT_BOLD)
          else:
            cm.Print("\nAttacker FAILURE! %s gets a free action!" %
                     defe.Person.Name.capitalize(),
                     attr=cm.ColorPair(TEXT_COLOR.YELLOW))
          ret = defe
        # more than 1 TAdv in a turn == MISS text
        else:
          res.Result = ResultEnum.MISS

      if res.Result == ResultEnum.MISS:
        if att.Person == player:
          cm.Print("\nYou MISS %s with your %s." %
                   (defe.Person.Name, at.Name.lower()))
        else:
          cm.Print("\n%s MISSES you with %s %s." %
                   (att.Person.Name.capitalize(),
                    att.Person.AttrSexPossessivePronounStr().lower(),
                    at.Name.lower()))

      # Only the current attacker can do damage
      if res.Result == ResultEnum.DMG:
        if HandleImpactDMG(player, att, defe, at, res.Level):
          break

    if defe.Flags & FLAG_DEAD > 0 and defe.Person is not player:
      HandleMobDeath(att, defe)

  else:
    logd("\n***%s HAD NO ATTACKS ***\n" % res)

  return ret


def combat(player, enemies):
  cm = GameData.GetConsole()
  # start of combat checks?
  order = []
  round_count = 0

  # setup combatants
  player_combatant = Combatant(player, 0)
  DetermineDefense(player_combatant)
  player_combatant.DefAction = player_combatant.Action
  order.append(player_combatant)
  for x in enemies:
      order.append(Combatant(x, x.UUID))

  while True:
    logd("** START ROUND **")
    round_count += 1

    # checks for:
    # - end of combat
    # - reduce stun levels
    # - bloodloss
    all_dead = True
    for x in order:
      if x.Person is None:
        continue
      # check for bleed every 6 rounds (1 minute)
      if round_count % 6 == 0:
        if x.Bleed > 0:
          if x.Person is player:
            cm.Print("\nYou are BLEEDING!",
                     attr=cm.ColorPair(TEXT_COLOR.BRIGHT_RED))
          else:
            cm.Print("\n%s is BLEEDING!" % (x.Person.Name.capitalize()),
                     attr=cm.ColorPair(TEXT_COLOR.BRIGHT_RED))
          x.Bloodloss += x.Bleed
          if x.Bloodloss > x.Person.AttrEndurance():
            # death from blood loss
            if x.Person is player:
              cm.Print("You EXPIRE from loss of blood!",
                       attr=ANSI.TEXT_BLINK | cm.ColorPair(TEXT_COLOR.BRIGHT_RED))
            else:
              cm.Print("%s EXPIRES from loss of blood!" %
                       (x.Person.Name.capitalize()),
                       attr=cm.ColorPair(TEXT_COLOR.BRIGHT_RED))
            x.Flags |= FLAG_DEAD
            if x.Person is player:
              HandlePlayerDeath(player)
              break
            else:
              HandleMobDeath(player_combatant, x)
      if x.StunLevel > 0 and x.Flags & FLAG_DEAD == 0:
        x.StunLevel -= 1
        logd("%s STUN_LEVEL %d" %
             (x.Person.Name, x.StunLevel))
        if x.StunLevel < 1:
          if x.Person is player:
            cm.Print("\nYour stun WEARS OFF!",
                     attr=cm.ColorPair(TEXT_COLOR.BRIGHT_YELLOW))
          else:
            cm.Print("\n%s's stun WEARS OFF!" %
                     (x.Person.Name.capitalize()),
                     attr=cm.ColorPair(TEXT_COLOR.BRIGHT_YELLOW))
      if x is not player_combatant and x.Flags & FLAG_DEAD == 0:
        all_dead = False
    if all_dead:
      player.CombatState = PlayerCombatState.NONE
      return

    if player_combatant.Flags & FLAG_DEAD > 0:
      return

    # 10 second rounds
    player.GameTime += 10
    player.CombatState = PlayerCombatState.WAIT
    for x in order:
        x.Refresh()
        logd("%s init %d" % (x.Person.Name, x.Init))

    # TURN loop
    for att in sorted(order, reverse=True):
      # enemy may be removed
      if att.Person is None:
        continue

      logd("** TURN %s **" % att.Person.Name)
      att.TurnTaken = True

      # reset combatants TAdvCount
      for x in order:
        x.TAdvCount = 0

      # turn attacks (combat returns TAdv target)
      x = att
      count = 0
      while True:
        count += 1
        x = HandleAttack(x, order, player_combatant, count > 1)
        if x is None:
          break

      # check if dead
      if player_combatant.Flags & FLAG_DEAD > 0:
        break

      if att.Action == Action.FLEE:
        break

    if player_combatant.Flags & FLAG_DEAD > 0:
      HandlePlayerDeath(player)
      break

    if att.Action == Action.FLEE:
      player.Room = player.LastRoom
      player.CombatState = PlayerCombatState.NONE
      cm.Print("\nYou FLEE!", attr=cm.ColorPair(TEXT_COLOR.BRIGHT_YELLOW))
      break

# vim: set tabstop=2 shiftwidth=2 expandtab:
