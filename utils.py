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
                            ItemTypeEnum, ItemFlagEnum, ItemEnum,
                            DiceRoll, DoorEnum, Mob,
                            TargetTypeEnum, ConditionCheckEnum,
                            TriggerTypeEnum,
                            ItemLink, DirectionEnum, ANSI, GameData)
from db import (LoadStatsDB, SavePlayer)


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
      print("%2d. %-30s%s%s" % (count, item_name, item_info, item_value))
    else:
      if il.Quantity > 1 and not il.Equipped:
        print("%-30s%s%s" %
              (("(%d) " % il.Quantity) + item_name, item_info, item_value))
      else:
        print("%-30s%s%s" % (item_name, item_info, item_value))


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
  player = GameData.GetPlayer()
  doors = GameData.GetDoors()
  rooms = GameData.GetRooms()
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
        exit_str = "To the %s%s%s" % (ANSI.TEXT_BOLD,
                                      directions[exit_dir][0].upper(),
                                      ANSI.TEXT_NORMAL)
        if ex.Door == DoorEnum.NONE:
          print("%s is %s" % (exit_str, rooms[ex.Room].ShortDescription))
        else:
          if player.DoorState(ex.Door).Closed:
            print("%s %s closed %s" %
                  (exit_str, doors[ex.Door].Verb(), doors[ex.Door].Name))
          else:
            print("%s is %s (via open %s)" %
                  (exit_str, rooms[ex.Room].ShortDescription,
                   doors[ex.Door].Name))


def printRoomObjects(room_id):
  rooms = GameData.GetRooms()
  # Persons
  if len(rooms[room_id].Persons) > 0:
    print("")
    for x in rooms[room_id].Persons:
      print("%s" % x.LongDescription)
  # Items
  if len(rooms[room_id].RoomItems) > 0:
    print("\nThe following items are here:")
    printItems(rooms[room_id].RoomItems)


def printStats(person):
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
  print("%-15s: %d" % ("Endurance", person.AttrEndurance()))
  print("%-15s: %d lbs" % ("Inven. Weight", person.ItemWeight()))
  print("%-15s: %d" % ("Enc. Points", person.EncumbrancePenalty()))
  print("%-15s: %d" % ("Injury Points", person.IP()))
  print("%-15s: %d" % ("Fatigue Points", person.FatiguePoints()))
  print("%-15s: %d" % ("Initiative", person.AttrInitiative()))
  print("\n%s%-15s: %d%s" % (ANSI.TEXT_BOLD, "Universal Pen.",
                             person.UniversalPenalty(), ANSI.TEXT_NORMAL))
  print("%s%-15s: %d%s" % (ANSI.TEXT_BOLD, "Physical Pen.",
                           person.PhysicalPenalty(), ANSI.TEXT_NORMAL))
  if person.PersonType == PersonTypeEnum.NPC:
    links = filterLinks(person.ItemLinks, equipped=True)
    if len(links) > 0:
      print("\n%sEQUIPMENT%s\n" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
      printItems(links, stats=True)
  print("\n%sWOUND LIST%s\n" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  if len(person.Wounds) < 1:
    print("[NONE]")
  else:
    for w in person.Wounds:
      print("%s %s %s wound [%d IP]" %
            (wounds[w.WoundType].Name,
             wounds[w.WoundType].Verbs[w.DamageType].lower(),
             body_parts[w.Location].PartName.lower(), w.Impact))


# GENERIC COMMAND FUNCTIONS

def actionComingSoon():
  print("\nComing soon!")


def chooseItem(links, verb, stats=False, shop=False, valueAdj=1):
  print("\nItems:\n")
  printItems(links, number=True, stats=stats, shop=shop, valueAdj=valueAdj)
  x = input("\nWhich item # to %s: " % verb).lower()
  if not x.isnumeric():
    print("\nInvalid item.")
    return ItemEnum.NONE
  itemNum = int(x)
  if itemNum < 1 or itemNum > len(links):
    print("\nInvalid item.")
    return ItemEnum.NONE
  count = 0
  for item_id, il in links.items():
    count += 1
    if count == itemNum:
      return item_id
  return ItemEnum.NONE


def actionGetItem():
  player = GameData.GetPlayer()
  items = GameData.GetItems()
  rooms = GameData.GetRooms()
  links = filterLinks(rooms[player.Room].RoomItems, equipped=False)
  if len(links) < 1:
    print("\nThere are no items in the room.")
    return
  item_id = chooseItem(links, "pick up")
  if item_id == ItemEnum.NONE:
    return
  if processTriggers(None, items[item_id].OnGet) == False:
    print("\nYou can't seem to pick up %s." %
          items[item_id].ItemName)
    return
  rooms[player.Room].RemoveItem(item_id, ItemLink(1))
  player.AddItem(item_id, ItemLink(1))
  print("\n%s picked up." % items[item_id].ItemName.capitalize())


def actionDropItem():
  player = GameData.GetPlayer()
  items = GameData.GetItems()
  rooms = GameData.GetRooms()
  links = filterLinks(player.ItemLinks, equipped=False)
  if len(links) < 1:
    print("\nNothing is droppable at the moment.")
    return
  item_id = chooseItem(links, "drop")
  if item_id == ItemEnum.NONE:
    return
  if items[item_id].Flags & item_flags[ItemFlagEnum.NO_DROP].Bit > 0:
    print("\n%s cannot be dropped." % items[item_id].ItemName.capitalize())
    return
  if items[item_id].Flags & item_flags[ItemFlagEnum.QUEST].Bit > 0:
    print("\n%s cannot be dropped." % items[item_id].ItemName.capitalize())
    return
  if processTriggers(None, items[item_id].OnDrop) == False:
    print("\nYou can't seem to drop %s." %
          items[item_id].ItemName)
    return
  player.RemoveItem(item_id, ItemLink(1))
  rooms[player.Room].AddItem(item_id, ItemLink(1))
  print("\n%s dropped." % items[item_id].ItemName.capitalize())


def actionEquipItem():
  player = GameData.GetPlayer()
  items = GameData.GetItems()
  links = filterLinks(player.ItemLinks, equipped=False, equippable=True)
  if len(links) < 1:
    print("\nNothing is equippable at the moment.")
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
  if processTriggers(None, items[item_id].OnEquip) == False:
    print("\nYou can't seem to eqiup %s." %
          items[item_id].ItemName)
    return
  player.ItemLinks[equip_id].Equipped = True
  # use a player's "attack" if in combat
  if player.CombatState != PlayerCombatState.NONE:
    print("\nYou take a moment to equip %s." % items[equip_id].ItemName)
    return False
  else:
    # 1 minute to equip
    player.GameTime += 60
    print("\n%s equipped." % items[equip_id].ItemName.capitalize())


def actionRemoveItem():
  player = GameData.GetPlayer()
  items = GameData.GetItems()
  links = filterLinks(player.ItemLinks, equipped=True)
  if len(links) < 1:
    print("\nNothing is equipped.")
    return
  item_id = chooseItem(links, "remove")
  if item_id == ItemEnum.NONE:
    return
  if processTriggers(None, items[item_id].OnRemove) == False:
    print("\nYou can't seem to remove %s." %
          items[item_id].ItemName)
    return
  player.ItemLinks[item_id].Equipped = False
  # 1 minute to equip
  player.GameTime += 60
  print("\n%s removed." % items[item_id].ItemName.capitalize())


def actionInventory():
  player = GameData.GetPlayer()
  print("\n%sCURRENCY%s: %d SP" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL,
                                   player.Currency))
  print("\n%sEQUIPMENT%s" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  links = filterLinks(player.ItemLinks, equipped=True)
  if len(links) < 1:
    print("[NONE]")
  else:
    printItems(links, stats=True)
  print("%s%-30s : %5s lbs%s" % (ANSI.TEXT_BOLD, "EQUIPPED WEIGHT",
                                 "{:3.1f}".format(player.EquipWeight()),
                                 ANSI.TEXT_NORMAL))
  print("\n%sITEMS%s" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  links = filterLinks(player.ItemLinks, equipped=False)
  if len(links) < 1:
    print("[NONE]")
  else:
    printItems(links, stats=True)
  print("%s%-30s : %5s lbs%s" % (ANSI.TEXT_BOLD, "INVENTORY WEIGHT",
                                 "{:3.1f}".format(player.InvenWeight()),
                                 ANSI.TEXT_NORMAL))
  print("\n%s%-30s : %5s lbs%s" % (ANSI.TEXT_BOLD, "TOTAL WEIGHT",
                                   "{:3.1f}".format(player.ItemWeight()),
                                   ANSI.TEXT_NORMAL))


def actionSave():
  player = GameData.GetPlayer()
  rooms = GameData.GetRooms()
  player.UpdatePlayerTime()
  if SavePlayer(player, rooms[player.Room].Title, player.Password):
    return True
  else:
    print("%sAn error occured during SAVE!%s" %
          (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return False


def actionSkills():
  player = GameData.GetPlayer()
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
             player.SkillML(sk_id)))


def actionInfo():
  player = GameData.GetPlayer()
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


def actionArmor():
  player = GameData.GetPlayer()
  items = GameData.GetItems()
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


def actionQuest():
  player = GameData.GetPlayer()
  quests = GameData.GetQuests()
  count = 0
  print("\n%sCOMPLETED QUESTS%s\n" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  for quest_id, completed in player.Quests.items():
    if quests[quest_id].Hidden:
      continue
    if completed:
      count += 1
      print("%s" % quests[quest_id].Name)
  if count < 1:
    print("[NONE]")
  count = 0
  print("\n%sCURRENT QUESTS%s\n" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  for quest_id, completed in player.Quests.items():
    if quests[quest_id].Hidden:
      continue
    if not completed:
      count += 1
      print("%s" % quests[quest_id].Name)
  if count < 1:
    print("[NONE]")


def chooseNPC(npcs, noun, stats=False):
  print("\nChoose a target:\n")
  count = 0
  for npc in npcs:
    count += 1
    if stats:
      print("%d. %s [%d IP]" % (count, npc.Name, npc.IP()))
    else:
      print("%d. %s" % (count, npc.Name))
  x = input("\nWhich # to %s: " % noun).lower()
  if not x.isnumeric():
    print("\nInvalid target.")
    return None
  personNum = int(x)
  if personNum < 1 or personNum > len(npcs):
    print("\nInvalid target.")
    return None
  return npcs[personNum - 1]


def actionAttack():
  player = GameData.GetPlayer()
  rooms = GameData.GetRooms()
  npcs = []
  if player.IsTalking():
    print("\n%sYou are talking! Enter \"DONE\" "
          "to end conversation.%s" %
          (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  # let combat "attack" handle work if in combat
  if player.CombatState != PlayerCombatState.NONE:
    return False
  for npc in rooms[player.Room].Persons:
    npcs.append(npc)
  if len(npcs) < 1:
    print("\nThere is nothing to attack nearby!")
    return
  p = chooseNPC(npcs, "target")
  if p is not None:
    print("\nYou attack %s!" % p.Name)
    player.CombatTarget = p.UUID
  if player.CombatTarget is not None:
    return True


def actionInspect():
  player = GameData.GetPlayer()
  rooms = GameData.GetRooms()
  npcs = []
  for npc in rooms[player.Room].Persons:
    npcs.append(npc)
  if len(npcs) < 1:
    print("\nThere is no one to inspect nearby!")
    return
  p = chooseNPC(npcs, "inspect")
  if p is not None:
    printStats(p)


def processConditions(conditions):
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
        if c.ConditionCheck == ConditionCheckEnum.HAS:
          if c.Data not in rooms[player.Room].RoomItems.keys():
            return False
        if c.ConditionCheck == ConditionCheckEnum.HAS_NOT:
          if c.Data in rooms[player.Room].RoomItems.keys():
            return False
      elif c.TargetType == TargetTypeEnum.MOB_IN_ROOM:
        match = False
        for p in rooms[player.Room].Persons:
          if p.PersonID == c.Data:
            match = True
            break
        if c.ConditionCheck == ConditionCheckEnum.HAS and not match:
            return False
        if c.ConditionCheck == ConditionCheckEnum.HAS_NOT and match:
            return False
      elif c.TargetType == TargetTypeEnum.LOCATED_IN_ROOM:
        # TODO:
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
        # TODO:
        return False
      elif c.TargetType == TargetTypeEnum.SKILL_CHECK:
        # TODO:
        return False
      else:
        return False
  return True


def processTriggers(obj, triggers):
  player = GameData.GetPlayer()
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
          print("%s%s attacks you!%s" %
                (ANSI.TEXT_BOLD, obj.Name.capitalize(),
                 ANSI.TEXT_NORMAL))
          player.CombatTarget = obj.UUID
      elif tr.TriggerType == TriggerTypeEnum.PERSON_DESC:
        obj.LongDescription = tr.Data
      elif tr.TriggerType == TriggerTypeEnum.MESSAGE:
        print("\n" + wrapper.fill(tr.Data))
      elif tr.TriggerType == TriggerTypeEnum.MOVE:
        # TODO:
        print("* Coming Soon *")
      elif tr.TriggerType == TriggerTypeEnum.DELAY:
        obj.DelayTimestamp = player.PlayerTime()
        obj.DelaySeconds = int(tr.Data)
      elif tr.TriggerType == TriggerTypeEnum.DENY:
        return False


def printNPCTalk(p, keyword):
  ret = False
  player = GameData.GetPlayer()
  for tk in p.Talks:
    if tk.Keyword.lower() == keyword:
      if processConditions(tk.Conditions):
        ret = True
        for t in tk.Texts:
          print("\n" + wrapper.fill(t))
        if tk.Triggers is not None:
          processTriggers(p, tk.Triggers)
  return ret


def roomTalkTrigger(keyword):
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
        if processConditions(tk.Conditions):
          for t in tk.Texts:
            print("\n" + wrapper.fill(t))
          if tk.Triggers is not None:
            if not processTriggers(npc, tk.Triggers):
              return False
  return True


def actionShopBuy(shopkeep):
  player = GameData.GetPlayer()
  items = GameData.GetItems()
  if player.CombatState != PlayerCombatState.NONE:
    print("\n%sYou can't BUY during combat!%s" %
          (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  links = filterLinks(shopkeep.SellItemLinks)
  if len(links) < 1:
    print("\nThere is nothing to buy.")
    return
  item_id = chooseItem(links, "buy", stats=True, shop=True)
  if item_id == ItemEnum.NONE:
    return
  if items[item_id].Value > player.Currency:
    print("\n%sYou cannot afford [%s].%s" %
          (ANSI.TEXT_BOLD, items[item_id].ItemName, ANSI.TEXT_NORMAL))
    return
  # TODO possible factors to raise price?
  price = items[item_id].Value
  x = input("\nConfirm purchase of [%s] for %d SP [y/N]: " %
            (items[item_id].ItemName, price)).lower()
  if x == "y" or x == "yes":
    player.Currency -= price
    player.AddItem(item_id, ItemLink(1))
    print("\n%s%s hands you [%s].%s" %
          (ANSI.TEXT_BOLD, shopkeep.Name.capitalize(),
           items[item_id].ItemName, ANSI.TEXT_NORMAL))
  else:
    print("\n%sPurchase aborted.%s" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))


def actionShopSell(shopkeep):
  player = GameData.GetPlayer()
  items = GameData.GetItems()
  if player.CombatState != PlayerCombatState.NONE:
    print("\n%sYou can't SELL during combat!%s" %
          (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  links = {}
  if shopkeep.BuyItemLinks is None:
    print("\n%s doesn't want to buy anything." %
          shopkeep.Name.capitalize())
    return
  for item_id, il in player.ItemLinks.items():
    if not il.Equipped or il.Quantity > 1:
      if item_id in shopkeep.BuyItemLinks.keys():
        links.update({item_id: il})
  if len(links) < 1:
    print("\n%s doesn't want to buy anything you have." %
          shopkeep.Name.capitalize())
    return
  # sell items for 1/2 value
  priceAdj = .5
  item_id = chooseItem(links, "sell", stats=True, shop=True,
                       valueAdj=priceAdj)
  if item_id == ItemEnum.NONE:
    return
  price = items[item_id].Value * priceAdj
  x = input("\nConfirm sale of [%s] for %d SP [y/N]: " %
            (items[item_id].ItemName, price)).lower()
  if x == "y" or x == "yes":
    player.Currency += price
    player.RemoveItem(item_id, ItemLink())
    print("\n%sYou hand [%s] to %s.%s" %
          (ANSI.TEXT_BOLD, items[item_id].ItemName,
           shopkeep.Name.capitalize(), ANSI.TEXT_NORMAL))
  else:
    print("\n%sSale aborted.%s" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))


def playerTalk(p, keyword=""):
  player = GameData.GetPlayer()
  player.SetTalking(True)
  printNPCTalk(p, keyword)
  while player.IsTalking():
    # Check for room events
    GameData.ProcessRoomEvents()
    prompt(func_break=True)
    if player.Command == "done":
      player.SetTalking(False)
      printNPCTalk(p, "~")
      player.Command = ""
      break
    elif player.Command != "":
      if not printNPCTalk(p, player.Command):
        print("\n%s doesn't know anything about that." %
              p.Name.capitalize())
      else:
        # 30 second talk turn
        player.GameTime += 30
  if player.CombatTarget is not None:
    return True


def actionTalk(keyword=""):
  player = GameData.GetPlayer()
  rooms = GameData.GetRooms()
  if player.CombatState != PlayerCombatState.NONE:
    print("\n%sYou can't TALK during combat!%s" %
          (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  npcs = []
  if player.IsTalking():
    print("\n%sYou are already talking!!%s" %
          (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  for npc in rooms[player.Room].Persons:
    npcs.append(npc)
  if len(npcs) < 1:
    print("\nThere is no one to talk to nearby!")
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
    print("\n%s ignores your attempts to talk." % p.Name.capitalize())
    return
  playerTalk(p, keyword)


def actionTalkBuy():
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
      print("\nNo one nearby wants to buy anything.")
      return
    playerTalk(shopkeep, "buy")


def actionTalkSell():
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
      print("\nNo one nearby wants to sell anything.")
      return
    playerTalk(shopkeep, "sell")


def chooseDoor(room_id, action, door_closed=None, door_locked=None):
  player = GameData.GetPlayer()
  doors = GameData.GetDoors()
  rooms = GameData.GetRooms()
  ret = DoorEnum.NONE
  count = 0
  print("\nChoose a door:\n")
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
          print("%d. %s" % (count, doors[ex.Door].Name))
  x = input("\nWhich # to %s: " % action).lower()
  if not x.isnumeric():
    print("\nInvalid door.")
    return ret
  doorNum = int(x)
  if doorNum < 1 or doorNum > count:
    print("\nInvalid door.")
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
  player = GameData.GetPlayer()
  items = GameData.GetItems()
  doors = GameData.GetDoors()
  door_id = chooseDoor(GameData.GetPlayer().Room, "unlock",
                       door_locked=True)
  if door_id != DoorEnum.NONE:
    key = doors[door_id].Key
    if key in player.ItemLinks.keys():
      player.SetDoorState(door_id).Locked = False
      print("\nYou unlock the %s with %s." %
            (doors[door_id].Name, items[key].ItemName))
      # 30 seconds door action
      player.GameTime += 30
    else:
      print("\n%sYou don't have the key for that!%s" %
            (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))


def actionClose():
  player = GameData.GetPlayer()
  doors = GameData.GetDoors()
  door_id = chooseDoor(GameData.GetPlayer().Room, "close", door_closed=False)
  if door_id != DoorEnum.NONE:
    player.SetDoorState(door_id).Closed = True
    print("\nYou close the %s." % doors[door_id].Name)
    # 30 seconds door action
    player.GameTime += 30


def actionOpen():
  player = GameData.GetPlayer()
  doors = GameData.GetDoors()
  door_id = chooseDoor(GameData.GetPlayer().Room, "open", door_closed=True)
  if door_id != DoorEnum.NONE:
    if player.DoorState(door_id).Locked:
      print("\n%sThe %s %s locked!%s" %
            (ANSI.TEXT_BOLD, doors[door_id].Name, doors[door_id].Verb(),
             ANSI.TEXT_NORMAL))
    else:
      player.SetDoorState(door_id).Closed = False
      print("\nYou open the %s." % doors[door_id].Name)
      # 30 seconds door action
      player.GameTime += 30


def actionListPlayers():
  pinfo = LoadStatsDB()
  if len(pinfo) == 0:
    print("\nThere are no saved characters!")
  else:
    print("\n%s%-20s %-5s %-11s %s%s" %
          (ANSI.TEXT_BOLD, "CHARACTER NAME", "SCORE", "TIME PLAYED",
           "SAVED IN ROOM", ANSI.TEXT_NORMAL))
    print("%s%-20s %-5s %-11s %s%s" %
          (ANSI.TEXT_BOLD, "--------------", "-----", "-----------",
           "-------------", ANSI.TEXT_NORMAL))
    for x in sorted(pinfo):
      day_plural = "s"
      if pinfo[x]["played"] == 1:
        day_plural = ""
      print("%-20s %-5s %-11s %s" %
            (x, str(pinfo[x]["score"]),
             "%d day%s" % (pinfo[x]["played"], day_plural),
             pinfo[x]["info"]))


def actionLook():
  player = GameData.GetPlayer()
  printRoomDescription(player.Room)
  printRoomObjects(player.Room)


def actionChangePassword():
  player = GameData.GetPlayer()
  if player.CombatState != PlayerCombatState.NONE:
    print("\n%sYou can't change your password in combat!%s" %
          (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  if player.IsTalking():
    print("\n%sYou are talking! Enter \"DONE\" "
          "to end conversation.%s" %
          (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  print("\nYour password is used to encrypt SAVE data.")
  print("It should NOT be a password used for anything important.")
  x = input("\nEnter a password: ").upper()
  if len(x) < 3 or len(x) > 10:
    print("\nPassword needs to be between 3 and 10 characters long.")
    return
  player.Password = x
  if actionSave():
    print("\nCharacter updated.")


def actionQuit():
  player = GameData.GetPlayer()
  if player.CombatState != PlayerCombatState.NONE:
    print("\n%sYou can't QUIT in combat!%s" %
          (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  if player.IsTalking():
    print("\n%sYou are talking! Enter \"DONE\" "
          "to end conversation.%s" %
          (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  y = input("\nAre you sure you wish to QUIT? ").lower()
  if y == "y" or y == "yes":
    actionSave()
    print("\nGoodbye!\n")
    exit()
  else:
    print("\nQuit aborted.")


def actionRest():
  player = GameData.GetPlayer()
  if player.CombatState != PlayerCombatState.NONE:
    print("\n%sYou can't REST during combat!%s" %
          (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  if player.IsTalking():
    print("\n%sYou are talking! Enter \"DONE\" "
          "to end conversation.%s" %
          (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  if player.IP() < 1:
    print("\nYou are well rested.")
    return
  # health restore
  print("\nYou take a moment to rest ...")
  combat = False
  for i in range(2):
    sleep(5)
    # 15 minute rest time each
    player.GameTime += 900
    GameData.ProcessRoomEvents()
    # Check if the room persons need to attack
    enemies = GameData.ProcessRoomCombat()
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


ATT_PER_TRAIN = 25


def actionTrain():
  player = GameData.GetPlayer()
  if player.CombatState != PlayerCombatState.NONE:
    print("\n%sYou can't TRAIN during combat!%s" %
          (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  if player.IsTalking():
    print("\n%sYou are talking! Enter \"DONE\" "
          "to end conversation.%s" %
          (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  print("\nChoose a trainable skill (>%d attempts):\n" % ATT_PER_TRAIN)
  count = 0
  for skill_id, sl in player.SkillLinks.items():
    if sl.Attempts > ATT_PER_TRAIN:
      count += 1
      attempts = int(sl.Attempts / ATT_PER_TRAIN)
      plural = ""
      if attempts > 1:
        plural = "s"
      print("%-3s %-15s [%d train%s]" %
            ("%d." % count, skills[skill_id].Name, attempts, plural))
  if count < 1:
    print("No skills are ready to be trained. Use them more!")
    return
  x = input("\nWhich skill # to train: ").lower()
  if not x.isnumeric():
    print("\nInvalid skill.")
    return
  skillNum = int(x)
  if skillNum < 1 or skillNum > count:
    print("\nInvalid skill.")
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
          print("\nYou GAIN an mastery level in %s!" %
                (skills[skill_id].Name.lower()))
          sl.Points += 1
        else:
          print("\nYour attempt to train %s FAILS!" %
                (skills[skill_id].Name.lower()))
        sl.Attempts -= ATT_PER_TRAIN
        break


def actionStatsGeneric():
  printStats(GameData.GetPlayer())


def actionSaveGeneric():
  player = GameData.GetPlayer()
  if player.CombatState != PlayerCombatState.NONE:
    print("\n%sYou can't SAVE in combat!%s" %
          (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  if player.IsTalking():
    print("\n%sYou are talking! Enter \"DONE\" "
          "to end conversation.%s" %
          (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return
  if actionSave():
    print("\nCharacter saved.")


def actionTime():
  player = GameData.GetPlayer()
  print("\nTime Played: %s minutes" % int(player.PlayerTime() / 60))
  print("Game Time: %s minutes" % int(player.GameTime / 60))


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


def prompt(func_break=False):
  player = GameData.GetPlayer()
  doors = GameData.GetDoors()
  rooms = GameData.GetRooms()
  player.Command = ""
  while True:
    if player.IsTalking():
      x = input("\n[? = HELP, \"DONE\" = Exit Talk] Command: ").lower()
    else:
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
          print("\n%sYou can't move in combat!  Try to FLEE!%s" %
                (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
        elif player.IsTalking():
          print("\n%sYou are talking! Enter \"DONE\" "
                "to end conversation.%s" %
                (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
        else:
          trigger_deny = False
          for exit_dir, ex in rooms[player.Room].Exits.items():
            if match_dir == exit_dir:
              if ex.Door != DoorEnum.NONE:
                if player.DoorState(ex.Door).Closed:
                  print("\n%sThe %s %s closed.%s" %
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
            print("\n%sYou can't go in that direction.%s" %
                  (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
        continue

      player.Command = x
      break

# vim: tabstop=2 shiftwidth=2 expandtab:
