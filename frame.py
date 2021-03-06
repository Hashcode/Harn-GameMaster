# Copyright (c) 2019-2020 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

from enum import (IntEnum)

from logger import (loge)


FRAME_HEIGHT = 24
FRAME_WIDTH = 26


def CopyLine(line1, line2):
  lenLine = len(line1)
  for x in range(len(line2)):
    if x > lenLine:
      break
    line1[x] = line2[x]


'''
OFFSET=0
  01234567
S[ ...... ]
OFFSET=2
    012345
D[   .....]
OFFSET=-2
  234567
D[.....   ]
'''


def MergeLine(line1, line2, offset, logon=False):
  counter = ""
  lenLine = len(line1)
  for x in range(len(line2)):
    if x > lenLine:
      break
    if offset >= 0 and x + offset < lenLine and line1[x + offset] == " ":
      counter = "%s%c" % (counter, line2[x])
      line1[x + offset] = line2[x]
    elif offset < 0 and x < lenLine + offset and line1[x] == " ":
      counter = "%s%c" % (counter, line2[x - offset])
      line1[x] = line2[x - offset]
    else:
      counter = "%s " % (counter)
  if logon:
    loge("  x[%s]" % (counter))


class FramePart:
  def __init__(self, filename):
    self._framePart = []
    self._framePartLines = 0
    with open(filename, "r") as f:
      for line in f:
        if self._framePartLines >= FRAME_HEIGHT:
          break
        self._framePart.append([])
        count = 0
        for c in line:
          if count >= FRAME_WIDTH:
            break
          self._framePart[self._framePartLines].append(c)
          count += 1
        self._framePartLines += 1


class FrameGroup:
  def __init__(self, filepaths, transparent=True):
    self.Facing = [
        FramePart("frames/%s_1.txt" % filepaths[0]),
        FramePart("frames/%s_2.txt" % filepaths[0]),
        FramePart("frames/%s_3.txt" % filepaths[0]),
    ]
    self.Left = [
        FramePart("frames/%s_1.txt" % filepaths[1]),
        FramePart("frames/%s_2.txt" % filepaths[1]),
        FramePart("frames/%s_3.txt" % filepaths[1]),
    ]
    self.Right = [
        FramePart("frames/%s_1.txt" % filepaths[2]),
        FramePart("frames/%s_2.txt" % filepaths[2]),
        FramePart("frames/%s_3.txt" % filepaths[2]),
    ]
    self.Transparent = transparent


class FrameItem:
  def __init__(self, filepath):
    self.Facing = [
        FramePart("frames/%s_1.txt" % filepath),
        FramePart("frames/%s_2.txt" % filepath),
        FramePart("frames/%s_3.txt" % filepath),
    ]


class Frame:
  def __init__(self):
    self._frame = []
    self._frameLines = 0
    for line in range(FRAME_HEIGHT):
      self._frame.append([])
      for c in range(FRAME_WIDTH):
        self._frame[self._frameLines].append(chr(32))
      self._frameLines += 1

  def Merge(self, fp, offset, logon=False):
    for l in range(len(fp._framePart)):
      if l < self._frameLines:
        MergeLine(self._frame[l], fp._framePart[l], offset, logon)

  def Render(self, cm, facing_caption):
    cm.ClearHud()
    cm.PrintHud("FACING: %s" % (facing_caption))
    cm.PrintHud("┌──────────────────────────┐")
    for line in self._frame:
      cm.PrintHud("│", end="")
      for c in line:
        if c == "#":
          cm.PrintHud(" ", end="")
        else:
          cm.PrintHud(c, end="")
      cm.PrintHud("│")
    cm.PrintHud("└──────────────────────────┘")


class FrameGroupEnum(IntEnum):
  BLANK = 0
  WALL = 1
  WALL_RAIL = 3
  WALL_CAVERN = 4
  WALL_SHORT = 5
  ARCHWAY = 10
  DOOR_CLOSED = 20
  DOOR_OPEN = 21
  DBL_DOOR_CLOSED = 22
  DBL_DOOR_OPEN = 23
  DRAWBRIDGE_CLOSED = 24
  DRAWBRIDGE_OPEN = 25
  PORTCULLIS_CLOSED = 26
  PORTCULLIS_OPEN = 27
  BRIDGE = 30
  CEILING_TRAPDOOR_CLOSED = 31
  CEILING_TRAPDOOR_OPEN = 32
  FLOOR_TRAPDOOR_CLOSED = 33
  FLOOR_TRAPDOOR_OPEN = 34
  DECO_TORCH = 100


class FrameItemEnum(IntEnum):
  NONE = 0
  CEILING_BLANK = 1
  CEILING_OUTSIDE = 2
  FLOOR_BLANK = 50
  FLOOR_WOOD = 51
  TREASURE = 100
  RAT = 101
  SPIDER = 102
  SKELETON = 200


frame_groups = {
    FrameGroupEnum.BLANK: FrameGroup(["blank", "blank", "blank"], True),
    FrameGroupEnum.WALL: FrameGroup(["facing_wall", "left_wall", "right_wall"], False),
    FrameGroupEnum.WALL_RAIL: FrameGroup(["facing_wall_rail", "left_wall_rail", "right_wall_rail"], False),
    FrameGroupEnum.WALL_CAVERN: FrameGroup(["facing_cavern", "left_cavern", "right_cavern"], True),
    FrameGroupEnum.WALL_SHORT: FrameGroup(["facing_wall_short", "left_wall_short", "right_wall_short"], True),
    FrameGroupEnum.ARCHWAY: FrameGroup(["facing_archway", "left_archway", "right_archway"]),
    FrameGroupEnum.DOOR_CLOSED: FrameGroup(["facing_door_closed", "left_door_closed", "right_door_closed"], False),
    FrameGroupEnum.DOOR_OPEN: FrameGroup(["facing_door_open", "left_door_open", "right_door_open"], True),
    FrameGroupEnum.DBL_DOOR_CLOSED: FrameGroup(["facing_dbl_door_closed", "left_dbl_door_closed", "right_dbl_door_closed"], False),
    FrameGroupEnum.DBL_DOOR_OPEN: FrameGroup(["facing_dbl_door_open", "left_dbl_door_open", "right_dbl_door_open"], True),
    FrameGroupEnum.DRAWBRIDGE_CLOSED: FrameGroup(["facing_drawbridge_closed", "blank", "blank"], False),
    FrameGroupEnum.DRAWBRIDGE_OPEN: FrameGroup(["blank", "blank", "blank"], True),
    FrameGroupEnum.PORTCULLIS_CLOSED: FrameGroup(["facing_portcullis_closed", "blank", "blank"], False),
    FrameGroupEnum.PORTCULLIS_OPEN: FrameGroup(["facing_portcullis_open", "blank", "blank"], True),
    FrameGroupEnum.BRIDGE: FrameGroup(["blank", "left_bridge", "right_bridge"], True),
    FrameGroupEnum.CEILING_TRAPDOOR_CLOSED: FrameGroup(["ceiling_trapdoor_closed", "blank", "blank"], False),
    FrameGroupEnum.CEILING_TRAPDOOR_OPEN: FrameGroup(["ceiling_trapdoor_open", "blank", "blank"], True),
    FrameGroupEnum.FLOOR_TRAPDOOR_CLOSED: FrameGroup(["floor_trapdoor_closed", "blank", "blank"], False),
    FrameGroupEnum.FLOOR_TRAPDOOR_OPEN: FrameGroup(["floor_trapdoor_open", "blank", "blank"], True),
    FrameGroupEnum.DECO_TORCH: FrameGroup(["facing_deco_torch", "left_deco_torch", "right_deco_torch"], True),
}


frame_items = {
    FrameItemEnum.CEILING_BLANK: FrameItem("ceiling_blank"),
    FrameItemEnum.CEILING_OUTSIDE: FrameItem("ceiling_outdoors"),
    FrameItemEnum.FLOOR_BLANK: FrameItem("floor_blank"),
    FrameItemEnum.FLOOR_WOOD: FrameItem("floor_wood"),
    FrameItemEnum.TREASURE: FrameItem("treasure"),
    FrameItemEnum.RAT: FrameItem("rat"),
    FrameItemEnum.SPIDER: FrameItem("spider"),
    FrameItemEnum.SKELETON: FrameItem("skeleton"),
}


# vim: set tabstop=2 shiftwidth=2 expandtab:
