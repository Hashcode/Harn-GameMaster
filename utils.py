# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Utility Functions

from sys import exit
from textwrap import TextWrapper
from time import sleep

from console import (ANSI, InputFlag)
from db import (LoadStatsDB, SavePlayer)
from gamedata import (GameData)
from global_defines import (attribute_classes, attributes, months, sunsigns,
                            cultures, social_classes, sibling_ranks, wounds,
                            parent_statuses, player_frames, comelinesses,
                            complexions, color_hairs, color_eyes,
                            skill_classes, skills, body_parts,
                            materials, DamageTypeEnum, AttrEnum,
                            Material, PlayerCombatState, PersonTypeEnum,
                            ItemTypeEnum, ItemFlagEnum, ItemEnum,
                            DiceRoll, DoorEnum, Mob, Player,
                            TargetTypeEnum, ConditionCheckEnum,
                            TriggerTypeEnum, RoomEnum, RoomFlag,
                            ItemLink, DirectionEnum, Roll)
from logger import (logd)


wrapper = TextWrapper(width=70, fix_sentence_endings=True)


def CalcEffect(eff_type):
  player = GameData.GetPlayer()
  items = GameData.GetItems()
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
  items = GameData.GetItems()
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


def printItems(item_links, number=False, stats=False, shop=False,
               valueAdj=1):
  cm = GameData.GetConsole()
  items = GameData.GetItems()
  count = 0
  for item_id, il in item_links.items():
    count += 1
    item_name = items[item_id].ItemName.capitalize()
    item_name += items[item_id].ItemFlagStr(" (%s)")
    if stats:
      weight = items[item_id].Weight * il.Quantity
      item_info = " : %5s lbs" % "{:3.1f}".format(weight)
    else:
      item_info = ""
    if shop:
      item_value = " [%d SP]" % int(items[item_id].Value * valueAdj)
    else:
      item_value = ""
    if number:
      cm.Print("%2d. %-30s%s%s" % (count, item_name, item_info, item_value))
    else:
      if il.Quantity > 1 and not il.Equipped:
        cm.Print("%-30s%s%s" %
                 (("(%d) " % il.Quantity) + item_name, item_info, item_value))
      else:
        cm.Print("%-30s%s%s" % (item_name, item_info, item_value))


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


def printRoomDescription(room_id):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  doors = GameData.GetDoors()
  rooms = GameData.GetRooms()

  cm.Print("")

  # check for darkness w/o light source
  if not rooms[room_id].HasLight():
    cm.Print("%sDarkness%s" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    cm.Print("\nIt's completely dark and you can't see.")
    return

  # Room Title
  if rooms[room_id].Title != "":
    cm.Print("%s%s%s" % (ANSI.TEXT_BOLD,
                         rooms[room_id].Title, ANSI.TEXT_NORMAL))
  # Room Description
  if len(rooms[room_id].LongDescription) > 0:
    for para in rooms[room_id].LongDescription:
      cm.Print("\n" + wrapper.fill(para))
    # Exits
    if len(rooms[room_id].Exits) > 0:
      cm.Print("")
      for exit_dir, ex in rooms[room_id].Exits.items():
        exit_str = "To the %s%s%s" % (ANSI.TEXT_BOLD,
                                      directions[exit_dir][0].upper(),
                                      ANSI.TEXT_NORMAL)
        if ex.Door == DoorEnum.NONE:
          cm.Print("%s is %s" % (exit_str, rooms[ex.Room].ShortDescription))
        else:
          if player.DoorState(ex.Door).Closed:
            cm.Print("%s %s closed %s" %
                     (exit_str, doors[ex.Door].Verb(), doors[ex.Door].Name))
          else:
            cm.Print("%s is %s (via open %s)" %
                     (exit_str, rooms[ex.Room].ShortDescription,
                      doors[ex.Door].Name))


def printRoomObjects(room_id):
  cm = GameData.GetConsole()
  rooms = GameData.GetRooms()
  # Persons
  if len(rooms[room_id].Persons) > 0:
    cm.Print("")
    for x in rooms[room_id].Persons:
      cm.Print("%s" % x.LongDescription)
  # Items
  if len(rooms[room_id].RoomItems) > 0:
    cm.Print("\nThe following items are here:")
    printItems(rooms[room_id].RoomItems)


def attrColor(attr):
  if attr <= 5:
    return ANSI.TEXT_COLOR_RED
  elif attr <= 8:
    return ANSI.TEXT_COLOR_YELLOW
  elif attr <= 13:
    return ANSI.TEXT_COLOR_WHITE
  else:
    return ANSI.TEXT_COLOR_GREEN


def printStats(person):
  cm = GameData.GetConsole()
  if person.PersonType == PersonTypeEnum.PLAYER:
    for ac_id, ac in attribute_classes.items():
      if ac.Hidden:
        continue
      cm.Print("\n%s%s STATS%s\n" % (ANSI.TEXT_BOLD, ac.Name.upper(),
                                     ANSI.TEXT_NORMAL))
      for attr, val in person.Attr.items():
        if not attributes[attr].Hidden:
          if attributes[attr].AttrClass == ac_id:
            cm.Print("%-15s: %s%d%s" % (attributes[attr].Name,
                                        attrColor(val), val,
                                        ANSI.TEXT_NORMAL))
    cm.Print("\n%sCHARACTER STATS%s\n" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  else:
    cm.Print("\n%s%s STATS%s\n" % (ANSI.TEXT_BOLD, person.Name.upper(),
                                   ANSI.TEXT_NORMAL))
  cm.Print("%-15s: %d" % ("Endurance", person.AttrEndurance()))
  cm.Print("%-15s: %d lbs" % ("Inven. Weight", person.ItemWeight()))
  cm.Print("%-15s: %d" % ("Enc. Points", person.EncumbrancePenalty()))
  cm.Print("%-15s: %d" % ("Injury Points", person.IP()))
  cm.Print("%-15s: %d" % ("Fatigue Points", person.FatiguePoints()))
  cm.Print("%-15s: %d" % ("Initiative", person.AttrInitiative()))
  cm.Print("\n%s%-15s: %d%s" % (ANSI.TEXT_BOLD, "Universal Pen.",
                                person.UniversalPenalty(), ANSI.TEXT_NORMAL))
  cm.Print("%s%-15s: %d%s" % (ANSI.TEXT_BOLD, "Physical Pen.",
                              person.PhysicalPenalty(), ANSI.TEXT_NORMAL))
  if person.PersonType == PersonTypeEnum.NPC:
    links = filterLinks(person.ItemLinks, equipped=True)
    if len(links) > 0:
      cm.Print("\n%sEQUIPMENT%s\n" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
      printItems(links, stats=True)
  cm.Print("\n%sWOUND LIST%s\n" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  if len(person.Wounds) < 1:
    cm.Print("[NONE]")
  else:
    for w in person.Wounds:
      cm.Print("%s %s %s wound [%d IP]" %
               (wounds[w.WoundType].Name,
                wounds[w.WoundType].Verbs[w.DamageType].lower(),
                body_parts[w.Location].PartName.lower(), w.Impact))


# GENERIC COMMAND FUNCTIONS

def actionComingSoon():
  cm = GameData.GetConsole()
  cm.Print("\nComing soon!")


def chooseItem(links, verb, stats=False, shop=False, valueAdj=1):
  cm = GameData.GetConsole()
  cm.Print("\nItems:\n")
  printItems(links, number=True, stats=stats, shop=shop, valueAdj=valueAdj)
  x = cm.Input("Which item # to %s:" % verb, line_length=3,
               input_flags=InputFlag.NUMERIC)
  if not x.isnumeric():
    cm.Print("\nInvalid item.")
    return ItemEnum.NONE
  itemNum = int(x)
  if itemNum < 1 or itemNum > len(links):
    cm.Print("\nInvalid item.")
    return ItemEnum.NONE
  count = 0
  for item_id, il in links.items():
    count += 1
    if count == itemNum:
      return item_id
  return ItemEnum.NONE


def actionGetItem():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  items = GameData.GetItems()
  rooms = GameData.GetRooms()
  links = filterLinks(rooms[player.Room].RoomItems, equipped=False)
  if len(links) < 1:
    cm.Print("\nThere are no items in the room.")
    return
  if not rooms[player.Room].HasLight():
    cm.Print("\nYou can't see anything in the dark.")
    return
  item_id = chooseItem(links, "pick up")
  if item_id == ItemEnum.NONE:
    return
  if processTriggers(None, items[item_id].OnGet) == False:
    cm.Print("\nYou can't seem to pick up %s." %
             items[item_id].ItemName)
    return
  rooms[player.Room].RemoveItem(item_id, ItemLink(1))
  player.AddItem(item_id, ItemLink(1))
  cm.Print("\n%s picked up." % items[item_id].ItemName.capitalize())


def actionDropItem():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  items = GameData.GetItems()
  rooms = GameData.GetRooms()
  links = filterLinks(player.ItemLinks, equipped=False)
  if len(links) < 1:
    cm.Print("\nNothing is droppable at the moment.")
    return
  if not rooms[player.Room].HasLight():
    cm.Print("\nYou can't see anything in the dark.")
    return
  item_id = chooseItem(links, "drop")
  if item_id == ItemEnum.NONE:
    return
  if items[item_id].Flags & 1 << ItemFlagEnum.NO_DROP > 0:
    cm.Print("\n%s cannot be dropped." %
             items[item_id].ItemName.capitalize())
    return
  if items[item_id].Flags & 1 << ItemFlagEnum.QUEST > 0:
    cm.Print("\n%s cannot be dropped." %
             items[item_id].ItemName.capitalize())
    return
  if processTriggers(None, items[item_id].OnDrop) == False:
    cm.Print("\nYou can't seem to drop %s." %
             items[item_id].ItemName)
    return
  player.RemoveItem(item_id, ItemLink(1))
  rooms[player.Room].AddItem(item_id, ItemLink(1))
  cm.Print("\n%s dropped." % items[item_id].ItemName.capitalize())


def actionEquipItem():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  items = GameData.GetItems()
  links = filterLinks(player.ItemLinks, equipped=False, equippable=True)
  if len(links) < 1:
    cm.Print("\nNothing is equippable at the moment.")
    return
  equip_id = chooseItem(links, "equip")
  if equip_id == ItemEnum.NONE:
    return
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
          cm.Print("\n%s is already equipped." %
                   items[item_id].ItemName.capitalize())
          return
    # only 2 weapons/shields
    if items[equip_id].ItemType == ItemTypeEnum.WEAPON or \
       items[equip_id].ItemType == ItemTypeEnum.WEAPON:
      if items[item_id].ItemType == ItemTypeEnum.SHIELD or \
         items[item_id].ItemType == ItemTypeEnum.WEAPON:
        count += 1
        if count > 1:
            cm.Print("\nAlready wielding 2 weapons or shields.")
            return
    # only 2 rings
    if items[equip_id].ItemType == ItemTypeEnum.RING and \
       items[item_id].ItemType == ItemTypeEnum.RING:
      count += 1
      if count > 1:
          cm.Print("\nAlready wielding 2 rings.")
          return
  if processTriggers(None, items[item_id].OnEquip) == False:
    cm.Print("\nYou can't seem to eqiup %s." %
             items[item_id].ItemName)
    return
  player.ItemLinks[equip_id].Equipped = True
  # use a player's "attack" if in combat
  if player.CombatState != PlayerCombatState.NONE:
    cm.Print("\nYou take a moment to equip %s." % items[equip_id].ItemName)
    return False
  else:
    # 1 minute to equip
    player.GameTime += 60
    cm.Print("\n%s equipped." % items[equip_id].ItemName.capitalize())


def actionRemoveItem():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  items = GameData.GetItems()
  links = filterLinks(player.ItemLinks, equipped=True)
  if len(links) < 1:
    cm.Print("\nNothing is equipped.")
    return
  item_id = chooseItem(links, "remove")
  if item_id == ItemEnum.NONE:
    return
  if processTriggers(None, items[item_id].OnRemove) == False:
    cm.Print("\nYou can't seem to remove %s." %
             items[item_id].ItemName)
    return
  player.ItemLinks[item_id].Equipped = False
  # 1 minute to equip
  player.GameTime += 60
  cm.Print("\n%s removed." % items[item_id].ItemName.capitalize())


def actionInventory():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  cm.Print("\n%sCURRENCY%s: %d SP" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL,
                                      player.Currency))
  cm.Print("\n%sEQUIPMENT%s" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  links = filterLinks(player.ItemLinks, equipped=True)
  if len(links) < 1:
    cm.Print("[NONE]")
  else:
    printItems(links, stats=True)
  cm.Print("%s%-30s : %5s lbs%s" % (ANSI.TEXT_BOLD, "EQUIPPED WEIGHT",
                                    "{:3.1f}".format(player.EquipWeight()),
                                    ANSI.TEXT_NORMAL))
  cm.Print("\n%sITEMS%s" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  links = filterLinks(player.ItemLinks, equipped=False)
  if len(links) < 1:
    cm.Print("[NONE]")
  else:
    printItems(links, stats=True)
  cm.Print("%s%-30s : %5s lbs%s" % (ANSI.TEXT_BOLD, "INVENTORY WEIGHT",
                                    "{:3.1f}".format(player.InvenWeight()),
                                    ANSI.TEXT_NORMAL))
  cm.Print("\n%s%-30s : %5s lbs%s" % (ANSI.TEXT_BOLD, "TOTAL WEIGHT",
                                      "{:3.1f}".format(player.ItemWeight()),
                                      ANSI.TEXT_NORMAL))


def actionSave():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  rooms = GameData.GetRooms()
  player.UpdatePlayerTime()
  if SavePlayer(player, rooms[player.Room].Title, player.Password):
    return True
  else:
    cm.Print("%sAn error occured during SAVE!%s" %
             (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return False


def actionSkills():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  for skc_id, skc in skill_classes.items():
    if skc.Hidden:
      continue
    cm.Print("\n%s%s SKILLS%s\n" %
             (ANSI.TEXT_BOLD, skc.Name.upper(), ANSI.TEXT_NORMAL))
    for sk_id, sk in skills.items():
      if sk.SkillClass != skc_id:
        continue
      if sk.Hidden:
        continue
      cm.Print("%-15s: %s%s%s/%s%s%s/%s%s%s  ML:%-3d" %
               (sk.Name,
                attrColor(player.Attr[skills[sk_id].Attr1]),
                attributes[skills[sk_id].Attr1].Abbrev,
                ANSI.TEXT_NORMAL,
                attrColor(player.Attr[skills[sk_id].Attr2]),
                attributes[skills[sk_id].Attr2].Abbrev,
                ANSI.TEXT_NORMAL,
                attrColor(player.Attr[skills[sk_id].Attr3]),
                attributes[skills[sk_id].Attr3].Abbrev,
                ANSI.TEXT_NORMAL,
                player.SkillML(sk_id)))


def actionInfo():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  cm.Print("\n%sBIRTH INFORMATION%s\n" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  # TODO: hardcoded Human for now
  cm.Print("%-15s: %s" % ("Name", player.Name))
  cm.Print("%-15s: %s" % (attributes[AttrEnum.SPECIES].Name, "Human"))
  cm.Print("%-15s: %s" % (attributes[AttrEnum.SEX].Name, player.AttrSexStr()))
  cm.Print("%-15s: %s %d" % ("Birth Month/Day",
                             months[player.Attr[AttrEnum.BIRTH_MONTH]].Name,
                             player.Attr[AttrEnum.BIRTH_DAY]))
  cm.Print("%-15s: %s (%s)" % ("Sunsign", sunsigns[player.Sunsign].Name,
                               sunsigns[player.Sunsign].Symbol))
  cm.Print("%-15s: %s" % (attributes[AttrEnum.CULTURE].Name,
                          cultures[player.AttrCulture()].Name))
  cm.Print("%-15s: %s" % (attributes[AttrEnum.SOCIAL_CLASS].Name,
                          social_classes[player.AttrSocialClass()].Name))
  cm.Print("%-15s: %s of %d" % (attributes[AttrEnum.SIBLING_RANK].Name,
                                sibling_ranks[player.AttrSiblingRank()].Name,
                                player.Attr[AttrEnum.SIBLING_COUNT]))
  cm.Print("%-15s: %s" % (attributes[AttrEnum.PARENT].Name,
                          parent_statuses[player.AttrParentStatus()].Name))
  cm.Print("\n%sAPPEARANCE%s\n" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  cm.Print("%-15s: %d\'%d\"" % (attributes[AttrEnum.HEIGHT].Name,
                                int(player.Attr[AttrEnum.HEIGHT] / 12),
                                player.Attr[AttrEnum.HEIGHT] % 12))
  cm.Print("%-15s: %s" % (attributes[AttrEnum.FRAME].Name,
                          player_frames[player.AttrFrame()].Name))
  cm.Print("%-15s: %d lbs" % (attributes[AttrEnum.WEIGHT].Name,
                              player.Attr[AttrEnum.WEIGHT]))
  cm.Print("%-15s: %s" % (attributes[AttrEnum.COMELINESS].Name,
                          comelinesses[player.AttrComeliness()].Name))
  cm.Print("%-15s: %s" % (attributes[AttrEnum.COMPLEXION].Name,
                          complexions[player.AttrComplexion()].Name))
  cm.Print("%-15s: %s" % (attributes[AttrEnum.COLOR_HAIR].Name,
                          color_hairs[player.AttrColorHair()].Name))
  cm.Print("%-15s: %s" % (attributes[AttrEnum.COLOR_EYE].Name,
                          color_eyes[player.AttrColorEye()].Name))


def actionArmor():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  items = GameData.GetItems()
  cm.Print("\n%sARMOR COVERAGE%s\n" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  cm.Print("%s%-15s  BLUNT EDGE PIERCE ELEMENTAL%s" %
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
    cm.Print("%-15s: %-5d %-4d %-6d %-9d" %
             (body_parts[bp_id].PartName,
              m.Protection[DamageTypeEnum.BLUNT],
              m.Protection[DamageTypeEnum.EDGE],
              m.Protection[DamageTypeEnum.PIERCE],
              m.Protection[DamageTypeEnum.ELEMENTAL]))
    m.Clear()


def actionQuest():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  quests = GameData.GetQuests()
  count = 0
  cm.Print("\n%sCOMPLETED QUESTS%s\n" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  for quest_id, completed in player.Quests.items():
    if quests[quest_id].Hidden:
      continue
    if completed:
      count += 1
      cm.Print("%s" % quests[quest_id].Name)
  if count < 1:
    cm.Print("[NONE]")
  count = 0
  cm.Print("\n%sCURRENT QUESTS%s\n" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  for quest_id, completed in player.Quests.items():
    if quests[quest_id].Hidden:
      continue
    if not completed:
      count += 1
      cm.Print("%s" % quests[quest_id].Name)
  if count < 1:
    cm.Print("[NONE]")


def chooseNPC(npcs, noun, stats=False):
  cm = GameData.GetConsole()
  cm.Print("\nChoose a target:\n")
  count = 0
  for npc in npcs:
    count += 1
    if stats:
      cm.Print("%d. %s [%d IP]" % (count, npc.Name, npc.IP()))
    else:
      cm.Print("%d. %s" % (count, npc.Name))
  x = cm.Input("Which # to %s:" % noun, line_length=3,
               input_flags=InputFlag.NUMERIC)
  if not x.isnumeric():
    cm.Print("\nInvalid target.")
    return None
  personNum = int(x)
  if personNum < 1 or personNum > len(npcs):
    cm.Print("\nInvalid target.")
    return None
  return npcs[personNum - 1]


def actionAttack():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  rooms = GameData.GetRooms()
  npcs = []
  if player.IsTalking():
    cm.Print("\n%sYou are talking! Enter \"DONE\" "
             "to end conversation.%s" %
             (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  # let combat "attack" handle work if in combat
  if player.CombatState != PlayerCombatState.NONE:
    return False
  for npc in rooms[player.Room].Persons:
    npcs.append(npc)
  if len(npcs) < 1:
    cm.Print("\nThere is nothing to attack nearby!")
    return
  p = chooseNPC(npcs, "target")
  if p is not None:
    cm.Print("\nYou attack %s!" % p.Name)
    player.CombatTarget = p.UUID
  if player.CombatTarget is not None:
    return True


def actionInspect():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  rooms = GameData.GetRooms()
  npcs = []
  for npc in rooms[player.Room].Persons:
    npcs.append(npc)
  if len(npcs) < 1:
    cm.Print("\nThere is no one to inspect nearby!")
    return
  p = chooseNPC(npcs, "inspect")
  if p is not None:
    printStats(p)


def processWeather():
  return


def processTime():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  rooms = GameData.GetRooms()
  if rooms[player.Room].Flags & RoomFlag.OUTSIDE == 0:
    return
  if player.GameTime > player.LastTimeUpdate + 7200:
    moon = player.GameTimeMoonPhase()
    hour = player.GameTimeHourOfDay()
    if hour >= 22:  # 10 pm
      cm.Print("The %s moon is nearing it's zenith." % moon)
    elif hour >= 20:  # 8 pm
      cm.Print("The %s moon rises into view in the night sky." % moon)
    elif hour >= 18:  # 6 pm
      cm.Print("The last of the sun disappears over the horizon.")
    elif hour >= 16:  # 4 pm
      cm.Print("The sun sinks ever lower in the afternoon sky.")
    elif hour >= 14:  # 2 pm
      cm.Print("The sun slowly makes it's way across the afternoon sky.")
    elif hour >= 12:  # noon
      cm.Print("The suns has reached it's zenith in the sky.")
    elif hour >= 10:  # 10 am
      cm.Print("The suns is nearly at it's peak in the late morning.")
    elif hour >= 8:  # 8 am
      cm.Print("The suns path arcs higher in the mid-morning sky.")
    elif hour >= 6:  # 6 am
      cm.Print("The sun peeks over the horizon.")
    elif hour >= 4:  # 4 am
      cm.Print("The %s moon slowly drops below the horizon." % moon)
    elif hour >= 2:  # 2 am
      cm.Print("The %s moon drifts lower in the night sky." % moon)
    else:  # midnight
      cm.Print("The %s moon is now high overhead." % moon)
    # set update time to last even hour block
    player.LastTimeUpdate = int(player.GameTime / 7200) * 7200
  return


def processConditions(room_id, obj, conditions):
  player = GameData.GetPlayer()
  rooms = GameData.GetRooms()
  if conditions is not None:
    for c in conditions:
      if c.TargetType == TargetTypeEnum.PLAYER_INVEN:
        if c.ConditionCheck == ConditionCheckEnum.HAS:
          if c.Data not in player.ItemLinks.keys():
            return False
        if c.ConditionCheck == ConditionCheckEnum.HAS_NOT:
          if c.Data in player.ItemLinks.keys():
            return False
      elif c.TargetType == TargetTypeEnum.PLAYER_QUEST:
        if c.ConditionCheck == ConditionCheckEnum.HAS:
          if not player.HasQuest(c.Data):
            return False
        if c.ConditionCheck == ConditionCheckEnum.HAS_NOT:
          if player.HasQuest(c.Data):
            return False
      elif c.TargetType == TargetTypeEnum.PLAYER_QUEST_COMPLETE:
        if c.ConditionCheck == ConditionCheckEnum.HAS:
          if not player.HasQuest(c.Data):
            return False
          if player.HasQuest(c.Data, completed=False):
            return False
        if c.ConditionCheck == ConditionCheckEnum.HAS_NOT:
          if not player.HasQuest(c.Data):
            return False
          if player.HasQuest(c.Data, completed=True):
            return False
      elif c.TargetType == TargetTypeEnum.ITEM_IN_ROOM:
        count = 0
        for item_id, ri in rooms[room_id].RoomItems.items():
          if item_id == c.Data:
            count += 1
        if c.ConditionCheck == ConditionCheckEnum.HAS and count < 1:
          return False
        if c.ConditionCheck == ConditionCheckEnum.HAS_NOT and count > 0:
          return False
        if c.ConditionCheck == ConditionCheckEnum.GREATER_THAN:
          if count <= c.Value:
            return False
        if c.ConditionCheck == ConditionCheckEnum.EQUAL_TO:
          if count == c.Value:
            return False
        if c.ConditionCheck == ConditionCheckEnum.LESS_THAN:
          if count >= c.Value:
            return False
      elif c.TargetType == TargetTypeEnum.MOB_IN_ROOM:
        match = False
        count = 0
        for p in rooms[room_id].Persons:
          if p.PersonID == c.Data:
            count += 1
            match = True
        logd("[cond] MOB_IN_ROOM: %d == %d" % (c.Data, count))
        if c.ConditionCheck == ConditionCheckEnum.HAS and not match:
            return False
        if c.ConditionCheck == ConditionCheckEnum.HAS_NOT and match:
            return False
        if c.ConditionCheck == ConditionCheckEnum.GREATER_THAN:
          if count <= c.Value:
            return False
        if c.ConditionCheck == ConditionCheckEnum.EQUAL_TO:
          if count != c.Value:
            return False
        if c.ConditionCheck == ConditionCheckEnum.LESS_THAN:
          if count >= c.Value:
            return False
      elif c.TargetType == TargetTypeEnum.LOCATED_IN_ROOM:
        match = False
        if type(obj) is Mob:
          for p in rooms[c.Data].Persons:
            if p.UUID == obj.UUID:
              match = True
              break
        logd("[cond] LOCATED_IN_ROOM: %s[%d] == %d" %
             (obj.Name, c.Data, match))
        if not match:
          return False
      elif c.TargetType == TargetTypeEnum.PERCENT_CHANCE:
        r = DiceRoll(1, 100).Result()
        if c.ConditionCheck == ConditionCheckEnum.GREATER_THAN and \
           r <= c.Value:
          return False
        if c.ConditionCheck == ConditionCheckEnum.EQUAL_TO and \
           r != c.Value:
          return False
        if c.ConditionCheck == ConditionCheckEnum.LESS_THAN and \
           r >= c.Value:
          return False
      elif c.TargetType == TargetTypeEnum.ATTR_CHECK:
        r = DiceRoll(1, c.Value).Result()
        logd("[cond] ATTR_CHECK: %d vs. %d" % (r, player.Attr[c.Data]))
        if r > player.Attr[c.Data]:
          return False
      elif c.TargetType == TargetTypeEnum.SKILL_CHECK:
        res = player.ResolveSkill(c.Value, c.Data)
        logd("[cond] SKILL_CHECK: %s" % (res))
        if res == Roll.MF or res == Roll.CF:
          return False
      elif c.TargetType == TargetTypeEnum.HOUR_OF_DAY_CHECK:
        logd("[cond] HOUR_OF_DAY_CHECK: %d vs. %d" %
             (player.GameTimeHourOfDay(), c.Value))
        if c.ConditionCheck == ConditionCheckEnum.GREATER_THAN:
          if player.GameTimeHourOfDay() <= c.Value:
            return False
        if c.ConditionCheck == ConditionCheckEnum.EQUAL_TO:
          if player.GameTimeHourOfDay() == c.Value:
            return False
        if c.ConditionCheck == ConditionCheckEnum.LESS_THAN:
          if player.GameTimeHourOfDay() >= c.Value:
            return False
      elif c.TargetType == TargetTypeEnum.MONTH_CHECK:
        if c.ConditionCheck == ConditionCheckEnum.GREATER_THAN:
          if player.GameTimeMonth() <= c.Value:
            return False
        if c.ConditionCheck == ConditionCheckEnum.EQUAL_TO:
          if player.GameTimeMonth() == c.Value:
            return False
        if c.ConditionCheck == ConditionCheckEnum.LESS_THAN:
          if player.GameTimeMonth() >= c.Value:
            return False
      elif c.TargetType == TargetTypeEnum.DAYLIGHT_CHECK:
        if c.ConditionCheck == ConditionCheckEnum.HAS:
          if not player.GameTimeIsDay():
            return False
        elif c.ConditionCheck == ConditionCheckEnum.HAS_NOT:
          if player.GameTimeIsDay():
            return False
      elif c.TargetType == TargetTypeEnum.MOONPHASE_CHECK:
        # TODO
        pass
      elif c.TargetType == TargetTypeEnum.FLAG_CHECK:
        if c.ConditionCheck == ConditionCheckEnum.HAS:
          if type(obj) is Mob:
            if obj.Flags & c.Data == 0:
              return False
        elif c.ConditionCheck == ConditionCheckEnum.HAS_NOT:
          if type(obj) is Mob:
            if obj.Flags & c.Data > 0:
              return False
      else:
        return False
  return True


def processTriggers(obj, triggers):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  rooms = GameData.GetRooms()
  if triggers is None:
    return
  for tr in triggers:
    r = DiceRoll(1, 100).Result()
    if r <= tr.Chance:
      if tr.TriggerType == TriggerTypeEnum.ITEM_GIVE:
        player.AddItem(tr.Data, ItemLink())
      elif tr.TriggerType == TriggerTypeEnum.ITEM_TAKE:
        player.RemoveItem(tr.Data, ItemLink())
      elif tr.TriggerType == TriggerTypeEnum.ITEM_SELL:
        actionShopSell(obj)
      elif tr.TriggerType == TriggerTypeEnum.ITEM_BUY:
        actionShopBuy(obj)
      elif tr.TriggerType == TriggerTypeEnum.ROOM_SPAWN:
        logd("[trigger] Room Spawn [%s]: %d" % (rooms[obj].Title, tr.Data))
        rooms[obj].AddPerson(tr.Data)
      elif tr.TriggerType == TriggerTypeEnum.ROOM_DESPAWN:
        # TODO:
        cm.Print("* Coming Soon *")
      elif tr.TriggerType == TriggerTypeEnum.CURRENCY_GIVE:
        player.Currency += int(tr.Data)
      elif tr.TriggerType == TriggerTypeEnum.CURRENCY_TAKE:
        player.Currency -= int(tr.Data)
      elif tr.TriggerType == TriggerTypeEnum.QUEST_GIVE:
        player.AddQuest(tr.Data)
      elif tr.TriggerType == TriggerTypeEnum.QUEST_COMPLETE:
        player.CompleteQuest(tr.Data)
      elif tr.TriggerType == TriggerTypeEnum.PERSON_ATTACK:
        if type(obj) is Mob:
          player.SetTalking(False)
          cm.Print("%s%s attacks you!%s" %
                   (ANSI.TEXT_BOLD, obj.Name.capitalize(),
                    ANSI.TEXT_NORMAL))
          player.CombatTarget = obj.UUID
      elif tr.TriggerType == TriggerTypeEnum.PERSON_DESC:
        if type(obj) == Mob:
          obj.LongDescription = tr.Data
      elif tr.TriggerType == TriggerTypeEnum.MESSAGE:
        cm.Print(wrapper.fill(tr.Data))
      elif tr.TriggerType == TriggerTypeEnum.ROOM_MESSAGE:
        if type(obj) == Mob:
          if rooms[player.Room].PersonInRoom(obj.UUID):
            cm.Print(wrapper.fill(tr.Data))
        elif type(obj) == RoomEnum:
          if player.Room == obj:
            cm.Print(wrapper.fill(tr.Data))
      elif tr.TriggerType == TriggerTypeEnum.MOVE:
        # TODO:
        cm.Print("* Coming Soon *")
      elif tr.TriggerType == TriggerTypeEnum.DELAY:
        obj.DelayTimestamp = player.PlayerTime()
        obj.DelaySeconds = int(tr.Data)
      elif tr.TriggerType == TriggerTypeEnum.GIVE_FLAG:
        if type(obj) == Mob or type(obj) == Player:
          obj.Flags |= tr.Data
      elif tr.TriggerType == TriggerTypeEnum.TAKE_FLAG:
        if type(obj) == Mob or type(obj) == Player:
          obj.Flags &= ~tr.Data
      elif tr.TriggerType == TriggerTypeEnum.PERSON_MOVE:
        if type(obj) == Mob:
          r = None
          for room_id in rooms.keys():
            if rooms[room_id].PersonInRoom(obj.UUID):
              r = rooms[room_id]
              break
          if r is not None:
            r.Persons.remove(obj)
          rooms[tr.Data].Persons.append(obj)
      elif tr.TriggerType == TriggerTypeEnum.DENY:
        return False
      elif tr.TriggerType == TriggerTypeEnum.END:
        logd("[trigger] END")
        return False


def printNPCTalk(p, keyword):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  ret = False
  for tk in p.Talks:
    if tk.Keyword.lower() == keyword:
      if processConditions(player.Room, p, tk.Conditions):
        ret = True
        for t in tk.Texts:
          cm.Print("\n" + wrapper.fill(t))
        if tk.Triggers is not None:
          processTriggers(p, tk.Triggers)
  return ret


def roomTalkTrigger(keyword):
  cm = GameData.GetConsole()
  keyword = "~%s~" % keyword
  player = GameData.GetPlayer()
  rooms = GameData.GetRooms()
  for npc in rooms[player.Room].Persons:
    if npc.Talks is None:
      continue
    if player.PlayerTime() - npc.DelayTimestamp <= npc.DelaySeconds:
      continue
    for tk in npc.Talks:
      if tk.Keyword.lower() == keyword:
        if processConditions(player.Room, npc, tk.Conditions):
          for t in tk.Texts:
            cm.Print("\n" + wrapper.fill(t))
          if tk.Triggers is not None:
            if not processTriggers(npc, tk.Triggers):
              return False
  return True


def actionShopBuy(shopkeep):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  items = GameData.GetItems()
  if player.CombatState != PlayerCombatState.NONE:
    cm.Print("\n%sYou can't BUY during combat!%s" %
             (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  links = filterLinks(shopkeep.SellItemLinks)
  if len(links) < 1:
    cm.Print("\nThere is nothing to buy.")
    return
  item_id = chooseItem(links, "buy", stats=True, shop=True)
  if item_id == ItemEnum.NONE:
    return
  if items[item_id].Value > player.Currency:
    cm.Print("\n%sYou cannot afford [%s].%s" %
             (ANSI.TEXT_BOLD, items[item_id].ItemName, ANSI.TEXT_NORMAL))
    return
  # TODO possible factors to raise price?
  price = items[item_id].Value
  x = cm.Input("Confirm purchase of [%s] for %d SP [y/n]:" %
               (items[item_id].ItemName, price), line_length=1).lower()
  if x == "y":
    player.Currency -= price
    player.AddItem(item_id, ItemLink(1))
    cm.Print("\n%s%s hands you [%s].%s" %
             (ANSI.TEXT_BOLD, shopkeep.Name.capitalize(),
              items[item_id].ItemName, ANSI.TEXT_NORMAL))
  else:
    cm.Print("\n%sPurchase aborted.%s" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))


def actionShopSell(shopkeep):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  items = GameData.GetItems()
  if player.CombatState != PlayerCombatState.NONE:
    cm.Print("\n%sYou can't SELL during combat!%s" %
             (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  links = {}
  if shopkeep.BuyItemLinks is None:
    cm.Print("\n%s doesn't want to buy anything." %
             shopkeep.Name.capitalize())
    return
  for item_id, il in player.ItemLinks.items():
    if not il.Equipped or il.Quantity > 1:
      if item_id in shopkeep.BuyItemLinks.keys():
        links.update({item_id: il})
  if len(links) < 1:
    cm.Print("\n%s doesn't want to buy anything you have." %
             shopkeep.Name.capitalize())
    return
  # sell items for 1/2 value
  priceAdj = .5
  item_id = chooseItem(links, "sell", stats=True, shop=True,
                       valueAdj=priceAdj)
  if item_id == ItemEnum.NONE:
    return
  price = items[item_id].Value * priceAdj
  x = cm.Input("Confirm sale of [%s] for %d SP [y/n]:" %
               (items[item_id].ItemName, price), line_length=1).lower()
  if x == "y":
    player.Currency += price
    player.RemoveItem(item_id, ItemLink())
    cm.Print("\n%sYou hand [%s] to %s.%s" %
             (ANSI.TEXT_BOLD, items[item_id].ItemName,
              shopkeep.Name.capitalize(), ANSI.TEXT_NORMAL))
  else:
    cm.Print("\n%sSale aborted.%s" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))


def playerTalk(p, keyword=""):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  player.SetTalking(True)
  printNPCTalk(p, keyword)
  while player.IsTalking():
    # Check for room events
    GameData.ProcessEvents(processTime, processWeather,
                           processConditions, processTriggers)
    prompt(func_break=True)
    if player.Command == "done":
      player.SetTalking(False)
      printNPCTalk(p, "~")
      player.Command = ""
      break
    elif player.Command != "":
      if not printNPCTalk(p, player.Command):
        cm.Print("\n%s doesn't know anything about that." %
                 p.Name.capitalize())
      else:
        # 30 second talk turn
        player.GameTime += 30
  if player.CombatTarget is not None:
    return True


def actionTalk(keyword=""):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  rooms = GameData.GetRooms()
  if player.CombatState != PlayerCombatState.NONE:
    cm.Print("\n%sYou can't TALK during combat!%s" %
             (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  npcs = []
  if player.IsTalking():
    cm.Print("\n%sYou are already talking!!%s" %
             (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  for npc in rooms[player.Room].Persons:
    npcs.append(npc)
  if len(npcs) < 1:
    cm.Print("\nThere is no one to talk to nearby!")
    return
  p = chooseNPC(npcs, "talk to")
  if p is None:
    return
  count = 0
  if p.Talks is not None:
    for t in p.Talks:
      if not t.Keyword.startswith("~"):
        count += 1
  if count == 0:
    cm.Print("\n%s ignores your attempts to talk." % p.Name.capitalize())
    return
  playerTalk(p, keyword)


def actionTalkBuy():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  rooms = GameData.GetRooms()
  if player.IsTalking():
    # let triggers handle
    return False
  else:
    shopkeep = None
    for npc in rooms[player.Room].Persons:
      if npc.SellItemLinks is not None:
        shopkeep = npc
        break
    if shopkeep is None:
      cm.Print("\nNo one nearby wants to buy anything.")
      return
    playerTalk(shopkeep, "buy")


def actionTalkSell():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  rooms = GameData.GetRooms()
  if player.IsTalking():
    # let triggers handle
    return False
  else:
    shopkeep = None
    for npc in rooms[player.Room].Persons:
      if npc.BuyItemLinks is not None:
        shopkeep = npc
        break
    if shopkeep is None:
      cm.Print("\nNo one nearby wants to sell anything.")
      return
    playerTalk(shopkeep, "sell")


def chooseDoor(room_id, action, door_closed=None, door_locked=None):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  doors = GameData.GetDoors()
  rooms = GameData.GetRooms()
  ret = DoorEnum.NONE
  count = 0
  cm.Print("\nChoose a door:\n")
  for exit_id, ex in rooms[player.Room].Exits.items():
    if ex.Door != DoorEnum.NONE:
      match = True
      if door_closed is not None:
        if player.DoorState(ex.Door).Closed != door_closed:
          match = False
      if door_locked is not None:
        if player.DoorState(ex.Door).Locked != door_locked:
          match = False
      if match:
          count += 1
          cm.Print("%d. %s" % (count, doors[ex.Door].Name))
  x = cm.Input("Which # to %s:" % action, line_length=3,
               input_flags=InputFlag.NUMERIC)
  if not x.isnumeric():
    cm.Print("\nInvalid door.")
    return ret
  doorNum = int(x)
  if doorNum < 1 or doorNum > count:
    cm.Print("\nInvalid door.")
    return ret
  count = 0
  for exit_id, ex in rooms[player.Room].Exits.items():
    if ex.Door != DoorEnum.NONE:
      match = True
      if door_closed is not None:
        if player.DoorState(ex.Door).Closed != door_closed:
          match = False
      if door_locked is not None:
        if player.DoorState(ex.Door).Locked != door_locked:
          match = False
      if match:
        count += 1
        if count == doorNum:
          ret = ex.Door
          break
  return ret


def actionUnlock():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  items = GameData.GetItems()
  doors = GameData.GetDoors()
  door_id = chooseDoor(GameData.GetPlayer().Room, "unlock",
                       door_locked=True)
  if door_id != DoorEnum.NONE:
    key = doors[door_id].Key
    if key in player.ItemLinks.keys():
      player.SetDoorState(door_id).Locked = False
      cm.Print("\nYou unlock the %s with %s." %
               (doors[door_id].Name, items[key].ItemName))
      # 30 seconds door action
      player.GameTime += 30
    else:
      cm.Print("\n%sYou don't have the key for that!%s" %
               (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))


def actionClose():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  doors = GameData.GetDoors()
  door_id = chooseDoor(GameData.GetPlayer().Room, "close", door_closed=False)
  if door_id != DoorEnum.NONE:
    player.SetDoorState(door_id).Closed = True
    cm.Print("\nYou close the %s." % doors[door_id].Name)
    # 30 seconds door action
    player.GameTime += 30


def actionOpen():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  doors = GameData.GetDoors()
  door_id = chooseDoor(GameData.GetPlayer().Room, "open", door_closed=True)
  if door_id != DoorEnum.NONE:
    if player.DoorState(door_id).Locked:
      cm.Print("\n%sThe %s %s locked!%s" %
               (ANSI.TEXT_BOLD, doors[door_id].Name, doors[door_id].Verb(),
                ANSI.TEXT_NORMAL))
    else:
      player.SetDoorState(door_id).Closed = False
      cm.Print("\nYou open the %s." % doors[door_id].Name)
      # 30 seconds door action
      player.GameTime += 30


def actionListPlayers():
  cm = GameData.GetConsole()
  pinfo = LoadStatsDB()
  if len(pinfo) == 0:
    cm.Print("\nThere are no saved characters!")
  else:
    cm.Print("\n%s%-20s %-5s %-11s %s%s" %
             (ANSI.TEXT_BOLD, "CHARACTER NAME", "SCORE", "TIME PLAYED",
              "SAVED IN ROOM", ANSI.TEXT_NORMAL))
    cm.Print("%s%-20s %-5s %-11s %s%s" %
             (ANSI.TEXT_BOLD, "--------------", "-----", "-----------",
              "-------------", ANSI.TEXT_NORMAL))
    for x in sorted(pinfo):
      day_plural = "s"
      if pinfo[x]["played"] == 1:
        day_plural = ""
      cm.Print("%-20s %-5s %-11s %s" %
               (x, str(pinfo[x]["score"]),
                "%d day%s" % (pinfo[x]["played"], day_plural),
                pinfo[x]["info"]))


def actionLook():
  player = GameData.GetPlayer()
  printRoomDescription(player.Room)
  printRoomObjects(player.Room)


def actionChangePassword():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  if player.CombatState != PlayerCombatState.NONE:
    cm.Print("\n%sYou can't change your password in combat!%s" %
             (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  if player.IsTalking():
    cm.Print("\n%sYou are talking! Enter \"DONE\" "
             "to end conversation.%s" %
             (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  cm.Print("\nYour password is used to encrypt SAVE data.")
  cm.Print("It should NOT be a password used for anything important.")
  x = cm.Input("Enter a password:", line_length=10,
               input_flags=InputFlag.PASSWORD).upper()
  if len(x) < 3 or len(x) > 10:
    cm.Print("\nPassword needs to be between 3 and 10 characters long.")
    return
  player.Password = x
  if actionSave():
    cm.Print("\nCharacter updated.")


def actionQuit():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  if player.CombatState != PlayerCombatState.NONE:
    cm.Print("\n%sYou can't QUIT in combat!%s" %
             (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  if player.IsTalking():
    cm.Print("\n%sYou are talking! Enter \"DONE\" "
             "to end conversation.%s" %
             (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  y = cm.Input("Are you sure you wish to QUIT?", line_length=1).lower()
  if y == "y":
    actionSave()
    cm.Print("\nGoodbye!\n")
    exit()
  else:
    cm.Print("\nQuit aborted.")


def actionRest():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  if player.CombatState != PlayerCombatState.NONE:
    cm.Print("\n%sYou can't REST during combat!%s" %
             (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  if player.IsTalking():
    cm.Print("\n%sYou are talking! Enter \"DONE\" "
             "to end conversation.%s" %
             (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  cm.Print("\nYou take a moment to rest ...")
  combat = False
  # 1 hour rest time, 10 minutes at a time
  for i in range(6):
    sleep(1)
    player.GameTime += 600
    GameData.ProcessEvents(processTime, processWeather,
                           processConditions, processTriggers)
    # Check if the room persons need to attack
    enemies = GameData.ProcessRoomCombat()
    if len(enemies) > 0:
      cm.Print("")
      combat = True
      break
  if combat:
    combat(player, enemies)
  else:
    if player.IP() > 0:
      for w in sorted(player.Wounds, reverse=True):
        cm.Print("\nYou clean and dress a %s %s %s wound ..." %
                 (wounds[w.WoundType].Name.lower(),
                  wounds[w.WoundType].Verbs[w.DamageType].lower(),
                  body_parts[w.Location].PartName.lower()))
        sleep(5)
        r = DiceRoll(1, player.Attr[AttrEnum.AURA]).Result()
        w.Impact -= r
        if w.Impact <= 0:
          player.Wounds.remove(w)
          cm.Print("It's all better!")
        else:
          cm.Print("It looks a bit better.")


ATT_PER_TRAIN = 25


def actionTrain():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  if player.CombatState != PlayerCombatState.NONE:
    cm.Print("\n%sYou can't TRAIN during combat!%s" %
             (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  if player.IsTalking():
    cm.Print("\n%sYou are talking! Enter \"DONE\" "
             "to end conversation.%s" %
             (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  cm.Print("\nChoose a trainable skill (>%d attempts):\n" % ATT_PER_TRAIN)
  count = 0
  for skill_id, sl in player.SkillLinks.items():
    if sl.Attempts > ATT_PER_TRAIN:
      count += 1
      attempts = int(sl.Attempts / ATT_PER_TRAIN)
      plural = ""
      if attempts > 1:
        plural = "s"
      cm.Print("%-3s %-15s [%d train%s]" %
               ("%d." % count, skills[skill_id].Name, attempts, plural))
  if count < 1:
    cm.Print("No skills are ready to be trained. Use them more!")
    return
  x = cm.Input("Which skill # to train:", line_length=3,
               input_flags=InputFlag.NUMERIC)
  if not x.isnumeric():
    cm.Print("\nInvalid skill.")
    return
  skillNum = int(x)
  if skillNum < 1 or skillNum > count:
    cm.Print("\nInvalid skill.")
    return
  count = 0
  for skill_id, sl in player.SkillLinks.items():
    if sl.Attempts > ATT_PER_TRAIN:
      count += 1
      if count == skillNum:
        # 30 minute train time
        player.GameTime += 1800
        # attempt to raise skill
        r = DiceRoll(1, 100).Result() + player.SkillBase(skill_id)
        if r > player.SkillML(skill_id, skipPenalty=True):
          cm.Print("\nYou GAIN an mastery level in %s!" %
                   (skills[skill_id].Name.lower()))
          sl.Points += 1
        else:
          cm.Print("\nYour attempt to train %s FAILS!" %
                   (skills[skill_id].Name.lower()))
        sl.Attempts -= ATT_PER_TRAIN
        break


def actionStatsGeneric():
  printStats(GameData.GetPlayer())


def actionSaveGeneric():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  if player.CombatState != PlayerCombatState.NONE:
    cm.Print("\n%sYou can't SAVE in combat!%s" %
             (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  if player.IsTalking():
    cm.Print("\n%sYou are talking! Enter \"DONE\" "
             "to end conversation.%s" %
             (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  if actionSave():
    cm.Print("\nCharacter saved.")


def actionTime():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  cm.Print("\n%s on %s" % (player.GameTimeStr(), player.GameTimeDateStr()))
  day_plural = "s"
  if int(player.PlayerTime() / 86400) == 1:
    day_plural = ""
  cm.Print("Time Played: %d day%s %d minutes" %
           (int(player.PlayerTime() / 86400), day_plural,
            int((player.PlayerTime() % 86400) / 60)))


class GenericCommand:
  def __init__(self, cmds, cmd_func, desc=""):
    self.Commands = []
    self.Description = desc
    self.Function = cmd_func
    if cmds is not None:
      for c in cmds:
        self.Commands.append(c)


commands = []


def actionPrintHelp():
  cm = GameData.GetConsole()
  cm.Print("\nGENERAL COMMANDS:\n")
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
    cm.Print("%-10s%s" % (cmd.Commands[0].upper(), abbrevs))
  # exits
  cm.Print("\nMOVE DIRECTION:\n")
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
    cm.Print("%-10s%s" % (exit_names[0].upper(), abbrevs))
  # break prompt loop to let other sections add commands
  return False


commands.append(GenericCommand(["armor", "ac"], actionArmor))
commands.append(GenericCommand(["attack", "a"], actionAttack))
commands.append(GenericCommand(["buy"], actionTalkBuy))
commands.append(GenericCommand(["close"], actionClose))
commands.append(GenericCommand(["drop"], actionDropItem))
commands.append(GenericCommand(["equip", "eq"], actionEquipItem))
commands.append(GenericCommand(["inspect"], actionInspect))
commands.append(GenericCommand(["get"], actionGetItem))
commands.append(GenericCommand(["help", "?"], actionPrintHelp))
commands.append(GenericCommand(["info", "inf"], actionInfo))
commands.append(GenericCommand(["inventory", "i"], actionInventory))
commands.append(GenericCommand(["look", "l"], actionLook))
commands.append(GenericCommand(["open"], actionOpen))
commands.append(GenericCommand(["password"], actionChangePassword))
commands.append(GenericCommand(["quests", "quest"], actionQuest))
commands.append(GenericCommand(["quit", "q"], actionQuit))
commands.append(GenericCommand(["remove", "rm"], actionRemoveItem))
commands.append(GenericCommand(["rest"], actionRest))
commands.append(GenericCommand(["save"], actionSaveGeneric))
commands.append(GenericCommand(["sell"], actionTalkSell))
commands.append(GenericCommand(["skills", "sk"], actionSkills))
commands.append(GenericCommand(["stats", "st"], actionStatsGeneric))
commands.append(GenericCommand(["talk"], actionTalk))
commands.append(GenericCommand(["time"], actionTime))
commands.append(GenericCommand(["train"], actionTrain))
commands.append(GenericCommand(["unlock"], actionUnlock))
commands.append(GenericCommand(["who"], actionListPlayers))


def promptTimeout():
  player = GameData.GetPlayer()
  # 5 minutes for idle
  player.GameTime += 300
  GameData.ProcessEvents(processTime, processWeather,
                         processConditions, processTriggers)


def prompt(func_break=False):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  doors = GameData.GetDoors()
  rooms = GameData.GetRooms()
  player.Command = ""
  while True:
    prompt_text = "[? = HELP] Command:"
    if player.IsTalking():
      prompt_text = "[? = HELP, \"DONE\" = Exit Talk] Command:"
    x = cm.Input(prompt_text, timeout=30, timeoutFunc=promptTimeout).lower()
    # Handle universal commands
    cmd_match = None
    for gen_cmd in commands:
      for cmds in gen_cmd.Commands:
        if x == cmds:
          cmd_match = gen_cmd
          break
    if cmd_match is not None:
      res = cmd_match.Function()
      if func_break and res == False:
        player.Command = x
        break
      elif res == True:
        # attack and talk cmds can return true to re-enter main for combat
        player.Command = ""
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
          cm.Print("\n%sYou can't move in combat!  Try to FLEE!%s" %
                   (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
        elif player.IsTalking():
          cm.Print("\n%sYou are talking! Enter \"DONE\" "
                   "to end conversation.%s" %
                   (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
        else:
          trigger_deny = False
          for exit_dir, ex in rooms[player.Room].Exits.items():
            if match_dir == exit_dir:
              if ex.Door != DoorEnum.NONE:
                if player.DoorState(ex.Door).Closed:
                  cm.Print("\n%sThe %s %s closed.%s" %
                           (ANSI.TEXT_BOLD, doors[ex.Door].Name,
                            doors[ex.Door].Verb(), ANSI.TEXT_NORMAL))
                  break
                else:
                  if not roomTalkTrigger("on_exit"):
                    trigger_deny = True
                    break
                  # time to cross room
                  player.GameTime += rooms[player.Room].TravelTime
                  player.SetRoom(ex.Room)
              else:
                if not roomTalkTrigger("on_exit"):
                  trigger_deny = True
                  break
                # time to cross room
                player.GameTime += rooms[player.Room].TravelTime
                player.SetRoom(ex.Room)
              return
          if not trigger_deny:
            cm.Print("\n%sYou can't go in that direction.%s" %
                     (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
        continue

      player.Command = x
      break

# vim: tabstop=2 shiftwidth=2 expandtab:
