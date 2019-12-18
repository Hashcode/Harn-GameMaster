# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

import pickle
import codecs
import requests
import re
import json

from hashlib import sha256

from gamedata import GameData
from logger import logd

# from simplecrypt import encrypt, decrypt

URL_BASE = "https://www.jsonstore.io"
DB_UUID = "e4cf4dfd5c61f35b78a0c07a01a3c1ca00d8cb3b98345829336c40caf4753183"
STATS_FILE = "stats"


global_use_encrypt = False


def get_valid_filename(s):
  s = str(s).strip().replace(' ', '_')
  return re.sub(r'(?u)[^-\w.]', '', s)


def get_char_url(name, password):
  m = sha256()
  m.update(name.upper().encode('utf-8'))
  m.update(password.encode('utf-8'))
  url = "%s/%s/%s" % (URL_BASE, DB_UUID, m.digest().hex())
  logd("URL=%s" % url)
  return url


def ExistsDB(name, password):
  r = requests.get(get_char_url(name, password))
  if r.status_code != 200:
    return False
  try:
    dict = r.json()
    if dict["result"] is not None:
      return True
  except:
    pass
  return False


def SaveDB(name, password, state):
  payload = {'state': state}
  try:
    r = requests.put(get_char_url(name, password), json=payload)
    if r.status_code in [200, 201]:
      return True
  except:
    pass
  return False


def LoadDB(name, password, legacy=False):
  ret = ""
  if legacy:
    r = requests.get("%s/%s/%s" % (URL_BASE, DB_UUID,
                                   get_valid_filename(name.upper())))
  else:
    r = requests.get(get_char_url(name, password))
  try:
    record = r.json()
    if record["result"] is not None:
      payload = record["result"]
      ret = payload["state"]
  except:
    GameData.GetConsole().Print("An error occurred during character load")
  return ret


# STATS structure

def LoadStatsDB():
  players = {}
  url = "%s/%s/%s" % (URL_BASE, DB_UUID, STATS_FILE)
  r = requests.get(url)
  try:
    record = r.json()
    if record["result"] is not None:
      players = json.loads(record["result"])
  finally:
    return players


def SaveStatsDB(name, played, info, score):
  url = "%s/%s/%s" % (URL_BASE, DB_UUID, STATS_FILE)
  name = name.upper()
  players = LoadStatsDB()
  players.update({name: {"played": played, "info": info, "score": score}})
  try:
    r = requests.put(url, json=json.dumps(players, indent=4))
    if r.status_code in [200, 201]:
      return True
  except:
    pass
  return False


def SavePlayer(save_obj, info, password):
  password = password.upper()
  state_bytes = pickle.dumps(save_obj)
  if global_use_encrypt:
    enc_state_bytes = encrypt(password, state_bytes)
    state_str = codecs.encode(enc_state_bytes, "base64").decode("utf-8")
  else:
    state_str = codecs.encode(state_bytes, "base64").decode("utf-8")
  if SaveDB(save_obj.Name, password, state_str):
    return SaveStatsDB(save_obj.Name, int(save_obj.SecondsPlayed / 86400),
                       info, 0)
  return False


def LoadPlayer(player, name, password, legacy=False):
  password = password.upper()
  state_str = LoadDB(name, password, legacy)
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
  player.Password = password
  return True

# vim: set tabstop=2 shiftwidth=2 expandtab:
