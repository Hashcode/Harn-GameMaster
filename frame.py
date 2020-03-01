# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

from enum import (IntEnum)

from console import (ANSI)


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


class Frame:
  FRAME_HEIGHT = 24
  FRAME_WIDTH = 26
  FRAME_LOC = "frames"

  def __init__(self, filename=None):
    self._frame = []
    self._frameLines = 0
    if filename is not None:
      with open(filename, "r") as f:
        for line in f:
          if self._frameLines >= Frame.FRAME_HEIGHT:
            break
          self._frame.append([])
          count = 0
          for c in line:
            if count >= Frame.FRAME_WIDTH:
              break
            self._frame[self._frameLines].append(c)
            count += 1
          self._frameLines += 1
    else:
      for line in range(Frame.FRAME_HEIGHT):
        self._frame.append([])
        for c in range(Frame.FRAME_WIDTH):
          self._frame[self._frameLines].append(chr(32))
        self._frameLines += 1

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

  def Copy(self, f):
    for l in range(len(f._frame)):
      if l < self._frameLines:
        CopyLine(self._frame[l], f._frame[l])

  def Merge(self, f):
    for l in range(len(f._frame)):
      if l < self._frameLines:
        MergeLine(self._frame[l], f._frame[l])


class FrameEnum(IntEnum):
  BLANK = 0
  FACING_1_WALL = 10
  LEFT_1_WALL = 12
  LEFT_1_NO_WALL = 13
  RIGHT_1_WALL = 14
  RIGHT_1_NO_WALL = 15
  FACING_2_WALL = 20
  LEFT_2_WALL = 22
  LEFT_2_NO_WALL = 23
  RIGHT_2_WALL = 24
  RIGHT_2_NO_WALL = 25
  FACING_3_WALL = 30
  FACING_3_NO_WALL = 31
  LEFT_3_WALL = 32
  LEFT_3_NO_WALL = 33
  RIGHT_3_WALL = 34
  RIGHT_3_NO_WALL = 35
  # MISC
  TREASURE_1 = 100
  TREASURE_2 = 101
  TREASURE_3 = 102


frame_parts = {
    FrameEnum.BLANK: Frame("%s/blank.txt" % (Frame.FRAME_LOC)),
    FrameEnum.FACING_1_WALL: Frame("%s/facing_1_wall.txt" % (Frame.FRAME_LOC)),
    FrameEnum.LEFT_1_WALL: Frame("%s/left_1_wall.txt" % (Frame.FRAME_LOC)),
    FrameEnum.LEFT_1_NO_WALL: Frame("%s/left_1_no_wall.txt" % (Frame.FRAME_LOC)),
    FrameEnum.RIGHT_1_WALL: Frame("%s/right_1_wall.txt" % (Frame.FRAME_LOC)),
    FrameEnum.RIGHT_1_NO_WALL: Frame("%s/right_1_no_wall.txt" % (Frame.FRAME_LOC)),
    FrameEnum.FACING_2_WALL: Frame("%s/facing_2_wall.txt" % (Frame.FRAME_LOC)),
    FrameEnum.LEFT_2_WALL: Frame("%s/left_2_wall.txt" % (Frame.FRAME_LOC)),
    FrameEnum.LEFT_2_NO_WALL: Frame("%s/left_2_no_wall.txt" % (Frame.FRAME_LOC)),
    FrameEnum.RIGHT_2_WALL: Frame("%s/right_2_wall.txt" % (Frame.FRAME_LOC)),
    FrameEnum.RIGHT_2_NO_WALL: Frame("%s/right_2_no_wall.txt" % (Frame.FRAME_LOC)),
    FrameEnum.FACING_3_WALL: Frame("%s/facing_3_wall.txt" % (Frame.FRAME_LOC)),
    FrameEnum.FACING_3_NO_WALL: Frame("%s/facing_3_no_wall.txt" % (Frame.FRAME_LOC)),
    FrameEnum.LEFT_3_WALL: Frame("%s/left_3_wall.txt" % (Frame.FRAME_LOC)),
    FrameEnum.LEFT_3_NO_WALL: Frame("%s/left_3_no_wall.txt" % (Frame.FRAME_LOC)),
    FrameEnum.RIGHT_3_WALL: Frame("%s/right_3_wall.txt" % (Frame.FRAME_LOC)),
    FrameEnum.RIGHT_3_NO_WALL: Frame("%s/right_3_no_wall.txt" % (Frame.FRAME_LOC)),
    FrameEnum.TREASURE_1: Frame("%s/treasure_1.txt" % (Frame.FRAME_LOC)),
    FrameEnum.TREASURE_2: Frame("%s/treasure_2.txt" % (Frame.FRAME_LOC)),
    FrameEnum.TREASURE_3: Frame("%s/treasure_3.txt" % (Frame.FRAME_LOC)),
}

# vim: set tabstop=2 shiftwidth=2 expandtab:
