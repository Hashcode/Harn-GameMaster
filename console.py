# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Console Handler

import atexit
import sys
import termios

from enum import IntEnum
from queue import Queue
from select import select
from threading import Thread, Event
from time import (sleep, time)


class InputFlag(IntEnum):
  NUMERIC = 1 << 1
  UPPERCASE = 1 << 2
  PASSWORD = 1 << 3


class ConsoleManager(Thread):
  CLEAR_LINE = "\x1B[1K"

  def __init__(self, prompt="[]:", line_length=60, input_flags=0):
    super().__init__()
    self.daemon = True
    self.fd = sys.stdin.fileno()
    self.out = sys.stdout
    self.new_term = termios.tcgetattr(self.fd)
    self.old_term = termios.tcgetattr(self.fd)
    self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
    self.cur_input = ""
    self._in_queue = Queue()
    self._echoed = Event()
    self._prompt = prompt
    self._input_flags = input_flags
    self._interrupted = 0
    self._prompted = False
    self._line_length = line_length
    atexit.register(self.SetNormalTerm)

  def SetNormalTerm(self):
    termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

  def SetRawTerm(self):
    termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

  def SetPrompt(self, prompt):
    self._prompt = prompt

  def SetLineLength(self, line_length):
    self._line_length = line_length

  def SetInputFlags(self, input_flags):
    self._input_flags = input_flags

  def PrintCH(self, char):
    self.out.write(char)
    self.out.flush()

  def Print(self, msg, end="\n"):
    if self._prompted:
      self.out.write("%s" % (ConsoleManager.CLEAR_LINE))
      self.out.write("\x1B[%dD" %
                     (len(self._prompt) + len(self.cur_input) + 1))
      self._prompted = False
    self.out.write("%s%s" % (msg, end))
    self._interrupted = 1

  def Bell(self):
    self.PrintCH("\a")

  def run(self):
    self._echoed.wait()
    self._echoed.clear()
    self.SetRawTerm()
    while True:
      self.out.write("\n%s %s" % (self._prompt, self.cur_input))
      self.out.flush()
      self._prompted = True
      self._interrupted = 0
      while self._interrupted == 0:
        dr, dw, de = select([sys.stdin, self._interrupted], [], [], 1)
        if sys.stdin in dr:
          c = sys.stdin.read(1)
          if ord(c) in {10, 13}:
            self._in_queue.put(self.cur_input)
            self.cur_input = ""
            self._prompted = False
            if self._interrupted == 0:
              self.PrintCH("\n")
            self._interrupted = 1
            self._echoed.wait()
            self._echoed.clear()
          elif ord(c) == 27:
            # TODO: handle escape codes
            self.Bell()
          elif ord(c) == 127:
            if len(self.cur_input) > 0:
              self.cur_input = self.cur_input[:-1]
              self.out.write("\b \b")
              self.out.flush()
            else:
              self.Bell()
          else:
            if len(self.cur_input) > self._line_length:
              self.Bell()
              continue
            if self._input_flags & InputFlag.NUMERIC == 0:
              if ord(c) >= 32 and ord(c) <= 126:
                if self._input_flags & InputFlag.UPPERCASE > 0:
                  c = c.upper()
                self.cur_input += "%c" % c
                if self._interrupted == 0:
                  if self._input_flags & InputFlag.PASSWORD > 0:
                    self.PrintCH("*")
                  else:
                    self.PrintCH("%c" % c)
                continue
            else:
              if ord(c) >= 48 and ord(c) <= 57:
                self.cur_input += "%c" % c
                if self._interrupted == 0:
                  self.PrintCH("%c" % c)
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
