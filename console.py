# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Console Handler

import sys
import curses

from enum import IntEnum
from queue import Queue
from select import select
from threading import Thread, Event
from time import (sleep, time)


MIN_WIDTH = 75


# FORMATTING

class TEXT_COLOR:
  NORMAL = 0
  BLACK = 1
  RED = 2
  GREEN = 3
  YELLOW = 4
  BLUE = 5
  PURPLE = 6
  CYAN = 7
  BRIGHT_WHITE = 8
  BRIGHT_BLACK = 9
  BRIGHT_RED = 10
  BRIGHT_GREEN = 11
  BRIGHT_YELLOW = 12
  BRIGHT_BLUE = 13
  BRIGHT_PURPLE = 14
  BRIGHT_CYAN = 15


class ANSI:
  TEXT_NORMAL = 0
  TEXT_BOLD = curses.A_BOLD
  TEXT_REVERSE = curses.A_REVERSE
  TEXT_BLINK = curses.A_BLINK


class InputFlag(IntEnum):
  NUMERIC = 1 << 1
  UPPERCASE = 1 << 2
  PASSWORD = 1 << 3


class ConsoleManager(Thread):
  def __init__(self, prompt="[]:", line_length=60, input_flags=0):
    super().__init__()
    self.daemon = True
    self.cur_input = ""
    self._in_queue = Queue()
    self._echoed = Event()
    self._prompt = prompt
    self._input_flags = input_flags
    self._interrupted = 0
    self._prompted = False
    self._line_length = line_length

  def ColorPair(self, color_enum):
    return curses.color_pair(color_enum)

  def StartScreen(self, stdscr):
    self.screen = stdscr
    curses.noecho()
    curses.cbreak()
    curses.nonl()
    self.screen.erase()
    self.screen.scrollok(True)
    self.screen.idlok(True)
    self.screen.keypad(True)
    self.screen.nodelay(True)
    curses.curs_set(0)
    curses.mousemask(True)
    (self.screenY, self.screenX) = self.screen.getmaxyx()

    self.window = self.screen.subwin(self.screenY, MIN_WIDTH - 1, 0, 0)
    self.window.scrollok(True)
    self.hud = self.screen.subwin(28, 30, 0, MIN_WIDTH)
    self.hud.scrollok(True)

    curses.start_color()
    curses.use_default_colors()
    for i in range(0, 16):
      curses.init_pair(i + 1, i, -1)

  def ClearWindow(self):
    self.window.erase()
    self.window.move(0, 0)

  def ClearHud(self):
    self.hud.erase()
    self.hud.move(0, 0)

  def SetPrompt(self, prompt):
    self._prompt = prompt

  def SetLineLength(self, line_length):
    self._line_length = line_length

  def SetInputFlags(self, input_flags):
    self._input_flags = input_flags

  def PrintCH(self, char):
    self.window.addch(char)
    self.window.refresh()

  def Print(self, msg, attr=0, end="\n"):
    if self._prompted:
      (Y, X) = self.window.getyx()
      self.window.move(Y, 0)
      self.window.clrtoeol()
      self.window.move(Y, 0)
      self._prompted = False
    self.window.addstr("%s%s" % (msg, end), attr)
    self.window.refresh()
    self._interrupted = 1

  def PrintHud(self, msg, attr=0, end="\n"):
    self.hud.addstr("%s%s" % (msg, end), attr)
    self.hud.refresh()

  def Bell(self):
    curses.beep()

  def run(self):
    self._echoed.wait()
    self._echoed.clear()
    while True:
      self.window.addstr("\n%s %s" % (self._prompt, self.cur_input))
      self.window.refresh()
      self._prompted = True
      self._interrupted = 0
      while self._interrupted == 0:
        dr, dw, de = select([sys.stdin, self._interrupted], [], [], 1)
        c = self.screen.getch()
        if c > -1:
          if c in {curses.KEY_ENTER, 10, 13}:
            self._in_queue.put(self.cur_input)
            self.cur_input = ""
            self._prompted = False
            if self._interrupted == 0:
              self.PrintCH("\n")
            self._interrupted = 1
            self._echoed.wait()
            self._echoed.clear()
          elif c == curses.KEY_UP:
            self._in_queue.put("arrow_up")
            self._interrupted = 1
            self._echoed.wait()
            self._echoed.clear()
          elif c == curses.KEY_DOWN:
            self._in_queue.put("arrow_down")
            self._interrupted = 1
            self._echoed.wait()
            self._echoed.clear()
          elif c == curses.KEY_RIGHT:
            self._in_queue.put("arrow_right")
            self._interrupted = 1
            self._echoed.wait()
            self._echoed.clear()
          elif c == curses.KEY_LEFT:
            self._in_queue.put("arrow_left")
            self._interrupted = 1
            self._echoed.wait()
            self._echoed.clear()
          elif c == curses.KEY_MOUSE:
            pass
          elif c == curses.KEY_RESIZE:
            (self.screenY, self.screenX) = self.screen.getmaxyx()
          elif c == curses.KEY_DC or c == curses.KEY_BACKSPACE or c == 127:
            if len(self.cur_input) > 0:
              self.cur_input = self.cur_input[:-1]
              self.window.addstr("\b \b")
              self.window.refresh()
            else:
              self.Bell()
          else:
            if len(self.cur_input) > self._line_length:
              self.Bell()
              continue
            if self._input_flags & InputFlag.NUMERIC == 0:
              if c >= 32 and c <= 126:
                if self._input_flags & InputFlag.UPPERCASE > 0:
                  c = ord(("%s" % chr(c)).upper())
                self.cur_input += "%c" % chr(c)
                if self._interrupted == 0:
                  if self._input_flags & InputFlag.PASSWORD > 0:
                    self.PrintCH("*")
                  else:
                    self.PrintCH("%c" % chr(c))
                continue
            else:
              if c >= 48 and c <= 57:
                self.cur_input += "%c" % chr(c)
                if self._interrupted == 0:
                  self.PrintCH("%c" % chr(c))
                continue
            self.Bell()

  def Poll(self):
    if not self._in_queue.empty():
      return self._in_queue.get()
    return None

  def Next(self):
    self._echoed.set()

  def Input(self, prompt, line_length=60, input_flags=0,
            timeout=0, timeoutFunc=None):
    self.SetPrompt(prompt)
    self.SetLineLength(line_length)
    self.SetInputFlags(input_flags)
    self.Next()
    t = time()
    while True:
      sleep(.1)
      if not self._in_queue.empty():
        return self._in_queue.get()
      # handle idle
      if timeout > 0 and timeoutFunc is not None:
        if time() - t > timeout:
          timeoutFunc()
          t = time()


# vim: tabstop=2 shiftwidth=2 expandtab:
