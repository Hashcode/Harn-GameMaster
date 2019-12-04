# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

import pickle
import codecs
import requests
import re

from hashlib import sha256

# from simplecrypt import encrypt, decrypt

URL_BASE = "https://www.jsonstore.io"
DB_UUID = "f4dd28e6f701809382924215197653375ae7bfeedadc1485196e72697392bc2c"


global_use_encrypt = False


def get_valid_filename(s):
  s = str(s).strip().replace(' ', '_')
  return re.sub(r'(?u)[^-\w.]', '', s)


def get_char_url(name, password):
  m = sha256()
  m.update(name.upper().encode('utf-8'))
  m.update(password.upper().encode('utf-8'))
  url = "%s/%s/%s" % (URL_BASE, DB_UUID, m.digest().hex())
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
    return False
  return False


def SaveDB(name, password, info, state):
  payload = {'state': state}
  try:
    r = requests.put(get_char_url(name, password), json=payload)
    if r.status_code in [200, 201]:
      return True
  except:
    return False


def LoadDB(name, password, legacy=False):
  if legacy:
    r = requests.get("%s/%s/%s" % (URL_BASE, DB_UUID,
                                   get_valid_filename(name.upper())))
  else:
    r = requests.get(get_char_url(name, password))
  try:
    record = r.json()
    if record["result"] is not None:
      payload = record["result"]
      return payload["state"]
  finally:
    return ""


def SavePlayer(save_obj, info, password):
  state_bytes = pickle.dumps(save_obj)
  if global_use_encrypt:
    enc_state_bytes = encrypt(password, state_bytes)
    state_str = codecs.encode(enc_state_bytes, "base64").decode("utf-8")
  else:
    state_str = codecs.encode(state_bytes, "base64").decode("utf-8")
  return SaveDB(save_obj.Name, password, info, state_str)


def LoadPlayer(player, name, password, legacy=False):
  state_str = LoadDB(name, password, legacy)
  print(state_str)
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
