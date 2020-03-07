# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

from enum import (IntEnum)

from logger import (logd, loge)


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
  WALL = 1
  ARCHWAY = 10
  DOOR_CLOSED = 20
  DOOR_OPEN = 21
  DBL_DOOR_CLOSED = 22
  DBL_DOOR_OPEN = 23


class FrameItemEnum(IntEnum):
  NONE = 0
  TREASURE = 1


frame_groups = {
    FrameGroupEnum.WALL: FrameGroup(["facing_wall", "left_wall", "right_wall"], False),
    FrameGroupEnum.ARCHWAY: FrameGroup(["facing_archway", "left_archway", "right_archway"]),
    FrameGroupEnum.DOOR_CLOSED: FrameGroup(["facing_door_closed", "left_door_closed", "right_door_closed"], False),
    FrameGroupEnum.DOOR_OPEN: FrameGroup(["facing_door_open", "left_door_open", "right_door_open"], True),
    FrameGroupEnum.DBL_DOOR_CLOSED: FrameGroup(["facing_dbl_door_closed", "left_dbl_door_closed", "right_dbl_door_closed"], False),
    FrameGroupEnum.DBL_DOOR_OPEN: FrameGroup(["facing_dbl_door_open", "left_dbl_door_open", "right_dbl_door_open"], True),
}


frame_items = {
    FrameItemEnum.TREASURE: FrameItem("treasure"),
}


# vim: set tabstop=2 shiftwidth=2 expandtab:
