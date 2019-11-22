# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Utility Functions

from sys import exit
from textwrap import TextWrapper

from global_defines import (attribute_classes, attributes, months, sunsigns,
                            cultures, social_classes, sibling_ranks,
                            parent_statuses, player_frames, comelinesses,
                            complexions, color_hairs, color_eyes,
                            skills, item_flags, body_parts, materials,
                            NumAdj, AttrEnum, Material,
                            EffectTypeEnum, ItemTypeEnum, ItemFlagEnum,
                            ItemLink, DirectionEnum,
                            PERS_COMBAT, ANSI)
from items import items
from person import persons
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


def CalcHitPoints_Max(player):
  return 10 + CalcEffect(player, EffectTypeEnum.HP_MAX)


def CalcMagicPoints_Max(player):
  return 10 + CalcEffect(player, EffectTypeEnum.MANA_MAX)


def CalcAttackPoints(player):
  return CalcEffect(player, EffectTypeEnum.ATK)


def CalcDefense(player):
  return CalcEffect(player, EffectTypeEnum.DEF)


def CalcHealing(player):
  return CalcEffect(player, EffectTypeEnum.HEALING)


def CalcMagicRegen(player):
  return CalcEffect(player, EffectTypeEnum.MANA_REGEN)


def ResetPlayerStats(player):
  player.HitPoints_Cur = CalcHitPoints_Max(player)
  player.MagicPoints_Cur = CalcMagicPoints_Max(player)
  player.ResetStats()


def printCombatActions():
  print("  ATTACK")
  print("  DODGE")
  print("  BLOCK")
  print("  FLEE")


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
        print("%-40s : %5s lbs" %
              (("(%d) " % il.Quantity) + items[item_id].ItemName + \
               items[item_id].ItemFlagStr(" (%s)"),
               "{:3.1f}".format(weight)))
      else:
        print("%-40s : %5s lbs" %
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
      print("%s" % persons[x.Person].LongDescription)
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
    print("Invalid item.")
    return
  itemNum = int(x)
  if itemNum < 1 or itemNum > len(links):
    print("Invalid item.")
    return
  count = 0
  for item_id, il in links.items():
    count += 1
    if count != itemNum:
      continue
    if items[item_id].Flags & item_flags[ItemFlagEnum.NO_DROP].Bit > 0:
      print("[%s] cannot be dropped." % items[item_id].ItemName)
      return
    player.RemoveItem(item_id, ItemLink(1))
    rooms[player.Room].AddItem(item_id, ItemLink(1))
    print("[%s] dropped." % items[item_id].ItemName)
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
    print("Invalid item.")
    return
  itemNum = int(x)
  if itemNum < 0 or itemNum > len(links):
    print("Invalid item.")
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
          print("[%s] is already equipped." % items[item_id].ItemName)
          return
    # only 2 weapons/shields
    if items[equip_id].ItemType == ItemTypeEnum.WEAPON or \
       items[equip_id].ItemType == ItemTypeEnum.WEAPON:
      if items[item_id].ItemType == ItemTypeEnum.SHIELD or \
         items[item_id].ItemType == ItemTypeEnum.WEAPON:
        count += 1
        if count > 1:
            print("Already wielding 2 weapons or shields.")
            return
    # only 2 rings
    if items[equip_id].ItemType == ItemTypeEnum.RING and \
       items[item_id].ItemType == ItemTypeEnum.RING:
      count += 1
      if count > 1:
          print("Already wielding 2 rings.")
          return
  player.ItemLinks[equip_id].Equipped = True
  print("[%s] equipped." % items[equip_id].ItemName)


def actionGetItem(player, rooms):
  print("\nItems in in the room:\n")
  links = filterLinks(rooms[player.Room].RoomItems, equipped=False)
  if len(links) < 1:
    print("There are no items in the room.")
    return
  printItems(links, number=True)
  x = input("\nWhich item # to pick up: ").lower()
  if not x.isnumeric():
    print("Invalid item.")
    return
  itemNum = int(x)
  if itemNum < 1 or itemNum > len(links):
    print("Invalid item.")
    return
  count = 0
  for item_id, il in links.items():
    count += 1
    if count == itemNum:
      rooms[player.Room].RemoveItem(item_id, ItemLink(1))
      player.AddItem(item_id, ItemLink(1))
      print("[%s] picked up." % items[item_id].ItemName)
      break


def actionInventory(player, rooms):
  print("\n%sCURRENCY%s: %dsp" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL,
                                  player.Currency))
  print("\n%sEQUIPMENT:%s" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  links = filterLinks(player.ItemLinks, equipped=True)
  if len(links) < 1:
    print("[NONE]")
  else:
    printItems(links)
  print("%s%-40s : %5s lbs%s" % (ANSI.TEXT_BOLD, "EQUIPPED WEIGHT (1/2)",
                                 "{:3.1f}".format(player.EquipWeight(items)),
                                 ANSI.TEXT_NORMAL))
  print("\n%sITEMS:%s" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  links = filterLinks(player.ItemLinks, equipped=False)
  if len(links) < 1:
    print("[NONE]")
  else:
    printItems(links)
  print("%s%-40s : %5s lbs%s" % (ANSI.TEXT_BOLD, "INVENTORY WEIGHT",
                                 "{:3.1f}".format(player.InvenWeight(items)),
                                 ANSI.TEXT_NORMAL))


def actionSave(player, rooms):
  if SavePlayer(player, rooms[player.Room].Title, player.Password):
    return True
  else:
    print("%sAn error occured during SAVE!%s" %
          (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return False


def actionSkills(player, rooms):
  print("\n%sCHARACTER SKILLS%s\n" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  for skill_id in player.SkillTrainings:
    train = 0
    if player.SkillTrainings[skill_id] is not None:
      train = player.SkillTrainings[skill_id].Points
    print("%-15s: %s/%s/%s  ML:%-3d(%d)" %
          (skills[skill_id].Name,
           attributes[skills[skill_id].Attr1].Abbrev,
           attributes[skills[skill_id].Attr2].Abbrev,
           attributes[skills[skill_id].Attr3].Abbrev,
           player.SkillML(skill_id), train))


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


def actionStats(player, rooms):
  for ac_id, ac in attribute_classes.items():
    if ac.Hidden:
      continue
    print("\n%s%s STATS%s\n" % (ANSI.TEXT_BOLD, ac.Name.upper(),
                                ANSI.TEXT_NORMAL))
    for attr, val in player.Attr.items():
      if not attributes[attr].Hidden and attributes[attr].AttrClass == ac_id:
        print("%-15s: %d" % (attributes[attr].Name, val))

  print("\n%sCHARACTER STATS%s\n" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  if player.Flags & PERS_COMBAT > 0:
    fighting = []
    for x in rooms[player.Room].Persons:
      if x.CombatEnemy == player:
        fighting.append(x.Name)
    print("%-15s: %s" % ("Fighting", ", ".join(fighting)))
  end = player.AttrEndurance()
  enc = player.Encumbrance(items)
  print("%-15s: %d" % ("Endurance", end))
  print("%-15s: %d lbs" % ("Encumbrance", enc))
  print("%-15s: %d" % ("Enc. Penalty", -round(enc / end)))


def actionArmor(player, rooms):
  print("\n%sARMOR COVERAGE%s\n" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  print("%s%-16s BLUNT EDGE PIERCE FIRE COLD SHOCK POISON MAGIC%s" %
        (ANSI.TEXT_BOLD, "LOCATION", ANSI.TEXT_NORMAL))
  m = Material(0, 0, 0, 0, 0, 0)
  for bp_id, bp in body_parts.items():
    m.Clear()
    for item_id, il in player.ItemLinks.items():
      if items[item_id].ItemType != ItemTypeEnum.ARMOR:
        continue
      if not il.Equipped:
        continue
      if items[item_id].Covered(bp_id):
        m.Add(materials[items[item_id].Material])
    print("%-16s %-5d %-4d %-6d %-4d %-4d %-5d %-6d %-5d" %
          (body_parts[bp_id].PartName, m.ProtBlunt, m.ProtEdge, m.ProtPierce,
           m.ProtFire, m.ProtCold, m.ProtShock, m.ProtPoison, m.ProtMagic))


def actionRemoveItem(player, rooms):
  print("\nYour equipped items:\n")
  links = filterLinks(player.ItemLinks, equipped=True)
  if len(links) < 1:
    print("Nothing is equipped.")
    return
  printItems(links, number=True)
  x = input("\nWhich item # to remove: ").lower()
  if not x.isnumeric():
    print("Invalid item.")
    return
  itemNum = int(x)
  if itemNum < 0 or itemNum > len(links):
    print("Invalid item.")
    return
  count = 0
  for item_id, il in links.items():
    count += 1
    if count == itemNum:
      player.ItemLinks[item_id].Equipped = False
      print("[%s] removed." % items[item_id].ItemName)
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
  if player.Flags & PERS_COMBAT > 0:
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
  if player.Flags & PERS_COMBAT > 0:
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


def actionSaveGeneric(player, rooms):
    if player.Flags & PERS_COMBAT > 0:
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
    print("\nGeneral Commands:")
    # generic commands
    for cmd in commands:
      print("  %s" % cmd.Commands[0].upper())
    # exits
    if not rooms[player.Room].Exits is None:
      print("\nDirection Commands:")
      for exit_dir, exit_names in directions.items():
        print("  %s" % exit_names[0].upper())
    # combat commands
    if player.Flags & PERS_COMBAT > 0:
      print("\nCombat Commands:")
      printCombatActions()


commands.append(GenericCommand(["armor"], actionArmor))
commands.append(GenericCommand(["close"], actionComingSoon))
commands.append(GenericCommand(["drop"], actionDropItem))
commands.append(GenericCommand(["equip"], actionEquipItem))
commands.append(GenericCommand(["get"], actionGetItem))
commands.append(GenericCommand(["help", "?"], actionPrintHelp))
commands.append(GenericCommand(["info"], actionInfo))
commands.append(GenericCommand(["inventory", "i"], actionInventory))
commands.append(GenericCommand(["look", "l"], actionLook))
commands.append(GenericCommand(["open"], actionComingSoon))
commands.append(GenericCommand(["password"], actionChangePassword))
commands.append(GenericCommand(["quit", "q"], actionQuit))
commands.append(GenericCommand(["remove"], actionRemoveItem))
commands.append(GenericCommand(["save"], actionSaveGeneric))
commands.append(GenericCommand(["skills"], actionSkills))
commands.append(GenericCommand(["stats"], actionStats))
commands.append(GenericCommand(["unlock"], actionComingSoon))
commands.append(GenericCommand(["who"], actionListPlayers))


def prompt(player, rooms, command_func=None):
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
      cmd_match.Function(player, rooms)
    else:
      # Handle directions
      match_dir = DirectionEnum.NONE
      for d, d_cmds in directions.items():
        for d_cmd in d_cmds:
          if x == d_cmd.lower():
            match_dir = d
            break

      if match_dir != DirectionEnum.NONE:
        if player.Flags & PERS_COMBAT > 0:
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
