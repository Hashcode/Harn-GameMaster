# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Utility Functions

from sys import exit
from textwrap import TextWrapper
from time import sleep
from xml.dom.minidom import parse

from console import (TEXT_COLOR, ANSI, InputFlag)
from db import (LoadStatsDB, SavePlayer)
from frame import (Frame, FrameGroupEnum, FrameItemEnum,
                   frame_groups, frame_items)
from gamedata import (GameData)
from global_defines import (attribute_classes, attributes, months, sunsigns,
                            cultures, social_classes, sibling_ranks, wounds,
                            parent_statuses, player_frames, comelinesses,
                            complexions, color_hairs, color_eyes,
                            SkillClassEnum, skill_classes, skills, body_parts,
                            materials, DamageTypeEnum, AttrEnum,
                            Material, PlayerCombatState, PersonTypeEnum,
                            ItemTypeEnum, ItemFlagEnum, ArmorLayer,
                            DiceRoll, DoorEnum, Mob, Player,
                            TargetTypeEnum, ConditionCheckEnum,
                            TriggerTypeEnum, RoomEnum, RoomFlag,
                            DirectionEnum, directions, Roll, armor_shapes,
                            aims, Effect, EffectTypeEnum)
from table_melee_attack import (Action)
from logger import (logd, loge)


wrapper = TextWrapper(width=70, fix_sentence_endings=True)


def CalcEffect(eff_type):
  player = GameData.GetPlayer()
  value = 0
  for item in player.Items:
    if item.Effects is not None:
      for y in item.Effects:
        if y.EffectType == eff_type:
          value += y.Modifier
  if player.Effects is not None:
    for y in player.Effects:
      if y.EffectType == eff_type:
        value += y.Modifer
  return value


class ItemQty:
  def __init__(self, item, qty=1):
    self.Item = item
    self.Desc = item.UniqueStr()
    self.Qty = qty

  def IsEqual(self, item):
    if self.Desc == item.UniqueStr():
      return True
    return False


def appendFilterItem(items, item):
  match = False
  for i in items:
    if i.IsEqual(item):
      match = True
      i.Qty += 1
      break
  if not match:
    items.append(ItemQty(item, 1))


def filterItems(items, equipped=False, equippable=False, flags=0, noflags=0):
  item_array = []

  # sort items
  items.sort(key=lambda x: x.ItemName)

  # clear temp flags
  for item in items:
    item.Flags &= ~ItemFlagEnum.TEMP

  for itp in ItemTypeEnum:
    if equippable:
      if itp not in [ItemTypeEnum.WEAPON, ItemTypeEnum.ARMOR, ItemTypeEnum.RING]:
        continue
    if itp == ItemTypeEnum.ARMOR:
      for al in ArmorLayer:
        for bp_id in body_parts.keys():
          for item in items:
            if item.ItemType != itp:
              continue
            if item.Flags & ItemFlagEnum.TEMP > 0:
              continue
            if item.Covered(bp_id) and item.Layer & al > 0:
              if not equipped and item.Equipped:
                continue
              if equipped and not item.Equipped:
                continue
              if flags > 0 and item.Flags & flags == 0:
                continue
              if noflags > 0 and item.Flags & noflags > 0:
                continue
              appendFilterItem(item_array, item)
              item.Flags |= ItemFlagEnum.TEMP
    else:
      for item in items:
        if item.ItemType != itp:
          continue
        if item.Flags & ItemFlagEnum.TEMP > 0:
          continue
        if not equipped and item.Equipped:
          continue
        if equipped and not item.Equipped:
          continue
        if flags > 0 and item.Flags & flags == 0:
          continue
        if noflags > 0 and item.Flags & noflags > 0:
          continue
        appendFilterItem(item_array, item)
        item.Flags |= ItemFlagEnum.TEMP

  # clear temp flags
  for item in items:
    item.Flags &= ~ItemFlagEnum.TEMP
  return item_array


def printItems(lines, itemqtylist, number=False, stats=False, shop=False, valueAdj=1):
  count = 0
  for itemqty in itemqtylist:
    count += 1
    if itemqty.Qty > 1:
      item_name = "[%d] %s" % (itemqty.Qty, itemqty.Item.ItemName.capitalize())
    else:
      item_name = itemqty.Item.ItemName.capitalize()
    item_name += itemqty.Item.ItemFlagStr(" (%s)")
    if stats:
      weight = itemqty.Item.Weight
      item_info = " : %5s lbs" % "{:3.1f}".format(itemqty.Qty * weight)
    else:
      item_info = ""
    if shop:
      item_value = " [%d SP]" % int(itemqty.Item.Value * valueAdj)
    else:
      item_value = ""
    item_desc = "%-30s%s%s" % (item_name, item_info, item_value)
    if number:
      appendLine(lines, "%2d. %s" % (count, item_desc))
    else:
      appendLine(lines, "%s" % (item_desc))
    if stats:
      if itemqty.Item.Effects is not None:
        for eff in itemqty.Item.Effects:
          if number:
            appendLine(lines, "      (%s)" % eff.toString())
          else:
            appendLine(lines, "  (%s)" % eff.toString())


'''
              :  |F3|  |  |F5|  |  |F7|  :
              :L3|  |R3|L5|  |R5|L7|  |R7:
                  /                  \
      --------   /     |---F4---|     \  :--------
      --------:-F2/L4--|        |--R4/F6-:--------

              /   |--------F1--------|   \
-------L1-----:---|                  |---:----R1--------|
'''

REND_LEFT = 1
REND_FACING = 2
REND_RIGHT = 3

render_offset = [
    [-38, -19, 0, 19, 38],
    [-18, -9, 0, 9, 18],
    [-6, -3, 0, 3, 6],
]


def renderOffset(facing, level, x_offset):
  return render_offset[level - 1][x_offset + 2]


def renderHudToFrame(cm, facing, frame, room_id, level, lighting_level, x_offset=0,
                     indent="", dirs=[REND_FACING, REND_LEFT, REND_RIGHT]):
  rooms = GameData.GetRooms()
  indent = "%s " % (indent)

  # TODO: misc items / enemies in the room
  for x in rooms[room_id].Persons:
    if x.Frame > FrameItemEnum.NONE:
      frame.Merge(frame_items[x.Frame].Facing[level - 1], renderOffset(REND_FACING, level, x_offset))

  # forward facing
  if REND_FACING in dirs:
    logd("%s[START F%d] r=%d, offset=%d/%d, dirs=%s" % (indent, level, room_id, x_offset,
                                                        renderOffset(REND_FACING, level, x_offset), dirs))
    if facing in rooms[room_id].Exits.keys():
      if rooms[room_id].Exits[facing].Frame() is not None:
        logd("%s[F%dA] (%d/%d) %s" % (indent, level, x_offset,
                                      renderOffset(REND_FACING, level, x_offset),
                                      rooms[room_id].Exits[facing].Frame()))
        frame.Merge(frame_groups[rooms[room_id].Exits[facing].Frame()].Facing[level - 1],
                    renderOffset(REND_FACING, level, x_offset))
    else:
      logd("%s[F%dB] (%d/%d) FrameGroupEnum.WALL" % (indent, level, x_offset,
                                                     renderOffset(REND_FACING, level, x_offset)))
      if facing in rooms[room_id].Walls.keys():
        frame.Merge(frame_groups[rooms[room_id].Walls[facing]].Facing[level - 1],
                    renderOffset(REND_FACING, level, x_offset))
      else:
        frame.Merge(frame_groups[FrameGroupEnum.WALL].Facing[level - 1],
                    renderOffset(REND_FACING, level, x_offset))

  # left of facing
  logd("%s[START L%d] r=%d, offset=%d/%d" % (indent, level, room_id, x_offset,
                                             renderOffset(REND_LEFT, level, x_offset)))
  if directions[facing].Left in rooms[room_id].Exits.keys():
    re = rooms[room_id].Exits[directions[facing].Left]
    if REND_LEFT in dirs and re.Frame() is not None:
      logd("%s[L%dA] (%d/%d) %s" % (indent, level, x_offset, renderOffset(REND_LEFT, level, x_offset), re.Frame()))
      frame.Merge(frame_groups[rooms[room_id].Exits[directions[facing].Left].Frame()].Left[level - 1],
                  renderOffset(REND_LEFT, level, x_offset))
    if REND_LEFT in dirs and level <= lighting_level and (re.Frame() is None or frame_groups[re.Frame()].Transparent):
      if facing in rooms[re.Room].Exits.keys():
        rre = rooms[re.Room].Exits[facing]
        if rre.Frame() is not None:
          logd("%s[LF%dA] (%d/%d) %s" % (indent, level, x_offset,
                                         renderOffset(REND_FACING, level, x_offset - 1),
                                         rre.Frame()))
          frame.Merge(frame_groups[rre.Frame()].Facing[level - 1],
                      renderOffset(REND_FACING, level, x_offset - 1))
      else:
        logd("%s[LF%dB] (%d/%d) FrameGroupEnum.WALL" % (indent, level, x_offset,
                                                        renderOffset(REND_FACING, level, x_offset - 1)))
        if facing in rooms[re.Room].Walls.keys():
          frame.Merge(frame_groups[rooms[re.Room].Walls[facing]].Facing[level - 1],
                      renderOffset(REND_FACING, level, x_offset - 1))
        else:
          frame.Merge(frame_groups[FrameGroupEnum.WALL].Facing[level - 1],
                      renderOffset(REND_FACING, level, x_offset - 1))
  elif REND_LEFT in dirs:
    logd("%s[L%dB] (%d/%d) FrameGroupEnum.WALL" % (indent, level, x_offset,
                                                   renderOffset(REND_LEFT, level, x_offset)))
    if directions[facing].Left in rooms[room_id].Walls.keys():
      frame.Merge(frame_groups[rooms[room_id].Walls[directions[facing].Left]].Left[level - 1],
                  renderOffset(REND_LEFT, level, x_offset))
    else:
      frame.Merge(frame_groups[FrameGroupEnum.WALL].Left[level - 1],
                  renderOffset(REND_LEFT, level, x_offset))

  # right of facing
  logd("%s[START R%d] r=%d, offset=%d/%d" % (indent, level, room_id, x_offset,
                                             renderOffset(REND_RIGHT, level, x_offset)))
  if directions[facing].Right in rooms[room_id].Exits.keys():
    re = rooms[room_id].Exits[directions[facing].Right]
    if REND_RIGHT in dirs and re.Frame() is not None:
      logd("%s[R%dA] (%d/%d) %s" % (indent, level, x_offset,
                                    renderOffset(REND_RIGHT, level, x_offset),
                                    re.Frame()))
      frame.Merge(frame_groups[re.Frame()].Right[level - 1],
                  renderOffset(REND_RIGHT, level, x_offset))
    if REND_RIGHT in dirs and level <= lighting_level and (re.Frame() is None or frame_groups[re.Frame()].Transparent):
      if facing in rooms[re.Room].Exits.keys():
        rre = rooms[re.Room].Exits[facing]
        if rre.Frame() is not None:
          logd("%s[RF%dA] (%d/%d) %s" % (indent, level, x_offset,
                                         renderOffset(REND_FACING, level, x_offset + 1),
                                         rre.Frame()))
          frame.Merge(frame_groups[rre.Frame()].Facing[level - 1],
                      renderOffset(REND_FACING, level, x_offset + 1))
      else:
        logd("%s[RF%dB] (%d/%d) FrameGroupEnum.WALL" % (indent, level, x_offset,
                                                        renderOffset(REND_FACING, level, x_offset + 1)))
        if facing in rooms[re.Room].Walls.keys():
          frame.Merge(frame_groups[rooms[re.Room].Walls[facing]].Facing[level - 1],
                      renderOffset(REND_FACING, level, x_offset + 1))
        else:
          frame.Merge(frame_groups[FrameGroupEnum.WALL].Facing[level - 1],
                      renderOffset(REND_FACING, level, x_offset + 1))
  elif REND_RIGHT in dirs:
    logd("%s[R%dB] (%d/%d) FrameGroupEnum.WALL" % (indent, level, x_offset,
                                                   renderOffset(REND_RIGHT, level, x_offset)))
    if directions[facing].Right in rooms[room_id].Walls.keys():
        frame.Merge(frame_groups[rooms[room_id].Walls[directions[facing].Right]].Right[level - 1],
                    renderOffset(REND_RIGHT, level, x_offset))
    else:
        frame.Merge(frame_groups[FrameGroupEnum.WALL].Right[level - 1],
                    renderOffset(REND_RIGHT, level, x_offset))

  if level > 2:
    return

  if level < lighting_level:
    # dive down facing path
    if facing in rooms[room_id].Exits.keys():
      if rooms[room_id].Exits[facing].Frame() is None or frame_groups[rooms[room_id].Exits[facing].Frame()].Transparent:
        logd("%s[DIVE F%d] r=%d, offset=%d" % (indent, level, room_id, x_offset))
        renderHudToFrame(cm, facing, frame, rooms[room_id].Exits[facing].Room,
                         level + 1, lighting_level, indent=indent, x_offset=x_offset)
    # dive down left path
    if directions[facing].Left in rooms[room_id].Exits.keys():
      re = rooms[room_id].Exits[directions[facing].Left]
      if re.Frame() is None or frame_groups[re.Frame()].Transparent:
        if REND_LEFT in dirs and facing in rooms[re.Room].Exits.keys():
          if level > 1:
            logd("%s[DIVE L%d] r=%d, offset=%d" % (indent, level, room_id, x_offset))
            renderHudToFrame(cm, facing, frame, rooms[re.Room].Exits[facing].Room,
                             level + 1, lighting_level, x_offset=x_offset - 1, indent=indent, dirs=[REND_FACING])
    # dive down right path if the room to the right's exit is clear
    if directions[facing].Right in rooms[room_id].Exits.keys():
      re = rooms[room_id].Exits[directions[facing].Right]
      if re.Frame() is None or frame_groups[re.Frame()].Transparent:
        if REND_RIGHT in dirs and facing in rooms[re.Room].Exits.keys():
          if level > 1:
            logd("%s[DIVE R%d] r=%d, offset=%d" % (indent, level, room_id, x_offset))
            renderHudToFrame(cm, facing, frame, rooms[re.Room].Exits[facing].Room,
                             level + 1, lighting_level, x_offset=x_offset + 1, indent=indent, dirs=[REND_FACING])


def printRoomDescription(room_id):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  doors = GameData.GetDoors()
  rooms = GameData.GetRooms()

  frame = Frame()
  lighting_level = 1
  if rooms[room_id].HasLight():
    lighting_level = 3
  renderHudToFrame(cm, player.Facing, frame, player.Room, 1, lighting_level)
  frame.Render(cm, directions[player.Facing].Names[0].capitalize())

  cm.Print("")

  # check for darkness w/o light source
  if not rooms[room_id].HasLight():
    cm.Print("Darkness", attr=ANSI.TEXT_BOLD)
    cm.Print("\nIt's completely dark and you can't see.")
    return

  # Room Title
  if rooms[room_id].Title != "":
    cm.Print(rooms[room_id].Title, attr=ANSI.TEXT_BOLD)
  # Room Description
  if len(rooms[room_id].LongDescription) > 0:
    for para in rooms[room_id].LongDescription:
      cm.Print("\n" + wrapper.fill(para))
    if rooms[room_id].OnLook is not None:
      for p in rooms[room_id].OnLook:
        if processConditions(room_id, rooms[room_id], p.Conditions):
          if p.Triggers is not None:
            if processTriggers(room_id, p.Triggers) is False:
              break
    # Exits
    if len(rooms[room_id].Exits) > 0:
      cm.Print("")
      for exit_dir, ex in rooms[room_id].Exits.items():
        cm.Print("%-9s" % (directions[exit_dir].Names[0].upper()),
                 attr=ANSI.TEXT_BOLD, end="")
        if ex.Door == DoorEnum.NONE:
          if rooms[ex.Room].HasLight():
            cm.Print(": %s" % (rooms[ex.Room].ShortDescription))
          else:
            cm.Print(": is darkness")
        else:
          if player.DoorState(ex.Door).Closed:
            cm.Print(": %s closed %s" %
                     (doors[ex.Door].Verb(), doors[ex.Door].Name))
          else:
            if rooms[ex.Room].HasLight():
              cm.Print(": %s (via open %s)" %
                       (rooms[ex.Room].ShortDescription, doors[ex.Door].Name))
            else:
              cm.Print(": is darkness (via open %s)" % (doors[ex.Door].Name))


def printRoomObjects(room_id):
  rooms = GameData.GetRooms()
  lines = []
  # Persons
  if len(rooms[room_id].Persons) > 0:
    appendLine(lines, "")
    for x in rooms[room_id].Persons:
      appendLine(lines, "%s" % x.LongDescription)
  # Items
  if len(rooms[room_id].Items) > 0:
    appendLine(lines, "")
    appendLine(lines, "The following items are here:")
    itemqtylist = []
    for it in rooms[room_id].Items:
      appendFilterItem(itemqtylist, it)
    printItems(lines, itemqtylist)
  printPaginate(lines)


def attrColor(attr):
  if attr <= 5:
    return TEXT_COLOR.RED
  elif attr <= 8:
    return TEXT_COLOR.YELLOW
  elif attr <= 13:
    return TEXT_COLOR.NORMAL
  else:
    return TEXT_COLOR.GREEN


class PageLine:
  def __init__(self, msg="", attr=0, end="\n"):
    self.Line = msg
    self.Attr = attr
    self.LineEnding = end


def appendLine(lines, line, attr=0, end="\n"):
  lines.append(PageLine(line, attr, end))


def printPaginate(lines, force_break=False):
  cm = GameData.GetConsole()
  if lines is not None and len(lines) > 0:
    count = 0
    for pl in lines:
      cm.Print(pl.Line, pl.Attr, pl.LineEnding)
      if pl.LineEnding == "\n":
        count += 1
      if count >= (cm.screenY - 2) and count < len(lines):
        x = cm.Input("<< [Q] to Quit and [Enter] to Continue >>", line_length=1).lower()
        if x == "q":
          return True
        count = 0
    if force_break and count > 0:
      x = cm.Input("<< [Q] to Quit and [Enter] to Continue >>", line_length=1).lower()
      if x == "q":
        return True
  return False


def printStats(person):
  cm = GameData.GetConsole()
  lines = []
  if person.PersonType == PersonTypeEnum.PLAYER:
    for ac_id, ac in attribute_classes.items():
      if ac.Hidden:
        continue
      appendLine(lines, "")
      appendLine(lines, "%s STATS" % (ac.Name.upper()), ANSI.TEXT_BOLD)
      appendLine(lines, "")
      for attr in person.Attr.keys():
        val = person.GetAttr(attr)
        if not attributes[attr].Hidden:
          if attributes[attr].AttrClass == ac_id:
            appendLine(lines, "%-15s: " % (attributes[attr].Name), end="")
            appendLine(lines, "%d" % (val), cm.ColorPair(attrColor(val)))
    appendLine(lines, "")
    appendLine(lines, "CHARACTER STATS", ANSI.TEXT_BOLD)
    appendLine(lines, "")
  else:
    appendLine(lines, "")
    appendLine(lines, "%s STATS" % (person.Name.upper()), ANSI.TEXT_BOLD)
    appendLine(lines, "")
  appendLine(lines, "%-15s: %d" % ("Endurance", person.AttrEndurance()))
  appendLine(lines, "%-15s: %d lbs" % ("Inven. Weight", person.ItemWeight()))
  appendLine(lines, "%-15s: %d" % ("Enc. Points", person.EncumbrancePenalty()))
  appendLine(lines, "%-15s: %d" % ("Injury Points", person.IP()))
  appendLine(lines, "%-15s: %d" % ("Fatigue Points", person.FatiguePoints()))
  appendLine(lines, "%-15s: %d" % ("Initiative", person.AttrInitiative()))
  appendLine(lines, "")
  appendLine(lines, "%-15s: %d" % ("Universal Pen.", person.UniversalPenalty()), ANSI.TEXT_BOLD)
  appendLine(lines, "%-15s: %d" % ("Physical Pen.", person.PhysicalPenalty()), ANSI.TEXT_BOLD)
  if person.PersonType == PersonTypeEnum.NPC:
    itemqtylist = filterItems(person.Items, equipped=True)
    if len(itemqtylist) > 0:
      appendLine(lines, "")
      appendLine(lines, "EQUIPMENT", ANSI.TEXT_BOLD)
      appendLine(lines, "")
      printItems(lines, itemqtylist, stats=True)
  appendLine(lines, "")
  appendLine(lines, "WOUND LIST", ANSI.TEXT_BOLD)
  appendLine(lines, "")
  if len(person.Wounds) < 1:
    appendLine(lines, "[NONE]")
  else:
    for w in person.Wounds:
      appendLine(lines, "%s %s %s wound [%d IP]" %
                 (wounds[w.WoundType].Name,
                  wounds[w.WoundType].Verbs[w.DamageType].lower(),
                  body_parts[w.Location].PartName.lower(), w.Impact))
  printPaginate(lines)


# GENERIC COMMAND FUNCTIONS

def actionComingSoon():
  cm = GameData.GetConsole()
  cm.Print("\nComing soon!")


def chooseItem(itemqtylist, verb, stats=True, shop=False, valueAdj=1):
  cm = GameData.GetConsole()
  lines = []
  appendLine(lines, "")
  appendLine(lines, "%s AN ITEM" % verb.upper(), ANSI.TEXT_BOLD)
  appendLine(lines, "")
  printItems(lines, itemqtylist, number=True, stats=stats, shop=shop, valueAdj=valueAdj)
  printPaginate(lines)
  x = cm.Input("Which item # to %s (0=Cancel):" % verb, line_length=3,
               input_flags=InputFlag.NUMERIC)
  if not x.isnumeric():
    cm.Print("\nInvalid item.")
    return (None, 0)
  itemNum = int(x)
  if itemNum == 0:
    cm.Print("\nCancelled.")
    return (None, 0)
  if itemNum < 1 or itemNum > len(itemqtylist):
    cm.Print("\nInvalid item.")
    return (None, 0)
  count = 0
  for itemqty in itemqtylist:
    count += 1
    if count == itemNum:
      return (itemqty.Item, itemqty.Qty)
  return (None, 0)


def actionGetItem(data=None):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  rooms = GameData.GetRooms()
  itemqtylist = filterItems(rooms[player.Room].Items, equipped=False)
  if len(itemqtylist) < 1:
    cm.Print("\nThere are no items in the room.")
    return
  if not rooms[player.Room].HasLight():
    cm.Print("\nYou can't see anything in the dark.")
    return
  (item, qty) = chooseItem(itemqtylist, "pick up")
  if item is None:
    return
  if processTriggers(None, item.OnGet) is False:
    cm.Print("\nYou can't seem to pick up %s." % item.ItemName)
    return
  rooms[player.Room].RemoveItem(item)
  player.AttachItem(item)
  cm.Print("\n%s picked up." % item.ItemName.capitalize())


def actionDropItem(data=None):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  rooms = GameData.GetRooms()
  itemqtylist = filterItems(player.Items, equipped=False)
  if len(itemqtylist) < 1:
    cm.Print("\nNothing is droppable at the moment.")
    return
  if not rooms[player.Room].HasLight():
    cm.Print("\nYou can't see anything in the dark.")
    return
  (item, qty) = chooseItem(itemqtylist, "drop")
  if item is None:
    return
  if item.Flags & ItemFlagEnum.NO_DROP > 0:
    cm.Print("\n%s cannot be dropped." % item.ItemName.capitalize())
    return
  if item.Flags & ItemFlagEnum.QUEST > 0:
    cm.Print("\n%s cannot be dropped." % item.ItemName.capitalize())
    return
  if processTriggers(None, item.OnDrop) is False:
    cm.Print("\nYou can't seem to drop %s." % item.ItemName)
    return
  player.RemoveItem(item)
  rooms[player.Room].AttachItem(item)
  cm.Print("\n%s dropped." % item.ItemName.capitalize())


def actionEquipItem(data=None):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  itemqtylist = filterItems(player.Items, equipped=False, equippable=True)
  if len(itemqtylist) < 1:
    cm.Print("\nNothing is equippable at the moment.")
    return
  (equip_item, qty) = chooseItem(itemqtylist, "equip")
  if equip_item is None:
    return
  # check for item conflicts
  count = 0
  for item in player.Items:
    if not item.Equipped:
      continue
    # check armor coverage / layer conflicts
    if equip_item.ItemType == ItemTypeEnum.ARMOR and item.ItemType == ItemTypeEnum.ARMOR:
      if item.Layer & equip_item.Layer > 0 and armor_shapes[item.Shape] & armor_shapes[equip_item.Shape] > 0:
        cm.Print("\n%s is already equipped." % item.ItemName.capitalize())
        return
    # only 2 weapons/shields
    if equip_item.ItemType in [ItemTypeEnum.SHIELD, ItemTypeEnum.WEAPON]:
      if item.ItemType in [ItemTypeEnum.SHIELD, ItemTypeEnum.WEAPON]:
        count += 1
        if count > 1:
          cm.Print("\nAlready wielding 2 weapons or shields.")
          return
    # only 2 rings
    if equip_item.ItemType == ItemTypeEnum.RING and item.ItemType == ItemTypeEnum.RING:
      count += 1
      if count > 1:
        cm.Print("\nAlready wielding 2 rings.")
        return
  if processTriggers(None, equip_item.OnEquip) is False:
    cm.Print("\nYou can't seem to eqiup %s." % equip_item.ItemName)
    return
  equip_item.Equipped = True
  # use a player's "attack" if in combat
  if player.CombatState != PlayerCombatState.NONE:
    cm.Print("\nYou take a moment to equip %s." % equip_item.ItemName)
    return False
  else:
    # 1 minute to equip
    player.GameTime += 60
    cm.Print("\n%s equipped." % equip_item.ItemName.capitalize())


def actionRemoveItem(data=None):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  itemqtylist = filterItems(player.Items, equipped=True)
  if len(itemqtylist) < 1:
    cm.Print("\nNothing is equipped.")
    return
  (item, qty) = chooseItem(itemqtylist, "remove")
  if item is None:
    return
  if processTriggers(None, item.OnRemove) is False:
    cm.Print("\nYou can't seem to remove %s." % item.ItemName)
    return
  item.Equipped = False
  # 1 minute to equip
  player.GameTime += 60
  cm.Print("\n%s removed." % item.ItemName.capitalize())


def actionInventory(data=None):
  player = GameData.GetPlayer()
  lines = []
  appendLine(lines, "")
  appendLine(lines, "CURRENCY", ANSI.TEXT_BOLD, end="")
  appendLine(lines, ": %d SP" % (player.Currency))
  itemqtylist = filterItems(player.Items, equipped=True)

  # weapon / shield
  hands = []
  for it in itemqtylist:
    if it.Item.ItemType in [ItemTypeEnum.WEAPON, ItemTypeEnum.SHIELD]:
      hands.append(it)
  appendLine(lines, "")
  appendLine(lines, "WIELDED", ANSI.TEXT_BOLD)
  if len(hands) <= 0:
    appendLine(lines, "[NONE]")
  else:
    printItems(lines, hands, stats=True)

  # rings
  rings = []
  for it in itemqtylist:
    if it.Item.ItemType == ItemTypeEnum.RING:
      rings.append(it)
  if len(rings) > 0:
    appendLine(lines, "RINGS", ANSI.TEXT_BOLD)
    printItems(lines, rings, stats=True)

  # armor
  armor = []
  for it in itemqtylist:
    if it.Item.ItemType == ItemTypeEnum.ARMOR:
      armor.append(it)
  appendLine(lines, "WORN", ANSI.TEXT_BOLD)
  if len(armor) <= 0:
    appendLine(lines, "[NONE]")
  else:
    printItems(lines, armor, stats=True)

  appendLine(lines, "%-30s : %5s lbs" % ("EQUIPPED WEIGHT=1/2",
                                         "{:3.1f}".format(player.EquipWeight() * 0.5)),
             ANSI.TEXT_BOLD)

  appendLine(lines, "")
  appendLine(lines, "ITEMS", ANSI.TEXT_BOLD)
  itemqtylist = filterItems(player.Items, equipped=False)
  if len(itemqtylist) < 1:
    appendLine(lines, "[NONE]")
  else:
    printItems(lines, itemqtylist, stats=True)
  appendLine(lines, "%-30s : %5s lbs" % ("INVENTORY WEIGHT",
                                         "{:3.1f}".format(player.EquipWeight(False))),
             ANSI.TEXT_BOLD)
  appendLine(lines, "")
  appendLine(lines, "%-30s : %5s lbs" % ("TOTAL WEIGHT",
                                         "{:3.1f}".format(player.ItemWeight())),
             ANSI.TEXT_BOLD)
  printPaginate(lines)


def actionSave():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  rooms = GameData.GetRooms()
  player.UpdatePlayerTime()
  if SavePlayer(player, rooms[player.Room].Title, player.Password):
    return True
  else:
    cm.Print("An error occured during SAVE!", attr=ANSI.TEXT_BOLD)
    return False


def actionSkills(data=None, id=None):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  lines = []
  for skc_id, skc in skill_classes.items():
    if id is not None and id != skc_id:
      continue
    if skc.Hidden:
      continue
    appendLine(lines, "")
    appendLine(lines, "%s SKILLS" % (skc.Name.upper()), ANSI.TEXT_BOLD)
    appendLine(lines, "")
    for sk_id, sk in skills.items():
      if sk.SkillClass != skc_id:
        continue
      if sk.Hidden:
        continue
      appendLine(lines, "%-15s: " % (sk.Name), end="")
      appendLine(lines, "%s" % (attributes[skills[sk_id].Attr1].Abbrev),
                 cm.ColorPair(attrColor(player.Attr[skills[sk_id].Attr1])),
                 end="")
      appendLine(lines, "/", end="")
      appendLine(lines, "%s" % (attributes[skills[sk_id].Attr2].Abbrev),
                 cm.ColorPair(attrColor(player.Attr[skills[sk_id].Attr2])),
                 end="")
      appendLine(lines, "/", end="")
      appendLine(lines, "%s" % (attributes[skills[sk_id].Attr3].Abbrev),
                 cm.ColorPair(attrColor(player.Attr[skills[sk_id].Attr3])),
                 end="")
      appendLine(lines, "  ML:%-3d" % (player.SkillML(sk_id)))
  printPaginate(lines)


def actionSkillsPhysical(data=None):
  actionSkills(data, SkillClassEnum.PHYSICAL)


def actionSkillsCommunication(data=None):
  actionSkills(data, SkillClassEnum.COMMUNICATION)


def actionSkillsCombat(data=None):
  actionSkills(data, SkillClassEnum.COMBAT)


def actionSkillsCrafts(data=None):
  actionSkills(data, SkillClassEnum.LORE_CRAFTS)


def actionInfo(data=None):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  cm.Print("\nBIRTH INFORMATION\n", attr=ANSI.TEXT_BOLD)
  # TODO: hardcoded Human for now
  cm.Print("%-15s: %s" % ("Name", player.Name))
  cm.Print("%-15s: %s" % (attributes[AttrEnum.SPECIES].Name, "Human"))
  cm.Print("%-15s: %s" % (attributes[AttrEnum.SEX].Name, player.AttrSexStr().capitalize()))
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
  cm.Print("\nAPPEARANCE\n", attr=ANSI.TEXT_BOLD)
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


def actionArmor(data=None):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  cm.Print("\nARMOR COVERAGE\n", attr=ANSI.TEXT_BOLD)
  cm.Print("%-15s  BLUNT EDGE PIERCE ELEMENTAL" % ("LOCATION"),
           attr=ANSI.TEXT_BOLD)
  m = Material("None", 0, 0, [0, 0, 0, 0])
  for bp_id, bp in body_parts.items():
    m.Copy(materials[player.SkinMaterial])
    for item in player.Items:
      if item.ItemType != ItemTypeEnum.ARMOR:
        continue
      if not item.Equipped:
        continue
      if item.Covered(bp_id):
        m.Add(materials[item.Material])
    cm.Print("%-15s: %-5d %-4d %-6d %-9d" %
             (body_parts[bp_id].PartName,
              m.Protection[DamageTypeEnum.BLUNT],
              m.Protection[DamageTypeEnum.EDGE],
              m.Protection[DamageTypeEnum.PIERCE],
              m.Protection[DamageTypeEnum.ELEMENTAL]))
    m.Clear()


def actionQuest(data=None):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  quests = GameData.GetQuests()
  count = 0
  cm.Print("\nCOMPLETED QUESTS\n", attr=ANSI.TEXT_BOLD)
  for quest_id, completed in player.Quests.items():
    if quests[quest_id].Hidden:
      continue
    if completed:
      count += 1
      flags = ""
      if quests[quest_id].Repeatable:
        flags = " (repeatable)"
      cm.Print("%s%s" % (quests[quest_id].Name, flags))
  if count < 1:
    cm.Print("[NONE]")
  count = 0
  cm.Print("\nCURRENT QUESTS\n", attr=ANSI.TEXT_BOLD)
  for quest_id, completed in player.Quests.items():
    if quests[quest_id].Hidden:
      continue
    if not completed:
      flags = ""
      if quests[quest_id].Repeatable:
        flags = " (repeatable)"
      count += 1
      cm.Print("%s%s" % (quests[quest_id].Name, flags))
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
  x = cm.Input("Which # to %s (0=Cancel):" % noun, line_length=3,
               input_flags=InputFlag.NUMERIC)
  if not x.isnumeric():
    cm.Print("\nInvalid target.")
    return None
  personNum = int(x)
  if personNum == 0:
    cm.Print("\nCancelled.")
    return None
  if personNum < 1 or personNum > len(npcs):
    cm.Print("\nInvalid target.")
    return None
  return npcs[personNum - 1]


def actionAttack(data=None):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  rooms = GameData.GetRooms()
  npcs = []
  if player.IsTalking():
    cm.Print("\nYou are talking! Enter \"DONE\" to end conversation.",
             attr=ANSI.TEXT_BOLD)
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


def actionInspect(data=None):
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
        logd("[cond] PLAYER_INVEN: %s" % (c.Data))
        item = player.HasItem(c.Data)
        if c.ConditionCheck == ConditionCheckEnum.HAS and item is None:
          return False
        if c.ConditionCheck == ConditionCheckEnum.HAS_NOT and item is not None:
          return False
      elif c.TargetType == TargetTypeEnum.PLAYER_QUEST:
        logd("[cond] PLAYER_QUEST: %d" % (c.Data))
        if c.ConditionCheck == ConditionCheckEnum.HAS:
          if not player.HasQuest(c.Data):
            return False
        if c.ConditionCheck == ConditionCheckEnum.HAS_NOT:
          if player.HasQuest(c.Data):
            return False
      elif c.TargetType == TargetTypeEnum.PLAYER_QUEST_COMPLETE:
        logd("[cond] PLAYER_QUEST_COMPLETE: %d" % (c.Data))
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
        logd("[cond] ITEM_IN_ROOM: room=%d, item=%s" % (room_id, c.Data))
        count = 0
        for item in rooms[room_id].Items:
          if item.Name.lower() == c.Data:
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
        logd("[cond] MOB_IN_ROOM: room=%d, mob=%d" % (room_id, c.Data))
        match = False
        count = 0
        for p in rooms[room_id].Persons:
          if p.PersonID == c.Data:
            count += 1
            match = True
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
        logd("[cond] LOCATED_IN_ROOM: room=%d" % (c.Data))
        if type(obj) is Mob:
          if c.ConditionCheck == ConditionCheckEnum.HAS and not rooms[c.Data].PersonInRoom(obj.UUID):
            return False
          if c.ConditionCheck == ConditionCheckEnum.HAS_NOT and rooms[c.Data].PersonInRoom(obj.UUID):
            return False
      elif c.TargetType == TargetTypeEnum.PERCENT_CHANCE:
        logd("[cond] PERCENT_CHANCE: percent=%d" % (c.Value))
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
        logd("[trigger] ITEM_GIVE: %s" % (tr.Data.ItemName))
        player.AddItem(tr.Data)
      elif tr.TriggerType == TriggerTypeEnum.ITEM_TAKE:
        logd("[trigger] ITEM_TAKE: %s" % (tr.Data))
        item = player.HasItem(tr.Data)
        if item is not None:
          player.RemoveItem(item)
          del item
      elif tr.TriggerType == TriggerTypeEnum.ITEM_SELL:
        logd("[trigger] ITEM_SELL")
        actionShopSell(obj)
      elif tr.TriggerType == TriggerTypeEnum.ITEM_BUY:
        logd("[trigger] ITEM_BUY")
        actionShopBuy(obj)
      elif tr.TriggerType == TriggerTypeEnum.ROOM_SPAWN_MOB:
        logd("[trigger] ROOM_SPAWN_MOB [%s]: %s" % (rooms[obj].Title, tr.Data.Person))
        p = tr.Data.Create(obj, processConditions, processTriggers)
        if p is not None:
          rooms[obj].AddPerson(p)
      elif tr.TriggerType == TriggerTypeEnum.ROOM_DESPAWN_MOB:
        logd("[trigger] ROOM_DESPAWN_MOB")
        # TODO:
        cm.Print("* Coming Soon *")
      elif tr.TriggerType == TriggerTypeEnum.CURRENCY_GIVE:
        logd("[trigger] CURRENCY_GIVE")
        player.Currency += int(tr.Data)
      elif tr.TriggerType == TriggerTypeEnum.CURRENCY_TAKE:
        logd("[trigger] CURRENCY_TAKE")
        player.Currency -= int(tr.Data)
      elif tr.TriggerType == TriggerTypeEnum.QUEST_GIVE:
        logd("[trigger] QUEST_GIVE")
        player.AddQuest(tr.Data)
      elif tr.TriggerType == TriggerTypeEnum.QUEST_COMPLETE:
        logd("[trigger] QUEST_COMPLETE")
        player.CompleteQuest(tr.Data)
      elif tr.TriggerType == TriggerTypeEnum.PERSON_ATTACK:
        logd("[trigger] PERSON_ATTACK")
        if type(obj) is Mob:
          player.SetTalking(None)
          cm.Print("%s attacks you!" % (obj.Name.capitalize()), attr=ANSI.TEXT_BOLD)
          player.CombatTarget = obj.UUID
      elif tr.TriggerType == TriggerTypeEnum.PERSON_DESC:
        logd("[trigger] PERSON_DESC")
        if type(obj) == Mob:
          obj.LongDescription = obj.TextTranslate(tr.Data)
      elif tr.TriggerType == TriggerTypeEnum.ZONE_MESSAGE:
        logd("[trigger] ZONE_MESSAGE")
        if tr.Data2 is None:
          if player.Room != obj and rooms[player.Room].Zone == rooms[obj].Zone:
            for m in tr.Data:
              cm.Print("\n" + wrapper.fill(rooms[obj].TextTranslate(m)))
        else:
          if player.Room != obj and rooms[player.Room].Zone == tr.Data2:
            for m in tr.Data:
              cm.Print("\n" + wrapper.fill(rooms[obj].TextTranslate(m)))
      elif tr.TriggerType == TriggerTypeEnum.MESSAGE:
        logd("[trigger] MESSAGE")
        if tr.Data2 is None:
          logd("[trigger] 1")
          if type(obj) == Mob:
            if rooms[player.Room].PersonInRoom(obj.UUID):
              for m in tr.Data:
                cm.Print("\n" + wrapper.fill(obj.TextTranslate(m)))
          elif type(obj) == RoomEnum:
            if player.Room == obj:
              for m in tr.Data:
                cm.Print(wrapper.fill(rooms[player.Room].TextTranslate(m)))
          else:
            for m in tr.Data:
              cm.Print(wrapper.fill(rooms[player.Room].TextTranslate(m)))
        elif player.Room == tr.Data2:
          for m in tr.Data:
            cm.Print(wrapper.fill(m))
      elif tr.TriggerType == TriggerTypeEnum.MOVE:
        logd("[trigger] MOVE")
        # TODO:
        cm.Print("* Coming Soon *")
      elif tr.TriggerType == TriggerTypeEnum.DELAY:
        logd("[trigger] DELAY")
        obj.DelayTimestamp = player.PlayerTime()
        obj.DelaySeconds = int(tr.Data)
      elif tr.TriggerType == TriggerTypeEnum.GIVE_FLAG:
        logd("[trigger] GIVE_FLAG")
        if type(obj) == Mob or type(obj) == Player:
          obj.Flags |= tr.Data
      elif tr.TriggerType == TriggerTypeEnum.TAKE_FLAG:
        logd("[trigger] TAKE_FLAG")
        if type(obj) == Mob or type(obj) == Player:
          obj.Flags &= ~tr.Data
      elif tr.TriggerType == TriggerTypeEnum.PERSON_MOVE:
        logd("[trigger] PERSON_MOVE")
        if type(obj) == Mob:
          r = None
          for room_id in rooms.keys():
            if rooms[room_id].PersonInRoom(obj.UUID):
              r = rooms[room_id]
              break
          if r is not None:
            if tr.Data in r.Exits.keys():
              if rooms[player.Room].PersonInRoom(obj.UUID):
                cm.Print(wrapper.fill("%s moves to the %s." % (obj.Name.capitalize(), directions[tr.Data].Names[0])))
              r.RemovePerson(obj.UUID)
              nroom_id = r.Exits[tr.Data].Room
              rooms[nroom_id].AddPerson(obj)
              exit_match = False
              for exit_dir, ex in rooms[nroom_id].Exits.items():
                if ex.Room == room_id:
                  exit_match = True
                  if rooms[player.Room].PersonInRoom(obj.UUID):
                    cm.Print(wrapper.fill("%s enters from the %s." % (obj.Name.capitalize(), directions[exit_dir].Names[0])))
                  break
              if exit_match is False:
                if rooms[player.Room].PersonInRoom(obj.UUID):
                  cm.Print(wrapper.fill("%s enters." % (obj.Name.capitalize())))
            else:
              loge("%s cannot move %s from %s" % (obj.Name.capitalize(), directions[tr.Data].Names[0], r.Title))
      elif tr.TriggerType == TriggerTypeEnum.DOOR_UNLOCK:
        logd("[trigger] DOOR_UNLOCK")
        ds = player.DoorState(tr.Data)
        if ds is not None:
          ds.Closed = True
          ds.Locked = False
      elif tr.TriggerType == TriggerTypeEnum.DOOR_LOCK:
        logd("[trigger] DOOR_LOCK")
        ds = player.DoorState(tr.Data)
        if ds is not None:
          ds.Closed = True
          ds.Locked = True
      elif tr.TriggerType == TriggerTypeEnum.PAUSE:
        logd("[trigger] PAUSE")
        sleep(tr.Data)
      elif tr.TriggerType == TriggerTypeEnum.ROOM_SPAWN_ITEM:
        logd("[trigger] ROOM_SPAWN_ITEM: %s" % (tr.Data.ItemName))
        rooms[obj].AddItem(tr.Data)
      elif tr.TriggerType == TriggerTypeEnum.ROOM_DESPAWN_ITEM:
        logd("[trigger] ROOM_DESPAWN_ITEM: %s" % (tr.Data))
        item = rooms[obj].HasItem(tr.Data)
        if item is not None:
          rooms[obj].RemoveItem(item)
          del item
      elif tr.TriggerType == TriggerTypeEnum.EFFECT_ATTR:
        logd("[trigger] EFFECT_ATTR: %s" % (attributes[tr.Data].Name))
        if type(obj) == Mob or type(obj) == Player:
          dur = 0
          if tr.Data3 is not None:
            dur = tr.Data3
          obj.Effects.append(Effect(EffectTypeEnum.ATTRIBUTE, tr.Data, tr.Data2, dur))
      elif tr.TriggerType == TriggerTypeEnum.EFFECT_SKILL:
        logd("[trigger] EFFECT_SKILL: %s" % (skills[tr.Data].Name))
        if type(obj) == Mob or type(obj) == Player:
          dur = 0
          if tr.Data3 is not None:
            dur = tr.Data3
          obj.Effects.append(Effect(EffectTypeEnum.SKILL, tr.Data, tr.Data2, dur))
      elif tr.TriggerType == TriggerTypeEnum.END:
        logd("[trigger] END")
        return False
    else:
        return False


def printNPCTalk(keyword):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  ret = False
  for tk in player.Talk.Talks:
    if tk.Keyword.lower() == keyword:
      if processConditions(player.Room, player.Talk, tk.Conditions):
        ret = True
        if tk.Triggers is not None:
          processTriggers(player.Talk, tk.Triggers)
  # handle shopkeep item names
  if player.Talk.SellItems is not None:
    for item in player.Talk.SellItems:
      if item.ItemName.lower() == keyword:
        ret = True
        cm.Print("\n" + wrapper.fill(item.Description()))
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
        if processConditions(player.Room, npc, tk.Conditions):
          if tk.Triggers is not None:
            if not processTriggers(npc, tk.Triggers):
              return False
  return True


def actionShopBuy(shopkeep):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  if player.CombatState != PlayerCombatState.NONE:
    cm.Print("\nYou can't BUY during combat!", attr=ANSI.TEXT_BOLD)
    return
  itemqtylist = filterItems(shopkeep.SellItems)
  if len(itemqtylist) < 1:
    cm.Print("\nThere is nothing to buy.")
    return
  (item, qty) = chooseItem(itemqtylist, "buy", shop=True)
  if item is None:
    return
  if item.Value > player.Currency:
    cm.Print("\nYou cannot afford [%s]." % (item.ItemName), attr=ANSI.TEXT_BOLD)
    return
  # TODO possible factors to raise price?
  price = item.Value
  x = cm.Input("Confirm purchase of [%s] for %d SP [y/n]:" %
               (item.ItemName, price), line_length=1).lower()
  if x == "y":
    player.Currency -= price
    player.AddItem(item)
    cm.Print("\n%s hands you [%s]." %
             (shopkeep.Name.capitalize(), item.ItemName),
             attr=ANSI.TEXT_BOLD)
  else:
    cm.Print("\nPurchase aborted.", attr=ANSI.TEXT_BOLD)


def actionShopSell(shopkeep):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  if player.CombatState != PlayerCombatState.NONE:
    cm.Print("\nYou can't SELL during combat!", attr=ANSI.TEXT_BOLD)
    return
  itemqtylist = []
  if shopkeep.BuyItems is None:
    cm.Print("\n%s doesn't want to buy anything." % shopkeep.Name.capitalize())
    return
  for item in player.Items:
    if not item.Equipped and item.ItemName.lower() in shopkeep.BuyItems:
      appendFilterItem(itemqtylist, item)
  if len(itemqtylist) < 1:
    cm.Print("\n%s doesn't want to buy anything you have." % shopkeep.Name.capitalize())
    return
  # sell items for 1/2 value
  priceAdj = .5
  (item, qty) = chooseItem(itemqtylist, "sell", shop=True, valueAdj=priceAdj)
  sellqty = qty
  if sellqty > 1:
    x = cm.Input("How many would you like to sell (1-%d, 0=Cancel):" % (qty), line_length=3,
                 input_flags=InputFlag.NUMERIC)
    if not x.isnumeric():
      cm.Print("\nSale aborted.", attr=ANSI.TEXT_BOLD)
      return
    sellqty = int(x)
    if sellqty == 0 or sellqty > qty:
      cm.Print("\nSale aborted.", attr=ANSI.TEXT_BOLD)
      return
  if item is None:
    return
  price = sellqty * item.Value * priceAdj
  x = cm.Input("Confirm sale of %d [%s] for %d SP [y/n]:" % (sellqty, item.ItemName, price), line_length=1).lower()
  if x == "y":
    cm.Print("\nYou hand %d [%s] to %s." %
             (sellqty, item.ItemName, shopkeep.Name.capitalize()),
             attr=ANSI.TEXT_BOLD)
    while sellqty > 0:
      sellqty -= 1
      player.RemoveItemUniqueStr(item.UniqueStr())
    player.Currency += price
    del item
  else:
    cm.Print("\nSale aborted.", attr=ANSI.TEXT_BOLD)


def talkHandler(command):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  if command == "done":
    printNPCTalk("~")
    player.SetTalking(None)
    command = ""
    # return True to end the talk prompt and reprint room desc
    return True
  if not printNPCTalk(command):
    cm.Print("\n%s doesn't know anything about that." % player.Talk.Name.capitalize())
  else:
    # 30 second talk turn
    player.GameTime += 30
  # return None so that we avoid "You cannot do that here."
  return None


def actionTalk(data=None):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  rooms = GameData.GetRooms()
  if player.CombatState != PlayerCombatState.NONE:
    cm.Print("\nYou can't TALK during combat!", attr=ANSI.TEXT_BOLD)
    return
  npcs = []
  if player.IsTalking():
    cm.Print("\nYou are already talking!!", attr=ANSI.TEXT_BOLD)
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
  player.SetTalking(p)
  printNPCTalk("")


def actionTalkBuy(data=None):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  rooms = GameData.GetRooms()
  if player.IsTalking():
    # let triggers handle
    return False
  else:
    shopkeep = None
    for npc in rooms[player.Room].Persons:
      if npc.SellItems is not None:
        shopkeep = npc
        break
    if shopkeep is None:
      cm.Print("\nNo one nearby wants to buy anything.")
      return
    player.SetTalking(shopkeep)
    printNPCTalk("buy")


def actionTalkSell(data=None):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  rooms = GameData.GetRooms()
  if player.IsTalking():
    # let triggers handle
    return False
  else:
    shopkeep = None
    for npc in rooms[player.Room].Persons:
      if npc.BuyItems is not None:
        shopkeep = npc
        break
    if shopkeep is None:
      cm.Print("\nNo one nearby wants to sell anything.")
      return
    player.SetTalking(shopkeep)
    printNPCTalk("sell")


def chooseDoor(room_id, action, door_closed=None, door_locked=None):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  doors = GameData.GetDoors()
  rooms = GameData.GetRooms()
  ret = DoorEnum.NONE
  count = 0
  cm.Print("\nChoose a door:\n")
  for ex in rooms[player.Room].Exits.values():
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
  x = cm.Input("Which # to %s (0=Cancel):" % action, line_length=3,
               input_flags=InputFlag.NUMERIC)
  if not x.isnumeric():
    cm.Print("\nInvalid door.")
    return ret
  doorNum = int(x)
  if doorNum == 0:
    cm.Print("\nCancelled.")
    return ret
  if doorNum < 1 or doorNum > count:
    cm.Print("\nInvalid door.")
    return ret
  count = 0
  for ex in rooms[player.Room].Exits.values():
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


def actionUnlock(data=None):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  doors = GameData.GetDoors()
  door_id = chooseDoor(GameData.GetPlayer().Room, "unlock", door_locked=True)
  if door_id == DoorEnum.NONE:
    return
  item = player.HasItem(doors[door_id].KeyName)
  if item is not None:
    player.SetDoorState(door_id).Locked = False
    cm.Print("\nYou unlock the %s with %s." % (doors[door_id].Name, item.ItemName))
    # 30 seconds door action
    player.GameTime += 30
  else:
    cm.Print("\nYou don't have the key for that!", attr=ANSI.TEXT_BOLD)


def actionClose(data=None):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  rooms = GameData.GetRooms()
  doors = GameData.GetDoors()
  door_id = chooseDoor(GameData.GetPlayer().Room, "close", door_closed=False)
  if door_id != DoorEnum.NONE:
    player.SetDoorState(door_id).Closed = True
    cm.Print("\nYou close the %s." % doors[door_id].Name)
    # 30 seconds door action
    player.GameTime += 30
    # update frame
    frame = Frame()
    lighting_level = 1
    if rooms[player.Room].HasLight():
      lighting_level = 3
    renderHudToFrame(cm, player.Facing, frame, player.Room, 1, lighting_level)
    frame.Render(cm, directions[player.Facing].Names[0].capitalize())


def actionOpen(data=None):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  rooms = GameData.GetRooms()
  doors = GameData.GetDoors()
  door_id = chooseDoor(GameData.GetPlayer().Room, "open", door_closed=True)
  if door_id != DoorEnum.NONE:
    if player.DoorState(door_id).Locked:
      cm.Print("\nThe %s %s locked!" %
               (doors[door_id].Name, doors[door_id].Verb()),
               attr=ANSI.TEXT_BOLD)
    else:
      player.SetDoorState(door_id).Closed = False
      cm.Print("\nYou open the %s." % doors[door_id].Name)
      # 30 seconds door action
      player.GameTime += 30
      # update frame
      frame = Frame()
      lighting_level = 1
      if rooms[player.Room].HasLight():
        lighting_level = 3
      renderHudToFrame(cm, player.Facing, frame, player.Room, 1, lighting_level)
      frame.Render(cm, directions[player.Facing].Names[0].capitalize())


def actionListPlayers(data=None):
  pinfo = LoadStatsDB()
  lines = []
  if len(pinfo) == 0:
    appendLine(lines, "")
    appendLine(lines, "There are no saved characters!")
  else:
    appendLine(lines, "")
    appendLine(lines, "%-20s %-11s %s" % ("CHARACTER NAME", "TIME PLAYED", "SAVED IN ROOM"), ANSI.TEXT_BOLD)
    appendLine(lines, "%-20s %-11s %s" % ("--------------", "-----------", "-------------"), ANSI.TEXT_BOLD)
    for x in sorted(pinfo):
      if pinfo[x]["played"] > 0:
        appendLine(lines, "%-20s %-11s %s" % (x, "%0.2f days" % (pinfo[x]["played"]), pinfo[x]["info"]))
    appendLine(lines, "")
    appendLine(lines, "%-20s %d" % ("TOTAL", len(lines) - 4), ANSI.TEXT_BOLD)
  printPaginate(lines)


def actionLook(data=None):
  player = GameData.GetPlayer()
  printRoomDescription(player.Room)
  printRoomObjects(player.Room)


def actionChangePassword(data=None):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  rooms = GameData.GetRooms()
  if player.CombatState != PlayerCombatState.NONE:
    cm.Print("\nYou can't change your password in combat!", attr=ANSI.TEXT_BOLD)
    return
  if rooms[player.Room].Flags & RoomFlag.NO_SAVE != 0:
    cm.Print("\nYou can't change your password in an unsafe area!", attr=ANSI.TEXT_BOLD)
    return
  if player.IsTalking():
    cm.Print("\nYou are talking! Enter \"DONE\" to end conversation.", attr=ANSI.TEXT_BOLD)
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


def actionQuit(data=None):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  rooms = GameData.GetRooms()
  if player.CombatState != PlayerCombatState.NONE:
    cm.Print("\nYou can't QUIT in combat!", attr=ANSI.TEXT_BOLD)
    return
  if rooms[player.Room].Flags & RoomFlag.NO_SAVE != 0:
    cm.Print("\nYou can't QUIT in an unsafe area!", attr=ANSI.TEXT_BOLD)
    return
  if player.IsTalking():
    cm.Print("\nYou are talking! Enter \"DONE\" to end conversation.", attr=ANSI.TEXT_BOLD)
    return
  x = cm.Input("Are you sure you wish to quit [y/n]:", line_length=1).lower()
  if x == "y":
    actionSave()
    cm.Print("\nGoodbye!\n")
    exit()
  else:
    cm.Print("\nQuit aborted.")


def actionRest(data=None):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  if player.CombatState != PlayerCombatState.NONE:
    cm.Print("\nYou can't REST during combat!", attr=ANSI.TEXT_BOLD)
    return
  if player.IsTalking():
    cm.Print("\nYou are talking! Enter \"DONE\" to end conversation.", attr=ANSI.TEXT_BOLD)
    return
  cm.Print("\nYou take a moment to rest ...")
  combat = False
  # 1 hour rest time, 10 minutes at a time
  for i in range(6):
    sleep(1)
    player.GameTime += 600
    GameData.ProcessEvents()
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
      r = player.Attr[AttrEnum.AURA]
      for w in sorted(player.Wounds, reverse=True):
        cm.Print("\nYou clean and dress a %s %s %s wound ..." %
                 (wounds[w.WoundType].Name.lower(),
                  wounds[w.WoundType].Verbs[w.DamageType].lower(),
                  body_parts[w.Location].PartName.lower()))
        sleep(3)
        i = w.Impact
        w.Impact -= r
        r -= i
        if w.Impact <= 0:
          player.Wounds.remove(w)
          cm.Print("It's all better!")
        else:
          cm.Print("It looks a bit better.")
        if r <= 0:
          break


def actionStatsGeneric(data=None):
  printStats(GameData.GetPlayer())


def actionSaveGeneric(data=None):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  rooms = GameData.GetRooms()
  if player.CombatState != PlayerCombatState.NONE:
    cm.Print("\nYou can't SAVE in combat!", attr=ANSI.TEXT_BOLD)
    return
  if rooms[player.Room].Flags & RoomFlag.NO_SAVE != 0:
    cm.Print("\nYou can't SAVE in an unsafe area!", attr=ANSI.TEXT_BOLD)
    return
  if player.IsTalking():
    cm.Print("\nYou are talking! Enter \"DONE\" to end conversation.", attr=ANSI.TEXT_BOLD)
    return
  if actionSave():
    cm.Print("\nCharacter saved.")


def actionTime(data=None):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  cm.Print("\n%s on %s" % (player.GameTimeStr(), player.GameTimeDateStr()))
  day_plural = "s"
  if int(player.PlayerTime() / 86400) == 1:
    day_plural = ""
  cm.Print("Time Played: %d day%s %d minutes" %
           (int(player.PlayerTime() / 86400), day_plural,
            int((player.PlayerTime() % 86400) / 60)))


def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


def actionPrintNews(data=None, filter=False):
  player = GameData.GetPlayer()
  cm = GameData.GetConsole()
  lines = []
  max_news = 0
  header = False
  doc = parse("NEWS.xml")
  news_items = doc.getElementsByTagName("item")
  for news in news_items:
    news_id = int(getText(news.getElementsByTagName("id")[0].childNodes))
    if news_id > max_news:
      max_news = news_id
    if not filter or news_id > player.NewsID:
      if not header:
        appendLine(lines, "")
        appendLine(lines, "NEWS:", ANSI.TEXT_BOLD)
        header = True
      appendLine(lines, "")
      appendLine(lines, "Date   : %s" % getText(news.getElementsByTagName("date")[0].childNodes))
      appendLine(lines, "Subject: %s" % getText(news.getElementsByTagName("subject")[0].childNodes))
      appendLine(lines, "")
      text_lines = getText(news.getElementsByTagName("text")[0].childNodes)
      for line in text_lines.split("\n"):
        appendLine(lines, "%s" % line.strip())
      quit = printPaginate(lines, force_break=True)
      player.NewsID = max_news
      while len(lines) > 0:
        lines.pop()
      if quit:
        return
  if not filter and not header and len(lines) == 0:
    cm.Print("\nThere is no new news items at this time.")


class GenericCommand:
  def __init__(self, cmds, cmd_func, desc=""):
    self.Commands = []
    self.Description = desc
    self.Function = cmd_func
    if cmds is not None:
      for c in cmds:
        self.Commands.append(c)


commands = []


def actionPrintCombatHelp(lines, data):
  cm = GameData.GetConsole()
  combatant = data[1]
  att = combatant.Person.GenerateCombatAttacks()
  if len(att) > 0:
    att_name = "%d ML [%s]" % (att[0].SkillML, att[0].Name)
  else:
    att_name = "no weapon!"
  if combatant.Target is not None:
    target_name = "%s [%d IP]" % (combatant.Target.Person.Name,
                                  combatant.Target.Person.IP())
  else:
    target_name = "[NO TARGET]"
  if combatant.Bloodloss > 0:
    appendLine(lines, "")
    appendLine(lines, "BLOODLOSS POINTS: %d of %d" %
               (combatant.Bloodloss, combatant.Person.AttrEndurance()))
  appendLine(lines, "")
  appendLine(lines, "COMBAT COMMANDS:", ANSI.TEXT_BOLD)
  appendLine(lines, "")
  appendLine(lines, "%-8s %-5s : %s" % ("AIM", "", aims[combatant.Aim].Name))
  if not combatant.Prone:
    appendLine(lines, "%-8s %-5s : %s" % ("ATTACK", "[A]", att_name))
  appendLine(lines, "%-8s %-5s :" % ("CAST", "[C]"))
  defe_att = combatant.Person.GenerateCombatAttacks(block=True)
  if combatant.DefAction == Action.DODGE or len(defe_att) < 1:
    defe_name = "%d ML [%s]" % (combatant.Person.AttrDodge(), "DODGE")
  else:
    defe_name = "%s ML [BLOCK with %s]" % (defe_att[0].SkillML, defe_att[0].Name)
  appendLine(lines, "%-8s %-5s : %s" % ("DEFENSE", "[DEF]", defe_name))
  appendLine(lines, "%-8s %-5s : %d ML" % ("FLEE", "[F]", combatant.Person.AttrDodge()))
  # appendLine(lines, "  GRAPPLE")
  # appendLine(lines, "  MISSILE")
  appendLine(lines, "%-8s %-5s :" % ("PASS", "[P]"))
  if combatant.Prone:
    appendLine(lines, "%-8s %-5s :" % ("STAND", ""), cm.ColorPair(TEXT_COLOR.YELLOW))
  appendLine(lines, "%-8s %-5s : %s" % ("TARGET", "[T]", target_name))


def actionPrintHelp(data=None):
  player = GameData.GetPlayer()
  lines = []
  appendLine(lines, "")
  appendLine(lines, "GENERAL COMMANDS:", ANSI.TEXT_BOLD)
  appendLine(lines, "")
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
    appendLine(lines, "%-10s%s" % (cmd.Commands[0].upper(), abbrevs))
  # exits
  appendLine(lines, "")
  appendLine(lines, "MOVE DIRECTIONS:", ANSI.TEXT_BOLD)
  appendLine(lines, "")
  for dir_id, dir_info in directions.items():
    dir_len = len(dir_info.Names)
    if dir_len > 1:
      abbrevs = " ["
      for x in range(1, dir_len):
        if x > 1:
          abbrevs += ", "
        abbrevs += dir_info.Names[x].upper()
      abbrevs += "]"
    else:
      abbrevs = ""
    appendLine(lines, "%-10s%s" % (dir_info.Names[0].upper(), abbrevs))

  if player.CombatState != PlayerCombatState.NONE and data is not None:
    actionPrintCombatHelp(lines, data)

  printPaginate(lines)


commands.append(GenericCommand(["armor", "ac"], actionArmor))
commands.append(GenericCommand(["attack", "a"], actionAttack))
commands.append(GenericCommand(["buy"], actionTalkBuy))
commands.append(GenericCommand(["character", "c"], actionInfo))
commands.append(GenericCommand(["close"], actionClose))
commands.append(GenericCommand(["drop"], actionDropItem))
commands.append(GenericCommand(["equip", "eq"], actionEquipItem))
commands.append(GenericCommand(["inspect"], actionInspect))
commands.append(GenericCommand(["get"], actionGetItem))
commands.append(GenericCommand(["help", "?"], actionPrintHelp))
commands.append(GenericCommand(["inventory", "i"], actionInventory))
commands.append(GenericCommand(["look", "l"], actionLook))
commands.append(GenericCommand(["news"], actionPrintNews))
commands.append(GenericCommand(["open"], actionOpen))
commands.append(GenericCommand(["password"], actionChangePassword))
commands.append(GenericCommand(["quests", "quest"], actionQuest))
commands.append(GenericCommand(["quit", "q"], actionQuit))
commands.append(GenericCommand(["remove", "rm"], actionRemoveItem))
commands.append(GenericCommand(["rest", "r"], actionRest))
commands.append(GenericCommand(["save"], actionSaveGeneric))
commands.append(GenericCommand(["sell"], actionTalkSell))
commands.append(GenericCommand(["skills", "sk"], actionSkills))
commands.append(GenericCommand(["skills-physical", "skp"], actionSkillsPhysical))
commands.append(GenericCommand(["skills-communication", "skcomm"], actionSkillsCommunication))
commands.append(GenericCommand(["skills-combat", "skcombat"], actionSkillsCombat))
commands.append(GenericCommand(["skills-crafts", "skcrafts"], actionSkillsCrafts))
commands.append(GenericCommand(["stats", "st"], actionStatsGeneric))
commands.append(GenericCommand(["talk"], actionTalk))
commands.append(GenericCommand(["time"], actionTime))
commands.append(GenericCommand(["unlock"], actionUnlock))
# No shiny things for silly users
# commands.append(GenericCommand(["who"], actionListPlayers))


def promptTimeout():
  player = GameData.GetPlayer()
  # 3 minutes for idle
  player.GameTime += 180
  GameData.ProcessEvents()


def prompt(cmdHandler=None, cmdHandlerData=None):
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  doors = GameData.GetDoors()
  rooms = GameData.GetRooms()
  while True:
    prompt_text = "[IP:%-3d PEN:%-3d | ? = HELP" % (player.IP(), player.PhysicalPenalty())
    if player.IsTalking():
      prompt_text += ", \"DONE\" = Exit Talk"
    prompt_text += "]:"
    x = cm.Input(prompt_text, timeout=5, timeoutFunc=promptTimeout).lower()
    # Handle universal commands
    cmd_match = None
    for gen_cmd in commands:
      for cmds in gen_cmd.Commands:
        if x == cmds:
          cmd_match = gen_cmd
          break
    if cmd_match is not None:
      res = cmd_match.Function(cmdHandlerData)
      if res is False:
        if cmdHandler is not None:
          if cmdHandler(x, cmdHandlerData):
            break
        elif player.IsTalking():
          if talkHandler(x):
            break
      elif res is True:
        # attack and talk cmds can return true to re-enter main for combat
        break
    else:
      match_dir = DirectionEnum.NONE
      orig_facing = facing = player.Facing
      # Handle facing
      if (x == "arrow_right"):
        facing = directions[orig_facing].Right
      elif (x == "arrow_left"):
        facing = directions[orig_facing].Left
      elif (x == "arrow_up"):
        x = "arrow_"
        match_dir = orig_facing
      elif (x == "arrow_down"):
        x = "arrow_"
        match_dir = directions[orig_facing].Reverse

      if (orig_facing != facing):
        player.Facing = facing
        frame = Frame()
        lighting_level = 1
        if rooms[player.Room].HasLight():
          lighting_level = 3
        renderHudToFrame(cm, facing, frame, player.Room, 1, lighting_level)
        frame.Render(cm, directions[facing].Names[0].capitalize())
        continue

      # Handle directions
      if match_dir == DirectionEnum.NONE:
        for d, d_info in directions.items():
          for d_cmd in d_info.Names:
            if x == d_cmd.lower():
              match_dir = d
              break

      if match_dir != DirectionEnum.NONE:
        if player.CombatState != PlayerCombatState.NONE:
          cm.Print("\nYou can't move in combat!  Try to FLEE!", attr=ANSI.TEXT_BOLD)
          continue
        elif player.IsTalking():
          printNPCTalk("~")
          player.SetTalking(None)

        trigger_deny = False
        for exit_dir, ex in rooms[player.Room].Exits.items():
          if match_dir == exit_dir:
            if ex.Door != DoorEnum.NONE:
              if player.DoorState(ex.Door).Closed:
                cm.Print("\nThe %s %s closed." %
                         (doors[ex.Door].Name, doors[ex.Door].Verb()),
                         attr=ANSI.TEXT_BOLD)
                break
              else:
                if not roomTalkTrigger("on_exit"):
                  trigger_deny = True
                  break
                # time to cross room
                player.GameTime += rooms[player.Room].TravelTime
                player.SetRoom(ex.Room)
                if x != "arrow_" and match_dir not in [DirectionEnum.DOWN, DirectionEnum.UP]:
                  player.Facing = match_dir
            else:
              if not roomTalkTrigger("on_exit"):
                trigger_deny = True
                break
              # time to cross room
              player.GameTime += rooms[player.Room].TravelTime
              player.SetRoom(ex.Room)
              if x != "arrow_" and match_dir not in [DirectionEnum.DOWN, DirectionEnum.UP]:
                player.Facing = match_dir
            return
        if not trigger_deny:
          cm.Print("\nYou can't go in that direction.", attr=ANSI.TEXT_BOLD)
          continue
      res = False
      if cmdHandler is not None:
        res = cmdHandler(x, cmdHandlerData)
      elif player.IsTalking():
        res = talkHandler(x)
      if res is True:
        break
      elif res is False:
        cm.Print("\nYou cannot do that here.", attr=ANSI.TEXT_BOLD)

# vim: tabstop=2 shiftwidth=2 expandtab:
