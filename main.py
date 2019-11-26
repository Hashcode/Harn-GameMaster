# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Game System:
# Based on "HârnMaster Third Edition"
# Copyright (c) 1986 - 2003 N. Robin Crossby & Columbia Games, Inc.
# By N. Robin Crossby and Tom Dalgliesh

# Adventure Setting:
# Based on "The Keep on the Borderlands"
# Copyright (c) 1980, 1981 - TSR Hobbies, Inc.
# By Gary Gygax

# Main setup

from random import seed
from time import gmtime
from calendar import timegm

from global_defines import (logd, DiceRoll, ItemEnum, ItemLink, Player,
                            RoomEnum, RoomFuncResponse, ANSI)
from utils import (printRoomDescription, printRoomObjects, prompt)
from rooms import rooms
from person import persons
from combat import combat

TestMode = True

ROOM_RESPAWN = RoomEnum.BL_PRIEST_CHAMBER

seed()
print(ANSI.CLEAR + ANSI.RESET_CURSOR, end='')

player = Player("Unknown")
player.SetRoom(RoomEnum.GAME_START)

if TestMode:
  player.AddItem(ItemEnum.WEAPON_DAGGER, ItemLink(1, equip=True))
  player.AddItem(ItemEnum.WEAPON_CLUB, ItemLink(1))
  player.AddItem(ItemEnum.SHIELD_BUCKLER_BANDED, ItemLink(1, equip=True))

  player.AddItem(ItemEnum.ARMOR_TUNIC_CLOTH, ItemLink(1, equip=True))
  player.AddItem(ItemEnum.ARMOR_LEGGINGS_CLOTH, ItemLink(1, equip=True))

  player.AddItem(ItemEnum.ARMOR_HALFHELM_LEATHER_RING, ItemLink(1, equip=True))
  player.AddItem(ItemEnum.ARMOR_HAUBERK_LEATHER_RING, ItemLink(1, equip=True))
  player.AddItem(ItemEnum.ARMOR_LEGGINGS_LEATHER_RING, ItemLink(1, equip=True))
  player.AddItem(ItemEnum.ARMOR_GAUNTLETS_LEATHER_RING, ItemLink(1,
                                                                 equip=True))
  player.AddItem(ItemEnum.ARMOR_SHOES_LEATHER, ItemLink(1, equip=True))

  player.AddItem(ItemEnum.RING_ATTACK_SILVER, ItemLink(1, equip=True))
  player.AddItem(ItemEnum.MISC_STONE, ItemLink(2))

NextRoomEvent = 0

while True:
  enemies = []
  res = RoomFuncResponse.NONE
  printRoomDescription(player.Room, rooms)

  # Call Room Function
  if rooms[player.Room].Function is not None:
    # Return value means: True == Print Prompt, False == Skip Prompt
    res = rooms[player.Room].Function(player)

  if res == RoomFuncResponse.SKIP:
    continue

  # Check for room spawns
  seconds = timegm(gmtime())
  if NextRoomEvent < seconds:
    logd("RoomEvents check")
    # Set NextRoomEvent max 10mins
    NextRoomEvent = seconds + (10 * 60)
    for r in rooms:
      if rooms[r].Spawns is None:
        continue
      for s in rooms[r].Spawns:
        if s.LastSpawnCheck + s.SpawnDelaySeconds >= seconds:
          if NextRoomEvent > s.LastSpawnCheck + s.SpawnDelaySeconds:
            NextRoomEvent = s.LastSpawnCheck + s.SpawnDelaySeconds
            logd("Next RoomEvents check in %d seconds" %
                 (NextRoomEvent - seconds))
          continue
        s.LastSpawnCheck = seconds
        if NextRoomEvent > seconds + s.SpawnDelaySeconds:
          NextRoomEvent = seconds + s.SpawnDelaySeconds
          logd("Next RoomEvents check in %d seconds" %
               (NextRoomEvent - seconds))
        count = 0
        for p in rooms[r].Persons:
          if p.PersonID == s.Person:
            count += 1
        if count < s.MaxQuantity:
          logd("SpawnCheck [%s] in %s [<=%d]" % (persons[s.Person].Name,
                                                 rooms[r].Title, s.Chance))
          if DiceRoll(1, 100).Result() <= s.Chance:
            rooms[r].AddPerson(s.Person, persons)

  printRoomObjects(player.Room, rooms)

  # Check if the room persons need to attack
  count = 0
  for x in rooms[player.Room].Persons:
    if x.IsAggressive():
      count += 1
      if count == 1:
        print("")
      enemies.append(x)
      print("%s%s attacks you!%s" %
            (ANSI.TEXT_BOLD, x.Name.capitalize(),
             ANSI.TEXT_NORMAL))
    if player.CombatTarget is not None:
      if player.CombatTarget == x.UUID:
        print("\nYou attack %s!" % x.Name)
        enemies.append(x)
        player.CombatTarget = None

  if len(enemies) > 0:
    combat(player, enemies)
    continue

  # Handle Commands
  if res != RoomFuncResponse.NO_PROMPT:
    prompt(player, rooms)
    if player.Command != "":
      print("\n%sYou cannot do that here.%s" %
            (ANSI.TEXT_BOLD, ANSI.TEXT_NORMAL))

# vim: set tabstop=2 shiftwidth=2 expandtab:
