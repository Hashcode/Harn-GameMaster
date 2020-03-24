# Copyright (c) 2019-2020 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Global Game Data

from console import ANSI


PERIODIC_TRIGGERED = 1 << 15


class GameData:
  _console = None
  _doors = None
  _rooms = None
  _quests = None
  _persons = None
  _player = None
  _NextRoomEvent = 0
  _processConditions = None
  _processTriggers = None
  _processTime = None
  _processWeather = None

  ROOM_START = 0
  ROOM_RESPAWN = 0

  @staticmethod
  def SetConsole(console):
    GameData._console = console

  @staticmethod
  def GetConsole():
    return GameData._console

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
  def SetProcessConditions(processConditions):
    GameData._processConditions = processConditions

  @staticmethod
  def SetProcessTriggers(processTriggers):
    GameData._processTriggers = processTriggers

  @staticmethod
  def SetProcessTime(processTime):
    GameData._processTime = processTime

  @staticmethod
  def SetProcessWeather(processWeather):
    GameData._processWeather = processWeather

  @staticmethod
  def ResetPersonTriggers():
    rooms = GameData.GetRooms()
    for room_id, r in rooms.items():
      for p in r.Persons:
        p.Flags &= ~PERIODIC_TRIGGERED

  @staticmethod
  def InitializeRooms():
    rooms = GameData.GetRooms()
    for r in rooms.values():
      r.Initialize(GameData._processConditions, GameData._processTriggers)

  @staticmethod
  def ProcessEvents(first=False):
    rooms = GameData.GetRooms()
    player = GameData.GetPlayer()
    # Check for time updates
    GameData._processTime()
    GameData._processWeather()
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
            if not first and next >= seconds:
              if GameData._NextRoomEvent > next:
                GameData._NextRoomEvent = next
              continue
            per.LastCheck = seconds
            if GameData._NextRoomEvent > seconds + per.DelaySeconds:
              GameData._NextRoomEvent = seconds + per.DelaySeconds
            if GameData._processConditions(room_id, rooms[room_id], per.Conditions):
              if per.Triggers is not None:
                if GameData._processTriggers(room_id, per.Triggers) is False:
                  break
        if rooms[room_id].Persons is not None:
          for npc in rooms[room_id].Persons:
            if npc.Periodics is not None:
              if npc.Flags & PERIODIC_TRIGGERED > 0:
                continue
              npc.Flags |= PERIODIC_TRIGGERED
              for per in npc.Periodics:
                next = per.LastCheck + per.DelaySeconds
                if not first and next >= seconds:
                  if not first and GameData._NextRoomEvent > next:
                    GameData._NextRoomEvent = next
                  continue
                per.LastCheck = seconds
                if GameData._NextRoomEvent > seconds + per.DelaySeconds:
                  GameData._NextRoomEvent = seconds + per.DelaySeconds
                if GameData._processConditions(room_id, npc, per.Conditions):
                  if per.Triggers is not None:
                    if GameData._processTriggers(npc, per.Triggers) is False:
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
        cm.Print("%s attacks you!" % (x.Name.capitalize()), attr=ANSI.TEXT_BOLD)
      if player.CombatTarget is not None:
        if player.CombatTarget == x.UUID:
          enemies.append(x)
          player.CombatTarget = None
    return enemies

# vim: tabstop=2 shiftwidth=2 expandtab:
