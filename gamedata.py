# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Global Game Data

from console import ANSI


PERIODIC_TRIGGERED = 1 << 15


class GameData:
  _console = None
  _doors = None
  _rooms = None
  _items = None
  _quests = None
  _persons = None
  _player = None
  _NextRoomEvent = 0

  ROOM_START = 0
  ROOM_RESPAWN = 0

  @staticmethod
  def SetConsole(console):
    GameData._console = console

  @staticmethod
  def GetConsole():
    return GameData._console

  @staticmethod
  def SetItems(items):
    GameData._items = items

  @staticmethod
  def GetItems():
    return GameData._items

  @staticmethod
  def SetPersons(persons):
    GameData._persons = persons

  @staticmethod
  def GetPersons():
    return GameData._persons

  @staticmethod
  def SetDoors(doors):
    GameData._doors = doors

  @staticmethod
  def GetDoors():
    return GameData._doors

  @staticmethod
  def SetRooms(rooms):
    GameData._rooms = rooms

  @staticmethod
  def GetRooms():
    return GameData._rooms

  @staticmethod
  def SetPlayer(player):
    GameData._player = player

  @staticmethod
  def GetPlayer():
    return GameData._player

  @staticmethod
  def SetQuests(quests):
    GameData._quests = quests

  @staticmethod
  def GetQuests():
    return GameData._quests

  @staticmethod
  def ResetPersonTriggers():
    rooms = GameData.GetRooms()
    for room_id, r in rooms.items():
      for p in r.Persons:
        p.Flags &= ~PERIODIC_TRIGGERED

  @staticmethod
  def ProcessEvents(processTime, processWeather,
                    processConditions, processTriggers):
    rooms = GameData.GetRooms()
    player = GameData.GetPlayer()
    # Check for time updates
    processTime()
    processWeather()
    # Check for room events
    seconds = player.PlayerTime()
    GameData.ResetPersonTriggers()
    if GameData._NextRoomEvent < seconds:
      # Set NextRoomEvent max 10mins
      GameData._NextRoomEvent = seconds + (10 * 60)
      for room_id, r in rooms.items():
        if rooms[player.Room].Zone != r.Zone:
          continue
        if rooms[room_id].Periodics is not None:
          for per in rooms[room_id].Periodics:
            next = per.LastCheck + per.DelaySeconds
            if next >= seconds:
              if GameData._NextRoomEvent > next:
                GameData._NextRoomEvent = next
              continue
            per.LastCheck = seconds
            if GameData._NextRoomEvent > seconds + per.DelaySeconds:
              GameData._NextRoomEvent = seconds + per.DelaySeconds
            if processConditions(room_id, rooms[room_id], per.Conditions):
              if per.Triggers is not None:
                if processTriggers(room_id, per.Triggers) == False:
                  break
        if rooms[room_id].Persons is not None:
          for npc in rooms[room_id].Persons:
            if npc.Periodics is not None:
              if npc.Flags & PERIODIC_TRIGGERED > 0:
                continue
              npc.Flags |= PERIODIC_TRIGGERED
              for per in npc.Periodics:
                next = per.LastCheck + per.DelaySeconds
                if next >= seconds:
                  if GameData._NextRoomEvent > next:
                    GameData._NextRoomEvent = next
                  continue
                per.LastCheck = seconds
                if GameData._NextRoomEvent > seconds + per.DelaySeconds:
                  GameData._NextRoomEvent = seconds + per.DelaySeconds
                if processConditions(room_id, npc, per.Conditions):
                  if per.Triggers is not None:
                    if processTriggers(npc, per.Triggers) == False:
                      break

  @staticmethod
  def ProcessRoomCombat():
    cm = GameData.GetConsole()
    player = GameData.GetPlayer()
    rooms = GameData.GetRooms()
    enemies = []

    # Check if the room persons need to attack
    count = 0
    for x in rooms[player.Room].Persons:
      if x.IsAggressive():
        count += 1
        if count == 1:
          cm.Print("")
        enemies.append(x)
        cm.Print("%s%s attacks you!%s" %
                 (ANSI.TEXT_BOLD, x.Name.capitalize(),
                  ANSI.TEXT_NORMAL))
      if player.CombatTarget is not None:
        if player.CombatTarget == x.UUID:
          enemies.append(x)
          player.CombatTarget = None
    return enemies

# vim: tabstop=2 shiftwidth=2 expandtab:
