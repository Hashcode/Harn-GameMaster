# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Global Definitions

import random

from enum import IntEnum
from uuid import uuid4


# Logging

LOG_OFF = 0
LOG_ERR = 1
LOG_WRN = 2
LOG_INF = 3
LOG_DBG = 4

LogLevel = LOG_DBG


def log(ll, line):
  if LogLevel >= ll:
    print(line)


def loge(line):
  log(LOG_ERR, "[error] %s" % line)


def logw(line):
  log(LOG_WRN, "[warn] %s" % line)


def logi(line):
  log(LOG_INF, "[info] %s" % line)


def logd(line):
  log(LOG_DBG, "[debug] %s" % line)


# ROLL

def roll(rolls, die_base, modifier=0):
  value = 0
  for x in range(rolls):
    y = random.randint(1, die_base) + modifier
    logd("ROLL %dD%d+%d = %d" % (rolls, die_base, modifier, y))
    value += y
  return value


# NUMBER

def NumAdj(num):
  ret = "th"
  digit = num % 10
  if digit == 1:
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
  def __init__(self, weight, cost, store_mod, blunt, edge, pierce, fire=0,
               cold=0, shock=0, poison=0, magic=0):
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

  def Clear(self):
    self.WeightBase = 0
    self.CostBase = 0
    self.StorageMod = 0
    self.ProtBlunt = 0
    self.ProtEdge = 0
    self.ProtPierce = 0
    self.ProtFire = 0
    self.ProtCold = 0
    self.ProtShock = 0
    self.ProtPoison = 0
    self.ProtMagic = 0

  def Add(self, m):
    self.WeightBase += m.WeightBase
    self.CostBase += m.CostBase
    self.StorageMod += m.StorageMod
    self.ProtBlunt += m.ProtBlunt
    self.ProtEdge += m.ProtEdge
    self.ProtPierce += m.ProtPierce
    self.ProtFire += m.ProtFire
    self.ProtCold += m.ProtCold
    self.ProtShock += m.ProtShock
    self.ProtPoison += m.ProtPoison
    self.ProtMagic += m.ProtMagic


materials = {
    MaterialEnum.CLOTH_HAIR: Material(0.1, 2, 0.25, 1, 1, 1, fire=1, cold=3),
    MaterialEnum.QUILT_FUR: Material(0.3, 4, 0.5, 5, 3, 2, fire=4, cold=5),
    MaterialEnum.LEATHER_HIDE: Material(0.2, 4, 0.75, 2, 4, 3, fire=3, cold=2),
    MaterialEnum.KURBUL: Material(0.25, 5, 1, 4, 5, 4, fire=3, cold=2),
    MaterialEnum.LEATHER_RING: Material(0.4, 7, 0.75, 3, 6, 4, fire=3, cold=2),
    MaterialEnum.MAIL: Material(0.5, 15, 0.5, 2, 8, 5, fire=1, cold=1),
    MaterialEnum.SCALE: Material(0.7, 10, 1, 5, 9, 4, fire=5, cold=2),
    MaterialEnum.STEEL: Material(0.8, 25, 1, 7, 11, 7, fire=2, cold=2),
    MaterialEnum.STEEL_WOOD: Material(0.8, 10, 1, 5, 8, 4, fire=1, cold=1),
    MaterialEnum.SILVER: Material(1.5, 60, 1, 3, 8, 3, fire=2, cold=2),
    MaterialEnum.GOLD: Material(3.0, 120, 1, 4, 9, 4, fire=2, cold=2),
    MaterialEnum.MITHRIL: Material(0.25, 1200, 0.5, 4, 10, 7, fire=8, cold=8),
    MaterialEnum.WOOD: Material(1.0, 2, 1, 3, 4, 3, fire=1, cold=2),
    MaterialEnum.STONE: Material(1.5, 0, 1, 6, 10, 6, fire=5, cold=2),
    MaterialEnum.BONE: Material(0.3, 0, 1, 4, 7, 5, fire=2, cold=2),
    MaterialEnum.DRAGON_HIDE: Material(0.2, 4800, 0.5, 7, 11, 8, fire=10,
                                       cold=10),
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


class BodyPart:
  def __init__(self, name, mass):
    self.PartName = name
    self.Mass = mass


body_parts = {
    CoverageEnum.SKULL: BodyPart("Skull", 4),
    CoverageEnum.FACE: BodyPart("Face", 3),
    CoverageEnum.NECK: BodyPart("Neck", 4),
    CoverageEnum.SHOULDERS: BodyPart("Shoulders", 4),
    CoverageEnum.UPPER_ARMS: BodyPart("Upper Arms", 6),
    CoverageEnum.ELBOWS: BodyPart("Elbows", 6),
    CoverageEnum.FOREARMS: BodyPart("Forearms", 6),
    CoverageEnum.HANDS: BodyPart("Hands", 4),
    CoverageEnum.FRONT_THORAX: BodyPart("Thorax (front)", 6),
    CoverageEnum.REAR_THORAX: BodyPart("Thorax (back)", 6),
    CoverageEnum.FRONT_ABDOMEN: BodyPart("Abdomen (front)", 6),
    CoverageEnum.REAR_ABDOMEN: BodyPart("Abdomen (back)", 6),
    CoverageEnum.HIPS: BodyPart("Hip", 8),
    CoverageEnum.GROIN: BodyPart("Groin", 2),
    CoverageEnum.THIGHS: BodyPart("Thighs", 7),
    CoverageEnum.KNEES: BodyPart("Knee", 3),
    CoverageEnum.CALVES: BodyPart("Calves", 8),
    CoverageEnum.FEET: BodyPart("Feet", 6),
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
  WEAPON_BITE_SMALL = 10010
  WEAPON_BITE_MED = 10011
  WEAPON_BITE_LARGE = 10012
  WEAPON_CLAW_SMALL = 10020
  WEAPON_CLAW_MED = 10021
  WEAPON_CLAW_LARGE = 10022
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
    self.StorageMass = mass * materials[self.Material].StorageMod
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
               dmg_rolls=0, dmg_dice=0, dmg_mod=0,
               dmg_type=DamageTypeEnum.NONE, flags=0, eff=None):
    super().__init__(ItemTypeEnum.WEAPON, name, qual, material, mass, flags,
                     eff)
    self.Skill = skill
    self.AttackRating = ar
    self.DefenseRating = dr
    self.SingleHandPenalty = sh_penalty
    self.DamageRolls = dmg_rolls
    self.DamageDice = dmg_dice
    self.DamageMod = dmg_mod
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

class CombatActionEnum(IntEnum):
  NONE = 0
  MELEE_ATTACK = 1
  DODGE = 2
  BLOCK = 3
  SPELL = 4
  ABILITY = 5
  FLEE = 6


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


class Culture:
  def __init__(self, name, attr_max, sc_attrmax):
    self.Name = name
    self.AttrMax = attr_max
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

class SiblingRank:
  def __init__(self, name, attr_max):
    self.Name = name
    self.AttrMax = attr_max


sibling_ranks = {
    1: SiblingRank("Eldest", 25),
    2: SiblingRank("2nd Child", 50),
    3: SiblingRank("3rd Child", 70),
    4: SiblingRank("4th Child", 85),
    5: SiblingRank("5th Child", 95),
    6: SiblingRank("6th Child", 100),
}


# PARENTS

class ParentStatusEnum:
  NONE = 0
  OFFSPRING = 1
  FOSTERED = 2
  ADOPTED = 3
  BASTARD = 4
  ORPHAN = 5


class ParentStatus:
  def __init__(self, name, attr_max):
    self.Name = name
    self.AttrMax = attr_max


parent_statuses = {
    ParentStatusEnum.OFFSPRING: ParentStatus("Normal", 50),
    ParentStatusEnum.FOSTERED: ParentStatus("Fostered", 70),
    ParentStatusEnum.ADOPTED: ParentStatus("Adopted", 70),
    ParentStatusEnum.BASTARD: ParentStatus("Bastard", 85),
    ParentStatusEnum.ORPHAN: ParentStatus("Orphaned", 95),
}


# FRAME / WEIGHT

class PlayerFrameEnum:
  NONE = 0
  SCANT = 1
  LIGHT = 2
  MEDIUM = 3
  HEAVY = 4
  MASSIVE = 5


class PlayerFrame:
  def __init__(self, name, attr_max, mod):
    self.Name = name
    self.AttrMax = attr_max
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


class Comeliness:
  def __init__(self, name, attr_max):
    self.Name = name
    self.AttrMax = attr_max


comelinesses = {
    ComelinessEnum.UGLY: Comeliness("Ugly", 5),
    ComelinessEnum.PLAIN: Comeliness("Plain", 8),
    ComelinessEnum.AVERAGE: Comeliness("Average", 12),
    ComelinessEnum.ATTRACTIVE: Comeliness("Attractive", 15),
    ComelinessEnum.HANDSOME: Comeliness("Handsome", 100),
}


# COMPLEXION

class ComplexionEnum:
  NONE = 0
  FAIR = 1
  MEDIUM = 2
  DARK = 3


class Complexion:
  def __init__(self, name, attr_max, eye_mod):
    self.Name = name
    self.AttrMax = attr_max
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


class ColorHair:
  def __init__(self, name, attr_max):
    self.Name = name
    self.AttrMax = attr_max


color_hairs = {
    ColorHairEnum.BROWN: ColorHair("Brown", 40),
    ColorHairEnum.BLACK: ColorHair("Black", 55),
    ColorHairEnum.RED: ColorHair("Red", 65),
    ColorHairEnum.SILVER: ColorHair("Silver", 70),
    ColorHairEnum.BLONDE: ColorHair("Blonde", 100),
}


class ColorEyeEnum:
  NONE = 0
  HAZEL = 1
  GRAY = 2
  VIOLET = 3
  GREEN = 4
  BLUE = 5


class ColorEye:
  def __init__(self, name, attr_max):
    self.Name = name
    self.AttrMax = attr_max


color_eyes = {
    ColorEyeEnum.HAZEL: ColorEye("Hazel", 40),
    ColorEyeEnum.GRAY: ColorEye("Gray", 55),
    ColorEyeEnum.VIOLET: ColorEye("Violet", 56),
    ColorEyeEnum.GREEN: ColorEye("Green", 70),
    ColorEyeEnum.BLUE: ColorEye("Blue", 200),
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
  COMELINESS = 32
  COMPLEXION = 33
  COLOR_HAIR = 34
  COLOR_EYE = 35
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
               hidden=False):
    self.Abbrev = abbrev
    self.Name = name
    self.AttrClass = attr_class
    self.GenRolls = rolls
    self.GenDice = dice
    self.GenMod = mod
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
    ATTR_CML: Attr("CML", "Comeliness", AttrClassEnum.APPEARANCE, 3, 6, 0),
    ATTR_CPL: Attr("CPL", "Complexion", AttrClassEnum.APPEARANCE, 1, 100, 0),
    ATTR_CHR: Attr("CHR", "Hair Color", AttrClassEnum.APPEARANCE, 1, 100, 0),
    ATTR_CEY: Attr("CEY", "Eye Color", AttrClassEnum.APPEARANCE, 1, 100, 0),
    # PHYSICAL
    ATTR_STR: Attr("STR", "Strength", AttrClassEnum.PHYSICAL, 3, 6, 0),
    ATTR_STA: Attr("STA", "Stamina", AttrClassEnum.PHYSICAL, 3, 6, 0),
    ATTR_DEX: Attr("DEX", "Dexterity", AttrClassEnum.PHYSICAL, 3, 6, 0),
    ATTR_AGL: Attr("AGL", "Agility", AttrClassEnum.PHYSICAL, 3, 6, 0),
    ATTR_EYE: Attr("EYE", "Eyesight", AttrClassEnum.PHYSICAL, 3, 6, 0),
    ATTR_HRG: Attr("HRG", "Hearing", AttrClassEnum.PHYSICAL, 3, 6, 0),
    ATTR_SML: Attr("SML", "Smelling", AttrClassEnum.PHYSICAL, 3, 6, 0),
    ATTR_VOI: Attr("VOI", "Voice", AttrClassEnum.PHYSICAL, 3, 6, 0),
    ATTR_MED: Attr("MED", "Medical", AttrClassEnum.PHYSICAL, 1, 100, 0,
                   hidden=True),
    # PERSONALITY
    ATTR_INT: Attr("INT", "Intelligence", AttrClassEnum.PERSONALITY, 3, 6, 0),
    ATTR_AUR: Attr("AUR", "Aura", AttrClassEnum.PERSONALITY, 3, 6, 0),
    ATTR_WIL: Attr("WIL", "Will", AttrClassEnum.PERSONALITY, 3, 6, 0),
    ATTR_PSY: Attr("PSY", "Psyche", AttrClassEnum.PERSONALITY, 1, 100, 0,
                   hidden=True),
    # OCCUPATION
    ATTR_OCC: Attr("OCC", "Occupation", AttrClassEnum.OCCUPATION, 1, 100, 0),
}


# SKILLS

class SkillTypeEnum(IntEnum):
  NONE = 0
  AUTO = 1
  TRAIN = 2


class SkillClassEnum(IntEnum):
  NONE = 0
  PHYSICAL = 1
  COMMUNICATION = 2
  COMBAT = 3


class SkillEnum(IntEnum):
  NONE = 0
  # PHYSICAL
  ACROBATICS = 100
  CLIMBING = 101
  DANCING = 102
  JUMPING = 103
  LEGERDEMAIN = 104
  STEALTH = 105
  SWIMMING = 106
  THROWING = 107
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
  def __init__(self, name, skill_type, skill_class, attr1=AttrEnum.NONE,
               attr2=AttrEnum.NONE, attr3=AttrEnum.NONE, oml_mod=1,
               sunsign_mod=None):
    self.Name = name
    self.SkillType = skill_type
    self.SkillClass = skill_class
    self.Attr1 = attr1
    self.Attr2 = attr2
    self.Attr3 = attr3
    self.OMLMod = oml_mod
    self.SunsignMod = dict()
    if sunsign_mod is not None:
      for ss, mod in sunsign_mod.items():
        self.SunsignMod.update({ss: mod})


skills = {
    # PHYSICAL
    SkillEnum.ACROBATICS:
        Skill("Acrobatics", SkillTypeEnum.TRAIN, SkillClassEnum.PHYSICAL,
              ATTR_STR, ATTR_AGL, ATTR_AGL, 2,
              {SS_NAD: 2, SS_HIR: 1}),
    SkillEnum.CLIMBING:
        Skill("Climbing", SkillTypeEnum.AUTO, SkillClassEnum.PHYSICAL,
              ATTR_STR, ATTR_DEX, ATTR_AGL, 4,
              {SS_ULA: 2, SS_ARA: 2}),
    SkillEnum.DANCING:
        Skill("Dancing", SkillTypeEnum.TRAIN, SkillClassEnum.PHYSICAL,
              ATTR_DEX, ATTR_AGL, ATTR_AGL, 2,
              {SS_ULA: 1, SS_LAD: 1}),
    SkillEnum.JUMPING:
        Skill("Jumping", SkillTypeEnum.AUTO, SkillClassEnum.PHYSICAL,
              ATTR_STR, ATTR_AGL, ATTR_AGL, 4,
              {SS_NAD: 2, SS_HIR: 2}),
    SkillEnum.LEGERDEMAIN:
        Skill("Legerdemain", SkillTypeEnum.TRAIN, SkillClassEnum.PHYSICAL,
              ATTR_DEX, ATTR_DEX, ATTR_WIL, 1,
              {SS_SKO: 2, SS_TAI: 2, SS_TAR: 2}),
    SkillEnum.STEALTH:
        Skill("Stealth", SkillTypeEnum.AUTO, SkillClassEnum.PHYSICAL,
              ATTR_AGL, ATTR_HRG, ATTR_WIL, 3,
              {SS_HIR: 2, SS_TAR: 2, SS_TAI: 2}),
    SkillEnum.SWIMMING:
        Skill("Swimming", SkillTypeEnum.TRAIN, SkillClassEnum.PHYSICAL,
              ATTR_STA, ATTR_DEX, ATTR_AGL, 1,
              {SS_SKO: 1, SS_MAS: 3, SS_LAD: 3}),
    SkillEnum.THROWING:
        Skill("Throwing", SkillTypeEnum.AUTO, SkillClassEnum.PHYSICAL,
              ATTR_STR, ATTR_DEX, ATTR_EYE, 4,
              {SS_HIR: 2, SS_TAR: 1, SS_NAD: 1}),
    # COMMUNICATION
    SkillEnum.AWARENESS:
        Skill("Awareness", SkillTypeEnum.AUTO,
              SkillClassEnum.COMMUNICATION,
              ATTR_EYE, ATTR_HRG, ATTR_SML, 4,
              {SS_HIR: 2, SS_TAR: 2}),
    SkillEnum.AWARENESS:
        Skill("Intrigue", SkillTypeEnum.AUTO,
              SkillClassEnum.COMMUNICATION,
              ATTR_INT, ATTR_AUR, ATTR_WIL, 3,
              {SS_TAI: 1, SS_TAR: 1, SS_SKO: 1}),
    SkillEnum.MENTAL_CONFLICT:
        Skill("Mental Conflict", SkillTypeEnum.TRAIN,
              SkillClassEnum.COMMUNICATION,
              ATTR_AUR, ATTR_WIL, ATTR_WIL, 3),
    SkillEnum.ORATORY:
        Skill("Oratory", SkillTypeEnum.AUTO, SkillClassEnum.COMMUNICATION,
              ATTR_CML, ATTR_VOI, ATTR_INT, 2,
              {SS_TAR: 1}),
    SkillEnum.RHETORIC:
        Skill("Rhetoric", SkillTypeEnum.AUTO,
              SkillClassEnum.COMMUNICATION,
              ATTR_VOI, ATTR_INT, ATTR_WIL, 3,
              {SS_TAI: 1, SS_TAR: 1, SS_SKO: 1}),
    SkillEnum.SINGING:
        Skill("Singing", SkillTypeEnum.AUTO, SkillClassEnum.COMMUNICATION,
              ATTR_HRG, ATTR_VOI, ATTR_VOI, 3,
              {SS_MAS: 1}),
    # COMBAT
    SkillEnum.INITIATIVE:
        Skill("Initiative", SkillTypeEnum.AUTO, SkillClassEnum.COMBAT,
              ATTR_AGL, ATTR_WIL, ATTR_WIL, 4),
    SkillEnum.UNARMED:
        Skill("Unarmed Combat", SkillTypeEnum.AUTO, SkillClassEnum.COMBAT,
              ATTR_STR, ATTR_DEX, ATTR_AGL, 4,
              {SS_MAS: 2, SS_LAD: 2, SS_ULA: 2}),
    SkillEnum.RIDING:
        Skill("Riding", SkillTypeEnum.TRAIN, SkillClassEnum.COMBAT,
              ATTR_DEX, ATTR_AGL, ATTR_WIL, 1,
              {SS_ULA: 1, SS_ARA: 1}),
}


class SkillTraining:
  def __init__(self, points, att=0):
    self.Points = points
    self.Attempts = att


# GENERIC PERSON

class PersonEnum(IntEnum):
  NONE = 0
  MON_RAT = 100
  BL_KEEP_GUARD = 10000


class PersonTypeEnum(IntEnum):
  NONE = 0
  MONSTER = 1
  NPC = 2
  PLAYER = 4


class PersonFlagEnum(IntEnum):
  COMBAT = 0
  AGGRESSIVE = 1
  SHOPKEEP = 2


PERS_COMBAT = 1 << PersonFlagEnum.COMBAT
PERS_AGGRESSIVE = 1 << PersonFlagEnum.AGGRESSIVE
PERS_SHOPKEEP = 1 << PersonFlagEnum.SHOPKEEP


class ItemLink:
  def __init__(self, qty=1, equip=False):
    self.Quantity = qty
    self.Equipped = equip


class Person:
  def __init__(self, person_type, name, long_desc="", flags=0, cur=0, it=None):
    # None == Template
    self.PersonType = person_type
    self.Name = name
    self.LongDescription = long_desc
    self.Flags = flags
    self.Action = CombatActionEnum.NONE
    self.CombatEnemy = None
    self.Currency = cur
    self.Attr = dict()
    self.SkillTrainings = dict()
    self.Effects = []
    self.ItemLinks = dict()
    if it is not None:
      for item_id, il in it.items():
        self.AddItem(item_id, il)

  def Copy(self, p):
    self.PersonType = p.PersonType
    self.Name = p.Name
    self.Flags = p.Flags
    self.Action = p.Action
    self.CombatEnemy = None
    self.Currency = p.Currency
    self.Attr.clear()
    for attr_id, value in p.Attr.items():
      self.Attr.update({attr_id: value})
    self.SkillTrainings.clear()
    for skill_id, st in p.SkillTrainings.items():
      self.SkillTrainings.update({skill_id: st})
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

  def SkillBase(self, skill_id):
    sb = round((self.Attr[skills[skill_id].Attr1] + \
                self.Attr[skills[skill_id].Attr2] + \
                self.Attr[skills[skill_id].Attr3]) / 3)
    return sb

  def SkillML(self, skill_id):
    ml = self.SkillBase(skill_id) * skills[skill_id].OMLMod
    ml += self.SkillTrainings[skill_id].Points
    return ml


# MONSTER

class Monster(Person):
  def __init__(self, name, long_desc, hp, skin, flags=0, attacks=None,
               loot=None):
    super().__init__(PersonTypeEnum.MONSTER, name, long_desc, flags)
    self.HitPoints_Max = hp
    self.SkinMaterial = skin
    self.Attacks = dict()
    self.Loot = dict()
    self.ResetStats()
    if attacks is not None:
      for item_id, chance in attacks.items():
        self.Attacks.update({item_id: chance})
    if loot is not None:
      for item_id, chance in loot.items():
        self.Loot.update({item_id: chance})
    # TODO: Initiative Stat
    # TODO: Currency drop
    # TODO: Loot drop

  def ResetStats(self):
    self.HitPoints_Cur = self.HitPoints_Max
    super().ResetStats()


# NPC

class NPC(Person):
  def __init__(self, name, long_desc, hp, flags=0, eq=None):
    super().__init__(PersonTypeEnum.NPC, name, long_desc, flags, it=eq)
    self.HitPoints_Max = hp
    self.ResetStats()
    # TODO: Items
    # TODO: Initiative Stat
    # TODO: Currency drop
    # TODO: Loot drop

  def ResetStats(self):
    self.HitPoints_Cur = self.HitPoints_Max
    super().ResetStats()


# PLAYER

class Player(Person):
  def __init__(self, name=""):
    super().__init__(PersonTypeEnum.PLAYER, name, "player")
    self.Password = ""
    self.Sunsign = SunsignEnum.NONE
    self.HitPoints_Cur = -1
    self.MagicPoints_Cur = -1
    self.Command = ""
    self.Room = None
    self.LastRoom = None

  def Copy(self, p):
    super().Copy(p)
    self.HitPoints_Cur = p.HitPoints_Cur
    self.MagicPoints_Cur = p.MagicPoints_Cur
    self.Room = p.Room
    self.LastRoom = p.LastRoom
    self.CalcSunsign()

  def SetRoom(self, room_id):
    self.LastRoom = self.Room
    self.Room = room_id

  def CalcSunsign(self):
    for ss_id, ss in sunsigns.items():
      if (self.Attr[AttrEnum.BIRTH_MONTH] == ss.StartMonth and \
         self.Attr[AttrEnum.BIRTH_DAY] >= ss.StartDay) or \
         (self.Attr[AttrEnum.BIRTH_MONTH] == ss.EndMonth and \
         self.Attr[AttrEnum.BIRTH_DAY] <= ss.EndDay):
          self.Sunsign = ss_id
          break

  def GenAttr(self):
    # Generate Attributes
    for attr_id, attr in attributes.items():
      self.Attr.update({attr_id: roll(attr.GenRolls, attr.GenDice) + \
                        attr.GenMod})
    self.CalcSunsign()
    # Sibling Count includes Sibling Rank
    self.Attr[AttrEnum.SIBLING_COUNT] += self.AttrSiblingRank()

  def GenSkills(self):
    for skill_id, skill in skills.items():
      if skill.SkillType == SkillTypeEnum.AUTO:
        points = 0
        for ss_id, mod in skills[skill_id].SunsignMod.items():
          if self.Sunsign == ss_id:
            points += mod
        self.SkillTrainings.update({skill_id: SkillTraining(points)})

  def AttrSexStr(self):
    if self.Attr[AttrEnum.SEX] <= 48:
      return "Male"
    else:
      return "Female"

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

  def AttrWeight(self):
    ret = player_weights[self.Attr[AttrEnum.HEIGHT]]
    ret *= player_frames[self.AttrFrame()].ModPercent
    return round(ret)

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

  def AttrEndurance(self):
    ret = self.Attr[AttrEnum.STRENGTH]
    ret += self.Attr[AttrEnum.STAMINA]
    ret += self.Attr[AttrEnum.WILL]
    return round(ret / 3)


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


class Exit:
  def __init__(self, room_id, name="", lock=False, key_item=ItemEnum.NONE):
    self.Room = room_id
    self.ExitName = name
    self.Locked = lock
    self.Key = key_item


class PersonLink:
  def __init__(self, person_id, unique):
    self.Person = person_id
    self.UUID = unique
    self.HitPoints_Cur = -1
    self.MagicPoints_Cur = -1
    self.CombatEnemy = None


class RoomSpawn:
  def __init__(self, person_id, chance, max_qty=1, delay=60):
    self.Person = person_id
    self.Chance = chance
    self.MaxQuantity = max_qty
    self.SpawnDelaySeconds = delay
    self.LastSpawnCheck = 0


class Room:
  def __init__(self, title, short_desc="", long_desc=None, func=None,
               persons=None, exits=None, room_items=None, spawns=None):
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
    if persons is not None:
      for person_id in persons:
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

  def AddItem(self, item_id, item):
    if item_id in self.RoomItems:
      self.RoomItems[item_id].Quantity += item.Quantity
    else:
      self.RoomItems.update({item_id: item})

  def RemoveItem(self, item_id, item):
    if item_id in self.RoomItems:
      if self.RoomItems[item_id].Quantity > item.Quantity:
        self.RoomItems[item_id].Quantity -= item.Quantity
      else:
        self.RoomItems.pop(item_id)

  def AddPerson(self, person_id):
    x = PersonLink(person_id, uuid4())
    self.Persons.append(x)

  def RemovePerson(self, uid):
    for x in self.Persons:
      if x == uid:
        self.Persons.remove(x)
        break


# FORMATTING

class ANSI:
  RESET_CURSOR = "\x1B[1;1H"
  CLEAR = "\x1B[2J"
  TEXT_NORMAL = "\x1B[0m"
  TEXT_BOLD = "\x1B[1m"


# vim: tabstop=2 shiftwidth=2 expandtab:
