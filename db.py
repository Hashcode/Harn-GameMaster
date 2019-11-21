# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

import pickle
import codecs

from tinydb import TinyDB, Query
from simplecrypt import encrypt, decrypt

DATABASE_FILE = "game.json"

global_db = None
global_id = -1
global_use_encrypt = True


def GetDB():
  global global_db
  global global_id
  if global_db is not None:
    return global_db
  global_db = TinyDB(DATABASE_FILE)
  for row in global_db.all():
    if row["id"] > global_id:
      global_id = row["id"]
  return global_db


def ExistsDB(name):
  return GetDB().contains(Query().name == name.upper())


def DeleteDB(name):
  return GetDB().remove(Query().name == name.upper())


def SaveDB(name, info, state):
  global global_id
  db = GetDB()
  if ExistsDB(name):
    db.update({'info': info, 'state': state}, Query().name == name.upper())
  else:
    global_id += 1
    db.insert({'id': global_id, 'name': name.upper(), 'info': info,
               'state': state})
  return True


def LoadDB(name):
  state = ""
  for row in GetDB().search(Query().name == name.upper()):
    state = row["state"]
    break
  return state


def ListDB():
  players = {}
  for row in GetDB().all():
    players.update({row["name"]: row["info"]})
  return players


def SavePlayer(save_obj, info, password):
  state_bytes = pickle.dumps(save_obj)
  if global_use_encrypt:
    enc_state_bytes = encrypt(password, state_bytes)
    state_str = codecs.encode(enc_state_bytes, "base64").decode("utf-8")
  else:
    state_str = codecs.encode(state_bytes, "base64").decode("utf-8")
  return SaveDB(save_obj.Name, info, state_str)


def LoadPlayer(player, name, password):
  state_str = LoadDB(name)
  if state_str == "":
    return False
  state_bytes = codecs.decode(state_str.encode("utf-8"), "base64")
  if global_use_encrypt:
    try:
      state_bytes = decrypt(password, state_bytes)
    except:
      return False
  p = pickle.loads(state_bytes)
  player.Copy(p)
  return True

# vim: set tabstop=2 shiftwidth=2 expandtab:
