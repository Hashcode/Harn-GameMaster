# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Utility Functions

from sys import exit
from textwrap import TextWrapper
from time import sleep

from global_defines import (attribute_classes, attributes, months, sunsigns,
                            cultures, social_classes, sibling_ranks, wounds,
                            parent_statuses, player_frames, comelinesses,
                            complexions, color_hairs, color_eyes,
                            skill_classes, skills, item_flags, body_parts,
                            materials, NumAdj, DamageTypeEnum, AttrEnum,
                            Material, PlayerCombatState, PersonTypeEnum,
                            ItemTypeEnum, ItemFlagEnum, DiceRoll,
                            ItemLink, DirectionEnum, ANSI, GameData)
from items import items
from db import (ListDB, SavePlayer)


wrapper = TextWrapper(width=70, fix_sentence_endings=True)


def CalcEffect(player, eff_type):
  value = 0
  for item_id, il in player.ItemLinks.items():
    if not items[item_id].Effects is None:
      for y in items[item_id].Effects:
        if y.EffectType == eff_type:
          value += y.Modifier * il.Quantity
  if player.Effects is not None:
    for y in player.Effects:
      if y.EffectType == eff_type:
        value += y.Modifer
  return value


def filterLinks(item_links, equipped=False, equippable=False, flags=0,
                noflags=0):
  item_dict = {}
  for item_id, il in item_links.items():
    if equippable:
      if not items[item_id].ItemType in \
          [ItemTypeEnum.WEAPON, ItemTypeEnum.ARMOR, ItemTypeEnum.RING]:
        continue
    if not equipped and il.Equipped and il.Quantity == 1:
      continue
    if equipped and not il.Equipped:
      continue
    if flags > 0 and items[item_id].Flags & flags == 0:
      continue
    if noflags > 0 and items[item_id].Flags & noflags > 0:
      continue
    item_dict.update({item_id: il})
  return item_dict


def printItems(item_links, number=False, stats=False):
  count = 0
  for item_id, il in item_links.items():
    count += 1
    if number:
      print("%d. %s%s" % (count, items[item_id].ItemName,
                          items[item_id].ItemFlagStr(" (%s)")))
    else:
      weight = items[item_id].Weight * il.Quantity
      if il.Quantity > 1 and not il.Equipped:
        print("%-30s : %5s lbs" %
              (("(%d) " % il.Quantity) + items[item_id].ItemName + \
               items[item_id].ItemFlagStr(" (%s)"),
               "{:3.1f}".format(weight)))
      else:
        print("%-30s : %5s lbs" %
              (items[item_id].ItemName + items[item_id].ItemFlagStr(" (%s)"),
               "{:3.1f}".format(weight)))


# Directions

directions = {
    DirectionEnum.NORTH: ["north", "n"],
    DirectionEnum.SOUTH: ["south", "s"],
    DirectionEnum.WEST: ["west", "w"],
    DirectionEnum.EAST: ["east", "e"],
    DirectionEnum.NORTHWEST: ["northwest", "nw"],
    DirectionEnum.NORTHEAST: ["northeast", "ne"],
    DirectionEnum.SOUTHWEST: ["southwest", "sw"],
    DirectionEnum.SOUTHEAST: ["southeast", "se"],
    DirectionEnum.UP: ["up", "u"],
    DirectionEnum.DOWN: ["down", "d"],
}


def printRoomDescription(room_id, rooms):
  print("")
  # Room Title
  if rooms[room_id].Title != "":
    print("%s%s%s" % (ANSI.TEXT_BOLD, rooms[room_id].Title, ANSI.TEXT_NORMAL))
  # Room Description
  if len(rooms[room_id].LongDescription) > 0:
    for para in rooms[room_id].LongDescription:
      print("\n" + wrapper.fill(para))
    # Exits
    if len(rooms[room_id].Exits) > 0:
      print("")
      for exit_dir, ex in rooms[room_id].Exits.items():
        print("To the %s%s%s is %s" % (ANSI.TEXT_BOLD,
                                       directions[exit_dir][0].upper(),
                                       ANSI.TEXT_NORMAL,
                                       rooms[ex.Room].ShortDescription))


def printRoomObjects(room_id, rooms):
  # Persons
  if len(rooms[room_id].Persons) > 0:
    print("")
    for x in rooms[room_id].Persons:
      print("%s" % x.LongDescription)
  # Items
  if len(rooms[room_id].RoomItems) > 0:
    print("\nThe following items are here:")
    printItems(rooms[room_id].RoomItems)


# GENERIC COMMAND FUNCTIONS

def actionComingSoon(player, rooms):
  print("\nComing soon!")


def actionDropItem(player, rooms):
  print("\nItems in your inventory:\n")
  links = filterLinks(player.ItemLinks, equipped=False)
  if len(links) < 1:
    print("Nothing is droppable at the moment.")
    return
  printItems(links, number=True)
  x = input("\nWhich item # to drop: ").lower()
  if not x.isnumeric():
    print("\nInvalid item.")
    return
  itemNum = int(x)
  if itemNum < 1 or itemNum > len(links):
    print("\nInvalid item.")
    return
  count = 0
  for item_id, il in links.items():
    count += 1
    if count != itemNum:
      continue
    if items[item_id].Flags & item_flags[ItemFlagEnum.NO_DROP].Bit > 0:
      print("\n%s cannot be dropped." % items[item_id].ItemName.capitalize())
      return
    player.RemoveItem(item_id, ItemLink(1))
    rooms[player.Room].AddItem(item_id, ItemLink(1))
    print("\n%s dropped." % items[item_id].ItemName.capitalize())
    break


def actionEquipItem(player, rooms):
  print("\nEquippable items in your inventory:\n")
  links = filterLinks(player.ItemLinks, equipped=False, equippable=True)
  if len(links) < 1:
    print("Nothing is equippable at the moment.")
    return
  printItems(links, number=True)
  x = input("\nWhich item # to equip: ").lower()
  if not x.isnumeric():
    print("\nInvalid item.")
    return
  itemNum = int(x)
  if itemNum < 0 or itemNum > len(links):
    print("\nInvalid item.")
    return
  count = 0
  for item_id, il in links.items():
    count += 1
    if count == itemNum:
      equip_id = item_id
  # check for item conflicts
  count = 0
  for item_id, il in player.ItemLinks.items():
    if not il.Equipped:
      continue
    # check armor coverage / layer conflicts
    if items[equip_id].ItemType == ItemTypeEnum.ARMOR and \
       items[item_id].ItemType == ItemTypeEnum.ARMOR:
      if items[item_id].Layer & items[equip_id].Layer > 0 and \
         items[item_id].Coverage & items[equip_id].Coverage > 0:
          print("\n%s is already equipped." %
                items[item_id].ItemName.capitalize())
          return
    # only 2 weapons/shields
    if items[equip_id].ItemType == ItemTypeEnum.WEAPON or \
       items[equip_id].ItemType == ItemTypeEnum.WEAPON:
      if items[item_id].ItemType == ItemTypeEnum.SHIELD or \
         items[item_id].ItemType == ItemTypeEnum.WEAPON:
        count += 1
        if count > 1:
            print("\nAlready wielding 2 weapons or shields.")
            return
    # only 2 rings
    if items[equip_id].ItemType == ItemTypeEnum.RING and \
       items[item_id].ItemType == ItemTypeEnum.RING:
      count += 1
      if count > 1:
          print("\nAlready wielding 2 rings.")
          return
  player.ItemLinks[equip_id].Equipped = True
  print("\n%s equipped." % items[equip_id].ItemName.capitalize())


def actionGetItem(player, rooms):
  print("\nItems in in the room:\n")
  links = filterLinks(rooms[player.Room].RoomItems, equipped=False)
  if len(links) < 1:
    print("There are no items in the room.")
    return
  printItems(links, number=True)
  x = input("\nWhich item # to pick up: ").lower()
  if not x.isnumeric():
    print("\nInvalid item.")
    return
  itemNum = int(x)
  if itemNum < 1 or itemNum > len(links):
    print("\nInvalid item.")
    return
  count = 0
  for item_id, il in links.items():
    count += 1
    if count == itemNum:
      rooms[player.Room].RemoveItem(item_id, ItemLink(1))
      player.AddItem(item_id, ItemLink(1))
      print("\n%s picked up." % items[item_id].ItemName.capitalize())
      break


def actionInventory(player, rooms):
  print("\n%sCURRENCY%s: %d SP" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL,
                                   player.Currency))
  print("\n%sEQUIPMENT%s" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  links = filterLinks(player.ItemLinks, equipped=True)
  if len(links) < 1:
    print("[NONE]")
  else:
    printItems(links)
  print("%s%-30s : %5s lbs%s" % (ANSI.TEXT_BOLD, "EQUIPPED WEIGHT",
                                 "{:3.1f}".format(player.EquipWeight(items)),
                                 ANSI.TEXT_NORMAL))
  print("\n%sITEMS%s" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  links = filterLinks(player.ItemLinks, equipped=False)
  if len(links) < 1:
    print("[NONE]")
  else:
    printItems(links)
  print("%s%-30s : %5s lbs%s" % (ANSI.TEXT_BOLD, "INVENTORY WEIGHT",
                                 "{:3.1f}".format(player.InvenWeight(items)),
                                 ANSI.TEXT_NORMAL))
  print("\n%s%-30s : %5s lbs%s" % (ANSI.TEXT_BOLD, "TOTAL WEIGHT",
                                   "{:3.1f}".format(player.ItemWeight(items)),
                                   ANSI.TEXT_NORMAL))


def actionSave(player, rooms):
  if SavePlayer(player, rooms[player.Room].Title, player.Password):
    return True
  else:
    print("%sAn error occured during SAVE!%s" %
          (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return False


def actionSkills(player, rooms):
  for skc_id, skc in skill_classes.items():
    if skc.Hidden:
      continue
    print("\n%s%s SKILLS%s\n" %
          (ANSI.TEXT_BOLD, skc.Name.upper(), ANSI.TEXT_NORMAL))
    for sk_id, sk in skills.items():
      if sk.SkillClass != skc_id:
        continue
      if sk.Hidden:
        continue
      print("%-15s: %s/%s/%s  ML:%-3d" %
            (sk.Name,
             attributes[skills[sk_id].Attr1].Abbrev,
             attributes[skills[sk_id].Attr2].Abbrev,
             attributes[skills[sk_id].Attr3].Abbrev,
             player.SkillML(sk_id, items)))


def actionInfo(player, rooms):
  print("\n%sBIRTH INFORMATION%s\n" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  # TODO: hardcoded Human for now
  print("%-15s: %s" % ("Name", player.Name))
  print("%-15s: %s" % (attributes[AttrEnum.SPECIES].Name, "Human"))
  print("%-15s: %s" % (attributes[AttrEnum.SEX].Name, player.AttrSexStr()))
  print("%-15s: %s %d%s" % ("Birth Month/Day",
                            months[player.Attr[AttrEnum.BIRTH_MONTH]].Name,
                            player.Attr[AttrEnum.BIRTH_DAY],
                            NumAdj(player.Attr[AttrEnum.BIRTH_DAY])))
  print("%-15s: %s (%s)" % ("Sunsign", sunsigns[player.Sunsign].Name,
                            sunsigns[player.Sunsign].Symbol))
  print("%-15s: %s" % (attributes[AttrEnum.CULTURE].Name,
                       cultures[player.AttrCulture()].Name))
  print("%-15s: %s" % (attributes[AttrEnum.SOCIAL_CLASS].Name,
                       social_classes[player.AttrSocialClass()].Name))
  print("%-15s: %s of %d" % (attributes[AttrEnum.SIBLING_RANK].Name,
                             sibling_ranks[player.AttrSiblingRank()].Name,
                             player.Attr[AttrEnum.SIBLING_COUNT]))
  print("%-15s: %s" % (attributes[AttrEnum.PARENT].Name,
                       parent_statuses[player.AttrParentStatus()].Name))
  print("\n%sAPPEARANCE%s\n" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  print("%-15s: %d\'%d\"" % (attributes[AttrEnum.HEIGHT].Name,
                             int(player.Attr[AttrEnum.HEIGHT] / 12),
                             player.Attr[AttrEnum.HEIGHT] % 12))
  print("%-15s: %s" % (attributes[AttrEnum.FRAME].Name,
                       player_frames[player.AttrFrame()].Name))
  print("%-15s: %d lbs" % (attributes[AttrEnum.WEIGHT].Name,
                           player.Attr[AttrEnum.WEIGHT]))
  print("%-15s: %s" % (attributes[AttrEnum.COMELINESS].Name,
                       comelinesses[player.AttrComeliness()].Name))
  print("%-15s: %s" % (attributes[AttrEnum.COMPLEXION].Name,
                       complexions[player.AttrComplexion()].Name))
  print("%-15s: %s" % (attributes[AttrEnum.COLOR_HAIR].Name,
                       color_hairs[player.AttrColorHair()].Name))
  print("%-15s: %s" % (attributes[AttrEnum.COLOR_EYE].Name,
                       color_eyes[player.AttrColorEye()].Name))


def actionStats(person, rooms):
  if person.PersonType == PersonTypeEnum.PLAYER:
    for ac_id, ac in attribute_classes.items():
      if ac.Hidden:
        continue
      print("\n%s%s STATS%s\n" % (ANSI.TEXT_BOLD, ac.Name.upper(),
                                  ANSI.TEXT_NORMAL))
      for attr, val in person.Attr.items():
        if not attributes[attr].Hidden:
          if attributes[attr].AttrClass == ac_id:
            print("%-15s: %d" % (attributes[attr].Name, val))
    print("\n%sCHARACTER STATS%s\n" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  else:
    print("\n%s%s STATS%s\n" % (ANSI.TEXT_BOLD, person.Name.upper(),
                                ANSI.TEXT_NORMAL))
  print("%-15s: %d" % ("Endurance", person.AttrEndurance(items)))
  print("%-15s: %d lbs" % ("Total Weight", person.ItemWeight(items)))
  print("%-15s: %d" % ("Enc. Points", person.EncumbrancePenalty(items)))
  print("%-15s: %d" % ("Injury Points", person.IP()))
  print("%-15s: %d" % ("Fatigue Points", person.FatiguePoints()))
  print("%-15s: %d" % ("Initiative", person.AttrInitiative(items)))
  print("\n%s%-15s: %d%s" % (ANSI.TEXT_BOLD, "Universal Pen.",
                             person.UniversalPenalty(), ANSI.TEXT_NORMAL))
  print("%s%-15s: %d%s" % (ANSI.TEXT_BOLD, "Physical Pen.",
                           person.PhysicalPenalty(items), ANSI.TEXT_NORMAL))
  print("\n%sWOUND LIST%s\n" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  if len(person.Wounds) < 1:
    print("[NONE]")
  else:
    for w in person.Wounds:
      print("%s %s %s wound [%d IP]" %
            (wounds[w.WoundType].Name,
             wounds[w.WoundType].Verbs[w.DamageType].lower(),
             body_parts[w.Location].PartName.lower(), w.Impact))


def actionArmor(player, rooms):
  print("\n%sARMOR COVERAGE%s\n" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  print("%s%-15s  BLUNT EDGE PIERCE ELEMENTAL%s" %
        (ANSI.TEXT_BOLD, "LOCATION", ANSI.TEXT_NORMAL))
  m = Material("None", 0, 0, [0, 0, 0, 0])
  for bp_id, bp in body_parts.items():
    m.Copy(materials[player.SkinMaterial])
    for item_id, il in player.ItemLinks.items():
      if items[item_id].ItemType != ItemTypeEnum.ARMOR:
        continue
      if not il.Equipped:
        continue
      if items[item_id].Covered(bp_id):
        m.Add(materials[items[item_id].Material])
    print("%-15s: %-5d %-4d %-6d %-9d" %
          (body_parts[bp_id].PartName,
           m.Protection[DamageTypeEnum.BLUNT],
           m.Protection[DamageTypeEnum.EDGE],
           m.Protection[DamageTypeEnum.PIERCE],
           m.Protection[DamageTypeEnum.ELEMENTAL]))
    m.Clear()


def actionRemoveItem(player, rooms):
  print("\nYour equipped items:\n")
  links = filterLinks(player.ItemLinks, equipped=True)
  if len(links) < 1:
    print("Nothing is equipped.")
    return
  printItems(links, number=True)
  x = input("\nWhich item # to remove: ").lower()
  if not x.isnumeric():
    print("\nInvalid item.")
    return
  itemNum = int(x)
  if itemNum < 0 or itemNum > len(links):
    print("\nInvalid item.")
    return
  count = 0
  for item_id, il in links.items():
    count += 1
    if count == itemNum:
      player.ItemLinks[item_id].Equipped = False
      print("\n%s removed." % items[item_id].ItemName.capitalize())
      break


def actionAttack(player, rooms):
  # let combat "attack" handle work if in combat
  if player.CombatState != PlayerCombatState.NONE:
    return False
  print("\nChoose a target:\n")
  if len(rooms[player.Room].Persons) < 1:
    print("[NONE]")
    return
  count = 0
  for t in rooms[player.Room].Persons:
    count += 1
    print("%d. %s" % (count, t.Name))
  x = input("\nWhich # to attack: ").lower()
  if not x.isnumeric():
    print("\nInvalid target.")
    return
  personNum = int(x)
  if personNum < 1 or personNum > len(rooms[player.Room].Persons):
    print("\nInvalid target.")
    return
  count = 0
  for x in rooms[player.Room].Persons:
    count += 1
    if count == personNum:
      player.CombatTarget = x.UUID
      break
  if player.CombatTarget is not None:
    return True


def actionExamine(player, rooms):
  print("\nChoose a target:\n")
  if len(rooms[player.Room].Persons) < 1:
    print("[NONE]")
    return
  count = 0
  for t in rooms[player.Room].Persons:
    count += 1
    print("%d. %s" % (count, t.Name))
  x = input("\nWhich # to examine: ").lower()
  if not x.isnumeric():
    print("\nInvalid target.")
    return
  personNum = int(x)
  if personNum < 1 or personNum > len(rooms[player.Room].Persons):
    print("\nInvalid target.")
    return
  count = 0
  for x in rooms[player.Room].Persons:
    count += 1
    if count == personNum:
      actionStats(x, rooms)
      break


def actionListPlayers(player, rooms):
  pinfo = ListDB()
  if len(pinfo) == 0:
    print("\nThere are no saved characters!")
  else:
    print("\n%s%-20s %s%s" % (ANSI.TEXT_BOLD, "CHARACTER NAME",
                              "SAVED IN ROOM", ANSI.TEXT_NORMAL))
    print("%s%-20s %s%s" % (ANSI.TEXT_BOLD, "--------------",
                            "-------------", ANSI.TEXT_NORMAL))
    for x in sorted(pinfo):
      print("%-20s %s" % (x, pinfo[x]))


def actionLook(player, rooms):
  printRoomDescription(player.Room, rooms)
  printRoomObjects(player.Room, rooms)


def actionChangePassword(player, rooms):
  if player.CombatState != PlayerCombatState.NONE:
    print("\n%sYou can't change your password in combat!%s" %
          (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  else:
    print("\nYour password is used to encrypt SAVE data.")
    print("It should NOT be a password used for anything important.")
    x = input("\nEnter a password: ").upper
    if len(x.Password) < 3 or len(x.Password) > 10:
      print("\nPassword needs to be between 3 and 10 characters long.")
    player.Password = x
    if actionSave(player, rooms):
      print("\nCharacter updated.")


def actionQuit(player, rooms):
  if player.CombatState != PlayerCombatState.NONE:
    print("\n%sYou can't QUIT in combat!%s" %
          (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  else:
    y = input("\nAre you sure you wish to QUIT? ").lower()
    if y == "y" or y == "yes":
      actionSave(player, rooms)
      print("\nGoodbye!\n")
      exit()
    else:
      print("\nQuit aborted.")


def actionRest(player, rooms):
  if player.CombatState != PlayerCombatState.NONE:
    print("\n%sYou can't REST during combat!%s" %
          (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  elif player.IP() < 1:
    print("\nYou are well rested.")
  else:
    # health restore
    print("\nYou take a moment to rest ...")
    combat = False
    for i in range(2):
      sleep(5)
      GameData.ProcessRoomEvents()
      # Check if the room persons need to attack
      enemies = GameData.ProcessRoomCombat(player)
      if len(enemies) > 0:
        print("")
        combat = True
        combat(player, enemies)
        break
      if not combat:
        for w in sorted(player.Wounds, reverse=True):
          print("\nYou clean and dress a %s %s %s wound." %
                (wounds[w.WoundType].Name.lower(),
                 wounds[w.WoundType].Verbs[w.DamageType].lower(),
                 body_parts[w.Location].PartName.lower()))
          sleep(5)
          r = DiceRoll(1, player.Attr[AttrEnum.AURA]).Result()
          w.Impact -= r
          if w.Impact <= 0:
            player.Wounds.remove(w)
            print("It's all better!")
          else:
            print("It looks a bit better.")
          break


def actionSaveGeneric(player, rooms):
  if player.CombatState != PlayerCombatState.NONE:
    print("\n%sYou can't SAVE in combat!%s" %
          (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  else:
    if actionSave(player, rooms):
      print("\nCharacter saved.")


class GenericCommand:
  def __init__(self, cmds, cmd_func, desc=""):
    self.Commands = []
    self.Description = desc
    self.Function = cmd_func
    if cmds is not None:
      for c in cmds:
        self.Commands.append(c)


commands = []


def actionPrintHelp(player, rooms):
    print("\nGENERAL COMMANDS:\n")
    # generic commands
    for cmd in commands:
      cmd_len = len(cmd.Commands)
      if cmd_len > 1:
        abbrevs = " ["
        for x in range(1, cmd_len):
          if x > 1:
            abbrevs += ", "
          abbrevs += cmd.Commands[x].upper()
        abbrevs += "]"
      else:
        abbrevs = ""
      print("%-10s%s" % (cmd.Commands[0].upper(), abbrevs))
    # exits
    if not rooms[player.Room].Exits is None:
      print("\nMOVE DIRECTION:\n")
      for exit_dir, exit_names in directions.items():
        dir_len = len(exit_names)
        if dir_len > 1:
          abbrevs = " ["
          for x in range(1, dir_len):
            if x > 1:
              abbrevs += ", "
            abbrevs += exit_names[x].upper()
          abbrevs += "]"
        else:
          abbrevs = ""
        print("%-10s%s" % (exit_names[0].upper(), abbrevs))
    # break prompt loop to let other sections add commands
    return False


commands.append(GenericCommand(["armor", "ac"], actionArmor))
commands.append(GenericCommand(["attack", "a"], actionAttack))
commands.append(GenericCommand(["close"], actionComingSoon))
commands.append(GenericCommand(["drop"], actionDropItem))
commands.append(GenericCommand(["equip", "eq"], actionEquipItem))
commands.append(GenericCommand(["examine", "ex"], actionExamine))
commands.append(GenericCommand(["get"], actionGetItem))
commands.append(GenericCommand(["help", "?"], actionPrintHelp))
commands.append(GenericCommand(["info", "inf"], actionInfo))
commands.append(GenericCommand(["inventory", "i"], actionInventory))
commands.append(GenericCommand(["look", "l"], actionLook))
commands.append(GenericCommand(["open"], actionComingSoon))
commands.append(GenericCommand(["password"], actionChangePassword))
commands.append(GenericCommand(["quit", "q"], actionQuit))
commands.append(GenericCommand(["remove", "rm"], actionRemoveItem))
commands.append(GenericCommand(["rest"], actionRest))
commands.append(GenericCommand(["save"], actionSaveGeneric))
commands.append(GenericCommand(["skills", "sk"], actionSkills))
commands.append(GenericCommand(["stats", "st"], actionStats))
commands.append(GenericCommand(["unlock"], actionComingSoon))
commands.append(GenericCommand(["who"], actionListPlayers))


def prompt(player, rooms, func_break=False):
  player.Command = ""
  while True:
    x = input("\n[? = HELP] Command: ").lower()
    if x == "":
      continue

    # Handle universal commands
    cmd_match = None
    for gen_cmd in commands:
      for cmds in gen_cmd.Commands:
        if x == cmds:
          cmd_match = gen_cmd
          break
    if cmd_match is not None:
      res = cmd_match.Function(player, rooms)
      if func_break and res == False:
        player.Command = x
        break
      elif res == True:
        player.Command = x
        break
    else:
      # Handle directions
      match_dir = DirectionEnum.NONE
      for d, d_cmds in directions.items():
        for d_cmd in d_cmds:
          if x == d_cmd.lower():
            match_dir = d
            break

      if match_dir != DirectionEnum.NONE:
        if player.CombatState != PlayerCombatState.NONE:
          print("\n%sYou can't move in combat!  Try to FLEE!%s" %
                (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
        else:
          for exit_dir, ex in rooms[player.Room].Exits.items():
            if match_dir == exit_dir:
              player.SetRoom(ex.Room)
              return
          print("\n%sYou can't go in that direction.%s" %
                (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
        continue

      player.Command = x
      break

# vim: tabstop=2 shiftwidth=2 expandtab:
