# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

from enum import (IntEnum)


FRAME_HEIGHT = 24
FRAME_WIDTH = 26


def CopyLine(line1, line2):
  lenLine = len(line1)
  for x in range(len(line2)):
    if x > lenLine:
      break
    line1[x] = line2[x]


def MergeLine(line1, line2):
  lenLine = len(line1)
  for x in range(len(line2)):
    if x > lenLine:
      break
    if line1[x] == " ":
      line1[x] = line2[x]


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
  def __init__(self, filepaths):
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

  def Copy(self, fp):
    for l in range(len(fp._framePart)):
      if l < self._frameLines:
        CopyLine(self._frame[l], fp._framePart[l])

  def Merge(self, fp):
    for l in range(len(fp._framePart)):
      if l < self._frameLines:
        MergeLine(self._frame[l], fp._framePart[l])

  def Render(self, cm, facing_caption):
    cm.ClearHud()
    cm.PrintHud("FACING: %s" % (facing_caption))
    cm.PrintHud("+--------------------------+")
    for line in self._frame:
      cm.PrintHud("|", end="")
      for c in line:
        if c == "#":
          cm.PrintHud(" ", end="")
        else:
          cm.PrintHud(c, end="")
      cm.PrintHud("|")
    cm.PrintHud("+--------------------------+")


class FrameGroupEnum(IntEnum):
  NO_WALL = 0
  WALL = 1
  ARCHWAY = 2
  DOOR = 3


class FrameItemEnum(IntEnum):
  NONE = 0
  TREASURE = 1


frame_groups = {
    FrameGroupEnum.NO_WALL: FrameGroup(["facing_no_wall", "left_no_wall", "right_no_wall"]),
    FrameGroupEnum.WALL: FrameGroup(["facing_wall", "left_wall", "right_wall"]),
    FrameGroupEnum.ARCHWAY: FrameGroup(["facing_archway", "left_archway", "right_archway"]),
}


frame_items = {
    FrameItemEnum.TREASURE: FrameItem("treasure"),
}


# vim: set tabstop=2 shiftwidth=2 expandtab:
