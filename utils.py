# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Utility FunctionsHas

import random

from global_defines import *
from items import *
from person import *
from db import *

# Logging

LOG_OFF = 0
LOG_ERR = 1
LOG_WRN = 2
LOG_INF = 3
LOG_DBG = 4

LogLevel = LOG_DBG

def log(ll, line):
  if LogLevel >= ll:
    print(line)

def loge(line):
  log(LOG_ERR, "[error] %s" % line)

def logw(line):
  log(LOG_WRN, "[warn] %s" % line)

def logi(line):
  log(LOG_INF, "[info] %s" % line)

def logd(line):
  log(LOG_DBG, "[debug] %s" % line)

# Roll

def roll(rolls, die_base, modifier=0):
  value = 0
  for x in range(rolls):
    y = random.randint(1, die_base) + modifier
    logd("ROLL %dD%d+%d = %d" % (rolls, die_base, modifier, y))
    value += y
  return value

def CalcEffect(player, eff_type):
  value = 0
  for item_id, il in player.ItemLinks.items():
    if not items[item_id].Effects is None:
      for y in items[item_id].Effects:
        if y.EffectType == eff_type:
          value += y.Modifier * il.Quantity
  if not player.Effects is None:
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

def filterLinks(item_links, equipped=False, equippable=False, flags=0, noflags=0):
  item_dict = {}
  for item_id, il in item_links.items():
    if equippable and not items[item_id].ItemType in [ItemTypeEnum.WEAPON, ItemTypeEnum.ARMOR, ItemTypeEnum.RING]:
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

def printItems(item_links, number=False):
  count = 0
  for item_id, il in item_links.items():
    count += 1
    if number:
      print("%d. %s%s" % (count, items[item_id].ItemName, items[item_id].ItemFlagStr(" (%s)")))
    else:
      if il.Quantity > 1 and not il.Equipped:
        print("(%d) %s%s" % (il.Quantity, items[item_id].ItemName, items[item_id].ItemFlagStr(" (%s)")))
      else:
        print("%s%s" % (items[item_id].ItemName, items[item_id].ItemFlagStr(" (%s)")))

# Directions

directions = {
  DirectionEnum.NORTH:    [ "north", "n" ],
  DirectionEnum.SOUTH:    [ "south", "s" ],
  DirectionEnum.WEST:     [ "west",  "w" ],
  DirectionEnum.EAST:     [ "east",  "e" ],
  DirectionEnum.NORTHWEST:[ "northwest", "nw" ],
  DirectionEnum.NORTHEAST:[ "northeast", "ne" ],
  DirectionEnum.SOUTHWEST:[ "southwest", "sw" ],
  DirectionEnum.SOUTHEAST:[ "southeast", "se" ],
  DirectionEnum.UP:       [ "up",    "u" ],
  DirectionEnum.DOWN:     [ "down",  "d" ],
}

def printRoomDescription(room_id, rooms):
  print("")
  # Room Title
  if rooms[room_id].Title != "":
    print("%s%s%s" % (ANSI.TEXT_BOLD, rooms[room_id].Title, ANSI.TEXT_NORMAL))
  # Room Description
  if rooms[room_id].LongDescription != "":
    print("\n%s" % rooms[room_id].LongDescription)
    # Exits
    if len(rooms[room_id].Exits) > 0:
      print("")
      for exit_dir,exit in rooms[room_id].Exits.items():
        print("To the %s is %s" % (
          ANSI.TEXT_BOLD + directions[exit_dir][0].upper() + ANSI.TEXT_NORMAL,
          rooms[exit.Room].ShortDescription))

  if len(rooms[room_id].RoomItems) > 0:
    print("\nThe following items are here:")
    printItems(rooms[room_id].RoomItems)

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

def actionEquipItem(player):
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
    if items[equip_id].ItemType == ItemTypeEnum.ARMOR and items[item_id].ItemType == ItemTypeEnum.ARMOR:
      if items[item_id].Layer & items[equip_id].Layer > 0 and items[item_id].Coverage & items[equip_id].Coverage > 0:
          print("[%s] is already equipped." % items[item_id].ItemName)
          return
    # only 2 weapons/shields
    if items[equip_id].ItemType == ItemTypeEnum.WEAPON or items[equip_id].ItemType == ItemTypeEnum.WEAPON:
      if items[item_id].ItemType == ItemTypeEnum.SHIELD or items[item_id].ItemType == ItemTypeEnum.WEAPON:
        count += 1
        if count > 1:
            print("Already wielding 2 weapons or shields.")
            return
    # only 2 rings
    if items[equip_id].ItemType == ItemTypeEnum.RING and items[item_id].ItemType == ItemTypeEnum.RING:
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

def actionInventory(player):
  print("\n%sCURRENCY%s: %dsp" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL, player.Currency))
  print("\n%sEQUIPMENT:%s" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  links = filterLinks(player.ItemLinks, equipped=True)
  if len(links) < 1:
    print("[NONE]")
  else:
    printItems(links)
  print("\n%sITEMS:%s" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  links = filterLinks(player.ItemLinks, equipped=False)
  if len(links) < 1:
    print("[NONE]")
  else:
    printItems(links)

def actionSave(player, rooms):
  if SavePlayer(player, rooms[player.Room].Title, player.Password):
    return True
  else:
    print("%sAn error occured during SAVE!%s" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
    return False

def actionStats(player, rooms):
  print("\n%sCHARACTER STATS%s\n" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
  if player.Flags & PERS_COMBAT > 0:
    fighting = []
    for x in rooms[player.Room].Persons:
      if x.CombatEnemy == player:
        fighting.append(x.Name)
    print("%-8s: %s" % ("Fighting", ", ".join(fighting)))
  print("%-8s: %d" % ("Health", player.HitPoints_Cur))
  print("%-8s: %d" % ("Mana", player.MagicPoints_Cur))
  print("%-8s: %d" % ("Attack", CalcAttackPoints(player)))
  print("%-8s: %d" % ("Defense", CalcDefense(player)))

def actionUnequipItem(player):
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

def actionListPlayers():
  pinfo = ListDB()
  if len(pinfo) == 0:
    print("\nThere are no saved characters!")
  else:
    print("\n%s%-20s %s%s" % (ANSI.TEXT_BOLD, "CHARACTER NAME", "SAVED IN ROOM", ANSI.TEXT_NORMAL))
    print("%s%-20s %s%s" %   (ANSI.TEXT_BOLD, "--------------", "-------------", ANSI.TEXT_NORMAL))
    for x in sorted(pinfo):
      print("%-20s %s" % (x, pinfo[x]))

def prompt(player, rooms):
  player.Command = ""
  while True:
    x = input("\nType your command: ").lower()
    if x == "":
      continue

    # CHECK FOR UNIVERSAL COMMANDS
    if x == "drop":
      actionDropItem(player, rooms)
    elif x == "equip":
      actionEquipItem(player)
    elif x == "get":
      actionGetItem(player, rooms)
    elif x == "help":
      print("\nGeneral Commands:")
      print("  DROP")
      print("  EQUIP")
      print("  GET")
      print("  INVENTORY")
      print("  LOOK")
      print("  OPEN")
      print("  PASSWORD")
      print("  QUIT")
      print("  SAVE")
      print("  SKILLS")
      print("  STATS")
      print("  UNEQUIP")
      print("  UNLOCK")
      print("  WHO")
      if not rooms[player.Room].Exits is None:
        print("\nDirection Commands:")
        for exit_dir,exit in rooms[player.Room].Exits.items():
          print("  %s" % directions[exit_dir].upper())
      if player.Flags & PERS_COMBAT > 0:
        print("\nCombat Commands:")
        printCombatActions()
    elif x == "i" or x == "inventory":
      actionInventory(player)
    elif x == "l" or x == "look":
      printRoomDescription(player.Room, rooms)
    elif x == "open":
      # TODO:
      print("Coming soon!")
    elif x == "password":
      if player.Flags & PERS_COMBAT > 0:
        print("\n%sYou can't change your password in combat!%s" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
      else:
        print("\nYour password is used to encrypt SAVE data.")
        print("It should NOT be a password used for anything important.")
        x = input("\nEnter a password: ").upper
        if len(x.Password) < 3 or len(x.Password) > 10:
          print("\nPassword needs to be between 3 and 10 characters long.")
        player.Password = x
        actionSave(player, rooms)
    elif x == "q" or x == "quit":
      if player.Flags & PERS_COMBAT > 0:
        print("\n%sYou can't QUIT in combat!%s" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
      else:
        y = input("\nAre you sure you wish to QUIT? ").lower()
        if y == "y" or y == "yes":
          actionSave(player, rooms)
          print("\nGoodbye!\n")
          player.Command = x
          break
        else:
          print("\nQuit aborted.")
    elif x == "save":
      if player.Flags & PERS_COMBAT > 0:
        print("\n%sYou can't SAVE in combat!%s" % (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))
      else:
        actionSave(player, rooms)
    elif x == "skills":
      # TODO:
      print("Coming soon!")
    elif x == "stats":
      actionStats(player, rooms)
    elif x == "unequip":
      actionUnequipItem(player)
    elif x == "unlock":
      # TODO:
      print("Coming soon!")
    elif x == "who":
      actionListPlayers()
    else:
      # Handle directions
      if not rooms[player.Room].Exits is None:
        for exit_dir,exit in rooms[player.Room].Exits.items():
          for d in directions[exit_dir]:
            if x == d.lower():
              player.SetRoom(exit.Room)
              return

      player.Command = x
      break

# vim: tabstop=2 shiftwidth=2 expandtab:
