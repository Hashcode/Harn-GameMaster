# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Global Definitions

import random

from enum import IntEnum
from uuid import uuid4
from copy import deepcopy
from time import gmtime
from calendar import timegm

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
    logd("DICE RESULT %dD%d+%d (flags:%x): %d" %
         (self.Num, self.Max, self.Mod, self.Flags, value))
    return value


class Roll(IntEnum):
  NONE = 0
  CS = 1
  MS = 2
  MF = 3
  CF = 4


# NUMBER

def NumAdj(num):
  ret = "th"
  digit = num % 10
  if num == 11 or num == 12 or num == 13:
    ret = "th"
  elif digit == 1:
    ret = "st"
  elif digit == 2:
    ret = "nd"
  elif digit == 3:
    ret = "rd"
  return ret


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
    MaterialEnum.FUR_LT: Material("Fur", 0, 0, [2, 1, 1, 2]),
    MaterialEnum.FUR_MD: Material("Fur", 0, 0, [4, 3, 1, 3]),
    MaterialEnum.FUR_HV: Material("Fur", 0, 0, [5, 4, 1, 3]),
    MaterialEnum.HIDE: Material("Hide", 0, 0, [5, 4, 1, 3]),
    MaterialEnum.HIDE_BEAR_LT: Material("Bear Hide", 0, 0, [5, 3, 2, 4]),
    MaterialEnum.HIDE_BEAR_MD: Material("Bear Hide", 0, 0, [6, 4, 3, 5]),
    MaterialEnum.HIDE_BEAR_HV: Material("Bear Hide", 0, 0, [7, 5, 3, 6]),
    MaterialEnum.HIDE_DRAGON_LT: Material("Dragon Hide", 0.2, 4800,
                                          [8, 5, 8, 7],
                                          flags=1 << MaterialFlagEnum.MAGIC),
    MaterialEnum.HIDE_DRAGON_MD: Material("Dragon Hide", 0.2, 6400,
                                          [10, 8, 7, 9],
                                          flags=1 << MaterialFlagEnum.MAGIC),
    MaterialEnum.HIDE_DRAGON_HV: Material("Dragon Hide", 0.2, 9600,
                                          [12, 15, 12, 14],
                                          flags=1 << MaterialFlagEnum.MAGIC),
    # CRAFTED
    MaterialEnum.CLOTH: Material("Cloth", 0.1, 2, [1, 1, 1, 1]),
    MaterialEnum.QUILT: Material("Quilt", 0.3, 4, [5, 3, 2, 4]),
    MaterialEnum.LEATHER: Material("Leather", 0.2, 4, [2, 4, 3, 3]),
    MaterialEnum.KURBUL: Material("Hardened Leather", 0.25, 5, [4, 5, 4, 3]),
    MaterialEnum.LEATHER_RING: Material("Studded Leather", 0.4, 7,
                                        [3, 6, 4, 3]),
    MaterialEnum.MAIL: Material("Chainmail", 0.5, 15, [2, 8, 5, 1]),
    MaterialEnum.SCALE: Material("Scale Mail", 0.7, 10, [5, 9, 4, 5]),
    MaterialEnum.STEEL: Material("Steel", 0.8, 25, [6, 10, 6, 2]),
    MaterialEnum.STEEL_WOOD: Material("Steel & Wood", 0.8, 10, [5, 8, 4, 1]),
    # PRECIOUS
    MaterialEnum.BRONZE: Material("Bronze", 0.8, 10, [2, 6, 2, 1]),
    MaterialEnum.SILVER: Material("Silver", 1.5, 60, [3, 8, 3, 2]),
    MaterialEnum.GOLD: Material("Gold", 3.0, 120, [4, 9, 4, 3]),
    MaterialEnum.MITHRIL: Material("Mithril", 0.25, 1200, [4, 10, 7, 8],
                                   flags=1 << MaterialFlagEnum.MAGIC),
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
  def __init__(self, name, mass, leftright=False, fumble=False,
               stumble=False):
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
    CoverageEnum.ELBOWS: BodyPart("Elbow", 6, True, fumble=True),
    CoverageEnum.FOREARMS: BodyPart("Forearm", 6, True, fumble=True),
    CoverageEnum.HANDS: BodyPart("Hand", 4, True, fumble=True),
    CoverageEnum.THORAX_FRONT: BodyPart("Thorax (front)", 6),
    CoverageEnum.THORAX_REAR: BodyPart("Thorax (back)", 6),
    CoverageEnum.ABDOMEN_FRONT: BodyPart("Abdomen (front)", 6),
    CoverageEnum.ABDOMEN_REAR: BodyPart("Abdomen (back)", 6),
    CoverageEnum.GROIN: BodyPart("Groin", 2, stumble=True),
    CoverageEnum.HIPS: BodyPart("Hip", 8, True, stumble=True),
    CoverageEnum.THIGHS: BodyPart("Thigh", 7, True, stumble=True),
    CoverageEnum.KNEES: BodyPart("Knee", 3, True, stumble=True),
    CoverageEnum.CALVES: BodyPart("Calf", 8, True, stumble=True),
    CoverageEnum.FEET: BodyPart("Foot", 6, True, stumble=True),
    # MOB PARTS
}


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
  MISC_RAT_FUR = 50001
  # KEYS
  KEY_WAREHOUSE_DBL_DOOR = 60000


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
  NO_GET = 2
  LIGHT = 2
  MAGIC = 3
  HIDDEN = 4
  INVIS = 5


class ItemFlag:
  def __init__(self, name, bit):
    self.Name = name
    self.Bit = bit


item_flags = {
    ItemFlagEnum.NO_SELL: ItemFlag("no sell", 1 << ItemFlagEnum.NO_SELL),
    ItemFlagEnum.NO_DROP: ItemFlag("no drop", 1 << ItemFlagEnum.NO_DROP),
    ItemFlagEnum.NO_GET: ItemFlag("no get", 1 << ItemFlagEnum.NO_GET),
    ItemFlagEnum.LIGHT: ItemFlag("light", 1 << ItemFlagEnum.LIGHT),
    ItemFlagEnum.MAGIC: ItemFlag("magic", 1 << ItemFlagEnum.MAGIC),
    ItemFlagEnum.HIDDEN: ItemFlag("hidden", 1 << ItemFlagEnum.HIDDEN),
    ItemFlagEnum.INVIS: ItemFlag("invisible", 1 << ItemFlagEnum.INVIS),
}


class Item:
  def __init__(self, item_type=ItemTypeEnum.NONE, name="",
               qual=QualityEnum.NONE, material=MaterialEnum.NONE, mass=0,
               flags=0, eff=None):
    self.ItemType = item_type
    self.ItemName = name
    self.Quality = qual
    self.Material = material
    self.Mass = mass
    self.Flags = flags
    self.Effects = eff
    # Calculations
    self.Weight = self.Mass * materials[self.Material].WeightBase
    self.Value = self.Mass * materials[self.Material].CostBase * \
        qualities[self.Quality].CostModifier

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
  def __init__(self, name, qual, material, mass, skill, ar, dr, flags=0,
               eff=None):
    super().__init__(ItemTypeEnum.SHIELD, name, qual, material, mass, flags,
                     eff)
    self.Skill = skill
    self.AttackRating = ar
    self.DefenseRating = dr


class Weapon(Item):
  def __init__(self, name, qual, material, mass, skill, ar, dr, sh_penalty,
               dice_roll, dmg_type=DamageTypeEnum.BLUNT, flags=0, eff=None):
    super().__init__(ItemTypeEnum.WEAPON, name, qual, material, mass, flags,
                     eff)
    self.Skill = skill
    self.AttackRating = ar
    self.DefenseRating = dr
    self.SingleHandPenalty = sh_penalty
    self.Roll = dice_roll
    self.DamageType = dmg_type


class Armor(Item):
  def __init__(self, name, qual, material, layer=0, coverage=0, flags=0,
               eff=None):
    # TODO use coverage / material Type
    mass = 0
    for x in CoverageEnum:
      if coverage & 1 << x > 0:
        mass += body_parts[x].Mass
    super().__init__(ItemTypeEnum.ARMOR, name, qual, material, mass, flags,
                     eff)
    self.Layer = layer
    self.Coverage = coverage

  def CoverageStr(self):
    cov_list = []
    for x in CoverageEnum:
      if self.Coverage & 1 << x > 0:
        cov_list.append(body_parts[x].PartName)
    return ", ".join(cov_list)

  def Covered(self, bp_id):
    if self.Coverage & 1 << bp_id > 0:
        return True
    return False


class Ring(Item):
  def __init__(self, name, qual, material, mass, value=0, flags=0, eff=None):
    super().__init__(ItemTypeEnum.RING, name, qual, material, mass, flags,
                     eff)
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
  def __init__(self, name, ml, skill_id, roll, dmg_type):
    self.Name = name
    self.SkillML = ml
    self.SkillID = skill_id
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
  def __init__(self, abbrev, name, symbol, start_day, start_month,
               end_day, end_month):
    self.Abbrev = abbrev
    self.Name = name
    self.Symbol = symbol
    self.StartDay = start_day
    self.StartMonth = start_month
    self.EndDay = end_day
    self.EndMonth = end_month


sunsigns = {
    SS_NON: Sunsign("NONE", "[None]", "[None]", 0,
                    MonthEnum.NONE, 0, MonthEnum.NONE),
    SS_ULA: Sunsign("ULA", "Ulandus", "Tree", 4,
                    MonthEnum.NUZYAEL, 3, MonthEnum.PEONU),
    SS_ARA: Sunsign("ARA", "Aralius", "Wands", 4,
                    MonthEnum.PEONU, 2, MonthEnum.KELEN),
    SS_FEN: Sunsign("FEN", "Feniri", "Smith", 3,
                    MonthEnum.KELEN, 3, MonthEnum.NOLUS),
    SS_AHN: Sunsign("AHN", "Ahnu", "Fire Dragon", 4,
                    MonthEnum.NOLUS, 4, MonthEnum.LARANE),
    SS_ANG: Sunsign("ANG", "Angberelius", "Flaming Swords", 5,
                    MonthEnum.LARANE, 6, MonthEnum.AGRAZHAR),
    SS_NAD: Sunsign("NAD", "Nadai", "Salamander", 7,
                    MonthEnum.AGRAZHAR, 5, MonthEnum.AZURA),
    SS_HIR: Sunsign("HIR", "Hirin", "Eagle", 6,
                    MonthEnum.AZURA, 4, MonthEnum.HALANE),
    SS_TAR: Sunsign("TAR", "Tarael", "Pentacle", 5,
                    MonthEnum.HALANE, 3, MonthEnum.SAVOR),
    SS_TAI: Sunsign("TAI", "Tai", "Lantern", 4,
                    MonthEnum.SAVOR, 2, MonthEnum.ILVIN),
    SS_SKO: Sunsign("SKO", "Skorus", "Mixer", 3,
                    MonthEnum.ILVIN, 2, MonthEnum.NAVEK),
    SS_MAS: Sunsign("MAS", "Masara", "Chalic", 3,
                    MonthEnum.NAVEK, 1, MonthEnum.MORGAT),
    SS_LAD: Sunsign("LAD", "Lado", "Galley", 2,
                    MonthEnum.MORGAT, 3, MonthEnum.NUZYAEL),
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
    SexEnum.NONE: AttrSexNameMax("None", "It", "Its", 0),
    SexEnum.MALE: AttrSexNameMax("Male", "He", "His", 48),
    SexEnum.FEMALE: AttrSexNameMax("Female", "She", "Her", 100),
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
    ParentStatusEnum.ADOPTED: AttrNameMax("Adopted", 70),
    ParentStatusEnum.BASTARD: AttrNameMax("Bastard", 85),
    ParentStatusEnum.ORPHAN: AttrNameMax("Orphaned", 95),
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
    ATTR_STR: Attr("STR", "Strength", AttrClassEnum.PHYSICAL, 4, 6, 0,
                   roll_flags=ROLLF_DROP_LOWEST),
    ATTR_STA: Attr("STA", "Stamina", AttrClassEnum.PHYSICAL, 4, 6, 0,
                   roll_flags=ROLLF_DROP_LOWEST),
    ATTR_DEX: Attr("DEX", "Dexterity", AttrClassEnum.PHYSICAL, 4, 6, 0,
                   roll_flags=ROLLF_DROP_LOWEST),
    ATTR_AGL: Attr("AGL", "Agility", AttrClassEnum.PHYSICAL, 4, 6, 0,
                   roll_flags=ROLLF_DROP_LOWEST),
    ATTR_EYE: Attr("EYE", "Eyesight", AttrClassEnum.PHYSICAL, 3, 6, 0),
    ATTR_HRG: Attr("HRG", "Hearing", AttrClassEnum.PHYSICAL, 3, 6, 0),
    ATTR_SML: Attr("SML", "Smelling", AttrClassEnum.PHYSICAL, 3, 6, 0),
    ATTR_VOI: Attr("VOI", "Voice", AttrClassEnum.PHYSICAL, 3, 6, 0),
    ATTR_MED: Attr("MED", "Medical", AttrClassEnum.PHYSICAL, 1, 100, 0,
                   hidden=True),
    # PERSONALITY
    ATTR_INT: Attr("INT", "Intelligence", AttrClassEnum.PERSONALITY, 4, 6, 0,
                   roll_flags=ROLLF_DROP_LOWEST),
    ATTR_AUR: Attr("AUR", "Aura", AttrClassEnum.PERSONALITY, 4, 6, 0,
                   roll_flags=ROLLF_DROP_LOWEST),
    ATTR_WIL: Attr("WIL", "Will", AttrClassEnum.PERSONALITY, 4, 6, 0,
                   roll_flags=ROLLF_DROP_LOWEST),
    ATTR_PSY: Attr("PSY", "Psyche", AttrClassEnum.PERSONALITY, 1, 100, 0,
                   hidden=True),
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
  def __init__(self, name, skill_class, attr1=AttrEnum.NONE,
               attr2=AttrEnum.NONE, attr3=AttrEnum.NONE, oml_mod=1, apsuc=100,
               sunsign_mod=None, hidden=False):
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
        Skill("Acrobatics", SkillClassEnum.PHYSICAL,
              ATTR_STR, ATTR_AGL, ATTR_AGL, 2,
              {SS_NAD: 2, SS_HIR: 1}),
    SkillEnum.CLIMBING:
        Skill("Climbing", SkillClassEnum.PHYSICAL,
              ATTR_STR, ATTR_DEX, ATTR_AGL, 4,
              {SS_ULA: 2, SS_ARA: 2}),
    SkillEnum.CONDITIONING:
        Skill("Conditioning", SkillClassEnum.PHYSICAL,
              ATTR_STR, ATTR_STA, ATTR_WIL, 5,
              {SS_ULA: 1, SS_LAD: 1}),
    SkillEnum.DANCING:
        Skill("Dancing", SkillClassEnum.PHYSICAL,
              ATTR_DEX, ATTR_AGL, ATTR_AGL, 2,
              {SS_ULA: 1, SS_LAD: 1}, hidden=True),
    SkillEnum.DODGE:
        Skill("Dodge", SkillClassEnum.PHYSICAL,
              ATTR_AGL, ATTR_AGL, ATTR_AGL, 5,
              {SS_HIR: 1, SS_TAR: 1, SS_TAI: 1}),
    SkillEnum.JUMPING:
        Skill("Jumping", SkillClassEnum.PHYSICAL,
              ATTR_STR, ATTR_AGL, ATTR_AGL, 4,
              {SS_NAD: 2, SS_HIR: 2}),
    SkillEnum.LEGERDEMAIN:
        Skill("Legerdemain", SkillClassEnum.PHYSICAL,
              ATTR_DEX, ATTR_DEX, ATTR_WIL, 1,
              {SS_SKO: 2, SS_TAI: 2, SS_TAR: 2}),
    SkillEnum.STEALTH:
        Skill("Stealth", SkillClassEnum.PHYSICAL,
              ATTR_AGL, ATTR_HRG, ATTR_WIL, 3,
              {SS_HIR: 2, SS_TAR: 2, SS_TAI: 2}),
    SkillEnum.SWIMMING:
        Skill("Swimming", SkillClassEnum.PHYSICAL,
              ATTR_STA, ATTR_DEX, ATTR_AGL, 1,
              {SS_SKO: 1, SS_MAS: 3, SS_LAD: 3}),
    SkillEnum.THROWING:
        Skill("Throwing", SkillClassEnum.PHYSICAL,
              ATTR_STR, ATTR_DEX, ATTR_EYE, 4,
              {SS_HIR: 2, SS_TAR: 1, SS_NAD: 1}),
    # COMMUNICATION
    SkillEnum.AWARENESS:
        Skill("Awareness", SkillClassEnum.COMMUNICATION,
              ATTR_EYE, ATTR_HRG, ATTR_SML, 4,
              {SS_HIR: 2, SS_TAR: 2}),
    SkillEnum.INTRIGUE:
        Skill("Intrigue", SkillClassEnum.COMMUNICATION,
              ATTR_INT, ATTR_AUR, ATTR_WIL, 3,
              {SS_TAI: 1, SS_TAR: 1, SS_SKO: 1}),
    SkillEnum.MENTAL_CONFLICT:
        Skill("Mental Conflict", SkillClassEnum.COMMUNICATION,
              ATTR_AUR, ATTR_WIL, ATTR_WIL, 3),
    SkillEnum.ORATORY:
        Skill("Oratory", SkillClassEnum.COMMUNICATION,
              ATTR_CML, ATTR_VOI, ATTR_INT, 2,
              {SS_TAR: 1}),
    SkillEnum.RHETORIC:
        Skill("Rhetoric", SkillClassEnum.COMMUNICATION,
              ATTR_VOI, ATTR_INT, ATTR_WIL, 3,
              {SS_TAI: 1, SS_TAR: 1, SS_SKO: 1}),
    SkillEnum.SINGING:
        Skill("Singing", SkillClassEnum.COMMUNICATION,
              ATTR_HRG, ATTR_VOI, ATTR_VOI, 3,
              {SS_MAS: 1}, hidden=True),
    # COMBAT
    SkillEnum.INITIATIVE:
        Skill("Initiative", SkillClassEnum.COMBAT,
              ATTR_AGL, ATTR_WIL, ATTR_WIL, 4),
    SkillEnum.UNARMED:
        Skill("Unarmed Combat", SkillClassEnum.COMBAT,
              ATTR_STR, ATTR_DEX, ATTR_AGL, 4,
              {SS_MAS: 2, SS_LAD: 2, SS_ULA: 2}),
    SkillEnum.RIDING:
        Skill("Riding", SkillClassEnum.COMBAT,
              ATTR_DEX, ATTR_AGL, ATTR_WIL, 1,
              {SS_ULA: 1, SS_ARA: 1}),
    SkillEnum.AXE:
        Skill("Axe", SkillClassEnum.COMBAT,
              ATTR_STR, ATTR_STR, ATTR_DEX, 3,
              {SS_AHN: 1, SS_FEN: 1, SS_ANG: 1}),
    SkillEnum.BLOWGUN:
        Skill("Blowgun", SkillClassEnum.COMBAT,
              ATTR_STA, ATTR_DEX, ATTR_EYE, 4,
              {SS_HIR: 2, SS_TAR: 1, SS_NAD: 1}),
    SkillEnum.BOW:
        Skill("Bow", SkillClassEnum.COMBAT,
              ATTR_STR, ATTR_DEX, ATTR_EYE, 2,
              {SS_HIR: 1, SS_TAR: 1, SS_NAD: 1}),
    SkillEnum.CLUB:
        Skill("Club", SkillClassEnum.COMBAT,
              ATTR_STR, ATTR_STR, ATTR_DEX, 4,
              {SS_ULA: 1, SS_ARA: 1}),
    SkillEnum.DAGGER:
        Skill("Dagger", SkillClassEnum.COMBAT,
              ATTR_DEX, ATTR_DEX, ATTR_EYE, 3,
              {SS_ANG: 2, SS_NAD: 2}),
    SkillEnum.FLAIL:
        Skill("Flail", SkillClassEnum.COMBAT,
              ATTR_DEX, ATTR_DEX, ATTR_DEX, 1,
              {SS_HIR: 1, SS_TAR: 1, SS_NAD: 1}),
    SkillEnum.NET:
        Skill("Net", SkillClassEnum.COMBAT,
              ATTR_DEX, ATTR_DEX, ATTR_EYE, 1,
              {SS_MAS: 1, SS_SKO: 1, SS_LAD: 1}),
    SkillEnum.POLEARM:
        Skill("Polearm", SkillClassEnum.COMBAT,
              ATTR_STR, ATTR_STR, ATTR_DEX, 2,
              {SS_ANG: 1, SS_ARA: 1}),
    SkillEnum.SHIELD:
        Skill("Shield", SkillClassEnum.COMBAT,
              ATTR_STR, ATTR_DEX, ATTR_DEX, 3,
              {SS_ULA: 1, SS_LAD: 1, SS_MAS: 1}),
    SkillEnum.SLING:
        Skill("Sling", SkillClassEnum.COMBAT,
              ATTR_DEX, ATTR_DEX, ATTR_EYE, 1,
              {SS_HIR: 1, SS_TAR: 1, SS_NAD: 1}),
    SkillEnum.SPEAR:
        Skill("Spear", SkillClassEnum.COMBAT,
              ATTR_STR, ATTR_STR, ATTR_DEX, 3,
              {SS_ARA: 1, SS_FEN: 1, SS_ULA: 1}),
    SkillEnum.SWORD:
        Skill("Sword", SkillClassEnum.COMBAT,
              ATTR_STR, ATTR_DEX, ATTR_DEX, 3,
              {SS_ANG: 3, SS_AHN: 1, SS_NAD: 1}),
    SkillEnum.WHIP:
        Skill("Whip", SkillClassEnum.COMBAT,
              ATTR_DEX, ATTR_DEX, ATTR_EYE, 1,
              {SS_HIR: 1, SS_NAD: 1}),
    # LORE / CRAFT
    SkillEnum.AGRICULTURE:
        Skill("Agriculture", SkillClassEnum.LORE_CRAFTS,
              ATTR_STR, ATTR_STA, ATTR_WIL, 2,
              {SS_ULA: 2, SS_ARA: 2}),
    SkillEnum.ALCHEMY:
        Skill("Alchemy", SkillClassEnum.LORE_CRAFTS,
              ATTR_SML, ATTR_INT, ATTR_AUR, 1,
              {SS_SKO: 3, SS_TAI: 2, SS_MAS: 2}),
    SkillEnum.ANIMALCRAFT:
        Skill("Animalcraft", SkillClassEnum.LORE_CRAFTS,
              ATTR_AGL, ATTR_VOI, ATTR_WIL, 1,
              {SS_ULA: 1, SS_ARA: 1}),
    SkillEnum.BREWING:
        Skill("Brewing", SkillClassEnum.LORE_CRAFTS,
              ATTR_DEX, ATTR_SML, ATTR_SML, 2,
              {SS_SKO: 3, SS_TAI: 2, SS_MAS: 2}),
    SkillEnum.COOKERY:
        Skill("Cookery", SkillClassEnum.LORE_CRAFTS,
              ATTR_DEX, ATTR_SML, ATTR_SML, 3,
              {SS_SKO: 1}),
    SkillEnum.FISHING:
        Skill("Fishing", SkillClassEnum.LORE_CRAFTS,
              ATTR_DEX, ATTR_EYE, ATTR_WIL, 3,
              {SS_MAS: 2, SS_LAD: 2}),
    SkillEnum.FLETCHING:
        Skill("Fletching", SkillClassEnum.LORE_CRAFTS,
              ATTR_DEX, ATTR_DEX, ATTR_EYE, 1,
              {SS_HIR: 2, SS_TAR: 1, SS_NAD: 1}),
    SkillEnum.FORAGING:
        Skill("Foraging", SkillClassEnum.LORE_CRAFTS,
              ATTR_DEX, ATTR_SML, ATTR_INT, 3,
              {SS_ULA: 2, SS_ARA: 2}),
    SkillEnum.HERBLORE:
        Skill("Herblore", SkillClassEnum.LORE_CRAFTS,
              ATTR_EYE, ATTR_SML, ATTR_INT, 1,
              {SS_ULA: 3, SS_ARA: 2}),
    SkillEnum.HIDEWORK:
        Skill("Hidework", SkillClassEnum.LORE_CRAFTS,
              ATTR_EYE, ATTR_SML, ATTR_WIL, 2,
              {SS_ULA: 1, SS_ARA: 1}),
    SkillEnum.JEWELCRAFT:
        Skill("Jewelcraft", SkillClassEnum.LORE_CRAFTS,
              ATTR_DEX, ATTR_EYE, ATTR_WIL, 1,
              {SS_FEN: 3, SS_TAR: 1, SS_ARA: 1}),
    SkillEnum.LOCKCRAFT:
        Skill("Lockcraft", SkillClassEnum.LORE_CRAFTS,
              ATTR_DEX, ATTR_EYE, ATTR_WIL, 1,
              {SS_FEN: 3}),
    SkillEnum.METALCRAFT:
        Skill("Metalcraft", SkillClassEnum.LORE_CRAFTS,
              ATTR_STR, ATTR_DEX, ATTR_WIL, 1,
              {SS_FEN: 3, SS_AHN: 1, SS_ANG: 1}),
    SkillEnum.MINING:
        Skill("Mining", SkillClassEnum.LORE_CRAFTS,
              ATTR_STR, ATTR_DEX, ATTR_INT, 1,
              {SS_ULA: 2, SS_ARA: 2, SS_FEN: 1}),
    SkillEnum.PHYSICIAN:
        Skill("Physician", SkillClassEnum.LORE_CRAFTS,
              ATTR_DEX, ATTR_EYE, ATTR_INT, 1,
              {SS_MAS: 2, SS_SKO: 1, SS_TAI: 1}),
    SkillEnum.SURVIVAL:
        Skill("Survival", SkillClassEnum.LORE_CRAFTS,
              ATTR_STR, ATTR_DEX, ATTR_INT, 3,
              {SS_ULA: 2, SS_ARA: 1}),
    SkillEnum.TIMBERCRAFT:
        Skill("Timbercraft", SkillClassEnum.LORE_CRAFTS,
              ATTR_STR, ATTR_DEX, ATTR_AGL, 2,
              {SS_ULA: 3, SS_ARA: 1}),
    SkillEnum.TRACKING:
        Skill("Tracking", SkillClassEnum.LORE_CRAFTS,
              ATTR_EYE, ATTR_SML, ATTR_WIL, 2,
              {SS_ULA: 3, SS_ARA: 3}),
    SkillEnum.WEAPONCRAFT:
        Skill("Weaponcraft", SkillClassEnum.LORE_CRAFTS,
              ATTR_STR, ATTR_DEX, ATTR_WIL, 1,
              {SS_FEN: 3, SS_AHN: 1, SS_ANG: 1}),
    SkillEnum.WOODCRAFT:
        Skill("Woodcraft", SkillClassEnum.LORE_CRAFTS,
              ATTR_DEX, ATTR_DEX, ATTR_WIL, 2,
              {SS_ULA: 2, SS_ARA: 2, SS_LAD: 1}),
}


class SkillLink:
  def __init__(self, points=0, att=0):
    self.Points = points
    self.Attempts = att


# GENERIC PERSON

class PersonEnum(IntEnum):
  NONE = 0
  MON_RAT = 100
  BL_KEEP_GUARD = 10000


class PersonTypeEnum(IntEnum):
  PLAYER = 0
  NPC = 1


class PersonFlagEnum(IntEnum):
  AGGRESSIVE = 0
  SHOPKEEP = 1


PERS_AGGRESSIVE = 1 << PersonFlagEnum.AGGRESSIVE
PERS_SHOPKEEP = 1 << PersonFlagEnum.SHOPKEEP


class ItemLink:
  def __init__(self, qty=1, equip=False):
    self.Quantity = qty
    self.Equipped = equip


class WoundDesc:
  def __init__(self, name, verbs, ip_bonus=0):
    self.Name = name
    self.Verbs = verbs
    self.IPBonus = ip_bonus


wounds = {
    ImpactActionEnum.WOUND_MLD: WoundDesc("Mild",
                                          ["Bruised",
                                           "Cut",
                                           "Poked",
                                           "Singed"], 0),
    ImpactActionEnum.WOUND_SRS: WoundDesc("Serious",
                                          ["Crushed",
                                           "Slashed",
                                           "Stabbed",
                                           "Scorched"], 5),
    ImpactActionEnum.WOUND_GRV: WoundDesc("Grievous",
                                          ["Pulverized",
                                           "Shredded",
                                           "Skewered",
                                           "Cremated"], 10),
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
  def __init__(self, person_type, name, long_desc="", flags=0,
               skin=MaterialEnum.NONE, it=None):
    self.PersonType = person_type
    self.Name = name
    self.LongDescription = long_desc
    self.DefaultAim = AimEnum.MID
    self.Flags = flags
    self.SkinMaterial = skin
    self.Attr = dict()
    self.SkillLinks = dict()
    self.Wounds = []
    self.Effects = []
    self.ItemLinks = dict()
    if it is not None:
      for item_id, il in it.items():
        self.AddItem(item_id, il)

  def Copy(self, p):
    self.PersonType = p.PersonType
    self.Name = p.Name
    self.Flags = p.Flags
    self.SkinMaterial = p.SkinMaterial
    self.Attr.clear()
    for attr_id, attr in attributes.items():
      if attr_id in p.Attr:
        self.Attr.update({attr_id: p.Attr[attr_id]})
      else:
        # add new attributes
        self.Attr.update({attr_id:
                          DiceRoll(attr.GenRolls,
                                   attr.GenDice,
                                   flags=attr.GenFlags).Result() + \
                          attr.GenMod})
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
      self.Effects.append(x)
    self.ItemLinks.clear()
    for item_id, il in p.ItemLinks.items():
      self.AddItem(item_id, il)

  def ResetStats(self):
    self.Effects.clear()

  def AddItem(self, item_id, item):
    if item_id in self.ItemLinks:
      self.ItemLinks[item_id].Quantity += item.Quantity
    else:
      self.ItemLinks.update({item_id: item})
    return True

  def RemoveItem(self, item_id, item):
    if item_id in self.ItemLinks:
      if self.ItemLinks[item_id].Equipped and \
         self.ItemLinks[item_id].Quantity == 1:
        return False
      if self.ItemLinks[item_id].Quantity > item.Quantity:
        self.ItemLinks[item_id].Quantity -= item.Quantity
      else:
        self.ItemLinks.pop(item_id)
    return True

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

  def EquipWeight(self):
    items = GameData.GetItems()
    eq = 0
    for item_id, il in self.ItemLinks.items():
      if il.Equipped:
        eq += items[item_id].Weight
    return eq

  def InvenWeight(self):
    items = GameData.GetItems()
    inv = 0
    for item_id, il in self.ItemLinks.items():
      if il.Equipped:
        if il.Quantity > 1:
          inv += items[item_id].Weight * (il.Quantity - 1)
      else:
        inv += items[item_id].Weight * il.Quantity
    return inv

  def ItemWeight(self):
    return self.EquipWeight() + self.InvenWeight()

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
      attr1 = self.Attr[skills[skill_id].Attr1]
    if skills[skill_id].Attr2 in self.Attr:
      attr2 = self.Attr[skills[skill_id].Attr2]
    if skills[skill_id].Attr3 in self.Attr:
      attr3 = self.Attr[skills[skill_id].Attr3]
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
    if not skipPenalty:
      if skills[skill_id].SkillClass == SkillClassEnum.PHYSICAL or \
         skills[skill_id].SkillClass == SkillClassEnum.COMBAT:
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
    # store attempts
    if skill_id != SkillEnum.NONE:
      if skill_id in self.SkillLinks:
        self.SkillLinks[skill_id].Attempts += 1
      else:
        self.SkillLinks.update({skill_id: SkillLink(0, 1)})
    r = DiceRoll(1, 100).Result()
    logd("%s RESOLVE SKILL: %d, ROLL: %d" % (self.Name, ml, r))
    if ml < 5:
      ml = 5
    elif ml > 95:
      ml = 95
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
    items = GameData.GetItems()
    m = Material("None", 0, 0, [0, 0, 0, 0])
    m.Copy(materials[self.SkinMaterial])
    for item_id, il in self.ItemLinks.items():
      if items[item_id].ItemType != ItemTypeEnum.ARMOR:
        continue
      if not il.Equipped:
        continue
      if items[item_id].Covered(bp_id):
        m.Add(materials[items[item_id].Material])
    return m.Protection[dmg_type]

  def AttrInitiative(self):
    return self.SkillML(SkillEnum.INITIATIVE)

  def AttrEndurance(self):
    sb = self.SkillBase(SkillEnum.CONDITIONING)
    ml = self.SkillML(SkillEnum.CONDITIONING, skipPenalty=True)
    return round(sb + (ml / sb - 5))

  def AttrDodge(self):
    return self.SkillML(SkillEnum.DODGE)

  def IsAggressive(self):
    return self.Flags & PERS_AGGRESSIVE > 0

  def GenerateCombatAttacks(self, block=False, default=ItemEnum.NONE):
    items = GameData.GetItems()
    attacks = []
    # count hands used
    count = 0
    def_skill = 0
    def_item_id = ItemEnum.NONE
    for item_id, il in self.ItemLinks.items():
      if not il.Equipped:
        continue
      if items[item_id].ItemType == ItemTypeEnum.WEAPON or \
         items[item_id].ItemType == ItemTypeEnum.SHIELD:
        if block:
          skill = self.SkillML(items[item_id].Skill)
          skill += items[item_id].DefenseRating
          if skill > def_skill:
            def_skill = skill
            def_item_id = item_id
        count += 1
    # create attacks
    # for BLOCK only generate the blocking weapon / shield
    if block:
      if def_item_id == ItemEnum.NONE:
        return attacks
      skill_id = items[def_item_id].Skill
      ml = self.SkillML(skill_id)
      ml += items[def_item_id].DefenseRating
      attacks.append(CombatAttack(items[def_item_id].ItemName, ml, skill_id,
                                  None, DamageTypeEnum.BLUNT))
    else:
      for item_id, il in self.ItemLinks.items():
        if not il.Equipped:
          continue
        if items[item_id].ItemType == ItemTypeEnum.WEAPON:
          skill_id = items[item_id].Skill
          ml = self.SkillML(skill_id)
          ml += items[item_id].AttackRating
          if count > 1:
            ml -= items[item_id].SingleHandPenalty
          attacks.append(CombatAttack(items[item_id].ItemName, ml, skill_id,
                                      items[item_id].Roll,
                                      items[item_id].DamageType))
    if len(attacks) < 1 and default != ItemEnum.NONE:
      skill_id = items[default].Skill
      ml = self.SkillML(skill_id)
      ml += items[default].AttackRating
      attacks.append(CombatAttack(items[default].ItemName, ml, skill_id,
                                  items[default].Roll,
                                  items[default].DamageType))
    return attacks


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
  def __init__(self, person_id, name, long_desc, ini, end, dodge,
               aim=AimEnum.MID, flags=0,
               skin=MaterialEnum.NONE, cur=None, attrs=None,
               num_attacks=1, mob_attacks=None, mob_skills=None, eq=None,
               loot=None):
    super().__init__(PersonTypeEnum.NPC, name, long_desc, flags, skin,
                     it=eq)
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
    super().ResetStats()

  def AttrInitiative(self):
    return self.Initiative - (self.PhysicalPenalty() * 5)

  def AttrEndurance(self):
    return self.Endurance

  def AttrDodge(self):
    return self.Dodge - (self.PhysicalPenalty() * 5)

  def GenerateCombatAttacks(self, block=False, default=ItemEnum.NONE):
    attacks = []
    # Look for a "natural" attack
    if not block and self.MobAttacks is not None:
      for a in range(self.NumAttacks):
        for ma in self.MobAttacks:
          if DiceRoll(1, 100).Result() <= ma.ChanceMax:
            ml = ma.SkillML + ma.AttackRating
            ml -= (self.PhysicalPenalty() * 5)
            ca = CombatAttack(ma.Name, ml, SkillEnum.UNARMED,
                              ma.Damage, ma.DamageType)
            attacks.append(ca)
            break
    # Look for equipped weapons
    if len(attacks) < 1:
      attacks = super().GenerateCombatAttacks(block, default)
    return attacks


# PLAYER


class PlayerCombatState(IntEnum):
  NONE = 0
  WAIT = 1
  ATTACK = 2
  DEFEND = 3


class Player(Person):
  def __init__(self, name=""):
    super().__init__(PersonTypeEnum.PLAYER, name, "player")
    self.Password = ""
    self.Sunsign = SunsignEnum.NONE
    self.Command = ""
    self.Room = None
    self.LastRoom = None
    self.Currency = 0
    self.CombatState = PlayerCombatState.NONE
    self.CombatTarget = None

  def Copy(self, p):
    super().Copy(p)
    self.Room = p.Room
    self.LastRoom = p.LastRoom
    self.Currency = p.Currency
    self.CalcSunsign()
    super().ResetStats()

  def SetRoom(self, room_id):
    self.LastRoom = self.Room
    self.Room = room_id

  def CalcSunsign(self):
    for ss_id, ss in sunsigns.items():
      bm = self.Attr[AttrEnum.BIRTH_MONTH]
      bd = self.Attr[AttrEnum.BIRTH_DAY]
      if (bm == ss.StartMonth and bd >= ss.StartDay) or \
         (bm == ss.EndMonth and bd <= ss.EndDay):
          self.Sunsign = ss_id
          break

  def GenAttr(self):
    # Generate Attributes
    for attr_id, attr in attributes.items():
      self.Attr.update({attr_id: DiceRoll(attr.GenRolls, attr.GenDice,
                                          flags=attr.GenFlags).Result() + \
                        attr.GenMod})
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

  def GenerateCombatAttacks(self, block=False, default=ItemEnum.WEAPON_HAND):
      return super().GenerateCombatAttacks(block, default)


# DOOR

class DoorEnum(IntEnum):
  NONE = 0
  WAREHOUSE_DBL_DOOR = 1


# ROOM

class RoomEnum(IntEnum):
  NONE = 0
  GAME_START = 1
  GAME_RESTORE_SAVE = 2
  GAME_CREATE_CHARACTER = 3
  BL_KEEP_GATEHOUSE = 10000
  BL_PRIEST_CHAMBER = 10001
  BL_GATEHOUSE_PASSAGE = 10002
  BL_ENTRY_YARD = 10010
  BL_STABLE = 10011
  BL_N_GATEHOUSE_TOWER = 10012
  BL_EASTERN_WALK = 10020
  BL_WAREHOUSE = 10021
  BL_S_GATEHOUSE_TOWER = 10022
  BL_SOUTHEASTERN_WALK = 10030
  BL_BAILIFF_TOWER = 10031
  BL_SOUTHERN_WALK = 10040
  BL_ARMORY = 10041
  BL_APARMENT_1 = 10042
  BL_SOUTHERN_WALK_2 = 10050
  BL_WOODWORKER = 10051
  BL_WEAPONSMITH = 10052
  BL_PROVISIONS = 10053
  BL_TRADER = 10054
  BL_FOUNTAIN_SQUARE = 10055
  BL_TAVERN_MAINROOM = 10056
  BL_TAVERN_KITCHEN = 10057
  BL_INN_ENTRYWAY = 10070
  BL_INN_COMMONROOM = 10071
  BL_INN_STAIRWAY = 10074
  BL_INN_HALLWAY_1 = 10075
  BL_INN_HALLWAY_2 = 10076
  BL_INN_ROOM_1 = 10077
  BL_INN_ROOM_2 = 10078
  BL_INN_ROOM_3 = 10079
  BL_INN_ROOM_4 = 10080
  BL_INN_OWNER_ROOM = 10081


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


class Door:
  def __init__(self, name, closed=False, locked=False,
               key_item=ItemEnum.NONE):
    self.Name = name
    self.Closed = closed
    self.Locked = locked
    self.Key = key_item

  def Verb(self):
    if self.Name.endswith("s"):
      return "are"
    else:
      return "is"


class Exit:
  def __init__(self, room_id, door_id=DoorEnum.NONE):
    self.Room = room_id
    self.Door = door_id


class RoomSpawn:
  def __init__(self, person_id, chance, max_qty=1, delay=60):
    self.Person = person_id
    self.Chance = chance
    self.MaxQuantity = max_qty
    self.SpawnDelaySeconds = delay
    self.LastSpawnCheck = 0


class Room:
  def __init__(self, title, short_desc="", long_desc=None, func=None,
               room_pers=None, exits=None, room_items=None,
               spawns=None):
    self.Title = title
    self.ShortDescription = short_desc
    self.LongDescription = []
    self.Function = func
    self.Persons = []
    self.Spawns = []
    self.Exits = dict()
    self.RoomItems = dict()
    if long_desc is not None:
      for para in long_desc:
        self.LongDescription.append(para)
    if exits is not None:
      for exit_dir, exit in exits.items():
        self.AddExit(exit_dir, exit)
    if room_items is not None:
      for item_id, qty in room_items.items():
        self.AddItem(item_id)
      self.RoomItems = room_items
    if room_pers is not None:
      for person_id in room_pers:
        self.AddPerson(person_id)
    if spawns is not None:
      for s in spawns:
        self.Spawns.append(s)

  def AddExit(self, exit_dir, exit):
    if exit_dir in self.Exits:
      self.Exits[exit_dir] = exit
    else:
      self.Exits.update({exit_dir: exit})

  def RemoveExit(self, direction):
    if direction in self.Exits:
        self.Exits.pop(direction)

  def AddItem(self, item_id, room_item):
    if item_id in self.RoomItems:
      self.RoomItems[item_id].Quantity += room_item.Quantity
    else:
      self.RoomItems.update({item_id: room_item})

  def RemoveItem(self, item_id, item):
    if item_id in self.RoomItems:
      if self.RoomItems[item_id].Quantity > item.Quantity:
        self.RoomItems[item_id].Quantity -= item.Quantity
      else:
        self.RoomItems.pop(item_id)

  def AddPerson(self, person_id):
    persons = GameData.GetPersons()
    p = deepcopy(persons[person_id])
    p.UUID = uuid4()
    self.Persons.append(p)

  def RemovePerson(self, uid):
    rp = None
    for x in self.Persons:
      if x.UUID == uid:
        rp = x
        break
    if rp is not None:
      self.Persons.remove(rp)
      del rp


# FORMATTING

class ANSI:
  RESET_CURSOR = "\x1B[1;1H"
  CLEAR = "\x1B[2J"
  TEXT_NORMAL = "\x1B[0m"
  TEXT_BOLD = "\x1B[1m"


# Game Globals

class GameData:
  _doors = None
  _rooms = None
  _items = None
  _persons = None
  _player = None
  _NextRoomEvent = 0

  ROOM_START = 0
  ROOM_RESPAWN = 0

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
  def ProcessRoomEvents():
    rooms = GameData.GetRooms()
    persons = GameData.GetPersons()

    # Check for room spawns
    seconds = timegm(gmtime())
    if GameData._NextRoomEvent < seconds:
      logd("RoomEvents check")
      # Set NextRoomEvent max 10mins
      GameData._NextRoomEvent = seconds + (10 * 60)
      for r in rooms:
        if rooms[r].Spawns is None:
          continue
        for s in rooms[r].Spawns:
          next = s.LastSpawnCheck + s.SpawnDelaySeconds
          if next >= seconds:
            if GameData._NextRoomEvent > next:
              GameData._NextRoomEvent = next
              logd("Next RoomEvents check in %d seconds" %
                   (GameData._NextRoomEvent - seconds))
            continue
          s.LastSpawnCheck = seconds
          if GameData._NextRoomEvent > seconds + s.SpawnDelaySeconds:
            GameData._NextRoomEvent = seconds + s.SpawnDelaySeconds
            logd("Next RoomEvents check in %d seconds" %
                 (GameData._NextRoomEvent - seconds))
          count = 0
          for p in rooms[r].Persons:
            if p.PersonID == s.Person:
              count += 1
          if count < s.MaxQuantity:
            logd("SpawnCheck [%s] in %s [<=%d]" % (persons[s.Person].Name,
                                                   rooms[r].Title, s.Chance))
            if DiceRoll(1, 100).Result() <= s.Chance:
              rooms[r].AddPerson(s.Person)

  @staticmethod
  def ProcessRoomCombat():
    player = GameData.GetPlayer()
    rooms = GameData.GetRooms()
    enemies = []

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
    return enemies


# vim: tabstop=2 shiftwidth=2 expandtab:
