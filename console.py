# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Console Handler

import sys
import atexit
import termios

from select import select
from threading import Thread, Event
from queue import Queue


class ConsoleManager(Thread):
  CLEAR_LINE = "\x1B[1K"

  def __init__(self, prompt=">$", line_length=60):
    super().__init__()
    self.daemon = True
    self.fd = sys.stdin.fileno()
    self.out = sys.stdout
    self.new_term = termios.tcgetattr(self.fd)
    self.old_term = termios.tcgetattr(self.fd)
    self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
    self._in_queue = Queue()
    self.cur_input = ""
    self._echoed = Event()
    self._prompt = prompt
    self._interrupted = 0
    self._prompted = False
    self.line_length = line_length
    atexit.register(self.SetNormalTerm)

  def SetNormalTerm(self):
    termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

  def SetPrompt(self, prompt):
    self._prompt = prompt

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
    while True:
      self.out.write("\n%s %s" % (self._prompt, self.cur_input))
      self.out.flush()
      self._prompted = True
      termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)
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
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)
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
          elif ord(c) >= 32 and ord(c) <= 126:
            if len(self.cur_input) <= self.line_length:
              self.cur_input += "%c" % c
              if self._interrupted == 0:
                self.PrintCH("%c" % c)
            else:
              self.Bell()
          else:
            self.Bell()

  def Poll(self):
    if not self._in_queue.empty():
      return self._in_queue.get()
    return None

  def Next(self):
    self._echoed.set()

# vim: tabstop=2 shiftwidth=2 expandtab:
