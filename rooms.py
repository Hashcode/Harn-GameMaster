# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Room Functions

from enum import IntEnum

from console import (ANSI, InputFlag)
from db import (ExistsDB, LoadPlayer)
from frame import (FrameGroupEnum)
from gamedata import (GameData)
from global_defines import (PersonEnum, PersonFlag, DoorEnum, Door, DoorState, DirectionEnum,
                            NewPerson, ConditionCheckEnum, TargetTypeEnum, Condition, TriggerTypeEnum, Trigger, Periodic,
                            RoomFuncResponse, RoomEnum, Exit, RoomFlag, Room, QuestEnum,
                            AttrEnum, attribute_classes, attributes,
                            ShapeEnum, QualityEnum, MaterialEnum, ItemTypeEnum, Item, ArmorLayer, Armor)
from utils import (attrColor, actionInfo, actionSave, actionPrintNews)

# from utils import (actionSave)


def room_StartGame():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()

  while True:
    x = cm.Input("CREATE a new character or RESTORE a saved game?", line_length=10).lower()
    if x == "restore":
      player.SetRoom(RoomEnum.GAME_RESTORE_SAVE)
      break
    elif x == "create":
      player.SetRoom(RoomEnum.GAME_CREATE_CHARACTER)
      break
  return RoomFuncResponse.SKIP


def room_RestoreSave():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  name = cm.Input("Character name:", line_length=20)
  pwd = cm.Input("Password:", line_length=10, input_flags=InputFlag.PASSWORD)

  cm.Print("\nPlease wait while saved data is loaded ...")
  ret = LoadPlayer(player, name, pwd)
  if not ret:
    cm.Print("Unable to find save data for %s!" % (name), attr=ANSI.TEXT_BOLD)
    player.SetRoom(RoomEnum.GAME_START)
    return RoomFuncResponse.SKIP

  cm.Print("Loaded.")
  player.ResetStats()
  # Finish Map Setup
  GameData.InitializeRooms()
  GameData.ProcessEvents(True)
  player.SetRoom(player.Room)

  actionPrintNews(filter=True)

  return RoomFuncResponse.SKIP


def downCost(val):
  if val == 10:
    return 1
  if val < 10:
    return abs((val - 1) - 10)
  if val > 10:
    return abs(val - 10)


def upCost(val):
  if val == 10:
    return 1
  if val < 10:
    return abs(val - 10)
  if val > 10:
    return abs((val + 1) - 10)


def primaryAttr(attr):
  if attr in [AttrEnum.EYESIGHT, AttrEnum.HEARING, AttrEnum.SMELL, AttrEnum.VOICE]:
    return False
  return True


def room_CreateCharacter():
  cm = GameData.GetConsole()
  player = GameData.GetPlayer()
  player.Name = cm.Input("Choose a character name:", line_length=20)
  if len(player.Name) < 3 or len(player.Name) > 20:
    cm.Print("\nCharacter name needs between 3 and 20 characters long.")
    return RoomFuncResponse.SKIP

  cm.Print("\nA password is used to encrypt your SAVE data.")
  cm.Print("It should NOT be a password used for anything important.")
  player.Password = cm.Input("Enter a password:", line_length=10,
                             input_flags=InputFlag.PASSWORD).upper()
  if len(player.Password) < 3 or len(player.Password) > 10:
    cm.Print("\nPassword needs to be between 3 and 10 characters long.")
    return RoomFuncResponse.SKIP

  if ExistsDB(player.Name, player.Password):
    cm.Print("\nCharacter aready exists.")
    player.SetRoom(RoomEnum.GAME_START)
    return RoomFuncResponse.SKIP

  keep = False
  while not keep:
    cm.ClearWindow()
    player.GenAttr()
    actionInfo()
    while True:
      x = cm.Input("[K]eep or [R]eroll:", line_length=1).lower()
      if x == "k":
        keep = True
        break
      if x == "r":
        break

  attr_list = [
      AttrEnum.STRENGTH,
      AttrEnum.STAMINA,
      AttrEnum.DEXTERITY,
      AttrEnum.AGILITY,
      AttrEnum.HEARING,
      AttrEnum.EYESIGHT,
      AttrEnum.SMELL,
      AttrEnum.VOICE,
      AttrEnum.INTELLIGENCE,
      AttrEnum.AURA,
      AttrEnum.WILL,
  ]
  keep = False
  selection = 0
  points = 20

  # calculate points to spend
  for x in attr_list:
    if player.Attr[x] != 10:
      for d in range(abs(player.Attr[x] - 10)):
        if player.Attr[x] < 10:
          points += downCost(10 - d)
        else:
          points -= upCost(10 + d)
  while not keep:
    cm.ClearWindow()
    cm.Print("CURRENT TRAINING POINTS: %d" % (points), attr=ANSI.TEXT_BOLD)
    cm.Print("NOTES:")
    cm.Print("- Training becomes more difficult as attribute goes higher")
    cm.Print("- Lower attributes to gain more training")
    cm.Print("- Primary attributes marked with *")
    for ac_id, ac in attribute_classes.items():
      if ac.Hidden:
        continue
      cm.Print("\n%s STATS\n" % (ac.Name.upper()), attr=ANSI.TEXT_BOLD)
      for attr in attr_list:
        val = player.Attr[attr]
        if not attributes[attr].Hidden:
          if attributes[attr].AttrClass == ac_id:
            pri = ""
            if primaryAttr(attr):
              pri = "*"
            if attr_list[selection] == attr:
              cm.Print("%-15s: %d :: < +%d | -%d >" %
                       ("%s%s" % (attributes[attr].Name, pri),
                        val, downCost(val), upCost(val)),
                       attr=cm.ColorPair(attrColor(val)) | ANSI.TEXT_REVERSE)
            else:
              cm.Print("%-15s: %d" %
                       ("%s%s" % (attributes[attr].Name, pri), val),
                       attr=cm.ColorPair(attrColor(val)))
    while True:
      x = cm.Input("Arrows to Adjust or [D]one:", line_length=1).lower()
      if x == "d":
        keep = True
        break
      if x == "arrow_up":
        if selection > 0:
          selection -= 1
        else:
          cm.Bell()
        break
      if x == "arrow_down":
        if selection < len(attr_list) - 1:
          selection += 1
        else:
          cm.Bell()
        break
      if x == "arrow_right":
        if player.Attr[attr_list[selection]] == 18:
          cm.Bell()
        elif upCost(player.Attr[attr_list[selection]]) > points:
          cm.Bell()
        else:
          points -= upCost(player.Attr[attr_list[selection]])
          player.Attr[attr_list[selection]] += 1
        break
      if x == "arrow_left":
        if primaryAttr(attr_list[selection]) and player.Attr[attr_list[selection]] <= 4:
          cm.Bell()
        if not primaryAttr(attr_list[selection]) and player.Attr[attr_list[selection]] <= 3:
          cm.Bell()
        else:
          points += downCost(player.Attr[attr_list[selection]])
          player.Attr[attr_list[selection]] -= 1
        break

  player.GenSkills()
  player.ResetStats()
  player.AddItem(Armor("cloth tunic", QualityEnum.AVE, MaterialEnum.CLOTH, ArmorLayer.AL_1, ShapeEnum.TUNIC), True)
  player.AddItem(Armor("cloth leggings", QualityEnum.AVE, MaterialEnum.CLOTH, ArmorLayer.AL_1_5, ShapeEnum.LEGGINGS), True)
  # Finish Map Setup
  GameData.InitializeRooms()
  GameData.ProcessEvents(True)
  player.SetRoom(GameData.ROOM_START)

  cm.Print("\nSaving character ...")
  actionSave()
  cm.Print("Done.")

  cm.Print("\nGood luck, %s!" % (player.Name))

  actionPrintNews(filter=True)

  return RoomFuncResponse.SKIP


# ZONES
class ZoneEnum(IntEnum):
  NONE = 0
  KEEP = 1
  INNER_KEEP = 2
  FOREST = 3


doors = {
    DoorEnum.KEEP_DRAWBRIDGE: Door("drawbridge", DoorState(True, True)),
    DoorEnum.WAREHOUSE_DBL_DOOR: Door("double doors to a warehouse", DoorState(True, True), "a large bronze warehouse key"),
    DoorEnum.CORPORAL_APPT_DOOR: Door("oak door to an apartment", DoorState(True, True), "a small iron apartment key"),
    DoorEnum.N_TOWER_TRAPDOOR_LEVEL_2: Door("bottom floor trapdoor", DoorState(True, False)),
    DoorEnum.N_TOWER_TRAPDOOR_LEVEL_3: Door("top floor trapdoor", DoorState(True, False)),
    DoorEnum.S_TOWER_TRAPDOOR_LEVEL_2: Door("bottom floor trapdoor", DoorState(True, False)),
    DoorEnum.S_TOWER_TRAPDOOR_LEVEL_3: Door("top floor trapdoor", DoorState(True, False)),
    DoorEnum.WARREN_DOOR_1: Door("scratched door", DoorState(True, True), "a tarnished bronze key"),
    DoorEnum.WARREN_DOOR_2: Door("door with a a strange triangle symbol", DoorState(True, True), "a triangle key"),
}

rooms = {
    # GAME ROOMS
    RoomEnum.GAME_START:
        Room(RoomEnum.GAME_START, ZoneEnum.NONE, "Welcome to Harn GameMaster!", "",
             [
                 "Take your characters on exciting journeys in the gritty world of the HârnMaster Game System in classic Dungeon's "
                 "and Dragons(tm) modules.",
                 "During your adventures you will accumulate skills, items and wealth. Make sure to SAVE along the way to ensure "
                 "your progress won't be lost.",
                 "NOTE: Best played with a fairly large window!"
             ],
             flags=RoomFlag.LIGHT,
             func=room_StartGame),
    RoomEnum.GAME_RESTORE_SAVE:
        Room(RoomEnum.GAME_RESTORE_SAVE, ZoneEnum.NONE, "Restore Saved Progress", flags=RoomFlag.LIGHT, func=room_RestoreSave),
    RoomEnum.GAME_CREATE_CHARACTER:
        Room(RoomEnum.GAME_CREATE_CHARACTER, ZoneEnum.NONE, "Create a New Character", flags=RoomFlag.LIGHT, func=room_CreateCharacter),

    # KEEP ON THE BORDERLANDS
    RoomEnum.BL_KEEP_GATEHOUSE:
        Room(RoomEnum.BL_KEEP_GATEHOUSE, ZoneEnum.KEEP, "The Main Gatehouse to Stonehaven Keep", "the main gatehouse",
             [
                 "Two 30' high towers complete with battlements, flank a 20' high gatehouse. All have holes for bow and "
                 "crossbow fire. A deep crevice in front of the place can be spanned by a drawbridge.",
                 "There is a portcullis at the entry way to the gatehouse, inside of which a passage leads to large gates. "
                 "The passage is about 10' wide and 10' high.",
                 "It is obvious that the building is constructed of great blocks of solid granite, undoubtedly common "
                 "throughout the entire fortress."
             ],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.WEST: Exit(RoomEnum.BL_GATEHOUSE_PASSAGE),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_ROAD_TO_KEEP,
                                          DoorEnum.KEEP_DRAWBRIDGE),
             },
             room_pers=[
                 NewPerson(PersonEnum.BL_KEEP_GUARD),
                 NewPerson(PersonEnum.BL_KEEP_SENTRY),
             ]),
    RoomEnum.BL_GATEHOUSE_PASSAGE:
        Room(RoomEnum.BL_GATEHOUSE_PASSAGE, ZoneEnum.KEEP, "Gatehouse Passage", "a gatehouse passage",
             [
                 "This 10' wide and 10' high passage leads from the main gatehouse of Stonehaven Keep to the entry yard. "
                 "The ceiling above is pierced with murder holes, and the walls to either side contain arrow slits for archery."
             ],
             flags=RoomFlag.LIGHT,
             room_pers=[
                 NewPerson(PersonEnum.BL_KEEP_BEGGAR),
             ],
             exits={
                 DirectionEnum.WEST: Exit(RoomEnum.BL_ENTRY_YARD),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_KEEP_GATEHOUSE),
             },
             walls={
                 DirectionEnum.NORTH: FrameGroupEnum.WALL_TORCH,
             }),
    RoomEnum.BL_ENTRY_YARD:
        Room(RoomEnum.BL_ENTRY_YARD, ZoneEnum.KEEP, "Entry Yard", "an entry yard",
             [
                 "This is a small area that is paved with cobblestones.  It forms a road of sorts along the eastern edge "
                 "of the keep interior. A long building with a 15' high roof runs the length of the yard. The smell of horses "
                 "eminates from it's interior."
             ],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_NORTHEASTERN_WALK),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_GATEHOUSE_PASSAGE),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_EASTERN_WALK),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_STABLE,
                                          frame_id=FrameGroupEnum.ARCHWAY),
             },
             room_pers=[
                 NewPerson(PersonEnum.BL_KEEP_CORPORAL_WATCH,
                           [
                               Condition(ConditionCheckEnum.GREATER_THAN, TargetTypeEnum.HOUR_OF_DAY_CHECK, value=6),
                               Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.HOUR_OF_DAY_CHECK, value=20),
                           ],
                           [
                               Trigger(TriggerTypeEnum.DOOR_LOCK, DoorEnum.CORPORAL_APPT_DOOR),
                           ]),
                 NewPerson(PersonEnum.BL_KEEP_YARD_SCRIBE),
                 NewPerson(PersonEnum.BL_KEEP_SENTRY),
             ],
             periodics=[
                 Periodic(
                     [
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=15),
                     ],
                     [
                         Trigger(TriggerTypeEnum.MESSAGE, ["A woman bumps into you as she crosses the yard heading south."]),
                     ], 300),
                 Periodic(
                     [
                         Condition(ConditionCheckEnum.HAS, TargetTypeEnum.MOB_IN_ROOM, PersonEnum.BL_KEEP_CORPORAL_WATCH),
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=25),
                     ],
                     [
                         Trigger(TriggerTypeEnum.MESSAGE,
                                 ["A lackey runs up and delivers a message to the corporal of the watch."]),
                     ], 450),
                 Periodic(
                     [
                         Condition(ConditionCheckEnum.HAS, TargetTypeEnum.MOB_IN_ROOM, PersonEnum.BL_KEEP_SENTRY),
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=15),
                     ],
                     [
                         Trigger(TriggerTypeEnum.MESSAGE,
                                 [
                                     "A sentry walks out of the north gatehouse and takes the place of the sentry "
                                     "currently on duty.",
                                 ]),
                     ], 300),
             ]),
    RoomEnum.BL_NORTHEASTERN_WALK:
        Room(RoomEnum.BL_NORTHEASTERN_WALK, ZoneEnum.KEEP, "North-Eastern Walk", "the north-eastern walk",
             [
                 "You stand on a cobblestone paved walk which follows the interior wall of the keep."
             ],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.EAST: Exit(RoomEnum.BL_N_GATEHOUSE_TOWER,
                                          frame_id=FrameGroupEnum.ARCHWAY),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_ENTRY_YARD),
             }),
    RoomEnum.BL_N_GATEHOUSE_TOWER:
        Room(RoomEnum.BL_N_GATEHOUSE_TOWER, ZoneEnum.KEEP, "North Gatehouse Tower", "the north gatehouse tower",
             [
                 "The bottom floor of the north gatehouse tower is strewn with sleeping pallets and spare clothing. "
                 "In the corner is a table and chairs used for eating in-between shifts.  A ladder in the northeast corner "
                 "leads up to a trapdoor in the ceiling."
             ],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.WEST: Exit(RoomEnum.BL_NORTHEASTERN_WALK,
                                          frame_id=FrameGroupEnum.ARCHWAY),
                 DirectionEnum.UP: Exit(RoomEnum.BL_N_GATEHOUSE_TOWER_LEVEL_2,
                                        DoorEnum.N_TOWER_TRAPDOOR_LEVEL_2,
                                        FrameGroupEnum.ARCHWAY),
             },
             room_pers=[
                 NewPerson(PersonEnum.BL_KEEP_SENTRY),
                 NewPerson(PersonEnum.BL_KEEP_SENTRY),
             ]),
    RoomEnum.BL_N_GATEHOUSE_TOWER_LEVEL_2:
        Room(RoomEnum.BL_N_GATEHOUSE_TOWER_LEVEL_2, ZoneEnum.KEEP,
             "Second Floor of the North Gatehouse Tower", "the second floor of the north gatehouse tower",
             [
                 "The second floor of the North Gatehouse tower contains several barrels of oil and stacks of rocks which "
                 "could be used as projectiles against attackers. A small trapdoor in the floor of the northeast corner "
                 "leads down and a ladder leads up to it's twin in the ceiling."
             ],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.DOWN: Exit(RoomEnum.BL_N_GATEHOUSE_TOWER,
                                          DoorEnum.N_TOWER_TRAPDOOR_LEVEL_2),
                 DirectionEnum.UP: Exit(RoomEnum.BL_N_GATEHOUSE_TOWER_LEVEL_3,
                                        DoorEnum.N_TOWER_TRAPDOOR_LEVEL_3),
             }),
    RoomEnum.BL_N_GATEHOUSE_TOWER_LEVEL_3:
        Room(RoomEnum.BL_N_GATEHOUSE_TOWER_LEVEL_3, ZoneEnum.KEEP,
             "Top Floor of the North Gatehouse Tower", "the top floor of the north gatehouse tower",
             [
                 "The expanse of forest to the east and north dominates the view from the top of the tower. The road "
                 "leading away from the keep winds between the forest and a river which passes through marshlands. "
                 "Eventually, the road bends to the north where it disappears into the forest. A low wall runs the "
                 "length of the outer wall providing cover for launching missile weapons at attackers coming in from "
                 "the road."
             ],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.DOWN: Exit(RoomEnum.BL_N_GATEHOUSE_TOWER_LEVEL_2,
                                          DoorEnum.N_TOWER_TRAPDOOR_LEVEL_3),
             }),
    RoomEnum.BL_STABLE:
        Room(RoomEnum.BL_STABLE, ZoneEnum.KEEP, "Common Stable", "a common stable",
             [
                 "The smell of horse and feed permeates the air inside the stable. A long row of stalls lines the "
                 "the back wall."
             ],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.EAST: Exit(RoomEnum.BL_ENTRY_YARD,
                                          frame_id=FrameGroupEnum.ARCHWAY),
             },
             onLook=[
                 Periodic(
                     [
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.HOUR_OF_DAY_CHECK, value=6),
                     ],
                     [
                         Trigger(TriggerTypeEnum.MESSAGE, ["At this quiet hour, the horses are silent their stalls."]),
                         Trigger(TriggerTypeEnum.END),
                     ]),
                 Periodic(
                     [
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.HOUR_OF_DAY_CHECK, value=20),
                     ],
                     [
                         Trigger(TriggerTypeEnum.MESSAGE,
                                 ["The stable is bustling with activity as stable hands move horses and gear."]),
                         Trigger(TriggerTypeEnum.END),
                     ]),
                 Periodic(
                     [
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.HOUR_OF_DAY_CHECK, value=25),
                     ],
                     [
                         Trigger(TriggerTypeEnum.MESSAGE,
                                 ["Activity in the stable has slowed. Occassionally, a horse is being readied for travel."]),
                         Trigger(TriggerTypeEnum.END),
                     ]),
             ]),
    RoomEnum.BL_EASTERN_WALK:
        Room(RoomEnum.BL_EASTERN_WALK, ZoneEnum.KEEP, "Eastern Walk", "the eastern walk",
             [
                 "You stand on a cobblestone paved walk which follows the interior wall of the keep."
             ],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_ENTRY_YARD),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_S_GATEHOUSE_TOWER,
                                          frame_id=FrameGroupEnum.ARCHWAY),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_EASTERN_WALK_2),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_WAREHOUSE,
                                          DoorEnum.WAREHOUSE_DBL_DOOR,
                                          FrameGroupEnum.DBL_DOOR_CLOSED,
                                          FrameGroupEnum.DBL_DOOR_OPEN),
             }),
    RoomEnum.BL_S_GATEHOUSE_TOWER:
        Room(RoomEnum.BL_S_GATEHOUSE_TOWER, ZoneEnum.KEEP, "South Gatehouse Tower", "the south gatehouse tower",
             [
                 "The bottom floor of the South Gatehouse tower is strewen with sleeping pallets and spare clothing. "
                 "Several stools are randomly located in clusters. Spare clothing hangs from a row of pegs along the far "
                 "wall. A ladder in the southeast corner leads up to a trapdoor in the ceiling."
             ],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.WEST: Exit(RoomEnum.BL_EASTERN_WALK,
                                          frame_id=FrameGroupEnum.ARCHWAY),
                 DirectionEnum.UP: Exit(RoomEnum.BL_S_GATEHOUSE_TOWER_LEVEL_2,
                                        DoorEnum.S_TOWER_TRAPDOOR_LEVEL_2),
             },
             room_pers=[
                 NewPerson(PersonEnum.BL_KEEP_SENTRY),
                 NewPerson(PersonEnum.BL_KEEP_SENTRY),
             ]),
    RoomEnum.BL_S_GATEHOUSE_TOWER_LEVEL_2:
        Room(RoomEnum.BL_S_GATEHOUSE_TOWER_LEVEL_2, ZoneEnum.KEEP,
             "Second Floor of the South Gatehouse Tower", "the second floor of the south gatehouse tower",
             [
                 "The second floor of the South Gatehouse tower contains several barrels of oil and stacks of rocks which "
                 "could be used as projectiles against attackers. A small trapdoor in the floor of the southeast corner "
                 "leads down and a ladder leads up to it's twin in the ceiling."
             ],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.DOWN: Exit(RoomEnum.BL_S_GATEHOUSE_TOWER,
                                          DoorEnum.S_TOWER_TRAPDOOR_LEVEL_2),
                 DirectionEnum.UP: Exit(RoomEnum.BL_S_GATEHOUSE_TOWER_LEVEL_3,
                                        DoorEnum.S_TOWER_TRAPDOOR_LEVEL_3),
             }),
    RoomEnum.BL_S_GATEHOUSE_TOWER_LEVEL_3:
        Room(RoomEnum.BL_S_GATEHOUSE_TOWER_LEVEL_3, ZoneEnum.KEEP,
             "Top Floor of the South Gatehouse Tower", "the top floor of the south gatehouse tower",
             [
                 "The expanse of forest to the east and north dominates the view from the top of the tower. The road "
                 "leading away from the keep winds between the forest and a river which passes through marshlands. "
                 "Eventually, the road bends to the north where it disappears into the forest. A low wall runs the "
                 "length of the outer wall providing cover for launching missile weapons at attackers coming in from "
                 "the road."
             ],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.DOWN: Exit(RoomEnum.BL_S_GATEHOUSE_TOWER_LEVEL_2,
                                          DoorEnum.S_TOWER_TRAPDOOR_LEVEL_3),
             }),
    RoomEnum.BL_WAREHOUSE:
        Room(RoomEnum.BL_WAREHOUSE, ZoneEnum.KEEP, "Common Warehouse", "a common warehouse",
             [
                 "Visiting merchants and other travelers who have quantities of goods are required to keep their materials "
                 "here until they are either sold to the persons at the keep or taken elsewhere.  Stored here are several "
                 "covered carts, many boxes, barrels, and bales.",
                 "Large rat droppings can be seen in several corners.",
                 "A rickety staircase leads down along the west wall."
             ],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.EAST: Exit(RoomEnum.BL_EASTERN_WALK,
                                          DoorEnum.WAREHOUSE_DBL_DOOR,
                                          FrameGroupEnum.DBL_DOOR_CLOSED,
                                          FrameGroupEnum.DBL_DOOR_OPEN),
                 DirectionEnum.DOWN: Exit(RoomEnum.BL_RAT_WARREN_1),
             },
             periodics=[
                 Periodic(
                     [
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.MOB_IN_ROOM, PersonEnum.MON_RAT, 1),
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=100),
                     ],
                     [
                         Trigger(TriggerTypeEnum.ROOM_SPAWN_MOB, NewPerson(PersonEnum.MON_RAT)),
                         Trigger(TriggerTypeEnum.MESSAGE, ["The sound of scurring claws comes from the west."],
                                 RoomEnum.BL_EASTERN_WALK),
                     ], 300),
             ]),
    RoomEnum.BL_EASTERN_WALK_2:
        Room(RoomEnum.BL_EASTERN_WALK_2, ZoneEnum.KEEP, "Eastern Walk", "the eastern walk",
             [
                 "You stand on a cobblestone paved walk which follows the interior wall of the keep."
             ],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_EASTERN_WALK),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_BAILIFF_TOWER,
                                          frame_id=FrameGroupEnum.ARCHWAY),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_SOUTHEASTERN_WALK),
             }),
    RoomEnum.BL_BAILIFF_TOWER:
        Room(RoomEnum.BL_BAILIFF_TOWER, ZoneEnum.KEEP, "Bailiff's Tower", "the Bailiff's tower",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.WEST: Exit(RoomEnum.BL_EASTERN_WALK_2,
                                          frame_id=FrameGroupEnum.ARCHWAY),
             }),
    RoomEnum.BL_SOUTHEASTERN_WALK:
        Room(RoomEnum.BL_SOUTHEASTERN_WALK, ZoneEnum.KEEP, "South-Eastern Walk", "the south-eastern walk",
             [
                 "You stand on a cobblestone paved walk which follows the interior wall of the keep."
             ],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_EASTERN_WALK_2),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_SOUTHERN_WALK),
             }),
    RoomEnum.BL_SOUTHERN_WALK:
        Room(RoomEnum.BL_SOUTHERN_WALK, ZoneEnum.KEEP, "Southern Walk", "the southern walk",
             ["** TODO **"],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_SMITHY,
                                           frame_id=FrameGroupEnum.ARCHWAY),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_SOUTHEASTERN_WALK),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_APARMENT_1,
                                           DoorEnum.CORPORAL_APPT_DOOR,
                                           FrameGroupEnum.DOOR_CLOSED,
                                           FrameGroupEnum.DOOR_OPEN),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_SOUTHERN_WALK_2),
             }),
    RoomEnum.BL_SMITHY:
        Room(RoomEnum.BL_SMITHY, ZoneEnum.KEEP, "The Smithy", "the smithy",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_SOUTHERN_WALK,
                                           frame_id=FrameGroupEnum.ARCHWAY),
             },
             room_pers=[
                 NewPerson(PersonEnum.BL_SMITHY),
             ]),
    RoomEnum.BL_APARMENT_1:
        Room(RoomEnum.BL_APARMENT_1, ZoneEnum.KEEP, "A Private Apartment", "a private apartment",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_SOUTHERN_WALK,
                                           DoorEnum.CORPORAL_APPT_DOOR,
                                           FrameGroupEnum.DOOR_CLOSED,
                                           FrameGroupEnum.DOOR_OPEN),
             },
             room_items=[
             ],
             room_pers=[
                 NewPerson(PersonEnum.BL_KEEP_CORPORAL_WATCH,
                           conditions=[
                               Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.HOUR_OF_DAY_CHECK, value=7),
                           ],
                           triggers=[
                               Trigger(TriggerTypeEnum.DOOR_UNLOCK, DoorEnum.CORPORAL_APPT_DOOR),
                               Trigger(TriggerTypeEnum.PERSON_DESC, "The corporal of the watch is resting here."),
                           ]),
                 NewPerson(PersonEnum.BL_KEEP_CORPORAL_WATCH,
                           [
                               Condition(ConditionCheckEnum.GREATER_THAN, TargetTypeEnum.HOUR_OF_DAY_CHECK, value=19),
                           ],
                           triggers=[
                               Trigger(TriggerTypeEnum.GIVE_FLAG, PersonFlag.BEHAVIOR_1),
                               Trigger(TriggerTypeEnum.DOOR_UNLOCK, DoorEnum.CORPORAL_APPT_DOOR),
                               Trigger(TriggerTypeEnum.PERSON_DESC, "The corporal of the watch is resting here."),
                           ]),
             ],
             periodics=[
                 Periodic(
                     [
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.ITEM_IN_ROOM, "a small iron apartment key", 1),
                         Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.PLAYER_INVEN, "a small iron apartment key"),
                     ],
                     [
                         Trigger(TriggerTypeEnum.ROOM_SPAWN_ITEM,
                                 Item(ItemTypeEnum.MISC, "a small iron apartment key", QualityEnum.AVE, MaterialEnum.STEEL, 0.1)),
                     ], 36000),
             ]),
    RoomEnum.BL_SOUTHERN_WALK_2:
        Room(RoomEnum.BL_SOUTHERN_WALK_2, ZoneEnum.KEEP, "Southern Walk", "the southern walk",
             ["** TODO **"],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_MAIN_WALK),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_SOUTHERN_WALK),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_APARMENT_2,
                                           frame_id=FrameGroupEnum.ARCHWAY),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_SOUTHERN_WALK_3),
             }),
    RoomEnum.BL_APARMENT_2:
        Room(RoomEnum.BL_APARMENT_2, ZoneEnum.KEEP, "A Private Apartment", "a private apartment",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_SOUTHERN_WALK_2,
                                           frame_id=FrameGroupEnum.ARCHWAY),
             }),
    RoomEnum.BL_SOUTHERN_WALK_3:
        Room(RoomEnum.BL_SOUTHERN_WALK_3, ZoneEnum.KEEP, "Southern Walk", "the southern walk",
             ["** TODO **"],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_LEATHERWORKS,
                                           frame_id=FrameGroupEnum.ARCHWAY),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_SOUTHERN_WALK_2),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_PROVISIONS,
                                           frame_id=FrameGroupEnum.ARCHWAY),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_SOUTHWESTERN_WALK),
             }),
    RoomEnum.BL_LEATHERWORKS:
        Room(RoomEnum.BL_LEATHERWORKS, ZoneEnum.KEEP, "The Tanner", "the tanner",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_SOUTHERN_WALK_3,
                                           frame_id=FrameGroupEnum.ARCHWAY),
             },
             room_pers=[
                 NewPerson(PersonEnum.BL_TANNER),
             ]),
    RoomEnum.BL_PROVISIONS:
        Room(RoomEnum.BL_PROVISIONS, ZoneEnum.KEEP, "Provisions Shop", "a provisions shop",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_SOUTHERN_WALK_3,
                                           frame_id=FrameGroupEnum.ARCHWAY),
             },
             room_pers=[
                 NewPerson(PersonEnum.BL_PROVISIONER),
             ]),
    RoomEnum.BL_SOUTHWESTERN_WALK:
        Room(RoomEnum.BL_SOUTHWESTERN_WALK, ZoneEnum.KEEP, "South-Western Walk", "the south-western walk",
             ["** TODO **"],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_FOUNTAIN_SQUARE),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_SOUTHERN_WALK_3),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_WATCH_TOWER,
                                           frame_id=FrameGroupEnum.ARCHWAY),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_WEAPONSMITH,
                                          frame_id=FrameGroupEnum.ARCHWAY),
             }),
    RoomEnum.BL_WEAPONSMITH:
        Room(RoomEnum.BL_WEAPONSMITH, ZoneEnum.KEEP, "The Arms Dealer", "the arms dealer",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.EAST: Exit(RoomEnum.BL_SOUTHWESTERN_WALK,
                                          frame_id=FrameGroupEnum.ARCHWAY),
             },
             room_pers=[
                 NewPerson(PersonEnum.BL_ARMS_DEALER),
             ]),
    RoomEnum.BL_WATCH_TOWER:
        Room(RoomEnum.BL_WATCH_TOWER, ZoneEnum.KEEP, "Southwest Watch Tower", "the southwest watch tower",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_SOUTHWESTERN_WALK,
                                           frame_id=FrameGroupEnum.ARCHWAY),
             }),
    RoomEnum.BL_FOUNTAIN_SQUARE:
        Room(RoomEnum.BL_FOUNTAIN_SQUARE, ZoneEnum.KEEP, "Fountain Square", "fountain square",
             ["** TODO **"],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.WEST: Exit(RoomEnum.BL_TAVERN_MAINROOM,
                                          frame_id=FrameGroupEnum.ARCHWAY),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_SOUTHWESTERN_WALK),
             }),
    RoomEnum.BL_TAVERN_MAINROOM:
        Room(RoomEnum.BL_TAVERN_MAINROOM, ZoneEnum.KEEP, "The Tavern", "the tavern",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.EAST: Exit(RoomEnum.BL_FOUNTAIN_SQUARE,
                                          frame_id=FrameGroupEnum.ARCHWAY),
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_TAVERN_KITCHEN),
             }),
    RoomEnum.BL_TAVERN_KITCHEN:
        Room(RoomEnum.BL_TAVERN_KITCHEN, ZoneEnum.KEEP, "Tavern Kitchen", "the tavern kitchen",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_TAVERN_MAINROOM),
                 DirectionEnum.UP: Exit(RoomEnum.BL_TAVERN_LOFT),
             }),
    RoomEnum.BL_TAVERN_LOFT:
        Room(RoomEnum.BL_TAVERN_LOFT, ZoneEnum.KEEP, "Tavern Loft", "a loft above the tavern",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.DOWN: Exit(RoomEnum.BL_TAVERN_KITCHEN),
             }),
    RoomEnum.BL_MAIN_WALK:
        Room(RoomEnum.BL_MAIN_WALK, ZoneEnum.KEEP, "Main Walk", "a main thorough fair",
             ["** TODO **"],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_MAIN_WALK_2),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_SOUTHERN_WALK_2),
             }),
    RoomEnum.BL_MAIN_WALK_2:
        Room(RoomEnum.BL_MAIN_WALK_2, ZoneEnum.KEEP, "Main Walk", "a main thorough fair",
             ["** TODO **"],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_INN_ENTRYWAY,
                                           frame_id=FrameGroupEnum.ARCHWAY),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_MAIN_WALK),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_MAIN_WALK_3),
             }),
    RoomEnum.BL_INN_ENTRYWAY:
        Room(RoomEnum.BL_INN_ENTRYWAY, ZoneEnum.KEEP, "Inn Entryway", "the entryway of the inn",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_INN_COMMONROOM),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_INN_STAIRWAY),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_MAIN_WALK_2,
                                           frame_id=FrameGroupEnum.ARCHWAY),
             }),
    RoomEnum.BL_INN_COMMONROOM:
        Room(RoomEnum.BL_INN_COMMONROOM, ZoneEnum.KEEP, "Inn Commonroom", "the commonroom",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_INN_ENTRYWAY),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_INN_HALLWAY_1),
             }),
    RoomEnum.BL_INN_STAIRWAY:
        Room(RoomEnum.BL_INN_STAIRWAY, ZoneEnum.KEEP, "Inn Stairway", "the stairway",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.WEST: Exit(RoomEnum.BL_INN_ENTRYWAY),
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_INN_HALLWAY_1),
             }),
    RoomEnum.BL_INN_HALLWAY_1:
        Room(RoomEnum.BL_INN_HALLWAY_1, ZoneEnum.KEEP, "Inn Hallway", "the hallway",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_INN_STAIRWAY),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_INN_COMMONROOM),
             }),
    RoomEnum.BL_MAIN_WALK_3:
        Room(RoomEnum.BL_MAIN_WALK_3, ZoneEnum.KEEP, "Main Walk", "a main thorough fair",
             ["** TODO **"],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_MAIN_WALK_4),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_MAIN_WALK_2),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_ALLEYWAY),
             }),
    RoomEnum.BL_ALLEYWAY:
        Room(RoomEnum.BL_ALLEYWAY, ZoneEnum.KEEP, "A Dark Narrow Alleyway", "a dark narrow alleyway",
             ["** TODO **"],
             flags=RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_APARMENT_5,
                                           frame_id=FrameGroupEnum.ARCHWAY),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_MAIN_WALK_3),
             }),
    RoomEnum.BL_APARMENT_5:
        Room(RoomEnum.BL_APARMENT_5, ZoneEnum.KEEP, "A Shabby Apartment", "a shabby apartment",
             ["** TODO **"],
             exits={
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_ALLEYWAY,
                                           frame_id=FrameGroupEnum.ARCHWAY),
             }),
    RoomEnum.BL_MAIN_WALK_4:
        Room(RoomEnum.BL_MAIN_WALK_4, ZoneEnum.KEEP, "Main Walk", "a main thorough fair",
             ["** TODO **"],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_ENTRY_INNER_GATEHOUSE),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_MAIN_WALK_3),
             }),
    RoomEnum.BL_ENTRY_INNER_GATEHOUSE:
        Room(RoomEnum.BL_ENTRY_INNER_GATEHOUSE, ZoneEnum.KEEP, "Outside the Inner Gatehouse", "the outside of the inner gatehouse",
             ["** TODO **"],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_MAIN_WALK_4),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_CHAPEL_MAINROOM,
                                          frame_id=FrameGroupEnum.ARCHWAY),
             }),
    RoomEnum.BL_CHAPEL_MAINROOM:
        Room(RoomEnum.BL_CHAPEL_MAINROOM, ZoneEnum.KEEP, "Chapel Mainroom", "the chapel mainroom",
             ["** TODO **"],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.WEST: Exit(RoomEnum.BL_ENTRY_INNER_GATEHOUSE,
                                          frame_id=FrameGroupEnum.ARCHWAY),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_PRIEST_CHAMBER,
                                          frame_id=FrameGroupEnum.ARCHWAY),
             }),
    RoomEnum.BL_PRIEST_CHAMBER:
        Room(RoomEnum.BL_PRIEST_CHAMBER, ZoneEnum.KEEP, "The Curates's Chamber", "the curate's chamber",
             [
                 "The well-appointed chamber you are standing in radiates warmth from a cozy fire roaring in a small "
                 "western alcove. While spartan in furnishings, a well-made armoire sits in a corner as well as a tidy "
                 "bed along one wall. Several religious paintings are hung on the walls."
             ],
             flags=RoomFlag.LIGHT,
             exits={
                 DirectionEnum.WEST: Exit(RoomEnum.BL_CHAPEL_MAINROOM,
                                          frame_id=FrameGroupEnum.ARCHWAY),
             }),


    # RAT WARREN
    RoomEnum.BL_RAT_WARREN_1:
        Room(RoomEnum.BL_RAT_WARREN_1, ZoneEnum.KEEP, "A Warren Below the Warehouse", "a warren below the warehouse",
             [
                 "This room is part of a series of interconnected tunnels. The walls expose earth and rock at irregular "
                 "intervals and the air is moist and foul.  The uneven ground is littered with roots, rat droppings and "
                 "occasional small scratch marks.",
                 "A rickety staircase leads up along the west wall."
             ],
             exits={
                 DirectionEnum.UP: Exit(RoomEnum.BL_WAREHOUSE),
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_RAT_WARREN_2,
                                           frame_id=FrameGroupEnum.ARCHWAY),
             },
             periodics=[
                 Periodic(
                     [
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.MOB_IN_ROOM, PersonEnum.MON_RAT, 1),
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=100),
                     ],
                     [
                         Trigger(TriggerTypeEnum.ROOM_SPAWN_MOB, NewPerson(PersonEnum.MON_RAT)),
                     ], 3600),
             ]),
    RoomEnum.BL_RAT_WARREN_2:
        Room(RoomEnum.BL_RAT_WARREN_2, ZoneEnum.KEEP, "A Warren Below the Warehouse", "a warren below the warehouse",
             [
                 "This room is part of a series of interconnected tunnels. The walls expose earth and rock at irregular "
                 "intervals and the air is moist and foul.  The uneven ground is littered with roots, rat droppings and "
                 "occasional small scratch marks."
             ],
             exits={
                 DirectionEnum.EAST: Exit(RoomEnum.BL_RAT_WARREN_3),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_RAT_WARREN_1,
                                           frame_id=FrameGroupEnum.ARCHWAY),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_RAT_WARREN_4),
             }),
    RoomEnum.BL_RAT_WARREN_3:
        Room(RoomEnum.BL_RAT_WARREN_3, ZoneEnum.KEEP, "A Warren Below the Warehouse", "a warren below the warehouse",
             [
                 "This room is part of a series of interconnected tunnels. The walls expose earth and rock at irregular "
                 "intervals and the air is moist and foul.  The uneven ground is littered with roots, rat droppings and "
                 "occasional small scratch marks."
             ],
             exits={
                 DirectionEnum.WEST: Exit(RoomEnum.BL_RAT_WARREN_2),
             },
             periodics=[
                 Periodic(
                     [
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.ITEM_IN_ROOM, "a tarnished bronze key", 1),
                         Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.PLAYER_INVEN, "a tarnished bronze key"),
                     ],
                     [
                         Trigger(TriggerTypeEnum.ROOM_SPAWN_ITEM,
                                 Item(ItemTypeEnum.MISC, "a tarnished bronze key", QualityEnum.AVE, MaterialEnum.BRONZE, 0.1)),
                     ], 36000),
                 Periodic(
                     [
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.MOB_IN_ROOM, PersonEnum.MON_RAT, 1),
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=100),
                     ],
                     [
                         Trigger(TriggerTypeEnum.ROOM_SPAWN_MOB, NewPerson(PersonEnum.MON_RAT)),
                     ], 3600),
             ]),
    RoomEnum.BL_RAT_WARREN_4:
        Room(RoomEnum.BL_RAT_WARREN_4, ZoneEnum.KEEP, "A Warren Below the Warehouse", "a warren below the warehouse",
             [
                 "This room is part of a series of interconnected tunnels. The walls expose earth and rock at irregular "
                 "intervals and the air is moist and foul.  The uneven ground is littered with roots, rat droppings and "
                 "occasional small scratch marks."
             ],
             exits={
                 DirectionEnum.EAST: Exit(RoomEnum.BL_RAT_WARREN_2),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_RAT_WARREN_5),
             },
             periodics=[
                 Periodic(
                     [
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.MOB_IN_ROOM, PersonEnum.MON_RAT, 1),
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=100),
                     ],
                     [
                         Trigger(TriggerTypeEnum.ROOM_SPAWN_MOB, NewPerson(PersonEnum.MON_RAT)),
                     ], 3600),
             ]),
    RoomEnum.BL_RAT_WARREN_5:
        Room(RoomEnum.BL_RAT_WARREN_5, ZoneEnum.KEEP, "A Warren Below the Warehouse", "a warren below the warehouse",
             [
                 "This room is part of a series of interconnected tunnels. The walls expose earth and rock at irregular "
                 "intervals and the air is moist and foul.  The uneven ground is littered with roots, rat droppings and "
                 "occasional small scratch marks."
             ],
             exits={
                 DirectionEnum.EAST: Exit(RoomEnum.BL_RAT_WARREN_4),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_RAT_WARREN_7, DoorEnum.WARREN_DOOR_1,
                                           FrameGroupEnum.DOOR_CLOSED, FrameGroupEnum.DOOR_OPEN),
             }),
    RoomEnum.BL_RAT_WARREN_6:
        Room(RoomEnum.BL_RAT_WARREN_6, ZoneEnum.KEEP, "A Warren Below the Warehouse", "a warren below the warehouse",
             [
                 "This open space is part of a series of interconnected tunnels. The walls expose earth and rock at irregular "
                 "intervals and the air is moist and foul.  The uneven ground is littered with roots, rat droppings and "
                 "occasional small scratch marks."
             ],
             exits={
                 DirectionEnum.EAST: Exit(RoomEnum.BL_RAT_WARREN_7),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_RAT_WARREN_8),
             }),
    RoomEnum.BL_RAT_WARREN_7:
        Room(RoomEnum.BL_RAT_WARREN_7, ZoneEnum.KEEP, "A Warren Below the Warehouse", "a warren below the warehouse",
             [
                 "This open space is part of a series of interconnected tunnels. The walls expose earth and rock at irregular "
                 "intervals and the air is moist and foul.  The uneven ground is littered with roots, rat droppings and "
                 "occasional small scratch marks."
             ],
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_RAT_WARREN_5, DoorEnum.WARREN_DOOR_1,
                                           FrameGroupEnum.DOOR_CLOSED, FrameGroupEnum.DOOR_OPEN),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_RAT_WARREN_6),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_RAT_WARREN_9),
             }),
    RoomEnum.BL_RAT_WARREN_8:
        Room(RoomEnum.BL_RAT_WARREN_8, ZoneEnum.KEEP, "A Warren Below the Warehouse", "a warren below the warehouse",
             [
                 "This open space is part of a series of interconnected tunnels. The walls expose earth and rock at irregular "
                 "intervals and the air is moist and foul.  The uneven ground is littered with roots, rat droppings and "
                 "occasional small scratch marks."
             ],
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_RAT_WARREN_6),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_RAT_WARREN_9),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_RAT_WARREN_10,
                                           frame_id=FrameGroupEnum.ARCHWAY),
             },
             periodics=[
                 Periodic(
                     [
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.MOB_IN_ROOM, PersonEnum.MON_RAT, 1),
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=100),
                     ],
                     [
                         Trigger(TriggerTypeEnum.ROOM_SPAWN_MOB, NewPerson(PersonEnum.MON_RAT)),
                     ], 3600),
             ]),
    RoomEnum.BL_RAT_WARREN_9:
        Room(RoomEnum.BL_RAT_WARREN_9, ZoneEnum.KEEP, "A Warren Below the Warehouse", "a warren below the warehouse",
             [
                 "This open space is part of a series of interconnected tunnels. The walls expose earth and rock at irregular "
                 "intervals and the air is moist and foul.  The uneven ground is littered with roots, rat droppings and "
                 "occasional small scratch marks."
             ],
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_RAT_WARREN_7),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_RAT_WARREN_8),
             },
             periodics=[
                 Periodic(
                     [
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.MOB_IN_ROOM, PersonEnum.MON_RAT, 1),
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=100),
                     ],
                     [
                         Trigger(TriggerTypeEnum.ROOM_SPAWN_MOB, NewPerson(PersonEnum.MON_RAT)),
                     ], 3600),
             ]),
    RoomEnum.BL_RAT_WARREN_10:
        Room(RoomEnum.BL_RAT_WARREN_10, ZoneEnum.KEEP, "A Warren Below the Warehouse", "a warren below the warehouse",
             [
                 "This room is part of a series of interconnected tunnels. The walls expose earth and rock at irregular "
                 "intervals and the air is moist and foul.  The uneven ground is littered with roots, rat droppings and "
                 "occasional small scratch marks."
             ],
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_RAT_WARREN_8,
                                           frame_id=FrameGroupEnum.ARCHWAY),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_RAT_WARREN_11),
             }),
    RoomEnum.BL_RAT_WARREN_11:
        Room(RoomEnum.BL_RAT_WARREN_11, ZoneEnum.KEEP, "A Warren Below the Warehouse", "a warren below the warehouse",
             [
                 "This room is part of a series of interconnected tunnels. The walls expose earth and rock at irregular "
                 "intervals and the air is moist and foul.  The uneven ground is littered with roots, rat droppings and "
                 "occasional small scratch marks."
             ],
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_RAT_WARREN_10),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_RAT_WARREN_12,
                                          frame_id=FrameGroupEnum.ARCHWAY),
             },
             periodics=[
                 Periodic(
                     [
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.ITEM_IN_ROOM, "stained quilt cowl", 1),
                         Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.PLAYER_QUEST, QuestEnum.WAREHOUSE_COWL),
                     ],
                     [
                         Trigger(TriggerTypeEnum.ROOM_SPAWN_ITEM,
                                 Armor("stained quilt cowl", QualityEnum.TER, MaterialEnum.QUILT, ArmorLayer.AL_2, ShapeEnum.COWL,
                                       onGet=[
                                           Trigger(TriggerTypeEnum.QUEST_COMPLETE, QuestEnum.WAREHOUSE_COWL)
                                       ])),
                     ], 36000),
                 Periodic(
                     [
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.MOB_IN_ROOM, PersonEnum.MON_RAT_LARGE, 1),
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=100),
                     ],
                     [
                         Trigger(TriggerTypeEnum.ROOM_SPAWN_MOB, NewPerson(PersonEnum.MON_RAT_LARGE)),
                     ], 3600),
             ]),
    RoomEnum.BL_RAT_WARREN_12:
        Room(RoomEnum.BL_RAT_WARREN_12, ZoneEnum.KEEP, "A Warren Below the Warehouse", "a warren below the warehouse",
             [
                 "This room is part of a series of interconnected tunnels. The walls expose earth and rock at irregular "
                 "intervals and the air is moist and foul.  The uneven ground is littered with roots, rat droppings and "
                 "occasional small scratch marks.",
                 "The eastern side of the area reveals a large cavern in the ground."
             ],
             exits={
                 DirectionEnum.WEST: Exit(RoomEnum.BL_RAT_WARREN_11,
                                          frame_id=FrameGroupEnum.ARCHWAY),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_RAT_WARREN_13),
             },
             walls={
                 DirectionEnum.EAST: FrameGroupEnum.CAVERN,
             }),
    RoomEnum.BL_RAT_WARREN_13:
        Room(RoomEnum.BL_RAT_WARREN_13, ZoneEnum.KEEP, "A Warren Below the Warehouse", "a warren below the warehouse",
             [
                 "This room is part of a series of interconnected tunnels. The walls expose earth and rock at irregular "
                 "intervals and the air is moist and foul.  The uneven ground is littered with roots, rat droppings and "
                 "occasional small scratch marks.",
                 "The eastern side of the area reveals a large cavern in the ground."
             ],
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_RAT_WARREN_12),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_RAT_WARREN_14),
             },
             walls={
                 DirectionEnum.EAST: FrameGroupEnum.CAVERN,
             }),
    RoomEnum.BL_RAT_WARREN_14:
        Room(RoomEnum.BL_RAT_WARREN_14, ZoneEnum.KEEP, "A Warren Below the Warehouse", "a warren below the warehouse",
             [
                 "This room is part of a series of interconnected tunnels. The walls expose earth and rock at irregular "
                 "intervals and the air is moist and foul.  The uneven ground is littered with roots, rat droppings and "
                 "occasional small scratch marks.",
                 "A moldy wooden bridge crosses a large cavern in the ground to the east."
             ],
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_RAT_WARREN_13),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_RAT_WARREN_15,
                                          frame_id=FrameGroupEnum.BRIDGE),
             },
             periodics=[
                 Periodic(
                     [
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.MOB_IN_ROOM, PersonEnum.MON_RAT_LARGE, 1),
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=100),
                     ],
                     [
                         Trigger(TriggerTypeEnum.ROOM_SPAWN_MOB, NewPerson(PersonEnum.MON_RAT_LARGE)),
                     ], 3600),
             ],
             walls={
                 DirectionEnum.SOUTH: FrameGroupEnum.CAVERN,
             }),
    RoomEnum.BL_RAT_WARREN_15:
        Room(RoomEnum.BL_RAT_WARREN_15, ZoneEnum.KEEP, "On the Bridge over a Cavern", "a bridge over a cavern",
             [
                 "This moldy bridge is made of small wooden planks laid across 2 long beams which stretch across "
                 "the cavern below.  A foul smelling wind rises below and blows across the bridge and back into "
                 "the entry tunnels."
             ],
             exits={
                 DirectionEnum.WEST: Exit(RoomEnum.BL_RAT_WARREN_14,
                                          frame_id=FrameGroupEnum.BRIDGE),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_RAT_WARREN_16,
                                          frame_id=FrameGroupEnum.BRIDGE),
             },
             walls={
                 DirectionEnum.NORTH: FrameGroupEnum.WALL_BRIDGE,
                 DirectionEnum.SOUTH: FrameGroupEnum.WALL_BRIDGE,
             }),
    RoomEnum.BL_RAT_WARREN_16:
        Room(RoomEnum.BL_RAT_WARREN_16, ZoneEnum.KEEP, "A Warren Below the Warehouse", "a warren below the warehouse",
             [
                 "This room is part of a series of interconnected tunnels. The walls expose earth and rock at irregular "
                 "intervals and the air is moist and foul.  The uneven ground is littered with roots, rat droppings and "
                 "occasional small scratch marks.",
                 "A moldy wooden bridge crosses a large cavern in the ground to the west."
             ],
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_RAT_WARREN_17),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_RAT_WARREN_15,
                                          frame_id=FrameGroupEnum.BRIDGE),
             },
             periodics=[
                 Periodic(
                     [
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.ITEM_IN_ROOM, "stained quilt leggings", 1),
                         Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.PLAYER_QUEST, QuestEnum.WAREHOUSE_LEGGINGS),
                     ],
                     [
                         Trigger(TriggerTypeEnum.ROOM_SPAWN_ITEM,
                                 Armor("stained quilt leggings", QualityEnum.TER, MaterialEnum.QUILT, ArmorLayer.AL_2_5, ShapeEnum.LEGGINGS,
                                       onGet=[
                                           Trigger(TriggerTypeEnum.QUEST_COMPLETE, QuestEnum.WAREHOUSE_LEGGINGS)
                                       ])),
                     ], 36000),
                 Periodic(
                     [
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.MOB_IN_ROOM, PersonEnum.MON_RAT_LARGE, 1),
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=100),
                     ],
                     [
                         Trigger(TriggerTypeEnum.ROOM_SPAWN_MOB, NewPerson(PersonEnum.MON_RAT_LARGE)),
                     ], 3600),
             ],
             walls={
                 DirectionEnum.SOUTH: FrameGroupEnum.CAVERN,
             }),
    RoomEnum.BL_RAT_WARREN_17:
        Room(RoomEnum.BL_RAT_WARREN_17, ZoneEnum.KEEP, "A Warren Below the Warehouse", "a warren below the warehouse",
             [
                 "This room is part of a series of interconnected tunnels. The walls expose earth and rock at irregular "
                 "intervals and the air is moist and foul.  The uneven ground is littered with roots, rat droppings and "
                 "occasional small scratch marks.",
                 "The western side of the area reveals a large cavern in the ground."
             ],
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_RAT_WARREN_18),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_RAT_WARREN_19,
                                          frame_id=FrameGroupEnum.ARCHWAY),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_RAT_WARREN_16),
             },
             walls={
                 DirectionEnum.WEST: FrameGroupEnum.CAVERN,
             }),
    RoomEnum.BL_RAT_WARREN_18:
        Room(RoomEnum.BL_RAT_WARREN_18, ZoneEnum.KEEP, "A Warren Below the Warehouse", "a warren below the warehouse",
             [
                 "This room is part of a series of interconnected tunnels. The walls expose earth and rock at irregular "
                 "intervals and the air is moist and foul.  The uneven ground is littered with roots, rat droppings and "
                 "occasional small scratch marks.",
                 "The west side of the area reveals a large cavern in the ground."
             ],
             exits={
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_RAT_WARREN_17),
             },
             periodics=[
                 Periodic(
                     [
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.ITEM_IN_ROOM, "a triangle key", 1),
                         Condition(ConditionCheckEnum.HAS_NOT, TargetTypeEnum.PLAYER_INVEN, "a triangle key"),
                     ],
                     [
                         Trigger(TriggerTypeEnum.ROOM_SPAWN_ITEM,
                                 Item(ItemTypeEnum.MISC, "a triangle key", QualityEnum.AVE, MaterialEnum.STEEL, 0.1)),
                     ], 36000),
                 Periodic(
                     [
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.MOB_IN_ROOM, PersonEnum.MON_RAT_LARGE, 1),
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=100),
                     ],
                     [
                         Trigger(TriggerTypeEnum.ROOM_SPAWN_MOB, NewPerson(PersonEnum.MON_RAT_LARGE)),
                     ], 3600),
             ],
             walls={
                 DirectionEnum.WEST: FrameGroupEnum.CAVERN,
             }),
    RoomEnum.BL_RAT_WARREN_19:
        Room(RoomEnum.BL_RAT_WARREN_19, ZoneEnum.KEEP, "A Warren Below the Warehouse", "a warren below the warehouse",
             [
                 "This room is part of a series of interconnected tunnels. The walls expose earth and rock at irregular "
                 "intervals and the air is moist and foul.  The uneven ground is littered with roots, rat droppings and "
                 "occasional small scratch marks."
             ],
             exits={
                 DirectionEnum.WEST: Exit(RoomEnum.BL_RAT_WARREN_17),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_RAT_WARREN_20,
                                          frame_id=FrameGroupEnum.ARCHWAY),
             }),
    RoomEnum.BL_RAT_WARREN_20:
        Room(RoomEnum.BL_RAT_WARREN_20, ZoneEnum.KEEP, "A well-appointed Ante-room", "a well-appointed ante-room",
             [
                 "The air is fresher in this open space.  A few of the walls have paintings hanging on them and a "
                 "large rug is laid across the center of the room.  In one corner a small divan which might sit a "
                 "small child or two."
             ],
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_RAT_WARREN_22),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_RAT_WARREN_21),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_RAT_WARREN_19,
                                          frame_id=FrameGroupEnum.ARCHWAY),
             }),
    RoomEnum.BL_RAT_WARREN_21:
        Room(RoomEnum.BL_RAT_WARREN_21, ZoneEnum.KEEP, "A well-appointed Ante-room", "a well-appointed ante-room",
             [
                 "The air is fresher in this open space.  A few of the walls have paintings hanging on them and a "
                 "large rug is laid across the center of the room.  In one corner a small divan which might sit a "
                 "small child or two."
             ],
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_RAT_WARREN_23),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_RAT_WARREN_20),
             },
             periodics=[
                 Periodic(
                     [
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.MOB_IN_ROOM, PersonEnum.MON_RAT_GUARD, 1),
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=100),
                     ],
                     [
                         Trigger(TriggerTypeEnum.ROOM_SPAWN_MOB, NewPerson(PersonEnum.MON_RAT_GUARD)),
                     ], 3600),
             ]),
    RoomEnum.BL_RAT_WARREN_22:
        Room(RoomEnum.BL_RAT_WARREN_22, ZoneEnum.KEEP, "A well-appointed Ante-room", "a well-appointed ante-room",
             [
                 "The air is fresher in this open space.  A few of the walls have paintings hanging on them and a "
                 "large rug is laid across the center of the room.  In one corner a small divan which might sit a "
                 "small child or two."
             ],
             exits={
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_RAT_WARREN_20),
                 DirectionEnum.EAST: Exit(RoomEnum.BL_RAT_WARREN_23),
             }),
    RoomEnum.BL_RAT_WARREN_23:
        Room(RoomEnum.BL_RAT_WARREN_23, ZoneEnum.KEEP, "A Well-Appointed Ante-Rroom", "a well-appointed ante-room",
             [
                 "The air is fresher in this open space.  A few of the walls have paintings hanging on them and a "
                 "large rug is laid across the center of the room.  In one corner a small divan which might sit a "
                 "small child or two."
             ],
             exits={
                 DirectionEnum.NORTH: Exit(RoomEnum.BL_RAT_WARREN_24, DoorEnum.WARREN_DOOR_2,
                                           FrameGroupEnum.DOOR_CLOSED, FrameGroupEnum.DOOR_OPEN),
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_RAT_WARREN_21),
                 DirectionEnum.WEST: Exit(RoomEnum.BL_RAT_WARREN_22),
             },
             periodics=[
                 Periodic(
                     [
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.MOB_IN_ROOM, PersonEnum.MON_RAT_GUARD, 1),
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=100),
                     ],
                     [
                         Trigger(TriggerTypeEnum.ROOM_SPAWN_MOB, NewPerson(PersonEnum.MON_RAT_GUARD)),
                     ], 3600),
             ]),
    RoomEnum.BL_RAT_WARREN_24:
        Room(RoomEnum.BL_RAT_WARREN_24, ZoneEnum.KEEP, "A small bedroom", "a small bedroom",
             [
                 "Crowded into this small space is a miniature bed, an armoire and small chest of drawers. "
                 "Small items of decoration adorn the walls and top of the chest."
             ],
             exits={
                 DirectionEnum.SOUTH: Exit(RoomEnum.BL_RAT_WARREN_23, DoorEnum.WARREN_DOOR_2,
                                           FrameGroupEnum.DOOR_CLOSED, FrameGroupEnum.DOOR_OPEN),
             },
             periodics=[
                 Periodic(
                     [
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.MOB_IN_ROOM, PersonEnum.MON_RAT_NOBLE, 1),
                         Condition(ConditionCheckEnum.LESS_THAN, TargetTypeEnum.PERCENT_CHANCE, value=100),
                     ],
                     [
                         Trigger(TriggerTypeEnum.ROOM_SPAWN_MOB, NewPerson(PersonEnum.MON_RAT_NOBLE)),
                     ], 3600),
             ]),

    # OUTSIDE KEEP
    RoomEnum.BL_ROAD_TO_KEEP:
        Room(RoomEnum.BL_ROAD_TO_KEEP, ZoneEnum.FOREST, "Road to the Keep", "on a steep road",
             ["** TODO **"],
             flags=RoomFlag.LIGHT | RoomFlag.OUTSIDE,
             exits={
                 DirectionEnum.WEST: Exit(RoomEnum.BL_KEEP_GATEHOUSE,
                                          DoorEnum.KEEP_DRAWBRIDGE,
                                          FrameGroupEnum.ARCHWAY),
             }),
}

# vim: tabstop=2 shiftwidth=2 expandtab:
