# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Global Definitions

import random

from enum import IntEnum
from uuid import uuid4
from copy import deepcopy
from time import time

from gamedata import GameData
from logger import logd


# ROLL

ROLLF_DROP_LOWEST = 1 << 0


class DiceRoll:
  def __init__(self, num, roll_max, mod=0, roll_min=1, flags=0):
    self.Num = num
    self.Min = roll_min
    self.Max = roll_max
    self.Mod = mod
    self.Flags = flags

  def Result(self):
    value = 0
    rollList = []
    for x in range(self.Num):
      y = random.randint(self.Min, self.Max) + self.Mod
      rollList.append(y)
    if self.Flags & ROLLF_DROP_LOWEST > 0:
      low = 99999
      for r in rollList:
        if low > r:
          low = r
      rollList.remove(low)
    for r in rollList:
      value += r
    logd("DICE RESULT %dD%d+%d (flags:%x): %d" % (self.Num, self.Max, self.Mod, self.Flags, value))
    return value

  def __str__(self):
    ret = "%dD%d" % (self.Num, self.Max)
    if self.Mod != 0:
      if self.Mod > 0:
        ret += "+%d" % self.Mod
      else:
        ret += "-%d" % self.Mod
    return ret


class Roll(IntEnum):
  NONE = 0
  CS = 1
  MS = 2
  MF = 3
  CF = 4


# QUALITY

class QualityEnum(IntEnum):
  NONE = 0
  TER = 1
  POR = 2
  INF = 3
  AVE = 4
  SUP = 5
  EXC = 6
  MAG = 7


class ItemQuality:
  def __init__(self, name, cost_mod):
    self.Name = name
    self.CostModifier = cost_mod


qualities = {
    QualityEnum.TER: ItemQuality("terrible", 0.1),
    QualityEnum.POR: ItemQuality("poor", 0.5),
    QualityEnum.INF: ItemQuality("inferior", 0.75),
    QualityEnum.AVE: ItemQuality("average", 1),
    QualityEnum.SUP: ItemQuality("sup", 1.5),
    QualityEnum.EXC: ItemQuality("excellent", 2),
    QualityEnum.MAG: ItemQuality("magnificent", 4),
}


# DAMAGE

class DamageTypeEnum(IntEnum):
  BLUNT = 0
  EDGE = 1
  PIERCE = 2
  ELEMENTAL = 3
  MAX = 4


damages = {
    DamageTypeEnum.BLUNT: "crushing",
    DamageTypeEnum.EDGE: "slashing",
    DamageTypeEnum.PIERCE: "piercing",
    DamageTypeEnum.ELEMENTAL: "elemental",
}


# MATERIALS

class MaterialFlagEnum(IntEnum):
  MAGIC = 0


class MaterialEnum(IntEnum):
  NONE = 0
  # SKIN TYPES
  FEATHERS_LT = 1
  FEATHERS_MD = 2
  FEATHERS_HV = 3
  FUR_LT = 7
  FUR_MD = 8
  FUR_HV = 9
  HIDE = 10
  HIDE_BEAR_LT = 11
  HIDE_BEAR_MD = 12
  HIDE_BEAR_HV = 13
  HIDE_DRAGON_LT = 14
  HIDE_DRAGON_MD = 15
  HIDE_DRAGON_HV = 16
  # CRAFTED
  CLOTH = 100
  QUILT = 101
  LEATHER = 102
  KURBUL = 103
  LEATHER_RING = 104
  MAIL = 105
  SCALE = 106
  STEEL = 107
  STEEL_WOOD = 108
  # PRECIOUS
  SILVER = 200
  BRONZE = 201
  GOLD = 202
  MITHRIL = 203
  # NATURAL
  WOOD = 300
  STONE = 301
  BONE = 302


class Material:
  def __init__(self, name, weight, cost, prot, flags=0):
    self.Name = name
    self.WeightBase = weight
    self.CostBase = cost
    self.Protection = []
    if prot is not None:
      for x in prot:
        self.Protection.append(x)
    self.Flags = flags

  def Clear(self):
    self.WeightBase = 0
    self.CostBase = 0
    self.Protection.clear()
    self.Flags = 0

  def Copy(self, m):
    self.Name = m.Name
    self.WeightBase = m.WeightBase
    self.CostBase = m.CostBase
    self.Protection.clear()
    for i, val in enumerate(m.Protection):
      self.Protection.append(val)
    self.Flags = m.Flags

  def Add(self, m):
    for i, val in enumerate(m.Protection):
      self.Protection[i] += val


materials = {
    MaterialEnum.NONE: Material("None", 0, 0, [0, 0, 0, 0]),
    # SKIN TYPES
    MaterialEnum.FEATHERS_LT: Material("Feathers", 0, 0, [3, 2, 1, 2]),
    MaterialEnum.FEATHERS_MD: Material("Feathers", 0, 0, [3, 4, 2, 4]),
    MaterialEnum.FUR_LT: Material("Fur", 0.1, 1, [2, 1, 1, 2]),
    MaterialEnum.FUR_MD: Material("Fur", 0.2, 2, [4, 3, 1, 3]),
    MaterialEnum.FUR_HV: Material("Fur", 0.3, 3, [5, 4, 1, 3]),
    MaterialEnum.HIDE: Material("Hide", 0.2, 4, [5, 4, 1, 3]),
    MaterialEnum.HIDE_BEAR_LT: Material("Bear Hide", 0.2, 3, [5, 3, 2, 4]),
    MaterialEnum.HIDE_BEAR_MD: Material("Bear Hide", 0.2, 5, [6, 4, 3, 5]),
    MaterialEnum.HIDE_BEAR_HV: Material("Bear Hide", 0.2, 7, [7, 5, 3, 6]),
    MaterialEnum.HIDE_DRAGON_LT: Material("Dragon Hide", 0.2, 4800, [8, 5, 8, 7], flags=1 << MaterialFlagEnum.MAGIC),
    MaterialEnum.HIDE_DRAGON_MD: Material("Dragon Hide", 0.2, 6400, [10, 8, 7, 9], flags=1 << MaterialFlagEnum.MAGIC),
    MaterialEnum.HIDE_DRAGON_HV: Material("Dragon Hide", 0.2, 9600, [12, 15, 12, 14], flags=1 << MaterialFlagEnum.MAGIC),
    # CRAFTED
    MaterialEnum.CLOTH: Material("Cloth", 0.1, 2, [1, 1, 1, 1]),
    MaterialEnum.QUILT: Material("Quilt", 0.3, 4, [5, 3, 2, 4]),
    MaterialEnum.LEATHER: Material("Leather", 0.2, 4, [2, 4, 3, 3]),
    MaterialEnum.KURBUL: Material("Hardened Leather", 0.25, 5, [4, 5, 4, 3]),
    MaterialEnum.LEATHER_RING: Material("Studded Leather", 0.4, 7, [3, 6, 4, 3]),
    MaterialEnum.MAIL: Material("Chainmail", 0.5, 15, [2, 8, 5, 1]),
    MaterialEnum.SCALE: Material("Scale Mail", 0.7, 10, [5, 9, 4, 5]),
    MaterialEnum.STEEL: Material("Steel", 0.8, 25, [6, 10, 6, 2]),
    MaterialEnum.STEEL_WOOD: Material("Steel & Wood", 0.8, 10, [5, 8, 4, 1]),
    # PRECIOUS
    MaterialEnum.BRONZE: Material("Bronze", 0.8, 10, [2, 6, 2, 1]),
    MaterialEnum.SILVER: Material("Silver", 1.5, 60, [3, 8, 3, 2]),
    MaterialEnum.GOLD: Material("Gold", 3.0, 120, [4, 9, 4, 3]),
    MaterialEnum.MITHRIL: Material("Mithril", 0.25, 1200, [4, 10, 7, 8], flags=1 << MaterialFlagEnum.MAGIC),
    # NATURAL
    MaterialEnum.WOOD: Material("Wood", 1.0, 2, [3, 4, 3, 1]),
    MaterialEnum.STONE: Material("Stone", 1.5, 0, [6, 10, 6, 3]),
    MaterialEnum.BONE: Material("Bone", 0.3, 0, [4, 7, 5, 2]),
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
  THORAX_FRONT = 8
  THORAX_REAR = 9
  ABDOMEN_FRONT = 10
  ABDOMEN_REAR = 11
  HIPS = 12
  GROIN = 13
  THIGHS = 14
  KNEES = 15
  CALVES = 16
  FEET = 17


class BodyPart:
  def __init__(self, name, mass, leftright=False, fumble=False, stumble=False):
    self.PartName = name
    self.Mass = mass
    self.LeftRight = leftright
    self.Fumble = stumble
    self.Stumble = fumble


body_parts = {
    # HUMAN PARTS
    CoverageEnum.SKULL: BodyPart("Skull", 4),
    CoverageEnum.FACE: BodyPart("Face", 3),
    CoverageEnum.NECK: BodyPart("Neck", 4),
    CoverageEnum.SHOULDERS: BodyPart("Shoulder", 4, True, fumble=True),
    CoverageEnum.UPPER_ARMS: BodyPart("Upper Arm", 6, True, fumble=True),
    CoverageEnum.ELBOWS: BodyPart("Elbow", 2, True, fumble=True),
    CoverageEnum.FOREARMS: BodyPart("Forearm", 5, True, fumble=True),
    CoverageEnum.HANDS: BodyPart("Hand", 4, True, fumble=True),
    CoverageEnum.THORAX_FRONT: BodyPart("Thorax (front)", 6),
    CoverageEnum.THORAX_REAR: BodyPart("Thorax (back)", 6),
    CoverageEnum.ABDOMEN_FRONT: BodyPart("Abdomen (front)", 6),
    CoverageEnum.ABDOMEN_REAR: BodyPart("Abdomen (back)", 6),
    CoverageEnum.GROIN: BodyPart("Groin", 2, stumble=True),
    CoverageEnum.HIPS: BodyPart("Hip", 8, True, stumble=True),
    CoverageEnum.THIGHS: BodyPart("Thigh", 14, True, stumble=True),
    CoverageEnum.KNEES: BodyPart("Knee", 3, True, stumble=True),
    CoverageEnum.CALVES: BodyPart("Calf", 10, True, stumble=True),
    CoverageEnum.FEET: BodyPart("Foot", 6, True, stumble=True),
    # MOB PARTS
}


class ShapeEnum(IntEnum):
  NONE = 0
  CAP = 10
  COWL = 11
  FULL_HELM = 12
  APRON = 20
  VEST = 21
  TUNIC = 22
  SURCOAT = 23
  ROBE = 24
  HAUBERK = 26
  BREASTPLATE = 27
  BACKPLATE = 28
  AILETTES = 29
  REREBRACES = 30
  COUDES = 31
  VAMBRACES = 32
  KNEECOPS = 33
  GREAVES = 34
  GAUNTLETS = 50
  LEGGINGS = 51
  SHOES = 52
  BOOTS_CALF = 53
  BOOTS_KNEE = 54


armor_shapes = {
    ShapeEnum.NONE: 0,
    ShapeEnum.CAP: (1 << CoverageEnum.SKULL),
    ShapeEnum.COWL: (1 << CoverageEnum.SKULL | 1 << CoverageEnum.NECK),
    ShapeEnum.FULL_HELM: (1 << CoverageEnum.SKULL | 1 << CoverageEnum.NECK | 1 << CoverageEnum.FACE),
    ShapeEnum.APRON:
        (1 << CoverageEnum.THORAX_FRONT | 1 << CoverageEnum.THORAX_REAR |
         1 << CoverageEnum.ABDOMEN_FRONT | 1 << CoverageEnum.ABDOMEN_REAR |
         1 << CoverageEnum.HIPS | 1 << CoverageEnum.GROIN | 1 << CoverageEnum.THIGHS),
    ShapeEnum.VEST:
        (1 << CoverageEnum.SHOULDERS | 1 << CoverageEnum.THORAX_FRONT | 1 << CoverageEnum.THORAX_REAR |
         1 << CoverageEnum.ABDOMEN_FRONT | 1 << CoverageEnum.ABDOMEN_REAR),
    ShapeEnum.TUNIC:
        (1 << CoverageEnum.UPPER_ARMS | 1 << CoverageEnum.SHOULDERS |
         1 << CoverageEnum.THORAX_FRONT | 1 << CoverageEnum.THORAX_REAR |
         1 << CoverageEnum.ABDOMEN_FRONT | 1 << CoverageEnum.ABDOMEN_REAR |
         1 << CoverageEnum.HIPS | 1 << CoverageEnum.GROIN),
    ShapeEnum.SURCOAT:
        (1 << CoverageEnum.SHOULDERS | 1 << CoverageEnum.THORAX_FRONT | 1 << CoverageEnum.THORAX_REAR |
         1 << CoverageEnum.ABDOMEN_FRONT | 1 << CoverageEnum.ABDOMEN_REAR |
         1 << CoverageEnum.HIPS | 1 << CoverageEnum.GROIN | 1 << CoverageEnum.THIGHS),
    ShapeEnum.ROBE:
        (1 << CoverageEnum.FOREARMS | 1 << CoverageEnum.ELBOWS | 1 << CoverageEnum.UPPER_ARMS |
         1 << CoverageEnum.SHOULDERS | 1 << CoverageEnum.THORAX_FRONT | 1 << CoverageEnum.THORAX_REAR |
         1 << CoverageEnum.ABDOMEN_FRONT | 1 << CoverageEnum.ABDOMEN_REAR |
         1 << CoverageEnum.HIPS | 1 << CoverageEnum.GROIN | 1 << CoverageEnum.THIGHS |
         1 << CoverageEnum.KNEES | 1 << CoverageEnum.CALVES),
    ShapeEnum.HAUBERK:
        (1 << CoverageEnum.FOREARMS | 1 << CoverageEnum.ELBOWS | 1 << CoverageEnum.UPPER_ARMS |
         1 << CoverageEnum.SHOULDERS | 1 << CoverageEnum.THORAX_FRONT | 1 << CoverageEnum.THORAX_REAR |
         1 << CoverageEnum.ABDOMEN_FRONT | 1 << CoverageEnum.ABDOMEN_REAR |
         1 << CoverageEnum.HIPS | 1 << CoverageEnum.GROIN | 1 << CoverageEnum.THIGHS),
    ShapeEnum.BREASTPLATE: (1 << CoverageEnum.THORAX_FRONT | 1 << CoverageEnum.ABDOMEN_FRONT),
    ShapeEnum.BACKPLATE: (1 << CoverageEnum.THORAX_REAR | 1 << CoverageEnum.ABDOMEN_REAR),
    ShapeEnum.AILETTES: (1 << CoverageEnum.SHOULDERS),
    ShapeEnum.REREBRACES: (1 << CoverageEnum.UPPER_ARMS),
    ShapeEnum.COUDES: (1 << CoverageEnum.ELBOWS),
    ShapeEnum.VAMBRACES: (1 << CoverageEnum.FOREARMS),
    ShapeEnum.KNEECOPS: (1 << CoverageEnum.KNEES),
    ShapeEnum.GREAVES: (1 << CoverageEnum.CALVES),
    ShapeEnum.GAUNTLETS: (1 << CoverageEnum.HANDS),
    ShapeEnum.LEGGINGS:
        (1 << CoverageEnum.HIPS | 1 << CoverageEnum.GROIN | 1 << CoverageEnum.THIGHS |
         1 << CoverageEnum.KNEES | 1 << CoverageEnum.CALVES | 1 << CoverageEnum.FEET),
    ShapeEnum.SHOES: (1 << CoverageEnum.FEET),
    ShapeEnum.BOOTS_CALF: (1 << CoverageEnum.CALVES | 1 << CoverageEnum.FEET),
    ShapeEnum.BOOTS_KNEE: (1 << CoverageEnum.KNEES | 1 << CoverageEnum.CALVES | 1 << CoverageEnum.FEET),
}


# EFFECTS

class EffectTypeEnum(IntEnum):
  NONE = 0
  ATTRIBUTE = 1
  SKILL = 2


class Effect:
  def __init__(self, effect_type, value, mod, dur=0):
    self.EffectType = effect_type
    self.Value= value
    self.Modifier = mod
    self.Duration = dur

  def Copy(self, e):
    # handle old effects
    try:
      self.EffectType = e.EffectType
      self.Value = e.Value
    except:
      self.EffectType = EffectTypeEnum.NONE
      self.Value = 0
    self.Modifier = e.Modifier
    self.Duration = e.Duration

  def toString(self):
    if self.EffectType == EffectTypeEnum.NONE:
      return "broken effect"
    desc = ""
    if self.Modifier >= 0:
      desc += "+"
    desc += "%d " % self.Modifier
    if self.EffectType == EffectTypeEnum.ATTRIBUTE:
      desc += attributes[self.Value].Abbrev
    elif self.EffectType == EffectTypeEnum.SKILL:
      desc += skills[self.Value].Name
    if self.Duration > 0:
      desc += " (%d seconds left)" % self.Duration
    return desc


# ITEMS

class ItemTypeEnum(IntEnum):
  NONE = 0
  WEAPON = 1
  SHIELD = 2
  ARMOR = 3
  RING = 4
  MISSILE = 5
  CONTAINER = 6
  MISC = 7
  QUEST = 8


class ItemFlagEnum(IntEnum):
  NO_SELL = 1 << 0
  NO_DROP = 1 << 1
  NO_GET = 1 << 2
  LIGHT = 1 << 3
  MAGIC = 1 << 4
  HIDDEN = 1 << 5
  INVIS = 1 << 6
  QUEST = 1 << 7


class ItemFlag:
  def __init__(self, name):
    self.Name = name


item_flags = {
    ItemFlagEnum.NO_SELL: ItemFlag("no sell"),
    ItemFlagEnum.NO_DROP: ItemFlag("no drop"),
    ItemFlagEnum.NO_GET: ItemFlag("no get"),
    ItemFlagEnum.LIGHT: ItemFlag("light"),
    ItemFlagEnum.MAGIC: ItemFlag("magic"),
    ItemFlagEnum.HIDDEN: ItemFlag("hidden"),
    ItemFlagEnum.INVIS: ItemFlag("invisible"),
    ItemFlagEnum.QUEST: ItemFlag("quest"),
}


class Item:
  def __init__(self, item_type=ItemTypeEnum.NONE, name="", qual=QualityEnum.NONE, material=MaterialEnum.NONE,
               mass=0, flags=0, eff=None, onGet=None, onDrop=None, onEquip=None, onRemove=None, equipped=False):
    self.ItemType = item_type
    self.ItemName = name
    self.Quality = qual
    self.Material = material
    self.Mass = mass
    self.Flags = flags
    self.Effects = eff
    # Calculations
    self.Weight = self.Mass * materials[self.Material].WeightBase
    self.Value = self.Mass * materials[self.Material].CostBase * qualities[self.Quality].CostModifier
    self.OnGet = onGet
    self.OnDrop = onDrop
    self.OnEquip = onEquip
    self.OnRemove = onRemove
    self.Equipped = equipped

  def ItemFlagStr(self, format="%s"):
    flag_list = []
    for x in ItemFlagEnum:
        if x & self.Flags > 0:
          flag_list.append(item_flags[x].Name)
    if len(flag_list) == 0:
      return ""
    else:
      return format % ", ".join(flag_list)

  def IsLight(self):
    if ItemFlagEnum.LIGHT & self.Flags > 0:
      return True
    return False

  def Description(self):
    return "%s : Made of %s%s" % (
        self.ItemName.capitalize(), materials[self.Material].Name.lower(),
        self.ItemFlagStr(": (%s)"))


class Shield(Item):
  def __init__(self, name, qual, material, mass, skill, ar, dr, flags=0, eff=None,
               onGet=None, onDrop=None, onEquip=None, onRemove=None, equipped=False):
    super().__init__(ItemTypeEnum.SHIELD, name, qual, material, mass, flags, eff,
                     onGet, onDrop, onEquip, onRemove, equipped)
    self.Skill = skill
    self.AttackRating = ar
    self.DefenseRating = dr

  def Description(self):
    return "%s : Made of %s and uses %s skill%s" % (
        self.ItemName.capitalize(), materials[self.Material].Name.lower(),
        skills[self.Skill].Name.lower(), self.ItemFlagStr(" (%s)"))


class Weapon(Item):
  def __init__(self, name, qual, material, mass, skill, ar, dr, sh_penalty, dice_roll, dmg_type=DamageTypeEnum.BLUNT,
               flags=0, eff=None, onGet=None, onDrop=None, onEquip=None, onRemove=None, equipped=False):
    super().__init__(ItemTypeEnum.WEAPON, name, qual, material, mass, flags, eff,
                     onGet, onDrop, onEquip, onRemove, equipped)
    self.Skill = skill
    self.AttackRating = ar
    self.DefenseRating = dr
    self.SingleHandPenalty = sh_penalty
    self.Roll = dice_roll
    self.DamageType = dmg_type

  def Description(self):
    return "%s : Made of %s, does %s %s damage and uses %s skill%s" % (
        self.ItemName.capitalize(), materials[self.Material].Name.lower(), self.Roll,
        damages[self.DamageType], skills[self.Skill].Name.lower(), self.ItemFlagStr(" (%s)"))


class ArmorLayer(IntEnum):
  NONE = 0
  AL_1 = 1 << 0
  AL_1_5 = 1 << 1
  AL_2 = 1 << 2
  AL_2_5 = 1 << 3
  AL_3 = 1 << 4
  AL_3_5 = 1 << 5
  AL_4 = 1 << 6
  AL_4_5 = 1 << 7
  AL_5 = 1 << 8
  AL_5_5 = 1 << 9


class Armor(Item):
  def __init__(self, name, qual, material, layer=0, shape=ShapeEnum.NONE, flags=0, eff=None,
               onGet=None, onDrop=None, onEquip=None, onRemove=None, equipped=False):
    # TODO use coverage / material Type
    mass = 0
    self.Shape = shape
    self.Layer = layer
    if shape > ShapeEnum.NONE:
      for x in CoverageEnum:
        if self.Covered(x):
          mass += body_parts[x].Mass
    super().__init__(ItemTypeEnum.ARMOR, name, qual, material, mass, flags, eff,
                     onGet, onDrop, onEquip, onRemove, equipped)

  def Covered(self, bp_id):
    if armor_shapes[self.Shape] & (1 << bp_id) > 0:
        return True
    return False

  def CoverageStr(self):
    cov_list = []
    for x in CoverageEnum:
      if self.Covered(x):
        cov_list.append(body_parts[x].PartName)
    return ", ".join(cov_list)

  def Description(self):
    return "%s : Made of %s and covers %s%s" % (
        self.ItemName.capitalize(), materials[self.Material].Name.lower(),
        self.CoverageStr().lower(), self.ItemFlagStr(" (%s)"))


class Ring(Item):
  def __init__(self, name, qual, material, mass, value=0, flags=0, eff=None,
               onGet=None, onDrop=None, onEquip=None, onRemove=None, equipped=False):
    super().__init__(ItemTypeEnum.RING, name, qual, material, mass, flags, eff,
                     onGet, onDrop, onEquip, onRemove, equipped)
    self.Value = value


# COMBAT

class AimEnum(IntEnum):
  HIGH = 0
  MID = 1
  LOW = 2


class Aim:
  def __init__(self, name, penalty):
    self.Name = name
    self.Penalty = penalty


aims = {
    AimEnum.HIGH: Aim("High Zone", 10),
    AimEnum.MID: Aim("Mid Zone", 0),
    AimEnum.LOW: Aim("Low Zone", 10),
}


class CombatAttack:
  def __init__(self, name, ml, skill_id, item, roll, dmg_type):
    self.Name = name
    self.SkillML = ml
    self.SkillID = skill_id
    self.Item = item
    self.Roll = roll
    self.DamageType = dmg_type


class CombatHit:
  def __init__(self, high_max, mid_max, low_max):
    self.High = high_max
    self.Mid = mid_max
    self.Low = low_max


class ImpactActionEnum(IntEnum):
  NONE = 0
  WOUND_MLD = 1
  WOUND_SRS = 2
  WOUND_GRV = 3
  KILL_CHECK = 4
  SHOCK = 5
  FUMBLE = 6
  STUMBLE = 7
  AMPUTATE_CHECK = 8
  BLEED = 9


class ImpactAction:
  def __init__(self, action, level=0):
    self.Action = action
    self.Level = level


class ImpactResult:
  def __init__(self, imp_max, actions):
    self.ImpactMax = imp_max
    self.ImpactActions = actions


# TIME

class SeasonEnum(IntEnum):
  NONE = 0
  SPRING = 1
  SUMMER = 2
  AUTUMN = 3
  WINTER = 4


class MonthEnum(IntEnum):
  NONE = 0
  NUZYAEL = 1
  PEONU = 2
  KELEN = 3
  NOLUS = 4
  LARANE = 5
  AGRAZHAR = 6
  AZURA = 7
  HALANE = 8
  SAVOR = 9
  ILVIN = 10
  NAVEK = 11
  MORGAT = 12


class HarnMonth:
  def __init__(self, name, season):
    self.Name = name
    self.Season = season


months = {
    MonthEnum.NUZYAEL: HarnMonth("Nuzyael", SeasonEnum.SPRING),
    MonthEnum.PEONU: HarnMonth("Peonu", SeasonEnum.SPRING),
    MonthEnum.KELEN: HarnMonth("Kelen", SeasonEnum.SPRING),
    MonthEnum.NOLUS: HarnMonth("Nolus", SeasonEnum.SUMMER),
    MonthEnum.LARANE: HarnMonth("Larane", SeasonEnum.SUMMER),
    MonthEnum.AGRAZHAR: HarnMonth("Agrazhar", SeasonEnum.SUMMER),
    MonthEnum.AZURA: HarnMonth("Azura", SeasonEnum.AUTUMN),
    MonthEnum.HALANE: HarnMonth("Halane", SeasonEnum.AUTUMN),
    MonthEnum.SAVOR: HarnMonth("Savor", SeasonEnum.AUTUMN),
    MonthEnum.ILVIN: HarnMonth("Ilvin", SeasonEnum.WINTER),
    MonthEnum.NAVEK: HarnMonth("Navek", SeasonEnum.WINTER),
    MonthEnum.MORGAT: HarnMonth("Morgat", SeasonEnum.WINTER),
}


# SUNSIGN

class SunsignEnum(IntEnum):
  NONE = 0
  ULA = 1
  ARA = 2
  FEN = 3
  AHN = 4
  ANG = 5
  NAD = 6
  HIR = 7
  TAR = 8
  TAI = 9
  SKO = 10
  MAS = 11
  LAD = 12


SS_NON = SunsignEnum.NONE
SS_ULA = SunsignEnum.ULA
SS_ARA = SunsignEnum.ARA
SS_FEN = SunsignEnum.FEN
SS_AHN = SunsignEnum.AHN
SS_ANG = SunsignEnum.ANG
SS_NAD = SunsignEnum.NAD
SS_HIR = SunsignEnum.HIR
SS_TAR = SunsignEnum.TAR
SS_TAI = SunsignEnum.TAI
SS_SKO = SunsignEnum.SKO
SS_MAS = SunsignEnum.MAS
SS_LAD = SunsignEnum.LAD


class Sunsign:
  def __init__(self, abbrev, name, symbol, start_day, start_month, end_day, end_month):
    self.Abbrev = abbrev
    self.Name = name
    self.Symbol = symbol
    self.StartDay = start_day
    self.StartMonth = start_month
    self.EndDay = end_day
    self.EndMonth = end_month


sunsigns = {
    SS_NON: Sunsign("NONE", "[None]", "[None]", 0, MonthEnum.NONE, 0, MonthEnum.NONE),
    SS_ULA: Sunsign("ULA", "Ulandus", "Tree", 4, MonthEnum.NUZYAEL, 3, MonthEnum.PEONU),
    SS_ARA: Sunsign("ARA", "Aralius", "Wands", 4, MonthEnum.PEONU, 2, MonthEnum.KELEN),
    SS_FEN: Sunsign("FEN", "Feniri", "Smith", 3, MonthEnum.KELEN, 3, MonthEnum.NOLUS),
    SS_AHN: Sunsign("AHN", "Ahnu", "Fire Dragon", 4, MonthEnum.NOLUS, 4, MonthEnum.LARANE),
    SS_ANG: Sunsign("ANG", "Angberelius", "Flaming Swords", 5, MonthEnum.LARANE, 6, MonthEnum.AGRAZHAR),
    SS_NAD: Sunsign("NAD", "Nadai", "Salamander", 7, MonthEnum.AGRAZHAR, 5, MonthEnum.AZURA),
    SS_HIR: Sunsign("HIR", "Hirin", "Eagle", 6, MonthEnum.AZURA, 4, MonthEnum.HALANE),
    SS_TAR: Sunsign("TAR", "Tarael", "Pentacle", 5, MonthEnum.HALANE, 3, MonthEnum.SAVOR),
    SS_TAI: Sunsign("TAI", "Tai", "Lantern", 4, MonthEnum.SAVOR, 2, MonthEnum.ILVIN),
    SS_SKO: Sunsign("SKO", "Skorus", "Mixer", 3, MonthEnum.ILVIN, 2, MonthEnum.NAVEK),
    SS_MAS: Sunsign("MAS", "Masara", "Chalic", 3, MonthEnum.NAVEK, 1, MonthEnum.MORGAT),
    SS_LAD: Sunsign("LAD", "Lado", "Galley", 2, MonthEnum.MORGAT, 3, MonthEnum.NUZYAEL),
}


class SunsignMod:
  def __init__(self, sign, mod):
    self.Sunsign = sign
    self.Mod = mod


# GENERIC ATTRIBUTE CLASSES

class AttrNameMax:
  def __init__(self, name, attr_max):
    self.Name = name
    self.AttrMax = attr_max


# SEX

class AttrSexNameMax(AttrNameMax):
  def __init__(self, name, pronoun, posses, attr_max):
    super().__init__(name, attr_max)
    self.Pronoun = pronoun
    self.PossessivePronoun = posses


class SexEnum(IntEnum):
  NONE = 0
  MALE = 1
  FEMALE = 2


sexes = {
    SexEnum.NONE: AttrSexNameMax("none", "it", "its", 0),
    SexEnum.MALE: AttrSexNameMax("male", "he", "his", 48),
    SexEnum.FEMALE: AttrSexNameMax("female", "she", "her", 100),
}


# SOCIAL CLASS

class SocialClassEnum:
  NONE = 0
  SLAVE = 1
  SERF = 2
  FREEMAN = 3
  UNGUILDED = 4
  GUILDED = 5
  NOBLE = 6


class SocialClass:
  def __init__(self, name):
    self.Name = name


social_classes = {
    SocialClassEnum.SLAVE: SocialClass("Slave"),
    SocialClassEnum.SERF: SocialClass("Serf"),
    SocialClassEnum.FREEMAN: SocialClass("Freeman"),
    SocialClassEnum.UNGUILDED: SocialClass("Unguilded"),
    SocialClassEnum.GUILDED: SocialClass("Guilded"),
    SocialClassEnum.NOBLE: SocialClass("Noble"),
}


# CULTURE

class CultureEnum:
  NONE = 0
  FEUDAL = 1
  IMPERIAL = 2
  VIKING = 3
  TRIBAL = 4


class Culture(AttrNameMax):
  def __init__(self, name, attr_max, sc_attrmax):
    super().__init__(name, attr_max)
    self.SCAttrMax = sc_attrmax


cultures = {
    CultureEnum.FEUDAL: Culture("Feudal", 80,
                                {
                                    SocialClassEnum.SLAVE: 15,
                                    SocialClassEnum.SERF: 70,
                                    SocialClassEnum.UNGUILDED: 93,
                                    SocialClassEnum.GUILDED: 98,
                                    SocialClassEnum.NOBLE: 100,
                                }),
    CultureEnum.IMPERIAL: Culture("Imperial", 90,
                                  {
                                      SocialClassEnum.SLAVE: 25,
                                      SocialClassEnum.UNGUILDED: 90,
                                      SocialClassEnum.GUILDED: 98,
                                      SocialClassEnum.NOBLE: 100,
                                  }),
    CultureEnum.VIKING: Culture("Viking", 95,
                                {
                                    SocialClassEnum.SLAVE: 15,
                                    SocialClassEnum.FREEMAN: 80,
                                    SocialClassEnum.UNGUILDED: 93,
                                    SocialClassEnum.GUILDED: 98,
                                    SocialClassEnum.NOBLE: 100,
                                }),
    CultureEnum.TRIBAL: Culture("Tribal", 100,
                                {
                                    SocialClassEnum.SLAVE: 10,
                                    SocialClassEnum.UNGUILDED: 99,
                                    SocialClassEnum.NOBLE: 100,
                                }),
}


# SIBLINK RANK

sibling_ranks = {
    1: AttrNameMax("Eldest", 25),
    2: AttrNameMax("2nd Child", 50),
    3: AttrNameMax("3rd Child", 70),
    4: AttrNameMax("4th Child", 85),
    5: AttrNameMax("5th Child", 95),
    6: AttrNameMax("6th Child", 100),
}


# PARENTS

class ParentStatusEnum:
  NONE = 0
  OFFSPRING = 1
  FOSTERED = 2
  ADOPTED = 3
  BASTARD = 4
  ORPHAN = 5


parent_statuses = {
    ParentStatusEnum.OFFSPRING: AttrNameMax("Normal", 50),
    ParentStatusEnum.FOSTERED: AttrNameMax("Fostered", 70),
    ParentStatusEnum.ADOPTED: AttrNameMax("Adopted", 75),
    ParentStatusEnum.BASTARD: AttrNameMax("Bastard", 90),
    ParentStatusEnum.ORPHAN: AttrNameMax("Orphaned", 100),
}


# FRAME / WEIGHT

class PlayerFrameEnum:
  NONE = 0
  SCANT = 1
  LIGHT = 2
  MEDIUM = 3
  HEAVY = 4
  MASSIVE = 5


class PlayerFrame(AttrNameMax):
  def __init__(self, name, attr_max, mod):
    super().__init__(name, attr_max)
    self.ModPercent = mod


player_frames = {
    PlayerFrameEnum.SCANT: PlayerFrame("Scant", 5, 0.8),
    PlayerFrameEnum.LIGHT: PlayerFrame("Light", 8, 0.9),
    PlayerFrameEnum.MEDIUM: PlayerFrame("Medium", 12, 1),
    PlayerFrameEnum.HEAVY: PlayerFrame("Heavy", 15, 1.1),
    PlayerFrameEnum.MASSIVE: PlayerFrame("Massive", 100, 1.2),
}


player_weights = {
    40: 75, 41: 77, 42: 79, 43: 81, 44: 83, 45: 85,
    46: 87, 47: 89, 48: 91, 49: 93, 50: 95, 51: 97,
    52: 100, 53: 103, 54: 106, 55: 109, 56: 112, 57: 115, 58: 118,
    59: 121, 60: 124, 61: 127, 62: 130, 63: 133, 64: 137, 65: 141,
    66: 145, 67: 149, 68: 153, 69: 157, 70: 160, 71: 165, 72: 170,
    73: 175, 74: 180, 75: 185, 76: 190, 77: 195, 78: 200, 79: 205,
    80: 210, 81: 215, 82: 220, 83: 225, 84: 230, 85: 235, 86: 240,
    87: 245, 88: 250, 89: 255,
}


# COMELINESS

class ComelinessEnum:
  NONE = 0
  UGLY = 1
  PLAIN = 2
  AVERAGE = 3
  ATTRACTIVE = 4
  HANDSOME = 5


comelinesses = {
    ComelinessEnum.UGLY: AttrNameMax("Ugly", 5),
    ComelinessEnum.PLAIN: AttrNameMax("Plain", 8),
    ComelinessEnum.AVERAGE: AttrNameMax("Average", 12),
    ComelinessEnum.ATTRACTIVE: AttrNameMax("Attractive", 15),
    ComelinessEnum.HANDSOME: AttrNameMax("Handsome", 100),
}


# COMPLEXION

class ComplexionEnum:
  NONE = 0
  FAIR = 1
  MEDIUM = 2
  DARK = 3


class Complexion(AttrNameMax):
  def __init__(self, name, attr_max, eye_mod):
    super().__init__(name, attr_max)
    self.EyeColorMod = eye_mod


complexions = {
    ComplexionEnum.FAIR: Complexion("Fair", 27, 25),
    ComplexionEnum.MEDIUM: Complexion("Medium", 74, 0),
    ComplexionEnum.DARK: Complexion("Dark", 100, -25),
}


# HAIR / EYE COLOR

class ColorHairEnum:
  NONE = 0
  BROWN = 1
  BLACK = 2
  RED = 3
  SILVER = 4
  BLONDE = 5


color_hairs = {
    ColorHairEnum.BROWN: AttrNameMax("Brown", 40),
    ColorHairEnum.BLACK: AttrNameMax("Black", 55),
    ColorHairEnum.RED: AttrNameMax("Red", 65),
    ColorHairEnum.SILVER: AttrNameMax("Silver", 70),
    ColorHairEnum.BLONDE: AttrNameMax("Blonde", 100),
}


class ColorEyeEnum:
  NONE = 0
  HAZEL = 1
  GRAY = 2
  VIOLET = 3
  GREEN = 4
  BLUE = 5


color_eyes = {
    ColorEyeEnum.HAZEL: AttrNameMax("Hazel", 40),
    ColorEyeEnum.GRAY: AttrNameMax("Gray", 55),
    ColorEyeEnum.VIOLET: AttrNameMax("Violet", 56),
    ColorEyeEnum.GREEN: AttrNameMax("Green", 70),
    ColorEyeEnum.BLUE: AttrNameMax("Blue", 200),
}


# ATTRIBUTES

class AttrClassEnum(IntEnum):
  NONE = 0
  BIRTH = 1
  APPEARANCE = 2
  PHYSICAL = 3
  PERSONALITY = 4
  OCCUPATION = 5


class AttrClass:
  def __init__(self, name, hidden=False):
    self.Name = name
    self.Hidden = hidden


attribute_classes = {
    AttrClassEnum.BIRTH: AttrClass("Birth", hidden=True),
    AttrClassEnum.APPEARANCE: AttrClass("Appearance", hidden=True),
    AttrClassEnum.PHYSICAL: AttrClass("Physical"),
    AttrClassEnum.PERSONALITY: AttrClass("Personality"),
    AttrClassEnum.OCCUPATION: AttrClass("Occupation", hidden=True),
}


class AttrEnum(IntEnum):
  NONE = 0
  # BIRTH
  SPECIES = 10
  SEX = 11
  BIRTH_MONTH = 12
  BIRTH_DAY = 13
  CULTURE = 14
  SOCIAL_CLASS = 15
  SIBLING_RANK = 16
  SIBLING_COUNT = 17
  PARENT = 18
  PARENT_SUB = 19
  ESTRANGEMENT = 20
  CLANHEAD = 21
  # APPEARANCE
  HEIGHT = 30
  FRAME = 31
  WEIGHT = 32
  COMELINESS = 33
  COMPLEXION = 34
  COLOR_HAIR = 35
  COLOR_EYE = 36
  # PHYSICAL
  STRENGTH = 50
  STAMINA = 51
  DEXTERITY = 52
  AGILITY = 53
  EYESIGHT = 54
  HEARING = 55
  SMELL = 56
  VOICE = 57
  MEDICAL = 58
  # PERSONALITY
  INTELLIGENCE = 70
  AURA = 71
  WILL = 72
  PSYCHE = 73
  # OCCUPATION
  OCCUPATION = 80


ATTR_SPE = AttrEnum.SPECIES
ATTR_SEX = AttrEnum.SEX
ATTR_BMO = AttrEnum.BIRTH_MONTH
ATTR_BDY = AttrEnum.BIRTH_DAY
ATTR_CUL = AttrEnum.CULTURE
ATTR_CLS = AttrEnum.SOCIAL_CLASS
ATTR_SIB = AttrEnum.SIBLING_RANK
ATTR_SBC = AttrEnum.SIBLING_COUNT
ATTR_PR1 = AttrEnum.PARENT
ATTR_PR2 = AttrEnum.PARENT_SUB
ATTR_EST = AttrEnum.ESTRANGEMENT
ATTR_CLN = AttrEnum.CLANHEAD
ATTR_HGT = AttrEnum.HEIGHT
ATTR_FRM = AttrEnum.FRAME
ATTR_WGT = AttrEnum.WEIGHT
ATTR_CML = AttrEnum.COMELINESS
ATTR_CPL = AttrEnum.COMPLEXION
ATTR_CHR = AttrEnum.COLOR_HAIR
ATTR_CEY = AttrEnum.COLOR_EYE
ATTR_STR = AttrEnum.STRENGTH
ATTR_STA = AttrEnum.STAMINA
ATTR_DEX = AttrEnum.DEXTERITY
ATTR_AGL = AttrEnum.AGILITY
ATTR_HRG = AttrEnum.HEARING
ATTR_EYE = AttrEnum.EYESIGHT
ATTR_SML = AttrEnum.SMELL
ATTR_VOI = AttrEnum.VOICE
ATTR_MED = AttrEnum.MEDICAL
ATTR_INT = AttrEnum.INTELLIGENCE
ATTR_AUR = AttrEnum.AURA
ATTR_WIL = AttrEnum.WILL
ATTR_PSY = AttrEnum.PSYCHE
ATTR_OCC = AttrEnum.OCCUPATION


class Attr:
  def __init__(self, abbrev, name, attr_class, rolls, dice, mod,
               roll_flags=0, hidden=False):
    self.Abbrev = abbrev
    self.Name = name
    self.AttrClass = attr_class
    self.GenRolls = rolls
    self.GenDice = dice
    self.GenMod = mod
    self.GenFlags = roll_flags
    self.Hidden = hidden


attributes = {
    # BIRTH
    ATTR_SPE: Attr("SPE", "Species", AttrClassEnum.BIRTH, 1, 1, 0),
    ATTR_SEX: Attr("SEX", "Sex", AttrClassEnum.BIRTH, 1, 100, 0),
    ATTR_BMO: Attr("BMO", "Birth Month", AttrClassEnum.BIRTH, 1, 12, 0),
    ATTR_BDY: Attr("BDY", "Birth Day", AttrClassEnum.BIRTH, 1, 30, 0),
    ATTR_CUL: Attr("CUL", "Culture", AttrClassEnum.BIRTH, 1, 100, 0),
    ATTR_CLS: Attr("CLS", "Social Class", AttrClassEnum.BIRTH, 1, 100, 0),
    ATTR_SIB: Attr("SIB", "Sibling Rank", AttrClassEnum.BIRTH, 1, 100, 0),
    ATTR_SBC: Attr("SBC", "Sibling Count", AttrClassEnum.BIRTH, 1, 6, -1),
    ATTR_PR1: Attr("PR1", "Parent Status", AttrClassEnum.BIRTH, 1, 100, 0),
    ATTR_PR2: Attr("PR2", "Parent Status2", AttrClassEnum.BIRTH, 1, 100, 0),
    ATTR_EST: Attr("EST", "Estrangement", AttrClassEnum.BIRTH, 1, 100, 0),
    ATTR_CLN: Attr("CLN", "Clanhead", AttrClassEnum.BIRTH, 1, 100, 0),
    # APPEARANCE
    ATTR_HGT: Attr("HGT", "Height", AttrClassEnum.APPEARANCE, 4, 6, 54),
    ATTR_FRM: Attr("FRM", "Frame", AttrClassEnum.APPEARANCE, 3, 6, 0),
    ATTR_WGT: Attr("WGT", "Weight", AttrClassEnum.APPEARANCE, 1, 1, 0),
    ATTR_CML: Attr("CML", "Comeliness", AttrClassEnum.APPEARANCE, 3, 6, 0),
    ATTR_CPL: Attr("CPL", "Complexion", AttrClassEnum.APPEARANCE, 1, 100, 0),
    ATTR_CHR: Attr("CHR", "Hair Color", AttrClassEnum.APPEARANCE, 1, 100, 0),
    ATTR_CEY: Attr("CEY", "Eye Color", AttrClassEnum.APPEARANCE, 1, 100, 0),
    # PHYSICAL
    ATTR_STR: Attr("STR", "Strength", AttrClassEnum.PHYSICAL, 0, 0, 10),
    ATTR_STA: Attr("STA", "Stamina", AttrClassEnum.PHYSICAL, 0, 0, 10),
    ATTR_DEX: Attr("DEX", "Dexterity", AttrClassEnum.PHYSICAL, 0, 0, 10),
    ATTR_AGL: Attr("AGL", "Agility", AttrClassEnum.PHYSICAL, 0, 0, 10),
    ATTR_EYE: Attr("EYE", "Eyesight", AttrClassEnum.PHYSICAL, 0, 0, 10),
    ATTR_HRG: Attr("HRG", "Hearing", AttrClassEnum.PHYSICAL, 0, 0, 10),
    ATTR_SML: Attr("SML", "Smelling", AttrClassEnum.PHYSICAL, 0, 0, 10),
    ATTR_VOI: Attr("VOI", "Voice", AttrClassEnum.PHYSICAL, 0, 0, 10),
    ATTR_MED: Attr("MED", "Medical", AttrClassEnum.PHYSICAL, 1, 100, 0,
                   hidden=True),
    # PERSONALITY
    ATTR_INT: Attr("INT", "Intelligence", AttrClassEnum.PERSONALITY, 0, 0, 10),
    ATTR_AUR: Attr("AUR", "Aura", AttrClassEnum.PERSONALITY, 0, 0, 10),
    ATTR_WIL: Attr("WIL", "Will", AttrClassEnum.PERSONALITY, 0, 0, 10),
    ATTR_PSY: Attr("PSY", "Psyche", AttrClassEnum.PERSONALITY, 1, 100, 0, hidden=True),
    # OCCUPATION
    ATTR_OCC: Attr("OCC", "Occupation", AttrClassEnum.OCCUPATION, 1, 100, 0),
}


# SKILLS

class SkillClassEnum(IntEnum):
  NONE = 0
  PHYSICAL = 1
  COMMUNICATION = 2
  RELIGION = 3
  COMBAT = 4
  LORE_CRAFTS = 5


skill_classes = {
    SkillClassEnum.PHYSICAL: AttrClass("Physical"),
    SkillClassEnum.COMMUNICATION: AttrClass("Communication"),
    SkillClassEnum.RELIGION: AttrClass("Religion", hidden=True),
    SkillClassEnum.COMBAT: AttrClass("Combat"),
    SkillClassEnum.LORE_CRAFTS: AttrClass("Lore & Crafts"),
}


class SkillEnum(IntEnum):
  NONE = 0
  # PHYSICAL
  ACROBATICS = 100
  CLIMBING = 101
  CONDITIONING = 102
  DANCING = 103
  DODGE = 104
  JUMPING = 105
  LEGERDEMAIN = 106
  STEALTH = 107
  SWIMMING = 108
  THROWING = 109
  # COMMUNICATION
  AWARENESS = 200
  INTRIGUE = 201
  MENTAL_CONFLICT = 202
  ORATORY = 203
  RHETORIC = 204
  SINGING = 205
  # COMBAT
  INITIATIVE = 300
  UNARMED = 301
  RIDING = 302
  AXE = 303
  BLOWGUN = 304
  BOW = 305
  CLUB = 306
  DAGGER = 307
  FLAIL = 308
  NET = 309
  POLEARM = 310
  SHIELD = 311
  SLING = 312
  SPEAR = 313
  SWORD = 314
  WHIP = 315
  # LORE / CRAFT
  AGRICULTURE = 400
  ALCHEMY = 401
  ANIMALCRAFT = 402
  BREWING = 403
  COOKERY = 404
  FISHING = 405
  FLETCHING = 406
  FORAGING = 407
  HERBLORE = 408
  HIDEWORK = 409
  JEWELCRAFT = 410
  LOCKCRAFT = 411
  METALCRAFT = 412
  MINING = 413
  PHYSICIAN = 414
  SURVIVAL = 415
  TIMBERCRAFT = 416
  TRACKING = 417
  WEAPONCRAFT = 418
  WOODCRAFT = 419


class Skill:
  def __init__(self, name, skill_class, attr1=AttrEnum.NONE, attr2=AttrEnum.NONE, attr3=AttrEnum.NONE,
               oml_mod=1, apsuc=50, sunsign_mod=None, hidden=False):
    self.Name = name
    self.SkillClass = skill_class
    self.Attr1 = attr1
    self.Attr2 = attr2
    self.Attr3 = attr3
    self.OMLMod = oml_mod
    self.AttemptsPerSkillUpCheck = apsuc
    self.SunsignMod = dict()
    if sunsign_mod is not None:
      for ss, mod in sunsign_mod.items():
        self.SunsignMod.update({ss: mod})
    self.Hidden = hidden


skills = {
    # PHYSICAL
    SkillEnum.ACROBATICS:
        Skill("Acrobatics", SkillClassEnum.PHYSICAL, ATTR_STR, ATTR_AGL, ATTR_AGL, 2, 50, {SS_NAD: 2, SS_HIR: 1}),
    SkillEnum.CLIMBING:
        Skill("Climbing", SkillClassEnum.PHYSICAL, ATTR_STR, ATTR_DEX, ATTR_AGL, 3, 25, {SS_ULA: 2, SS_ARA: 2}),
    SkillEnum.CONDITIONING:
        Skill("Conditioning", SkillClassEnum.PHYSICAL, ATTR_STR, ATTR_STA, ATTR_WIL, 4, 50, {SS_ULA: 1, SS_LAD: 1}),
    SkillEnum.DANCING:
        Skill("Dancing", SkillClassEnum.PHYSICAL, ATTR_DEX, ATTR_AGL, ATTR_AGL, 2, 10, {SS_ULA: 1, SS_LAD: 1}, hidden=True),
    SkillEnum.DODGE:
        Skill("Dodge", SkillClassEnum.PHYSICAL, ATTR_AGL, ATTR_AGL, ATTR_AGL, 4, 50, {SS_HIR: 1, SS_TAR: 1, SS_TAI: 1}),
    SkillEnum.JUMPING:
        Skill("Jumping", SkillClassEnum.PHYSICAL, ATTR_STR, ATTR_AGL, ATTR_AGL, 3, 25, {SS_NAD: 2, SS_HIR: 2}),
    SkillEnum.LEGERDEMAIN:
        Skill("Legerdemain", SkillClassEnum.PHYSICAL, ATTR_DEX, ATTR_DEX, ATTR_WIL, 1, 25, {SS_SKO: 2, SS_TAI: 2, SS_TAR: 2}),
    SkillEnum.STEALTH:
        Skill("Stealth", SkillClassEnum.PHYSICAL, ATTR_AGL, ATTR_HRG, ATTR_WIL, 3, 50, {SS_HIR: 2, SS_TAR: 2, SS_TAI: 2}),
    SkillEnum.SWIMMING:
        Skill("Swimming", SkillClassEnum.PHYSICAL, ATTR_STA, ATTR_DEX, ATTR_AGL, 1, 25, {SS_SKO: 1, SS_MAS: 3, SS_LAD: 3}),
    SkillEnum.THROWING:
        Skill("Throwing", SkillClassEnum.PHYSICAL, ATTR_STR, ATTR_DEX, ATTR_EYE, 3, 25, {SS_HIR: 2, SS_TAR: 1, SS_NAD: 1}),
    # COMMUNICATION
    SkillEnum.AWARENESS:
        Skill("Awareness", SkillClassEnum.COMMUNICATION, ATTR_EYE, ATTR_HRG, ATTR_SML, 3, 50, {SS_HIR: 2, SS_TAR: 2}),
    SkillEnum.INTRIGUE:
        Skill("Intrigue", SkillClassEnum.COMMUNICATION, ATTR_INT, ATTR_AUR, ATTR_WIL, 3, 50, {SS_TAI: 1, SS_TAR: 1, SS_SKO: 1}),
    SkillEnum.MENTAL_CONFLICT:
        Skill("Mental Conflict", SkillClassEnum.COMMUNICATION, ATTR_AUR, ATTR_WIL, ATTR_WIL, 3, 50),
    SkillEnum.ORATORY:
        Skill("Oratory", SkillClassEnum.COMMUNICATION, ATTR_CML, ATTR_VOI, ATTR_INT, 2, 50, {SS_TAR: 1}),
    SkillEnum.RHETORIC:
        Skill("Rhetoric", SkillClassEnum.COMMUNICATION, ATTR_VOI, ATTR_INT, ATTR_WIL, 3, 50, {SS_TAI: 1, SS_TAR: 1, SS_SKO: 1}),
    SkillEnum.SINGING:
        Skill("Singing", SkillClassEnum.COMMUNICATION, ATTR_HRG, ATTR_VOI, ATTR_VOI, 3, 50, {SS_MAS: 1}, hidden=True),
    # COMBAT
    SkillEnum.INITIATIVE:
        Skill("Initiative", SkillClassEnum.COMBAT, ATTR_AGL, ATTR_WIL, ATTR_WIL, 3, 50),
    SkillEnum.UNARMED:
        Skill("Unarmed Combat", SkillClassEnum.COMBAT, ATTR_STR, ATTR_DEX, ATTR_AGL, 4, 50, {SS_MAS: 2, SS_LAD: 2, SS_ULA: 2}),
    SkillEnum.RIDING:
        Skill("Riding", SkillClassEnum.COMBAT, ATTR_DEX, ATTR_AGL, ATTR_WIL, 1, 50, {SS_ULA: 1, SS_ARA: 1}),
    SkillEnum.AXE:
        Skill("Axe", SkillClassEnum.COMBAT, ATTR_STR, ATTR_STR, ATTR_DEX, 4, 50, {SS_AHN: 1, SS_FEN: 1, SS_ANG: 1}),
    SkillEnum.BLOWGUN:
        Skill("Blowgun", SkillClassEnum.COMBAT, ATTR_STA, ATTR_DEX, ATTR_EYE, 4, 50, {SS_HIR: 2, SS_TAR: 1, SS_NAD: 1}),
    SkillEnum.BOW:
        Skill("Bow", SkillClassEnum.COMBAT, ATTR_STR, ATTR_DEX, ATTR_EYE, 4, 50, {SS_HIR: 1, SS_TAR: 1, SS_NAD: 1}),
    SkillEnum.CLUB:
        Skill("Club", SkillClassEnum.COMBAT, ATTR_STR, ATTR_STR, ATTR_DEX, 4, 50, {SS_ULA: 1, SS_ARA: 1}),
    SkillEnum.DAGGER:
        Skill("Dagger", SkillClassEnum.COMBAT, ATTR_DEX, ATTR_DEX, ATTR_EYE, 4, 50, {SS_ANG: 2, SS_NAD: 2}),
    SkillEnum.FLAIL:
        Skill("Flail", SkillClassEnum.COMBAT, ATTR_DEX, ATTR_DEX, ATTR_DEX, 4, 50, {SS_HIR: 1, SS_TAR: 1, SS_NAD: 1}),
    SkillEnum.NET:
        Skill("Net", SkillClassEnum.COMBAT, ATTR_DEX, ATTR_DEX, ATTR_EYE, 4, 50, {SS_MAS: 1, SS_SKO: 1, SS_LAD: 1}),
    SkillEnum.POLEARM:
        Skill("Polearm", SkillClassEnum.COMBAT, ATTR_STR, ATTR_STR, ATTR_DEX, 4, 50, {SS_ANG: 1, SS_ARA: 1}),
    SkillEnum.SHIELD:
        Skill("Shield", SkillClassEnum.COMBAT, ATTR_STR, ATTR_DEX, ATTR_DEX, 4, 50, {SS_ULA: 1, SS_LAD: 1, SS_MAS: 1}),
    SkillEnum.SLING:
        Skill("Sling", SkillClassEnum.COMBAT, ATTR_DEX, ATTR_DEX, ATTR_EYE, 4, 50, {SS_HIR: 1, SS_TAR: 1, SS_NAD: 1}),
    SkillEnum.SPEAR:
        Skill("Spear", SkillClassEnum.COMBAT, ATTR_STR, ATTR_STR, ATTR_DEX, 4, 50, {SS_ARA: 1, SS_FEN: 1, SS_ULA: 1}),
    SkillEnum.SWORD:
        Skill("Sword", SkillClassEnum.COMBAT, ATTR_STR, ATTR_DEX, ATTR_DEX, 4, 50, {SS_ANG: 3, SS_AHN: 1, SS_NAD: 1}),
    SkillEnum.WHIP:
        Skill("Whip", SkillClassEnum.COMBAT, ATTR_DEX, ATTR_DEX, ATTR_EYE, 4, 50, {SS_HIR: 1, SS_NAD: 1}),
    # LORE / CRAFT
    SkillEnum.AGRICULTURE:
        Skill("Agriculture", SkillClassEnum.LORE_CRAFTS, ATTR_STR, ATTR_STA, ATTR_WIL, 2, 10, {SS_ULA: 2, SS_ARA: 2}),
    SkillEnum.ALCHEMY:
        Skill("Alchemy", SkillClassEnum.LORE_CRAFTS, ATTR_SML, ATTR_INT, ATTR_AUR, 1, 10, {SS_SKO: 3, SS_TAI: 2, SS_MAS: 2}),
    SkillEnum.ANIMALCRAFT:
        Skill("Animalcraft", SkillClassEnum.LORE_CRAFTS, ATTR_AGL, ATTR_VOI, ATTR_WIL, 1, 10, {SS_ULA: 1, SS_ARA: 1}),
    SkillEnum.BREWING:
        Skill("Brewing", SkillClassEnum.LORE_CRAFTS, ATTR_DEX, ATTR_SML, ATTR_SML, 2, 10, {SS_SKO: 3, SS_TAI: 2, SS_MAS: 2}),
    SkillEnum.COOKERY:
        Skill("Cookery", SkillClassEnum.LORE_CRAFTS, ATTR_DEX, ATTR_SML, ATTR_SML, 3, 10, {SS_SKO: 1}),
    SkillEnum.FISHING:
        Skill("Fishing", SkillClassEnum.LORE_CRAFTS, ATTR_DEX, ATTR_EYE, ATTR_WIL, 3, 10, {SS_MAS: 2, SS_LAD: 2}),
    SkillEnum.FLETCHING:
        Skill("Fletching", SkillClassEnum.LORE_CRAFTS, ATTR_DEX, ATTR_DEX, ATTR_EYE, 1, 10, {SS_HIR: 2, SS_TAR: 1, SS_NAD: 1}),
    SkillEnum.FORAGING:
        Skill("Foraging", SkillClassEnum.LORE_CRAFTS, ATTR_DEX, ATTR_SML, ATTR_INT, 3, 10, {SS_ULA: 2, SS_ARA: 2}),
    SkillEnum.HERBLORE:
        Skill("Herblore", SkillClassEnum.LORE_CRAFTS, ATTR_EYE, ATTR_SML, ATTR_INT, 1, 10, {SS_ULA: 3, SS_ARA: 2}),
    SkillEnum.HIDEWORK:
        Skill("Hidework", SkillClassEnum.LORE_CRAFTS, ATTR_EYE, ATTR_SML, ATTR_WIL, 2, 10, {SS_ULA: 1, SS_ARA: 1}),
    SkillEnum.JEWELCRAFT:
        Skill("Jewelcraft", SkillClassEnum.LORE_CRAFTS, ATTR_DEX, ATTR_EYE, ATTR_WIL, 1, 10, {SS_FEN: 3, SS_TAR: 1, SS_ARA: 1}),
    SkillEnum.LOCKCRAFT:
        Skill("Lockcraft", SkillClassEnum.LORE_CRAFTS, ATTR_DEX, ATTR_EYE, ATTR_WIL, 1, 10, {SS_FEN: 3}),
    SkillEnum.METALCRAFT:
        Skill("Metalcraft", SkillClassEnum.LORE_CRAFTS, ATTR_STR, ATTR_DEX, ATTR_WIL, 1, 10, {SS_FEN: 3, SS_AHN: 1, SS_ANG: 1}),
    SkillEnum.MINING:
        Skill("Mining", SkillClassEnum.LORE_CRAFTS, ATTR_STR, ATTR_DEX, ATTR_INT, 1, 10, {SS_ULA: 2, SS_ARA: 2, SS_FEN: 1}),
    SkillEnum.PHYSICIAN:
        Skill("Physician", SkillClassEnum.LORE_CRAFTS, ATTR_DEX, ATTR_EYE, ATTR_INT, 1, 10, {SS_MAS: 2, SS_SKO: 1, SS_TAI: 1}),
    SkillEnum.SURVIVAL:
        Skill("Survival", SkillClassEnum.LORE_CRAFTS, ATTR_STR, ATTR_DEX, ATTR_INT, 3, 10, {SS_ULA: 2, SS_ARA: 1}),
    SkillEnum.TIMBERCRAFT:
        Skill("Timbercraft", SkillClassEnum.LORE_CRAFTS, ATTR_STR, ATTR_DEX, ATTR_AGL, 2, 10, {SS_ULA: 3, SS_ARA: 1}),
    SkillEnum.TRACKING:
        Skill("Tracking", SkillClassEnum.LORE_CRAFTS, ATTR_EYE, ATTR_SML, ATTR_WIL, 2, 10, {SS_ULA: 3, SS_ARA: 3}),
    SkillEnum.WEAPONCRAFT:
        Skill("Weaponcraft", SkillClassEnum.LORE_CRAFTS, ATTR_STR, ATTR_DEX, ATTR_WIL, 1, 10, {SS_FEN: 3, SS_AHN: 1, SS_ANG: 1}),
    SkillEnum.WOODCRAFT:
        Skill("Woodcraft", SkillClassEnum.LORE_CRAFTS, ATTR_DEX, ATTR_DEX, ATTR_WIL, 2, 10, {SS_ULA: 2, SS_ARA: 2, SS_LAD: 1}),
}


class SkillLink:
  def __init__(self, points=0, att=0):
    self.Points = points
    self.Attempts = att


# GENERIC PERSON

class PersonEnum(IntEnum):
  NONE = 0
  MON_RAT = 100
  MON_RAT_LARGE = 101
  MON_RAT_GUARD = 102
  MON_RAT_NOBLE = 103
  BL_KEEP_GUARD = 10000
  BL_KEEP_SENTRY = 10001
  BL_KEEP_BEGGAR = 10002
  BL_KEEP_CORPORAL_WATCH = 10010
  BL_KEEP_YARD_SCRIBE = 10011
  BL_SMITHY = 10015
  BL_PROVISIONER = 10020
  BL_TANNER = 10021
  BL_ARMS_DEALER = 10030


class PersonTypeEnum(IntEnum):
  PLAYER = 0
  NPC = 1


class PersonFlag(IntEnum):
  AGGRESSIVE = 1 << 0
  BEHAVIOR_1 = 1 << 6
  BEHAVIOR_2 = 1 << 7
  PERIODIC_TRIGGERED = 1 << 15  # keep in sync with gamedata


class WoundDesc:
  def __init__(self, name, verbs, ip_bonus=0):
    self.Name = name
    self.Verbs = verbs
    self.IPBonus = ip_bonus


wounds = {
    ImpactActionEnum.WOUND_MLD: WoundDesc("Mild", ["Bruised", "Cut", "Poked", "Singed"], 0),
    ImpactActionEnum.WOUND_SRS: WoundDesc("Serious", ["Crushed", "Slashed", "Stabbed", "Scorched"], 5),
    ImpactActionEnum.WOUND_GRV: WoundDesc("Grievous", ["Pulverized", "Shredded", "Skewered", "Cremated"], 10),
}


class PersonWound:
  def __init__(self, wound_type, dmg_type, loc, impact):
    self.WoundType = wound_type
    self.DamageType = dmg_type
    self.Location = loc
    self.Impact = impact

  def __eq__(self, other):
    if self.Impact == other.Impact:
      if self.WoundType == other.WoundType:
        if self.Location == other.Location:
          if self.DamageType == other.DamageType:
            return True
    return False

  def __gt__(self, other):
    if self.Impact <= other.Impact:
      if self.WoundType <= other.WoundType:
        if self.Location <= other.Location:
          if self.DamageType <= other.DamageType:
            return False
    return True

  def __lt__(self, other):
    if self.Impact >= other.Impact:
      if self.WoundType >= other.WoundType:
        if self.Location >= other.Location:
          if self.DamageType >= other.DamageType:
            return False
    return True


class Person:
  def __init__(self, person_type, name, long_desc="", flags=0, skin=MaterialEnum.NONE, it=None, frame=0):
    self.PersonType = person_type
    self.Name = name
    self.LongDescription = long_desc
    self.DefaultAim = AimEnum.MID
    self.Flags = flags
    self.Talk = None
    self.SkinMaterial = skin
    self.Attr = dict()
    self.SkillLinks = dict()
    self.Frame = frame
    self.Wounds = []
    self.Effects = []
    self.Items = []
    if it is not None:
      for i in it:
        self.AddItem(i, i.Equipped)

  def Copy(self, p):
    self.PersonType = p.PersonType
    self.Name = p.Name
    self.Flags = p.Flags
    self.Talk = None
    self.SkinMaterial = p.SkinMaterial
    self.Attr.clear()
    for attr_id, attr in attributes.items():
      if attr_id in p.Attr:
        self.Attr.update({attr_id: p.Attr[attr_id]})
      else:
        # add new attributes
        self.Attr.update({attr_id: DiceRoll(attr.GenRolls, attr.GenDice, flags=attr.GenFlags).Result() + attr.GenMod})
    self.SkillLinks.clear()
    # copy all skills into skill training
    for skill_id, skill in skills.items():
      if skill_id in p.SkillLinks:
        self.SkillLinks.update({skill_id: p.SkillLinks[skill_id]})
      else:
        points = 0
        for ss_id, mod in skill.SunsignMod.items():
          if self.Sunsign == ss_id:
            points += mod
            break
        # add new skills
        self.SkillLinks.update({skill_id: SkillLink(points)})
    self.Wounds.clear()
    for x in p.Wounds:
      self.Wounds.append(x)
    self.Effects.clear()
    for x in p.Effects:
      self.Effects.append(Effect(EffectTypeEnum.NONE, 0, 0).Copy(x))
    self.Items.clear()
    for it in p.Items:
      self.AddItem(it, it.Equipped)

  def ResetStats(self):
    self.Effects.clear()

  def CalcEffect(self, efType, efValue):
    ret = 0
    if self.Effects is not None:
      for eff in self.Effects:
        if eff.EffectType == efType and eff.Value == efValue:
          ret += eff.Modifier
    if self.Items is not None:
      for it in self.Items:
        if it.Equipped and it.Effects is not None:
          for eff in it.Effects:
            if eff.EffectType == efType and eff.Value == efValue:
              ret += eff.Modifier
    return ret

  def GetAttr(self, attr):
    if attr in self.Attr:
      return self.Attr[attr] + self.CalcEffect(EffectTypeEnum.ATTRIBUTE, attr)
    else:
      return 0

  def AddItem(self, item, equipped=False):
    effs = item.Effects
    item.Effects = None
    i = deepcopy(item)
    i.UUID = uuid4()
    i.Equipped = equipped
    if effs is not None:
      cm = GameData.GetConsole()
      i.Effects = []
      for eff in effs:
        e = Effect(EffectTypeEnum.NONE, 0, 0)
        e.Copy(eff)
        i.Effects.append(e)
      del effs
    self.Items.append(i)
    return True

  def AttachItem(self, item, equipped=False):
    item.Equipped = equipped
    self.Items.append(item)
    return True

  def RemoveItem(self, it):
    for item in self.Items:
      if item.UUID == it.UUID:
        self.Items.remove(item)
        return True
    return False

  def HasItem(self, item_name):
    for item in self.Items:
      if item.ItemName.lower() == item_name.lower():
        return item
    return None

  def AttrSex(self):
    ret = SexEnum.NONE
    for s_id, s in sexes.items():
      if self.Attr[AttrEnum.SEX] <= s.AttrMax:
        ret = s_id
        break
    return ret

  def AttrSexStr(self):
    return sexes[self.AttrSex()].Name

  def AttrSexPronounStr(self):
    return sexes[self.AttrSex()].Pronoun

  def AttrSexPossessivePronounStr(self):
    return sexes[self.AttrSex()].PossessivePronoun

  def TextTranslate(self, text):
    ret = text.replace("@@NAME@@", self.Name)
    ret = ret.replace("@@NAME_CAP@@", self.Name.capitalize())
    ret = ret.replace("@@SEX@@", self.AttrSexStr())
    ret = ret.replace("@@SEX_CAP@@", self.AttrSexStr().capitalize())
    ret = ret.replace("@@SEX_PRONOUN@@", self.AttrSexPronounStr())
    ret = ret.replace("@@SEX_PRONOUN_CAP@@", self.AttrSexPronounStr().capitalize())
    ret = ret.replace("@@SEX_POSSESSIVE_PRONOUN@@", self.AttrSexPossessivePronounStr().lower())
    ret = ret.replace("@@SEX_POSSESSIVE_PRONOUN_CAP@@", self.AttrSexPossessivePronounStr().capitalize())
    return ret

  def IP(self):
    ret = 0
    for x in self.Wounds:
      ret += x.Impact
    return ret

  def IPIndex(self):
    ret = 0
    for x in self.Wounds:
      ret += x.Impact
    return int(ret / 10)

  def FatiguePoints(self):
    return 0

  def UniversalPenalty(self):
    ret = self.IP()
    ret += self.FatiguePoints()
    return int(ret / 10)

  def UniversalPenaltyIndex(self):
    return int(self.UniversalPenalty() / 10)

  def EquipWeight(self, equipped=True):
    eq = 0
    for item in self.Items:
      if item.Equipped == equipped:
        eq += item.Weight
    return eq

  def ItemWeight(self):
    return self.EquipWeight() * 0.5 + self.EquipWeight(False)

  def FatigueRate(self):
    return self.ItemWeight() / self.AttrEndurance()

  def EncumbrancePenalty(self):
    return round(self.FatigueRate() * 3)

  def PhysicalPenalty(self):
    ret = self.IP()
    ret += self.FatiguePoints()
    ret += self.EncumbrancePenalty()
    return int(ret / 10)

  def SkillBase(self, skill_id):
    attr1 = 0
    attr2 = 0
    attr3 = 0
    if skills[skill_id].Attr1 in self.Attr:
      attr1 = self.GetAttr(skills[skill_id].Attr1)
    if skills[skill_id].Attr2 in self.Attr:
      attr2 = self.GetAttr(skills[skill_id].Attr2)
    if skills[skill_id].Attr3 in self.Attr:
      attr3 = self.GetAttr(skills[skill_id].Attr3)
    sb = round((attr1 + attr2 + attr3) / 3)
    return sb

  def SkillAttempts(self, skill_id):
    ret = 0
    if skill_id in self.SkillLinks:
      ret = self.SkillLinks[skill_id].Attempts
    return ret

  def SkillML(self, skill_id, skipPenalty=False):
    ml = self.SkillBase(skill_id) * skills[skill_id].OMLMod
    if skill_id in self.SkillLinks:
      ml += self.SkillLinks[skill_id].Points
    ml += self.CalcEffect(EffectTypeEnum.SKILL, skill_id)
    if not skipPenalty:
      if skills[skill_id].SkillClass == SkillClassEnum.PHYSICAL or skills[skill_id].SkillClass == SkillClassEnum.COMBAT:
        ml -= (self.PhysicalPenalty() * 5)
      else:
        ml -= (self.UniversalPenalty() * 5)
    if ml < 5:
      ml = 5
    return ml

  def SkillIndex(self, skill_id):
    return round(self.SkillML(skill_id) / 10)

  def SkillMax(self, skill_id):
    return 100 + self.SkillBase(skill_id)

  def ResolveSkill(self, ml, skill_id):
    if type(self) is Player:
      # store attempts
      if skill_id != SkillEnum.NONE:
        if self.SkillML(skill_id, True) < self.SkillMax(skill_id):
          if skill_id in self.SkillLinks:
            self.SkillLinks[skill_id].Attempts += 1
          else:
            self.SkillLinks.update({skill_id: SkillLink(0, 1)})
          # check for skillup
          if self.SkillLinks[skill_id].Attempts > skills[skill_id].AttemptsPerSkillUpCheck:
            # attempt to raise skill
            r = DiceRoll(1, 100).Result() + self.SkillBase(skill_id)
            if r > self.SkillML(skill_id, skipPenalty=True):
              GameData.GetConsole().Print("\nYou've become better at the %s skill!" % (skills[skill_id].Name.lower()))
              self.SkillLinks[skill_id].Points += 1
            self.SkillLinks[skill_id].Attempts -= skills[skill_id].AttemptsPerSkillUpCheck
    r = DiceRoll(1, 100).Result()
    if ml < 5:
      ml = 5
    elif ml > 95:
      ml = 95
    logd("%s RESOLVE SKILL [%s]: %d, ROLL: %d" % (self.Name, skills[skill_id].Name, ml, r))
    # success
    if r <= ml:
      if r % 5 == 0:
        return Roll.CS
      else:
        return Roll.MS
    # failure
    else:
      if r % 5 == 0:
        return Roll.CF
      else:
        return Roll.MF

  def Defense(self, bp_id, dmg_type):
    m = Material("None", 0, 0, [0, 0, 0, 0])
    m.Copy(materials[self.SkinMaterial])
    for item in self.Items:
      if item.ItemType != ItemTypeEnum.ARMOR:
        continue
      if not item.Equipped:
        continue
      if item.Covered(bp_id):
        m.Add(materials[item.Material])
    return m.Protection[dmg_type]

  def AttrInitiative(self):
    return self.SkillML(SkillEnum.INITIATIVE)

  def AttrEndurance(self):
    sb = self.SkillBase(SkillEnum.CONDITIONING)
    ml = self.SkillML(SkillEnum.CONDITIONING, skipPenalty=True)
    return round(sb + (ml / sb - skills[SkillEnum.CONDITIONING].OMLMod))

  def AttrDodge(self):
    return self.SkillML(SkillEnum.DODGE)

  def IsAggressive(self):
    return self.Flags & PersonFlag.AGGRESSIVE > 0

  def IsTalking(self):
    return self.Talk is not None

  def SetTalking(self, talk):
    self.Talk = talk

  def GenerateCombatAttacks(self, block=False):
    default = Weapon("punch", QualityEnum.AVE, MaterialEnum.BONE, 0,
                     SkillEnum.UNARMED, 0, 5, 0, DiceRoll(1, 2), DamageTypeEnum.BLUNT)
    attacks = []
    # count hands used
    count = 0
    def_skill = 0
    def_item = None
    for item in self.Items:
      if not item.Equipped:
        continue
      if item.ItemType == ItemTypeEnum.WEAPON or item.ItemType == ItemTypeEnum.SHIELD:
        if block:
          skill = self.SkillML(item.Skill)
          skill += item.DefenseRating
          if skill > def_skill:
            def_skill = skill
            def_item = item
        count += 1
    # create attacks
    # for BLOCK only generate the blocking weapon / shield
    if block:
      if def_item is None:
        return attacks
      skill_id = def_item.Skill
      ml = self.SkillML(skill_id)
      ml += def_item.DefenseRating
      attacks.append(CombatAttack(def_item.ItemName, ml, skill_id, def_item, None, DamageTypeEnum.BLUNT))
    else:
      for item in self.Items:
        if not item.Equipped:
          continue
        if item.ItemType == ItemTypeEnum.WEAPON:
          skill_id = item.Skill
          ml = self.SkillML(skill_id)
          ml += item.AttackRating
          if count > 1:
            ml -= item.SingleHandPenalty
          attacks.append(CombatAttack(item.ItemName, ml, skill_id, item, item.Roll,
                                      item.DamageType))
    if len(attacks) < 1 and default is not None:
      skill_id = default.Skill
      ml = self.SkillML(skill_id)
      ml += default.AttackRating
      attacks.append(CombatAttack(default.ItemName, ml, skill_id, default, default.Roll,
                                  default.DamageType))
    return attacks

  def HasLight(self):
    if self.Items is not None:
      for item in self.Items:
        if item.IsLight():
          return True
    return False


# CONDITIONALS

class TargetTypeEnum(IntEnum):
  NONE = 0
  PLAYER_INVEN = 1
  PLAYER_QUEST = 2
  PLAYER_QUEST_COMPLETE = 3
  ITEM_IN_ROOM = 4
  MOB_IN_ROOM = 5
  LOCATED_IN_ROOM = 6
  PERCENT_CHANCE = 7
  ATTR_CHECK = 8
  SKILL_CHECK = 9
  HOUR_OF_DAY_CHECK = 10
  MONTH_CHECK = 11
  DAYLIGHT_CHECK = 12
  MOONPHASE_CHECK = 13
  FLAG_CHECK = 14


class ConditionCheckEnum(IntEnum):
  NONE = 0
  HAS = 1
  HAS_NOT = 2
  GREATER_THAN = 3
  EQUAL_TO = 4
  LESS_THAN = 5


class TriggerTypeEnum(IntEnum):
  NONE = 0
  ITEM_GIVE = 1
  ITEM_TAKE = 2
  ITEM_BUY = 3
  ITEM_SELL = 4
  ROOM_SPAWN_MOB = 5
  ROOM_DESPAWN_MOB = 6
  CURRENCY_GIVE = 7
  CURRENCY_TAKE = 8
  QUEST_GIVE = 9
  QUEST_COMPLETE = 10
  PERSON_ATTACK = 11
  PERSON_DESC = 12
  ZONE_MESSAGE = 13
  MESSAGE = 14
  MOVE = 15
  DELAY = 16
  DENY = 17
  GIVE_FLAG = 18
  TAKE_FLAG = 19
  PERSON_MOVE = 20
  DOOR_UNLOCK = 21
  DOOR_LOCK = 22
  PAUSE = 23
  ROOM_SPAWN_ITEM = 24
  ROOM_DESPAWN_ITEM = 25
  EFFECT_ATTR = 26
  EFFECT_SKILL = 27
  END = 127


class Condition:
  def __init__(self, cond, target_type=TargetTypeEnum.NONE, data=None, value=0):
    self.ConditionCheck = cond
    self.TargetType = target_type
    self.Data = data
    self.Value = value


class Trigger:
  def __init__(self, trigger_type, data=None, data2=None, data3=None, chance=100):
    self.TriggerType = trigger_type
    self.Data = data
    self.Data2 = data2
    self.Data3 = data2
    self.Chance = chance


# PERIODIC

class Periodic:
  def __init__(self, conditions, triggers, delay=60):
    self.Conditions = conditions
    self.Triggers = triggers
    self.DelaySeconds = delay
    self.LastCheck = 0


# TALK

class MobTalk:
  def __init__(self, keyword, conditions=None, triggers=None):
    self.Keyword = keyword
    self.Conditions = conditions
    self.Triggers = triggers


# MOB

class MobAttack:
  def __init__(self, name, chance, ml, ar=0, dr=0, dmg=None,
               dmg_type=DamageTypeEnum.BLUNT):
    self.Name = name
    self.ChanceMax = chance
    self.SkillML = ml
    self.AttackRating = ar
    self.DefenseRating = dr
    self.Damage = dmg
    self.DamageType = dmg_type


class Mob(Person):
  def __init__(self, person_id, name, long_desc, ini, end, dodge, aim=AimEnum.MID, flags=0,
               skin=MaterialEnum.NONE, cur=None, attrs=None, num_attacks=1, mob_attacks=None, mob_skills=None, eq=None,
               loot=None, sell_items=None, buy_items=None, talk=None, periodics=None, frame=0):
    super().__init__(PersonTypeEnum.NPC, name, long_desc, flags, skin, it=eq, frame=frame)
    # None == Template / Char
    self.UUID = None
    self.PersonID = person_id
    self.CurrencyGen = cur
    self.Initiative = ini
    self.Endurance = end
    self.Dodge = dodge
    self.DefaultAim = aim
    self.NumAttacks = num_attacks
    self.MobAttacks = mob_attacks
    if attrs is not None:
      for attr_id, value in attrs.items():
        self.Attr.update({attr_id: value})
    if mob_skills is not None:
      for skill_id, points in mob_skills.items():
        self.SkillLinks.update({skill_id: SkillLink(points)})
    self.Loot = loot
    self.SellItems = sell_items
    self.BuyItems = buy_items
    self.DelayTimestamp = 0
    self.DelaySeconds = 0
    self.Talks = talk
    self.Periodics = periodics
    super().ResetStats()

  def AttrInitiative(self):
    return self.Initiative - (self.PhysicalPenalty() * 5)

  def AttrEndurance(self):
    return self.Endurance

  def AttrDodge(self):
    return self.Dodge - (self.PhysicalPenalty() * 5)

  def GenerateCombatAttacks(self, block=False):
    attacks = []
    # Look for a "natural" attack
    if not block and self.MobAttacks is not None:
      for a in range(self.NumAttacks):
        for ma in self.MobAttacks:
          if DiceRoll(1, 100).Result() <= ma.ChanceMax:
            ml = ma.SkillML + ma.AttackRating
            ml -= (self.PhysicalPenalty() * 5)
            ca = CombatAttack(ma.Name, ml, SkillEnum.UNARMED, None, ma.Damage, ma.DamageType)
            attacks.append(ca)
            break
    # Look for equipped weapons
    if len(attacks) < 1:
      attacks = super().GenerateCombatAttacks(block)
    return attacks


# PLAYER

class QuestEnum(IntEnum):
  NONE = 0
  GUARD_DELIVERY = 1
  GUARD_INTRO = 2
  WAREHOUSE_RATS = 3
  WAREHOUSE_COWL = 4
  WAREHOUSE_LEGGINGS = 5


class Quest:
  def __init__(self, name, hidden=False, triggers=None, repeatable=False):
    self.Name = name
    self.Hidden = hidden
    self.Triggers = triggers
    self.Repeatable = repeatable


quests = {
    QuestEnum.GUARD_INTRO: Quest("Talk to the guard.", hidden=True),
    QuestEnum.GUARD_DELIVERY: Quest("Deliver a weathered package to the provisioner."),
    QuestEnum.WAREHOUSE_RATS: Quest("Sell rat furs to the provisioner.", repeatable=True),
    QuestEnum.WAREHOUSE_COWL: Quest("Find the stained cowl.", hidden=True),
    QuestEnum.WAREHOUSE_LEGGINGS: Quest("Find the stained leggings.", hidden=True),
}


class PlayerQuest:
  def __init__(self, quest, complete=False):
    self.Quest = quest
    self.Complete = complete


class PlayerCombatState(IntEnum):
  NONE = 0
  WAIT = 1
  ATTACK = 2
  DEFEND = 3


class Player(Person):
  def __init__(self, name=""):
    super().__init__(PersonTypeEnum.PLAYER, name, "player")
    self.Time = int(time())  # epoch at login
    self.NewsID = 0
    self.SecondsPlayed = 0
    self.GameTime = 43200  # 12 noon
    self.LastTimeUpdate = 0
    self.Password = ""
    self.Sunsign = SunsignEnum.NONE
    self.Room = None
    self.Facing = DirectionEnum.WEST
    self.LastRoom = None
    self.Currency = 0
    self.CombatState = PlayerCombatState.NONE
    self.CombatTarget = None
    self.Doors = {}
    self.Quests = {}

  def Copy(self, p):
    super().Copy(p)
    self.Time = int(time())  # epoch at login
    try:
      self.NewsID = p.NewsID
    except:
      self.NewsID = 0
    self.SecondsPlayed = p.SecondsPlayed
    self.GameTime = p.GameTime
    self.LastTimeUpdate = p.LastTimeUpdate
    self.Room = p.Room
    try:
      self.Facing = p.Facing
    except:
      self.Facing = DirectionEnum.NORTH
    self.LastRoom = p.LastRoom
    self.Currency = p.Currency
    self.CalcSunsign()
    if p.Doors is not None:
      for door_id, state in p.Doors.items():
        self.Doors.update({door_id: deepcopy(state)})
    if p.Quests is not None:
      for quest_id, complete in p.Quests.items():
        self.Quests.update({quest_id: complete})
    super().ResetStats()

  def UpdatePlayerTime(self):
    self.SecondsPlayed += (int(time()) - self.Time)
    self.Time = int(time())

  def PlayerTime(self):
    return self.SecondsPlayed + (int(time()) - self.Time)

  def SetRoom(self, room_id):
    self.LastRoom = self.Room
    self.Room = room_id

  def CalcSunsign(self):
    for ss_id, ss in sunsigns.items():
      bm = self.Attr[AttrEnum.BIRTH_MONTH]
      bd = self.Attr[AttrEnum.BIRTH_DAY]
      if (bm == ss.StartMonth and bd >= ss.StartDay) or (bm == ss.EndMonth and bd <= ss.EndDay):
        self.Sunsign = ss_id
        break

  def GenAttr(self):
    # Generate Attributes
    for attr_id, attr in attributes.items():
      self.Attr.update({attr_id: DiceRoll(attr.GenRolls, attr.GenDice, flags=attr.GenFlags).Result() + attr.GenMod})
    # Adjustments
    # Frame: -3 Human Female
    if self.AttrSex() == SexEnum.FEMALE:
      self.Attr[AttrEnum.FRAME] -= 3
    # Calc Weight
    self.Attr[AttrEnum.WEIGHT] = player_weights[self.Attr[AttrEnum.HEIGHT]]
    self.Attr[AttrEnum.WEIGHT] *= player_frames[self.AttrFrame()].ModPercent
    # Strength: Weight Modifier
    if self.Attr[AttrEnum.WEIGHT] <= 85:
      self.Attr[AttrEnum.STRENGTH] -= 4
    elif self.Attr[AttrEnum.WEIGHT] <= 110:
      self.Attr[AttrEnum.STRENGTH] -= 3
    elif self.Attr[AttrEnum.WEIGHT] <= 130:
      self.Attr[AttrEnum.STRENGTH] -= 2
    elif self.Attr[AttrEnum.WEIGHT] <= 145:
      self.Attr[AttrEnum.STRENGTH] -= 1
    elif self.Attr[AttrEnum.WEIGHT] >= 216:
      self.Attr[AttrEnum.STRENGTH] += 4
    elif self.Attr[AttrEnum.WEIGHT] >= 191:
      self.Attr[AttrEnum.STRENGTH] += 3
    elif self.Attr[AttrEnum.WEIGHT] >= 171:
      self.Attr[AttrEnum.STRENGTH] += 2
    elif self.Attr[AttrEnum.WEIGHT] >= 156:
      self.Attr[AttrEnum.STRENGTH] += 1
    # Agility: +2 Scant Frame, +1 Light Frame, -1 Heavy Frame, -2 Massive Frame
    frame = self.AttrFrame()
    if frame == PlayerFrameEnum.SCANT:
      self.Attr[AttrEnum.AGILITY] += 2
    elif frame == PlayerFrameEnum.LIGHT:
      self.Attr[AttrEnum.AGILITY] += 1
    elif frame == PlayerFrameEnum.HEAVY:
      self.Attr[AttrEnum.AGILITY] -= 1
    elif frame == PlayerFrameEnum.MASSIVE:
      self.Attr[AttrEnum.AGILITY] -= 2
    # Hearing: +2 Tribesmen
    # Smell: +2 Tribesmen
    if self.AttrCulture() == CultureEnum.TRIBAL:
      self.Attr[AttrEnum.HEARING] += 2
      self.Attr[AttrEnum.SMELL] += 2
    self.CalcSunsign()
    # Sibling Count includes Sibling Rank
    self.Attr[AttrEnum.SIBLING_COUNT] += self.AttrSiblingRank()

  def GenSkills(self):
    for skill_id, skill in skills.items():
      points = 0
      for ss_id, mod in skill.SunsignMod.items():
        if self.Sunsign == ss_id:
          points += mod
          break
      self.SkillLinks.update({skill_id: SkillLink(points)})

  def AttrCulture(self):
    ret = CultureEnum.NONE
    for c_id, c in cultures.items():
      if self.Attr[AttrEnum.CULTURE] <= c.AttrMax:
        ret = c_id
        break
    return ret

  def AttrSocialClass(self):
    sc = SocialClassEnum.NONE
    c_id = self.AttrCulture()
    for sc_id, attr_max in cultures[c_id].SCAttrMax.items():
      if self.Attr[AttrEnum.SOCIAL_CLASS] <= attr_max:
        sc = sc_id
        break
    return sc

  def AttrSiblingRank(self):
    ret = 1
    for sr_id, sr in sibling_ranks.items():
      if self.Attr[AttrEnum.SIBLING_RANK] <= sr.AttrMax:
        ret = sr_id
        break
    return ret

  def AttrParentStatus(self):
    ret = ParentStatusEnum.NONE
    for ps_id, ps in parent_statuses.items():
      if self.Attr[AttrEnum.PARENT] <= ps.AttrMax:
        ret = ps_id
        break
    return ret

  def AttrFrame(self):
    ret = PlayerFrameEnum.NONE
    for pf_id, pf in player_frames.items():
      if self.Attr[AttrEnum.FRAME] <= pf.AttrMax:
        ret = pf_id
        break
    return ret

  def AttrComeliness(self):
    ret = ComelinessEnum.NONE
    for c_id, c in comelinesses.items():
      if self.Attr[AttrEnum.COMELINESS] <= c.AttrMax:
        ret = c_id
        break
    return ret

  def AttrColorHair(self):
    ret = ColorHairEnum.NONE
    for c_id, c in color_hairs.items():
      if self.Attr[AttrEnum.COLOR_HAIR] <= c.AttrMax:
        ret = c_id
        break
    return ret

  def AttrColorEye(self):
    ret = ColorEyeEnum.NONE
    for c_id, c in color_eyes.items():
      if self.Attr[AttrEnum.COLOR_EYE] + \
         complexions[self.AttrComplexion()].EyeColorMod <= c.AttrMax:
        ret = c_id
        break
    return ret

  def AttrComplexion(self):
    ret = ComplexionEnum.NONE
    for c_id, c in complexions.items():
      if self.Attr[AttrEnum.COMPLEXION] <= c.AttrMax:
        ret = c_id
        break
    return ret

  def GenerateCombatAttacks(self, block=False):
    return super().GenerateCombatAttacks(block)

  def DoorState(self, door_id):
    doors = GameData.GetDoors()
    if door_id in self.Doors.keys():
      return self.Doors[door_id]
    return doors[door_id].State

  def SetDoorState(self, door_id):
    doors = GameData.GetDoors()
    if door_id not in self.Doors.keys():
      self.Doors.update({door_id: deepcopy(doors[door_id].State)})
    return self.Doors[door_id]

  def AddQuest(self, quest_id):
    if quest_id not in self.Quests.keys():
      self.Quests.update({quest_id: False})

  def CompleteQuest(self, quest_id):
    if quest_id in self.Quests.keys():
      self.Quests[quest_id] = True
    else:
      self.Quests.update({quest_id: True})

  def HasQuest(self, quest_id, completed=None):
    for q_id, q_completed in self.Quests.items():
      if q_id == quest_id:
        if completed is not None:
          if completed is True and not q_completed:
            return False
          if completed is False and q_completed:
            return False
        return True
    return False

  def GameTimeYear(self):
    return int(self.GameTime / 31104000) + 720

  def GameTimeMonth(self):
    return int((self.GameTime % 31104000) / 2592000) + 1

  def GameTimeDayOfMonth(self):
    return int((self.GameTime % 2592000) / 86400) + 1

  def GameTimeMoonPhase(self):
    day = self.GameTimeDayOfMonth()
    if day == 30:
      return "new"
    elif day >= 27:
      return "waning crescent"
    elif day >= 24:
      return "waning quarter"
    elif day >= 21:
      return "waning half"
    elif day >= 18:
      return "waning three-quarter"
    elif day >= 16:
      return "waning gibbous"
    elif day == 15:
      return "full"
    elif day >= 13:
      return "waxing gibbous"
    elif day >= 10:
      return "waxing three-quarter"
    elif day >= 7:
      return "waxing half"
    elif day >= 4:
      return "waxing quarter"
    else:
      return "waxing crescent"

  def GameTimeHourOfDay(self):
    return int((self.GameTime % 86400) / 3600)

  def GameTimeMinuteOfHour(self):
    return int((self.GameTime % 3600) / 60)

  def GameTimeDateStr(self):
    day = self.GameTimeDayOfMonth()
    return "%s %d %d TR" % (months[self.GameTimeMonth()].Name, day, self.GameTimeYear())

  def GameTimeStr(self):
    return "%02d:%02d" % (self.GameTimeHourOfDay(), self.GameTimeMinuteOfHour())

  def GameTimeIsDay(self):
    hour = self.GameTimeHourOfDay()
    if hour >= 6 and hour <= 17:
      return True
    return False


# DOOR

class DoorEnum(IntEnum):
  NONE = 0
  KEEP_DRAWBRIDGE = 1
  WAREHOUSE_DBL_DOOR = 2
  CORPORAL_APPT_DOOR = 3
  N_TOWER_TRAPDOOR_LEVEL_2 = 4
  N_TOWER_TRAPDOOR_LEVEL_3 = 5
  S_TOWER_TRAPDOOR_LEVEL_2 = 6
  S_TOWER_TRAPDOOR_LEVEL_3 = 7
  WARREN_DOOR_1 = 100
  WARREN_DOOR_2 = 101


# ROOM

class RoomEnum(IntEnum):
  NONE = 0
  GAME_START = 1
  GAME_RESTORE_SAVE = 2
  GAME_CREATE_CHARACTER = 3
  BL_KEEP_GATEHOUSE = 10000
  BL_GATEHOUSE_PASSAGE = 10002
  BL_ENTRY_YARD = 10010
  BL_STABLE = 10011
  BL_N_GATEHOUSE_TOWER = 10012
  BL_N_GATEHOUSE_TOWER_LEVEL_2 = 10013
  BL_N_GATEHOUSE_TOWER_LEVEL_3 = 10014
  BL_NORTHEASTERN_WALK = 10015
  BL_EASTERN_WALK = 10020
  BL_WAREHOUSE = 10021
  BL_S_GATEHOUSE_TOWER = 10022
  BL_S_GATEHOUSE_TOWER_LEVEL_2 = 10023
  BL_S_GATEHOUSE_TOWER_LEVEL_3 = 10024
  BL_EASTERN_WALK_2 = 10025
  BL_BAILIFF_TOWER = 10026
  BL_SOUTHEASTERN_WALK = 10030
  BL_SOUTHERN_WALK = 10040
  BL_SMITHY = 10041
  BL_APARMENT_1 = 10042
  BL_SOUTHERN_WALK_2 = 10050
  BL_APARMENT_2 = 10051
  BL_SOUTHERN_WALK_3 = 10060
  BL_PROVISIONS = 10061
  BL_LEATHERWORKS = 10062
  BL_SOUTHWESTERN_WALK = 10070
  BL_WEAPONSMITH = 10071
  BL_WATCH_TOWER = 10073
  BL_FOUNTAIN_SQUARE = 10080
  BL_TAVERN_MAINROOM = 10081
  BL_TAVERN_KITCHEN = 10082
  BL_TAVERN_LOFT = 10083
  BL_MAIN_WALK = 10085
  BL_MAIN_WALK_2 = 10090
  BL_INN_ENTRYWAY = 10091
  BL_INN_COMMONROOM = 10092
  BL_INN_STAIRWAY = 10093
  BL_INN_HALLWAY_1 = 10094
  BL_INN_ROOM_1 = 10095
  BL_INN_ROOM_2 = 10096
  BL_INN_ROOM_3 = 10097
  BL_INN_OWNER_ROOM = 10098
  BL_MAIN_WALK_3 = 10099
  BL_ALLEYWAY = 10100
  BL_APARMENT_5 = 10101
  BL_MAIN_WALK_4 = 10109
  BL_ENTRY_INNER_GATEHOUSE = 10110
  BL_CHAPEL_MAINROOM = 10111
  BL_PRIEST_CHAMBER = 10112

  BL_INNER_GATEHOUSE = 10120

  BL_MID_INNER_BAILY = 10130

  BL_WEST_INNER_BAILY = 10140
  BL_NORTHWEST_GUARD_TOWER = 10141
  BL_GREATTOWER = 10142

  BL_EAST_INNER_BAILY = 10150
  BL_CAVALRY_STABLE = 10151
  BL_CAVALRY_STABLE_2 = 10152
  BL_SMALL_TOWER = 10153

  BL_KEEP_FORTRESS_ENTRY = 10160
  BL_INNER_PATH_FRONT = 10170
  BL_INNER_PATH_NW = 10180
  BL_INNER_PATH_SW = 10190
  BL_INNER_PATH_BACK = 10200
  BL_INNER_PATH_NE = 10210
  BL_INNER_PATH_SE = 10220

  BL_CASTELLIAN_HOUSE = 10230
  BL_CENTRAL_WEST_TOWER = 10240
  BL_CENTRAL_EAST_TOWER = 10250

  BL_NORTHWEST_KEEP_TOWER = 10260
  BL_NORTHEAST_KEEP_TOWER = 10270

  # BATTLEMENTS

  # RAT WARREN
  BL_RAT_WARREN_1 = 10900
  BL_RAT_WARREN_2 = 10901
  BL_RAT_WARREN_3 = 10902
  BL_RAT_WARREN_4 = 10903
  BL_RAT_WARREN_5 = 10904
  BL_RAT_WARREN_6 = 10905
  BL_RAT_WARREN_7 = 10906
  BL_RAT_WARREN_8 = 10907
  BL_RAT_WARREN_9 = 10908
  BL_RAT_WARREN_10 = 10909
  BL_RAT_WARREN_11 = 10910
  BL_RAT_WARREN_12 = 10911
  BL_RAT_WARREN_13 = 10912
  BL_RAT_WARREN_14 = 10913
  BL_RAT_WARREN_15 = 10914
  BL_RAT_WARREN_16 = 10915
  BL_RAT_WARREN_17 = 10916
  BL_RAT_WARREN_18 = 10917
  BL_RAT_WARREN_19 = 10918
  BL_RAT_WARREN_20 = 10919
  BL_RAT_WARREN_21 = 10920
  BL_RAT_WARREN_22 = 10921
  BL_RAT_WARREN_23 = 10922
  BL_RAT_WARREN_24 = 10923

  BL_ROAD_TO_KEEP = 11000


class RoomFuncResponse(IntEnum):
  NONE = 0
  NO_PROMPT = 1
  SKIP = 2


# DIRECTIONS

class DirectionEnum(IntEnum):
  NONE = 0
  NORTH = 1
  SOUTH = 2
  WEST = 3
  EAST = 4
  UP = 9
  DOWN = 10


class Direction:
  def __init__(self, names, left, right, reverse):
    self.Names = names
    self.Left = left
    self.Right = right
    self.Reverse = reverse


directions = {
    DirectionEnum.NORTH: Direction(["north", "n"], DirectionEnum.WEST, DirectionEnum.EAST, DirectionEnum.SOUTH),
    DirectionEnum.SOUTH: Direction(["south", "s"], DirectionEnum.EAST, DirectionEnum.WEST, DirectionEnum.NORTH),
    DirectionEnum.WEST: Direction(["west", "w"], DirectionEnum.SOUTH, DirectionEnum.NORTH, DirectionEnum.EAST),
    DirectionEnum.EAST: Direction(["east", "e"], DirectionEnum.NORTH, DirectionEnum.SOUTH, DirectionEnum.WEST),
    DirectionEnum.UP: Direction(["up", "u"], DirectionEnum.NONE, DirectionEnum.NONE, DirectionEnum.DOWN),
    DirectionEnum.DOWN: Direction(["down", "d"], DirectionEnum.NONE, DirectionEnum.NONE, DirectionEnum.UP),
}


class DoorState:
  def __init__(self, closed=False, locked=False):
    self.Closed = closed
    self.Locked = locked


class Door:
  def __init__(self, name, state, key_name=""):
    self.Name = name
    self.State = state
    self.KeyName = key_name

  def Verb(self):
    if self.Name.endswith("s"):
      return "are"
    else:
      return "is"


class Exit:
  def __init__(self, room_id, door_id=DoorEnum.NONE,
               frame_id=None, frame_id_open=None):
    self.Room = room_id
    self.Door = door_id
    self.FrameClosed = frame_id
    self.FrameOpen = frame_id_open

  def Frame(self):
    player = GameData.GetPlayer()
    if self.Door == DoorEnum.NONE:
      return self.FrameClosed
    elif player.DoorState(self.Door).Closed:
      return self.FrameClosed
    elif self.FrameOpen is None:
      return self.FrameClosed
    else:
      return self.FrameOpen


class NewPerson:
  def __init__(self, person, conditions=None, triggers=None):
    self.Person = person
    self.Conditions = conditions
    self.Triggers = triggers

  def Create(self, room_id, processConditions, processTriggers):
    rooms = GameData.GetRooms()
    persons = GameData.GetPersons()
    p = deepcopy(persons[self.Person])
    p.UUID = uuid4()
    if processConditions(room_id, p, self.Conditions):
      if self.Triggers is not None:
        processTriggers(p, self.Triggers)
      rooms[room_id].AddPerson(p)
    else:
      del p


class RoomFlag(IntEnum):
  PEACEFUL = 1 << 0
  OUTSIDE = 1 << 1
  LIGHT = 1 << 2
  NO_SAVE = 1 << 3


class Room:
  def __init__(self, room_id, zone, title, short_desc="", long_desc=None, travel_time=60, flags=0, func=None,
               room_pers=None, exits=None, walls=None, room_items=None, onLook=None, periodics=None):
    self.RoomID = room_id
    self.Zone = zone
    self.Title = title
    self.ShortDescription = short_desc
    self.LongDescription = []
    self.TravelTime = travel_time
    self.Flags = flags
    self.Function = func
    self.NewPersons = room_pers
    self.Persons = []
    self.Periodics = []
    self.Exits = dict()
    self.Walls = dict()
    self.Items = []
    self.OnLook = onLook
    if long_desc is not None:
      for para in long_desc:
        self.LongDescription.append(para)
    if exits is not None:
      for exit_dir, exit in exits.items():
        self.AddExit(exit_dir, exit)
    if walls is not None:
      for wall_dir, fg in walls.items():
        self.AddWall(wall_dir, fg)
    if room_items is not None:
      for item in room_items:
        self.AddItem(item)
    if periodics is not None:
      for per in periodics:
        self.Periodics.append(per)

  def Initialize(self, processConditions, processTriggers):
    if self.NewPersons is not None:
      for np in self.NewPersons:
        p = np.Create(self.RoomID, processConditions, processTriggers)
        if p is not None:
          self.AddPerson(p)

  def TextTranslate(self, text):
    ret = text.replace("@@TITLE@@", self.Title)
    return ret

  def AddExit(self, exit_dir, exit):
    if exit_dir in self.Exits:
      self.Exits[exit_dir] = exit
    else:
      self.Exits.update({exit_dir: exit})

  def AddWall(self, wall_dir, fg):
    if wall_dir in self.Walls:
      self.Walls[wall_dir] = fg
    else:
      self.Walls.update({wall_dir: fg})

  def RemoveExit(self, direction):
    if direction in self.Exits:
        self.Exits.pop(direction)

  def AddItem(self, item):
    i = deepcopy(item)
    i.UUID = uuid4()
    self.Items.append(i)
    return True

  def AttachItem(self, item):
    self.Items.append(item)
    return True

  def RemoveItem(self, it):
    for item in self.Items:
      if item.UUID == it.UUID:
        self.Items.remove(item)
        return True
    return False

  def HasItem(self, item_name):
    for item in self.Items:
      if item.ItemName.lower() == item_name.lower():
        return item
    return None

  def AddPerson(self, person):
    self.Persons.append(person)

  def RemovePerson(self, uid):
    rp = None
    for x in self.Persons:
      if x.UUID == uid:
        rp = x
        break
    if rp is not None:
      self.Persons.remove(rp)

  def PersonInRoom(self, uid):
    for x in self.Persons:
      if x.UUID == uid:
        return True
    return False

  def HasLight(self):
    player = GameData.GetPlayer()
    if self.Flags & RoomFlag.OUTSIDE > 0 and player.GameTimeIsDay():
      return True
    if self.Flags & RoomFlag.LIGHT > 0:
      return True
    if player.HasLight():
      return True
    for x in self.Persons:
      if x.HasLight():
        return True
    for item in self.Items:
      if item.IsLight():
        return True
    return False

# vim: tabstop=2 shiftwidth=2 expandtab:
