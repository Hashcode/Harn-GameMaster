# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Global Definitions

from array import *
from enum import IntEnum
import pickle
import codecs

# SKILLS

class SkillEnum(IntEnum):
  NONE = 0
  UNARMED = 1
  SHIELD = 2
  DAGGER = 3
  SWORD = 4
  CLUB = 5
  AXE = 6
  FLAIL = 7
  SPEAR = 8
  POLEARM = 9
  NET = 10
  WHIP = 11
  BOW = 12
  BLOWGUN = 13
  SLING = 14

class QualityEnum(IntEnum):
  NONE = 0
  TERRIBLE = 1
  POOR = 2
  INFERIOR = 3
  AVERAGE = 4
  SUPERIOR = 5
  EXCELLENT = 6
  MAGNIFICENT = 7

class ItemQuality:
  def __init__(self, cost_mod):
    self.CostModifier = cost_mod

qualities = {
  QualityEnum.TERRIBLE:   ItemQuality(0.1),
  QualityEnum.POOR:       ItemQuality(0.5),
  QualityEnum.INFERIOR:   ItemQuality(0.75),
  QualityEnum.AVERAGE:    ItemQuality(1),
  QualityEnum.SUPERIOR:   ItemQuality(1.5),
  QualityEnum.EXCELLENT:  ItemQuality(2),
  QualityEnum.MAGNIFICENT:ItemQuality(4),
}

# MATERIALS

class MaterialEnum(IntEnum):
  NONE = 0
  # BASIC
  CLOTH_HAIR = 1
  QUILT_FUR = 2
  LEATHER_HIDE = 3
  KURBUL = 4
  LEATHER_RING = 5
  MAIL = 6
  SCALE = 7
  STEEL = 8
  STEEL_WOOD = 9
  # PRECIOUS
  SILVER = 100
  GOLD = 101
  MITHRIL = 102
  # NATURAL
  WOOD = 200
  STONE = 201
  BONE = 202
  # MAGIC
  DRAGON_HIDE = 300

class Material:
  def __init__(self, weight, cost, store_mod, blunt, edge, pierce, fire = 0, cold = 0, shock = 0, poison = 0, magic = 0):
    self.WeightBase = weight
    self.CostBase = cost
    self.StorageMod = store_mod
    self.ProtBlunt = blunt
    self.ProtEdge = edge
    self.ProtPierce = pierce
    self.ProtFire = fire
    self.ProtCold = cold
    self.ProtShock = shock
    self.ProtPoison = poison
    self.ProtMagic = magic

materials = {
  MaterialEnum.CLOTH_HAIR:    Material(0.1,     2, 0.25, 1,  1, 1, fire=1,  cold=3),
  MaterialEnum.QUILT_FUR:     Material(0.3,     4, 0.5,  5,  3, 2, fire=4,  cold=5),
  MaterialEnum.LEATHER_HIDE:  Material(0.2,     4, 0.75, 2,  4, 3, fire=3,  cold=2),
  MaterialEnum.KURBUL:        Material(0.25,    5, 1,    4,  5, 4, fire=3,  cold=2),
  MaterialEnum.LEATHER_RING:  Material(0.4,     7, 0.75, 3,  6, 4, fire=3,  cold=2),
  MaterialEnum.MAIL:          Material(0.5,    15, 0.5,  2,  8, 5, fire=1,  cold=1),
  MaterialEnum.SCALE:         Material(0.7,    10, 1,    5,  9, 4, fire=5,  cold=2),
  MaterialEnum.STEEL:         Material(1.0,    25, 1,    7, 11, 7, fire=2,  cold=2),
  MaterialEnum.STEEL_WOOD:    Material(1.0,    10, 1,    5,  8, 4, fire=1,  cold=1),
  MaterialEnum.SILVER:        Material(1.5,    60, 1,    3,  8, 3, fire=2,  cold=2),
  MaterialEnum.GOLD:          Material(3.0,   120, 1,    4,  9, 4, fire=2,  cold=2),
  MaterialEnum.MITHRIL:       Material(0.25, 1200, 0.5,  4, 10, 7, fire=8,  cold=8),
  MaterialEnum.WOOD:          Material(1.0,     2, 1,    3,  4, 3, fire=1,  cold=2),
  MaterialEnum.STONE:         Material(1.5,     0, 1,    6, 10, 6, fire=5,  cold=2),
  MaterialEnum.BONE:          Material(0.3,     0, 1,    4,  7, 5, fire=2,  cold=2),
  MaterialEnum.DRAGON_HIDE:   Material(0.2,  4800, 0.5,  7, 11, 8, fire=10, cold=10),
}

# BODY COVERAGE

class CoverageEnum(IntEnum):
  SKULL = 0
  FACE = 1
  NECK = 2
  SHOULDERS = 3
  UPPER_ARMS = 4
  ELBOWS = 5
  FOREARMS = 6
  HANDS = 7
  FRONT_THORAX = 8
  REAR_THORAX = 9
  FRONT_ABDOMEN = 10
  REAR_ABDOMEN = 11
  HIPS = 12
  GROIN = 13
  THIGHS = 14
  KNEES = 15
  CALVES = 16
  FEET = 17

COV_Sk = 1 << CoverageEnum.SKULL
COV_Fa = 1 << CoverageEnum.FACE
COV_Nk = 1 << CoverageEnum.NECK
COV_Sh = 1 << CoverageEnum.SHOULDERS
COV_Ua = 1 << CoverageEnum.UPPER_ARMS
COV_El = 1 << CoverageEnum.ELBOWS
COV_Fo = 1 << CoverageEnum.FOREARMS
COV_Ha = 1 << CoverageEnum.HANDS
COV_Tx_F = 1 << CoverageEnum.FRONT_THORAX
COV_Tx_R = 1 << CoverageEnum.REAR_THORAX
COV_Ab_F = 1 << CoverageEnum.FRONT_ABDOMEN
COV_Ab_R = 1 << CoverageEnum.REAR_ABDOMEN
COV_Hp = 1 << CoverageEnum.HIPS
COV_Gr = 1 << CoverageEnum.GROIN
COV_Th = 1 << CoverageEnum.THIGHS
COV_Kn = 1 << CoverageEnum.KNEES
COV_Ca = 1 << CoverageEnum.CALVES
COV_Ft = 1 << CoverageEnum.FEET
COV_Tx = COV_Tx_F | COV_Tx_R
COV_Ab = COV_Ab_F | COV_Ab_R
COV_Ch = COV_Tx_F | COV_Ab_F
COV_Bk = COV_Tx_R | COV_Ab_R

class BodyPart:
  def __init__(self, name, mass):
    self.PartName = name
    self.Mass = mass

body_parts = {
  CoverageEnum.SKULL:         BodyPart("skull", 4),
  CoverageEnum.FACE:          BodyPart("face", 3),
  CoverageEnum.NECK:          BodyPart("neck", 4),
  CoverageEnum.SHOULDERS:     BodyPart("shoulder", 4),
  CoverageEnum.UPPER_ARMS:    BodyPart("upper arm", 6),
  CoverageEnum.ELBOWS:        BodyPart("elbow", 6),
  CoverageEnum.FOREARMS:      BodyPart("forearm", 6),
  CoverageEnum.HANDS:         BodyPart("haand", 4),
  CoverageEnum.FRONT_THORAX:  BodyPart("thorax (front)", 6),
  CoverageEnum.REAR_THORAX:   BodyPart("thorax (back)", 6),
  CoverageEnum.FRONT_ABDOMEN: BodyPart("abdomen (front)", 6),
  CoverageEnum.REAR_ABDOMEN:  BodyPart("abdomen (back)", 6),
  CoverageEnum.HIPS:          BodyPart("hip", 8),
  CoverageEnum.GROIN:         BodyPart("groin", 2),
  CoverageEnum.THIGHS:        BodyPart("thigh", 7),
  CoverageEnum.KNEES:         BodyPart("knee", 3),
  CoverageEnum.CALVES:        BodyPart("calf", 10),
  CoverageEnum.FEET:          BodyPart("foot", 6),
}

# DAMAGE

class DamageTypeEnum(IntEnum):
  NONE = 0
  BLUNT = 1
  EDGE = 2
  PIERCE = 3
  FIRE = 4
  COLD = 5
  SHOCK = 6
  POISON = 7
  MAGIC = 8

# EFFECTS

class EffectTypeEnum(IntEnum):
  NONE = 0
  STR = 1
  DEX = 2
  WIS = 3
  CON = 4
  ATK = 5
  DEF = 6
  HP_MAX = 7
  HP_REGEN = 8
  MANA_MAX = 9
  MANA_REGEN = 10
  HEALING = 11
  DAMAGE = 12

class Effect:
  def __init__(self, effect_type, mod, dur=0):
    self.EffectType = effect_type
    self.Modifier = mod
    self.Duration = dur

# ITEMS

class ItemEnum(IntEnum):
  NONE = 0

  # WEAPON [UNARMED]
  WEAPON_HAND = 10000
  WEAPON_FOOT = 10001
  WEAPON_BITE = 10002
  # WEAPON [DAGGER]
  WEAPON_KNIFE = 10200
  WEAPON_DAGGER = 10210
  WEAPON_MAIN_GAUCHE = 10220
  # WEAPON [SWORD]
  WEAPON_SHORTSWORD = 10300
  WEAPON_BROADSWORD = 10310
  WEAPON_FALCHION = 10320
  WEAPON_BASTARD_SWORD = 10330
  WEAPON_BATTLESWORD = 10340
  # WEAPON [CLUB]
  WEAPON_STICK = 10400
  WEAPON_CLUB = 10401
  WEAPON_MACE = 10402
  WEAPON_MORNINGSTAR = 10403
  WEAPON_MAUL = 10404
  # WEAPON [AXE]
  WEAPON_SICKLE = 10500
  WEAPON_HATCHET = 10501
  WEAPON_HANDAXE = 10502
  WEAPON_WARHAMMER = 10503
  WEAPON_BATTLEAXE = 10504
  # WEAPON [FLAIL]
  WEAPON_GRAINFLAIL = 10600
  WEAPON_BALL_AND_CHAIN = 10601
  WEAPON_WARFLAIL = 10602
  # WEAPON [SPEAR]
  WEAPON_STAFF = 10700
  WEAPON_JAVELIN = 10701
  WEAPON_SPEAR = 10702
  WEAPON_TRIDENT = 10703
  # WEAPON [POLEARM]
  WEAPON_LANCE = 10800
  WEAPON_GLAIVE = 10801
  WEAPON_POLEAXE = 10802
  WEAPON_PIKE = 10803
  # WEAPON [NET]
  # WEAPON [WHIP]
  # WEAPON [BOW]
  # WEAPON [BLOWGUN]
  # WEAPON [SLING]

  # SHIELD
  SHIELD_BUCKLER_WOOD = 15000
  SHIELD_BUCKLER_BANDED = 15001
  SHIELD_BUCKLER_STEEL = 15002
  SHIELD_KNIGHT_STEEL = 15010
  SHIELD_ROUND_WOOD = 15020
  SHIELD_ROUND_BANDED = 15021
  SHIELD_KITE_STEEL = 15030
  SHIELD_TOWER_WOOD = 15040
  SHIELD_TOWER_BANDED = 15041

  # ARMOR [CLOTH]
  ARMOR_CAP_CLOTH = 20000
  ARMOR_HOOD_CLOTH = 20001
  ARMOR_VEST_CLOTH = 20002
  ARMOR_TUNIC_CLOTH = 20003
  ARMOR_SURCOAT_CLOTH = 20004
  ARMOR_ROBE_CLOTH = 20005
  ARMOR_LEGGINGS_CLOTH = 20006
  # ARMOR [QUILT]
  ARMOR_CAP_QUILT = 20100
  ARMOR_COWL_QUILT = 20101
  ARMOR_TUNIC_QUILT = 20102
  ARMOR_GAMBESON_QUILT = 20103
  ARMOR_LEGGINGS_QUILT = 20104
  # ARMOR [LEATHER]
  ARMOR_CAP_LEATHER = 20200
  ARMOR_COWL_LEATHER = 20201
  ARMOR_VEST_LEATHER = 20202
  ARMOR_TUNIC_LEATHER = 20203
  ARMOR_SURCOAT_LEATHER = 20204
  ARMOR_LEGGINGS_LEATHER = 20205
  ARMOR_SHOES_LEATHER = 20206
  ARMOR_CALF_BOOTS_LEATHER = 20207
  ARMOR_KNEE_BOOTS_LEATHER = 20208
  ARMOR_GAUNTLETS_LEATHER = 20209
  # ARMOR [KURBUL]
  ARMOR_HALFHELM_KURBUL = 20300
  ARMOR_BREASTPLATE_KURBUL = 20301
  ARMOR_BACKPLATE_KURBUL = 20302
  ARMOR_AILETTES_KURBUL = 20303
  ARMOR_REREBRACES_KURBUL = 20304
  ARMOR_COUDES_KURBUL = 20305
  ARMOR_VAMBRACES_KURBUL = 20306
  ARMOR_KNEECOPS_KURBUL = 20307
  ARMOR_GREAVES_KURBUL = 20308
  # ARMOR [LEATHER RING]
  ARMOR_HALFHELM_LEATHER_RING = 20400
  ARMOR_VEST_LEATHER_RING = 20401
  ARMOR_BYRNIE_LEATHER_RING = 20402
  ARMOR_HAUBERK_LEATHER_RING = 20403
  ARMOR_LEGGINGS_LEATHER_RING = 20404
  ARMOR_GAUNTLETS_LEATHER_RING = 20405
  # ARMOR [MAIL]
  ARMOR_COWL_MAIL = 20500
  ARMOR_BYRNIE_MAIL = 20501
  ARMOR_HAUBERK_MAIL = 20502
  ARMOR_LEGGINGS_MAIL = 20503
  ARMOR_MITTENS_MAIL = 20504
  # ARMOR [SCALE]
  ARMOR_VEST_SCALE = 20600
  ARMOR_BYRNIE_SCALE = 20601
  ARMOR_HAUBERK_SCALE = 20602
  # ARMOR [PLATE]
  ARMOR_HALFHELM_STEEL = 20700
  ARMOR_GREAT_HELM_STEEL = 20701
  ARMOR_BREASTPLATE_STEEL = 20702
  ARMOR_BACKPLATE_STEEL = 20703
  ARMOR_AILETTES_STEEL = 20704
  ARMOR_REREBRACES_STEEL = 20705
  ARMOR_COUDES_STEEL = 20706
  ARMOR_VAMBRACES_STEEL = 20707
  ARMOR_KNEECOPS_STEEL = 20708
  ARMOR_GREAVES_STEEL = 20709
 
  # RINGS
  RING_ATTACK_SILVER = 30000
  RING_HP_GOLD = 30001

  # MISC
  MISC_STONE = 50000

class ItemTypeEnum(IntEnum):
  NONE = 0
  WEAPON = 1
  SHIELD = 2
  ARMOR = 3
  RING = 4
  MISSILE = 5
  CONTAINER = 6
  MISC = 7

class ItemFlagEnum(IntEnum):
  NO_SELL = 0
  NO_DROP = 1
  LIGHT = 2
  MAGIC = 3

class ItemFlag:
  def __init__(self, name, bit):
    self.Name = name
    self.Bit = bit

item_flags = {
  ItemFlagEnum.NO_SELL: ItemFlag("no sell", 1 << ItemFlagEnum.NO_SELL),
  ItemFlagEnum.NO_DROP: ItemFlag("no drop", 1 << ItemFlagEnum.NO_DROP),
  ItemFlagEnum.LIGHT: ItemFlag("light", 1 << ItemFlagEnum.LIGHT),
  ItemFlagEnum.MAGIC: ItemFlag("magic", 1 << ItemFlagEnum.MAGIC),
}

class Item:
  def __init__(self, item_type = ItemTypeEnum.NONE, name = "", qual = QualityEnum.NONE, material = MaterialEnum.NONE, mass = 0, flags = 0, eff = None):
    self.ItemType = item_type
    self.ItemName = name
    self.Quality = qual
    self.Material = material
    self.Mass = mass
    self.StorageMass = mass * materials[self.Material].StorageMod
    self.Flags = flags
    self.Effects = eff
    # Calculations
    self.Weight = self.Mass * materials[self.Material].WeightBase
    self.Value = self.Mass * materials[self.Material].CostBase * qualities[self.Quality].CostModifier

  def ItemFlagStr(self, format="%s"):
    flag_list = []
    for x in ItemFlagEnum:
        if item_flags[x].Bit & self.Flags > 0:
          flag_list.append(item_flags[x].Name)
    if len(flag_list) == 0:
      return ""
    else:
      return format % ", ".join(flag_list)

class Shield(Item):
  def __init__(self, name, qual, material, mass, skill, ar, dr, flags = 0, eff = None):
    super().__init__(ItemTypeEnum.SHIELD, name, qual, material, mass, flags, eff)
    self.Skill = skill
    self.AttackRating = ar
    self.DefenseRating = dr

class Weapon(Item):
  def __init__(self, name, qual, material, mass, skill, ar, dr, sh_penalty, dmg_rolls = 0, dmg_dice = 0, dmg_mod = 0, dmg_type = DamageTypeEnum.NONE, flags = 0, eff = None):
    super().__init__(ItemTypeEnum.WEAPON, name, qual, material, mass, flags, eff)
    self.Skill = skill
    self.AttackRating = ar
    self.DefenseRating = dr
    self.SingleHandPenalty = sh_penalty
    self.DamageRolls = dmg_rolls
    self.DamageDice = dmg_dice
    self.DamageMod = dmg_mod
    self.DamageType = dmg_type

ARMOR_LAYER1 = 0
ARMOR_LAYER1_5 = 1
ARMOR_LAYER2 = 2
ARMOR_LAYER2_5 = 3
ARMOR_LAYER3 = 4
ARMOR_LAYER3_5 = 5
ARMOR_LAYER4 = 6
ARMOR_LAYER4_5 = 7
ARMOR_LAYER5 = 8

AL_1 = 1 << ARMOR_LAYER1
AL_1_5 = 1 << ARMOR_LAYER1_5
AL_2 = 1 << ARMOR_LAYER2
AL_2_5 = 1 << ARMOR_LAYER2_5
AL_3 = 1 << ARMOR_LAYER3
AL_3_5 = 1 << ARMOR_LAYER3_5
AL_4 = 1 << ARMOR_LAYER4
AL_4_5 = 1 << ARMOR_LAYER4_5
AL_5 = 1 << ARMOR_LAYER5

class Armor(Item):
  def __init__(self, name, qual, material, layer = 0, coverage = 0, flags = 0, eff = None):
    # TODO use coverage / material Type
    mass = 0
    for x in CoverageEnum:
      if coverage & 1 << x > 0:
        mass += body_parts[x].Mass
    super().__init__(ItemTypeEnum.ARMOR, name, qual, material, mass, flags, eff)
    self.Layer = layer
    self.Coverage = coverage

  def CoverageStr(self):
    cov_list = []
    for x in CoverageEnum:
      if self.Coverage & 1 << x > 0:
        cov_list.append(body_parts[x].PartName)
    return ", ".join(cov_list)

class Ring(Item):
  def __init__(self, name, qual, material, mass, value = 0, flags = 0, eff = None):
    super().__init__(ItemTypeEnum.RING, name, qual, material, mass, flags, eff)
    self.Value = value

  def Value(self):
    return Value


# COMBAT

class CombatActionEnum(IntEnum):
  NONE = 0
  MELEE_ATTACK = 1
  DODGE = 2
  BLOCK = 3
  SPELL = 4
  ABILITY = 5
  FLEE = 6

class ItemLink:
  def __init__(self, qty = 1, equip = False):
    self.Quantity = qty
    self.Equipped = equip


# GENERIC PERSON

class Person:
  def __init__(self, name = ""):
    self.Name = name
    self.HitPoints_Cur = -1
    self.Action = CombatActionEnum.NONE
    self.Effects = []
    self.ItemLinks = {}

  def Copy(self, p):
    self.Name = p.Name
    self.HitPoints_Cur = p.HitPoints_Cur
    self.Action = p.Action
    self.Effects.clear()
    for x in p.Effects:
      self.Effects.append(x)
    self.ItemLinks.clear()
    for item_id, il in p.ItemLinks.items():
      self.AddItem(item_id, il)

  def ResetStats(self):
    self.Action = CombatActionEnum.NONE
    self.Effects.clear()

  def AddItem(self, item_id, item):
    if item_id in self.ItemLinks:
      self.ItemLinks[item_id].Quantity += item.Quantity
    else:
      self.ItemLinks.update({ item_id: item })
    return True

  def RemoveItem(self, item_id, item):
    if item_id in self.ItemLinks:
      if self.ItemLinks[item_id].Equipped and self.ItemLinks[item_id].Quantity == 1:
        return False
      if self.ItemLinks[item_id].Quantity > item.Quantity:
        self.ItemLinks[item_id].Quantity -= item.Quantity
      else:
        self.ItemLinks.pop(item_id)
    return True

# ENEMY

class EnemyEnum(IntEnum):
  NONE = 0
  RAT = 100

class Enemy(Person):
  def __init__(self, name, hp, dmg_rolls, dmg_dice, dmg_type,
              defen, startFunc, endFunc):
    super().__init__(name)
    self.Alive = True
    self.HitPoints_Max = hp
    self.DamageRolls = dmg_rolls
    self.DamageDice = dmg_dice
    self.DamageType = dmg_type
    self.Defense = defen
    self.StartRound = startFunc
    self.EndRound = endFunc
    self.ResetStats()

  def ResetStats(self):
    self.HitPoints_Cur = self.HitPoints_Max
    super().ResetStats()

# PLAYER

class Player(Person):
  def __init__(self, name = ""):
    super().__init__(name)
    self.MagicPoints_Cur = -1
    self.Currency = 0
    self.Lives = 3
    self.Command = ""
    self.Room = None
    self.LastRoom = None
    self.CombatEnemy = EnemyEnum.NONE

  def Copy(self, p):
    super().Copy(p)
    self.MagicPoints_Cur = p.MagicPoints_Cur
    self.Currency = p.Currency
    self.Lives = p.Lives
    self.Room = p.Room
    self.LastRoom = p.LastRoom
    self.CombatEnemy = p.CombatEnemy

  def SetRoom(self, room_id):
    self.LastRoom = self.Room
    self.Room = room_id

# ROOM

class RoomEnum(IntEnum):
  NONE = 0
  START_GAME = 1
  RESTORE_SAVE = 2
  CREATE_CHARACTER = 3
  DEAD = 10
  BL_BEGIN = 10000
  BL_RESPAWN = 10001

class RoomFuncResponse(IntEnum):
  NONE = 0
  NO_PROMPT = 1
  SKIP = 2
  
class DirectionEnum(IntEnum):
  NONE = 0
  NORTH = 1
  SOUTH = 2
  WEST = 3
  EAST = 4
  NORTHWEST = 5
  NORTHEAST = 6
  SOUTHWEST = 7
  SOUTHEAST = 8
  UP = 9
  DOWN = 10

class Exit:
  def __init__(self, room_id, name="", lock=False, key_item=ItemEnum.NONE):
    self.Room = room_id
    self.ExitName = name
    self.Locked = lock
    self.Key = key_item

class Room:
  def __init__(self, title, short_desc, long_desc="", func=None, enemy=EnemyEnum.NONE,
              exits=None, room_items=None):
    self.Title = title
    self.ShortDescription = short_desc
    self.LongDescription = long_desc
    self.Function = func
    self.Enemy = enemy
    self.Exits = {}
    self.RoomItems = {}
    if not exits is None:
      for exit_dir, exit in exits.items():
        self.AddExit(exit_dir, exit)
    if not room_items is None:
      for item_id, qty in room_items.items():
        self.AddItem(item_id)
      self.RoomItems = room_items

  def AddExit(self, exit_dir, exit):
    if exit_dir in self.Exits:
      self.Exits[exit_dir] = exit
    else:
      self.Exits.update({ exit_dir: exit })

  def RemoveExit(self, direction):
    if direction in self.Exits:
        self.Exits.pop(direction)

  def AddItem(self, item_id, item):
    if item_id in self.RoomItems:
      self.RoomItems[item_id].Quantity += item.Quantity
    else:
      self.RoomItems.update({ item_id: item })

  def RemoveItem(self, item_id, item):
    if item_id in self.RoomItems:
      if self.RoomItems[item_id].Quantity > item.Quantity:
        self.RoomItems[item_id].Quantity -= item.Quantity
      else:
        self.RoomItems.pop(item_id)

# FORMATTING

class ANSI:
  RESET_CURSOR =  "\x1B[1;1H"
  CLEAR =         "\x1B[2J"
  TEXT_NORMAL =   "\x1B[0m"
  TEXT_BOLD =   "\x1B[1m"

# vim: tabstop=2 shiftwidth=2 expandtab:
