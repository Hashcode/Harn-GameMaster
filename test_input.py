# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

import random

from console import ConsoleManager

cm = ConsoleManager()
cm.start()

def promptTimeout():
  if random.randint(1, 100) < 50:
    cm.Print("Interrupt!")

def Loop():
  while True:
    x = cm.Input(">:", timeout=5, timeoutFunc=promptTimeout).lower()
    if x != "":
      cm.Print("ECHO: %s" % x)
      if x == "done":
        return
      cm.Next()


if __name__ == '__main__':
  Loop()

cm.SetNormalTerm()

# vim: set tabstop=2 shiftwidth=2 expandtab:
