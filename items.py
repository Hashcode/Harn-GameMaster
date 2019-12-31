# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

from global_defines import (DiceRoll, MaterialEnum, QualityEnum, CoverageEnum,
                            Effect, EffectTypeEnum, ItemFlagEnum, ItemTypeEnum,
                            ItemEnum, Item, Weapon, Shield, Armor, Ring,
                            DamageTypeEnum, SkillEnum,
                            Trigger, TriggerTypeEnum)


# Coverage Abbreviations

COV_Sk = 1 << CoverageEnum.SKULL
COV_Fa = 1 << CoverageEnum.FACE
COV_Nk = 1 << CoverageEnum.NECK
COV_Sh = 1 << CoverageEnum.SHOULDERS
COV_Ua = 1 << CoverageEnum.UPPER_ARMS
COV_El = 1 << CoverageEnum.ELBOWS
COV_Fo = 1 << CoverageEnum.FOREARMS
COV_Ha = 1 << CoverageEnum.HANDS
COV_Tx_F = 1 << CoverageEnum.THORAX_FRONT
COV_Tx_R = 1 << CoverageEnum.THORAX_REAR
COV_Ab_F = 1 << CoverageEnum.ABDOMEN_FRONT
COV_Ab_R = 1 << CoverageEnum.ABDOMEN_REAR
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

# Item Flag Abbreviations

IFLAG_NO_SELL = 1 << ItemFlagEnum.NO_SELL
IFLAG_NO_DROP = 1 << ItemFlagEnum.NO_DROP
IFLAG_NO_GET = 1 << ItemFlagEnum.NO_GET
IFLAG_LIGHT = 1 << ItemFlagEnum.LIGHT
IFLAG_MAGIC = 1 << ItemFlagEnum.MAGIC
IFLAG_HIDDEN = 1 << ItemFlagEnum.HIDDEN
IFLAG_INVIS = 1 << ItemFlagEnum.INVIS
IFLAG_QUEST = 1 << ItemFlagEnum.QUEST


# Armor Layer Abbreviations

ARMOR_LAYER1 = 0
ARMOR_LAYER1_5 = 1
ARMOR_LAYER2 = 2
ARMOR_LAYER2_5 = 3
ARMOR_LAYER3 = 4
ARMOR_LAYER3_5 = 5
ARMOR_LAYER4 = 6
ARMOR_LAYER4_5 = 7
ARMOR_LAYER5 = 8
ARMOR_LAYER5_5 = 9

AL_1 = 1 << ARMOR_LAYER1
AL_1_5 = 1 << ARMOR_LAYER1_5
AL_2 = 1 << ARMOR_LAYER2
AL_2_5 = 1 << ARMOR_LAYER2_5
AL_3 = 1 << ARMOR_LAYER3
AL_3_5 = 1 << ARMOR_LAYER3_5
AL_4 = 1 << ARMOR_LAYER4
AL_4_5 = 1 << ARMOR_LAYER4_5
AL_5 = 1 << ARMOR_LAYER5
AL_5_5 = 1 << ARMOR_LAYER5_5


items = {
    # WEAPON [UNARMED]
    ItemEnum.WEAPON_HAND:
        Weapon("punch", QualityEnum.AVE, MaterialEnum.BONE, 0,
               SkillEnum.UNARMED, 0, 5, 0, DiceRoll(1, 2),
               DamageTypeEnum.BLUNT, flags=IFLAG_NO_SELL | IFLAG_NO_DROP),
    ItemEnum.WEAPON_FOOT:
        Weapon("kick", QualityEnum.AVE, MaterialEnum.BONE, 0,
               SkillEnum.UNARMED, 5, 5, 0, DiceRoll(1, 2),
               DamageTypeEnum.BLUNT,
               flags=IFLAG_NO_SELL | IFLAG_NO_DROP),
    # WEAPON [DAGGER]
    ItemEnum.WEAPON_KNIFE:
        Weapon("hunting knife", QualityEnum.POR, MaterialEnum.STEEL_WOOD, 1.5,
               SkillEnum.DAGGER, 5, 0, 0, DiceRoll(1, 4),
               DamageTypeEnum.PIERCE),
    ItemEnum.WEAPON_DAGGER:
        Weapon("sharp dagger", QualityEnum.AVE, MaterialEnum.STEEL, 1,
               SkillEnum.DAGGER, 5, 5, 0, DiceRoll(1, 6),
               DamageTypeEnum.PIERCE),
    ItemEnum.WEAPON_WICKED_DAGGER:
        Weapon("wicked-looking dagger", QualityEnum.INF, MaterialEnum.STEEL, 1,
               SkillEnum.DAGGER, 5, 5, 0, DiceRoll(1, 6),
               DamageTypeEnum.PIERCE),
    ItemEnum.WEAPON_MAIN_GAUCHE:
        Weapon("small parrying blade", QualityEnum.AVE,
               MaterialEnum.STEEL, 1.4,
               SkillEnum.DAGGER, 5, 10, 0, DiceRoll(1, 6),
               DamageTypeEnum.PIERCE),
    # WEAPON [SWORD]
    ItemEnum.WEAPON_SHORTSWORD:
        Weapon("steel shortsword", QualityEnum.SUP, MaterialEnum.STEEL, 2.5,
               SkillEnum.SWORD, 10, 5, 0, DiceRoll(1, 6, 1),
               DamageTypeEnum.EDGE),
    ItemEnum.WEAPON_FALCHION:
        Weapon("steel falchion", QualityEnum.AVE, MaterialEnum.STEEL, 4.8,
               SkillEnum.SWORD, 15, 5, 0, DiceRoll(1, 6, 1),
               DamageTypeEnum.EDGE),
    ItemEnum.WEAPON_BROADSWORD:
        Weapon("steel broadsword", QualityEnum.AVE, MaterialEnum.STEEL, 6,
               SkillEnum.SWORD, 15, 10, 0, DiceRoll(1, 6, 2),
               DamageTypeEnum.EDGE),
    ItemEnum.WEAPON_BASTARD_SWORD:
        Weapon("steel bastard sword", QualityEnum.AVE, MaterialEnum.STEEL, 7.5,
               SkillEnum.SWORD, 20, 10, 10, DiceRoll(1, 6, 2),
               DamageTypeEnum.EDGE),
    ItemEnum.WEAPON_BATTLESWORD:
        Weapon("steel battlesword", QualityEnum.AVE, MaterialEnum.STEEL, 9.5,
               SkillEnum.SWORD, 25, 10, 20, DiceRoll(2, 6, 1),
               DamageTypeEnum.EDGE),
    # WEAPON [CLUB]
    ItemEnum.WEAPON_STICK:
        Weapon("wooden stick", QualityEnum.TER, MaterialEnum.WOOD, 5,
               SkillEnum.CLUB, 10, 5, 0, DiceRoll(0, 0, 2),
               DamageTypeEnum.BLUNT, flags=IFLAG_NO_SELL),
    ItemEnum.WEAPON_CLUB:
        Weapon("wooden club", QualityEnum.INF, MaterialEnum.WOOD, 4.5,
               SkillEnum.CLUB, 15, 5, 0, DiceRoll(1, 4),
               DamageTypeEnum.BLUNT),
    ItemEnum.WEAPON_MACE:
        Weapon("iron mace", QualityEnum.SUP, MaterialEnum.STEEL_WOOD, 6,
               SkillEnum.CLUB, 15, 5, 0, DiceRoll(1, 6, 1),
               DamageTypeEnum.BLUNT),
    ItemEnum.WEAPON_MORNINGSTAR:
        Weapon("morningstar",
               QualityEnum.INF, MaterialEnum.STEEL_WOOD, 7.5,
               SkillEnum.CLUB, 20, 5, 10, DiceRoll(1, 6, 2),
               DamageTypeEnum.PIERCE),
    ItemEnum.WEAPON_MAUL:
        Weapon("spiked maul", QualityEnum.SUP, MaterialEnum.WOOD, 8,
               SkillEnum.CLUB, 20, 5, 20, DiceRoll(1, 6, 3),
               DamageTypeEnum.BLUNT),
    # WEAPON [AXE]
    ItemEnum.WEAPON_SICKLE:
        Weapon("sickle", QualityEnum.INF, MaterialEnum.STEEL_WOOD, 1.5,
               SkillEnum.AXE, 5, 5, 0, DiceRoll(1, 4, 0),
               DamageTypeEnum.EDGE),
    ItemEnum.WEAPON_HATCHET:
        Weapon("hatchet", QualityEnum.POR, MaterialEnum.STEEL_WOOD, 2.5,
               SkillEnum.AXE, 5, 5, 0, DiceRoll(1, 6, 0),
               DamageTypeEnum.EDGE),
    ItemEnum.WEAPON_HANDAXE:
        Weapon("handaxe", QualityEnum.SUP, MaterialEnum.STEEL_WOOD, 5,
               SkillEnum.AXE, 10, 5, 0, DiceRoll(1, 6, 1),
               DamageTypeEnum.EDGE),
    ItemEnum.WEAPON_WARHAMMER:
        Weapon("warhammer", QualityEnum.SUP, MaterialEnum.STEEL_WOOD, 6.3,
               SkillEnum.AXE, 15, 5, 5, DiceRoll(1, 6, 1),
               DamageTypeEnum.BLUNT),
    ItemEnum.WEAPON_BATTLEAXE:
        Weapon("battleaxe", QualityEnum.SUP, MaterialEnum.STEEL_WOOD, 7.5,
               SkillEnum.AXE, 20, 10, 15, DiceRoll(1, 6, 2),
               DamageTypeEnum.EDGE),
    # WEAPON [FLAIL]
    ItemEnum.WEAPON_GRAINFLAIL:
        Weapon("grainflail", QualityEnum.SUP, MaterialEnum.WOOD, 4,
               SkillEnum.FLAIL, 20, 5, 0, DiceRoll(1, 6),
               DamageTypeEnum.BLUNT),
    ItemEnum.WEAPON_BALL_AND_CHAIN:
        Weapon("ball and chain", QualityEnum.AVE, MaterialEnum.STEEL_WOOD, 6.4,
               SkillEnum.FLAIL, 20, 10, 0, DiceRoll(1, 6, 2),
               DamageTypeEnum.BLUNT),
    ItemEnum.WEAPON_WARFLAIL:
        Weapon("warflail", QualityEnum.AVE, MaterialEnum.STEEL_WOOD, 7.5,
               SkillEnum.FLAIL, 20, 10, 20, DiceRoll(2, 6),
               DamageTypeEnum.BLUNT),
    # WEAPON [SPEAR]
    ItemEnum.WEAPON_STAFF:
        Weapon("wooden staff", QualityEnum.SUP, MaterialEnum.WOOD, 6,
               SkillEnum.SPEAR, 20, 15, 10, DiceRoll(1, 6),
               DamageTypeEnum.BLUNT),
    ItemEnum.WEAPON_JAVELIN:
        Weapon("javelin", QualityEnum.AVE, MaterialEnum.STEEL_WOOD, 5,
               SkillEnum.SPEAR, 15, 5, 0, DiceRoll(1, 6, 1),
               DamageTypeEnum.PIERCE),
    ItemEnum.WEAPON_SPEAR:
        Weapon("spear", QualityEnum.AVE, MaterialEnum.STEEL_WOOD, 6,
               SkillEnum.SPEAR, 20, 10, 5, DiceRoll(1, 6, 2),
               DamageTypeEnum.PIERCE),
    ItemEnum.WEAPON_TRIDENT:
        Weapon("trident", QualityEnum.AVE, MaterialEnum.STEEL_WOOD, 8.2,
               SkillEnum.SPEAR, 20, 15, 10, DiceRoll(1, 6, 2),
               DamageTypeEnum.PIERCE),
    ItemEnum.WEAPON_LANCE:
        Weapon("lance", QualityEnum.AVE, MaterialEnum.STEEL_WOOD, 10,
               SkillEnum.SPEAR, 25, 5, 15, DiceRoll(2, 6),
               DamageTypeEnum.PIERCE),
    # WEAPON [POLEARM]
    ItemEnum.WEAPON_GLAIVE:
        Weapon("glaive", QualityEnum.INF, MaterialEnum.STEEL_WOOD, 9,
               SkillEnum.POLEARM, 25, 10, 20, DiceRoll(1, 6, 3),
               DamageTypeEnum.EDGE),
    ItemEnum.WEAPON_POLEAXE:
        Weapon("poleaxe", QualityEnum.AVE, MaterialEnum.STEEL_WOOD, 10.5,
               SkillEnum.POLEARM, 25, 5, 20, DiceRoll(2, 6, 0),
               DamageTypeEnum.EDGE),
    ItemEnum.WEAPON_PIKE:
        Weapon("pike", QualityEnum.INF, MaterialEnum.STEEL_WOOD, 15,
               SkillEnum.POLEARM, 25, 5, 25, DiceRoll(2, 6, 0),
               DamageTypeEnum.PIERCE),

    # SHIELD
    ItemEnum.SHIELD_BUCKLER_BANDED:
        Shield("buckler",
               QualityEnum.AVE, MaterialEnum.STEEL_WOOD, 3,
               SkillEnum.SHIELD, 5, 15),
    ItemEnum.SHIELD_ROUND_BANDED:
        Shield("round shield",
               QualityEnum.INF, MaterialEnum.STEEL_WOOD, 6.8,
               SkillEnum.SHIELD, 5, 20),
    ItemEnum.SHIELD_KNIGHT_STEEL:
        Shield("knight shield",
               QualityEnum.AVE, MaterialEnum.STEEL_WOOD, 7.5,
               SkillEnum.SHIELD, 5, 20),
    ItemEnum.SHIELD_KITE_BANDED:
        Shield("kite shield",
               QualityEnum.AVE, MaterialEnum.STEEL_WOOD, 9,
               SkillEnum.SHIELD, 5, 25),
    ItemEnum.SHIELD_TOWER_BANDED:
        Shield("tower shield",
               QualityEnum.AVE, MaterialEnum.STEEL_WOOD, 11,
               SkillEnum.SHIELD, 5, 25),

    # ARMOR [CLOTH]
    ItemEnum.ARMOR_CAP_CLOTH:
        Armor("cloth cap",
              QualityEnum.AVE, MaterialEnum.CLOTH, AL_1,
              COV_Sk),
    ItemEnum.ARMOR_HOOD_CLOTH:
        Armor("cloth hood",
              QualityEnum.AVE, MaterialEnum.CLOTH, AL_1,
              COV_Sk | COV_Nk),
    ItemEnum.ARMOR_VEST_CLOTH:
        Armor("cloth vest",
              QualityEnum.AVE, MaterialEnum.CLOTH, AL_1,
              COV_Sh | COV_Tx | COV_Ab),
    ItemEnum.ARMOR_TUNIC_CLOTH:
        Armor("cloth tunic",
              QualityEnum.AVE, MaterialEnum.CLOTH, AL_1,
              COV_Ua | COV_Sh | COV_Tx | COV_Ab | COV_Hp | COV_Gr),
    ItemEnum.ARMOR_SURCOAT_CLOTH:
        Armor("cloth surcoat",
              QualityEnum.AVE, MaterialEnum.CLOTH, AL_1,
              COV_Sh | COV_Tx | COV_Ab | COV_Hp | COV_Gr | COV_Th),
    ItemEnum.ARMOR_ROBE_CLOTH:
        Armor("cloth robe",
              QualityEnum.AVE, MaterialEnum.CLOTH, AL_1,
              COV_Ua | COV_Sh | COV_Tx | COV_Ab | COV_Hp | COV_Gr | COV_Fo | \
              COV_El | COV_Th | COV_Kn | COV_Ca),
    ItemEnum.ARMOR_LEGGINGS_CLOTH:
        Armor("cloth leggings",
              QualityEnum.AVE, MaterialEnum.CLOTH, AL_1_5,
              COV_Hp | COV_Gr | COV_Th | COV_Kn | COV_Ca | COV_Ft),
    # ARMOR [QUILT]
    ItemEnum.ARMOR_CAP_QUILT:
        Armor("quilt cap",
              QualityEnum.AVE, MaterialEnum.QUILT, AL_2,
              COV_Sk),
    ItemEnum.ARMOR_COWL_QUILT:
        Armor("quilt cowl",
              QualityEnum.AVE, MaterialEnum.QUILT, AL_2,
              COV_Sk | COV_Nk),
    ItemEnum.ARMOR_TUNIC_QUILT:
        Armor("quilt tunic",
              QualityEnum.AVE, MaterialEnum.QUILT, AL_2,
              COV_Ua | COV_Sh | COV_Tx | COV_Ab | COV_Hp | COV_Gr),
    ItemEnum.ARMOR_GAMBESON_QUILT:
        Armor("quilt gambeson",
              QualityEnum.AVE, MaterialEnum.QUILT, AL_2,
              COV_Fo | COV_El | COV_Ua | COV_Sh | COV_Tx | COV_Ab | COV_Hp | \
              COV_Gr | COV_Th),
    ItemEnum.ARMOR_LEGGINGS_QUILT:
        Armor("quilt leggings",
              QualityEnum.AVE, MaterialEnum.QUILT, AL_2_5,
              COV_Hp | COV_Gr | COV_Th | COV_Kn | COV_Ca | COV_Ft),
    # ARMOR [LEATHER]
    ItemEnum.ARMOR_CAP_LEATHER:
        Armor("leather cap",
              QualityEnum.AVE, MaterialEnum.LEATHER, AL_3,
              COV_Sk),
    ItemEnum.ARMOR_COWL_LEATHER:
        Armor("leather cowl",
              QualityEnum.AVE, MaterialEnum.LEATHER, AL_3,
              COV_Sk | COV_Nk),
    ItemEnum.ARMOR_VEST_LEATHER:
        Armor("leather vest",
              QualityEnum.AVE, MaterialEnum.LEATHER, AL_3,
              COV_Sh | COV_Tx | COV_Ab),
    ItemEnum.ARMOR_TUNIC_LEATHER:
        Armor("leather tunic",
              QualityEnum.AVE, MaterialEnum.LEATHER, AL_3,
              COV_Ua | COV_Sh | COV_Tx | COV_Ab | COV_Hp | COV_Gr),
    ItemEnum.ARMOR_SURCOAT_LEATHER:
        Armor("leather surcoat",
              QualityEnum.AVE, MaterialEnum.LEATHER, AL_3,
              COV_Sh | COV_Tx | COV_Ab | COV_Hp | COV_Gr | COV_Th),
    ItemEnum.ARMOR_LEGGINGS_LEATHER:
        Armor("leather leggings",
              QualityEnum.AVE, MaterialEnum.LEATHER, AL_3_5,
              COV_Hp | COV_Gr | COV_Th | COV_Kn | COV_Ca | COV_Ft),
    ItemEnum.ARMOR_SHOES_LEATHER:
        Armor("leather shoes",
              QualityEnum.AVE, MaterialEnum.LEATHER, AL_3_5,
              COV_Ft),
    ItemEnum.ARMOR_CALF_BOOTS_LEATHER:
        Armor("leather calf boots",
              QualityEnum.AVE, MaterialEnum.LEATHER, AL_3_5,
              COV_Ca | COV_Ft),
    ItemEnum.ARMOR_KNEE_BOOTS_LEATHER:
        Armor("leather knee boots",
              QualityEnum.AVE, MaterialEnum.LEATHER, AL_3_5,
              COV_Kn | COV_Ca | COV_Ft),
    ItemEnum.ARMOR_GAUNTLETS_LEATHER:
        Armor("leather gauntlets",
              QualityEnum.AVE, MaterialEnum.LEATHER, AL_3,
              COV_Ha),
    ItemEnum.ARMOR_APRON_LEATHER:
        Armor("leather apron",
              QualityEnum.AVE, MaterialEnum.LEATHER, AL_3,
              COV_Tx | COV_Ab | COV_Hp | COV_Gr | COV_Th),
    # ARMOR [KURBUL]
    ItemEnum.ARMOR_HALFHELM_KURBUL:
        Armor("hardened leather halfhelm",
              QualityEnum.AVE, MaterialEnum.KURBUL, AL_3 | AL_4 | AL_5,
              COV_Sk),
    ItemEnum.ARMOR_BREASTPLATE_KURBUL:
        Armor("hardened leather breastplate",
              QualityEnum.AVE, MaterialEnum.KURBUL, AL_3 | AL_4 | AL_5,
              COV_Ch),
    ItemEnum.ARMOR_BACKPLATE_KURBUL:
        Armor("hardened leather backplate",
              QualityEnum.AVE, MaterialEnum.KURBUL, AL_3 | AL_4 | AL_5,
              COV_Bk),
    ItemEnum.ARMOR_AILETTES_KURBUL:
        Armor("hardened leather ailettes",
              QualityEnum.AVE, MaterialEnum.KURBUL, AL_3 | AL_4 | AL_5,
              COV_Sh),
    ItemEnum.ARMOR_REREBRACES_KURBUL:
        Armor("hardened leather rerebraces",
              QualityEnum.AVE, MaterialEnum.KURBUL, AL_3 | AL_4 | AL_5,
              COV_Ua),
    ItemEnum.ARMOR_COUDES_KURBUL:
        Armor("hardened leather coudes",
              QualityEnum.AVE, MaterialEnum.KURBUL, AL_3 | AL_4 | AL_5,
              COV_El),
    ItemEnum.ARMOR_VAMBRACES_KURBUL:
        Armor("hardened leather vambraces",
              QualityEnum.AVE, MaterialEnum.KURBUL, AL_3 | AL_4 | AL_5,
              COV_Fo),
    ItemEnum.ARMOR_KNEECOPS_KURBUL:
        Armor("hardened leather kneecops",
              QualityEnum.AVE, MaterialEnum.KURBUL, AL_3_5 | AL_4 | AL_5,
              COV_Kn),
    ItemEnum.ARMOR_GREAVES_KURBUL:
        Armor("hardened leather greaves",
              QualityEnum.AVE, MaterialEnum.KURBUL, AL_3_5 | AL_4 | AL_5,
              COV_Ca),
    # ARMOR [LEATHER+RING]
    ItemEnum.ARMOR_HALFHELM_LEATHER_RING:
        Armor("studded leather halfhelm",
              QualityEnum.AVE, MaterialEnum.LEATHER_RING, AL_3 | AL_4 | AL_5,
              COV_Sk),
    ItemEnum.ARMOR_VEST_LEATHER_RING:
        Armor("studded leather vest",
              QualityEnum.AVE, MaterialEnum.LEATHER_RING, AL_3 | AL_4 | AL_5,
              COV_Sh | COV_Tx | COV_Ab),
    ItemEnum.ARMOR_BYRNIE_LEATHER_RING:
        Armor("studded leather byrnie",
              QualityEnum.AVE, MaterialEnum.LEATHER_RING, AL_3 | AL_4 | AL_5,
              COV_Ua | COV_Sh | COV_Tx | COV_Ab | COV_Hp | COV_Gr),
    ItemEnum.ARMOR_HAUBERK_LEATHER_RING:
        Armor("studded leather hauberk",
              QualityEnum.AVE, MaterialEnum.LEATHER_RING, AL_3 | AL_4 | AL_5,
              COV_Fo | COV_El | COV_Ua | COV_Sh | COV_Tx | COV_Ab | COV_Hp | \
              COV_Gr | COV_Th),
    ItemEnum.ARMOR_LEGGINGS_LEATHER_RING:
        Armor("studded leather leggings",
              QualityEnum.AVE, MaterialEnum.LEATHER_RING,
              AL_3_5 | AL_4_5 | AL_5_5,
              COV_Hp | COV_Gr | COV_Th | COV_Kn | COV_Ca | COV_Ft),
    ItemEnum.ARMOR_GAUNTLETS_LEATHER_RING:
        Armor("studded leather gauntlets",
              QualityEnum.AVE, MaterialEnum.LEATHER_RING, AL_3 | AL_4 | AL_5,
              COV_Ha),
    # ARMOR [MAIL]
    ItemEnum.ARMOR_COWL_MAIL:
        Armor("chainmail cowl",
              QualityEnum.AVE, MaterialEnum.MAIL, AL_4,
              COV_Sk | COV_Nk),
    ItemEnum.ARMOR_BYRNIE_MAIL:
        Armor("chainmail byrnie",
              QualityEnum.AVE, MaterialEnum.MAIL, AL_4,
              COV_Ua | COV_Sh | COV_Tx | COV_Ab | COV_Hp | COV_Gr),
    ItemEnum.ARMOR_HAUBERK_MAIL:
        Armor("chainmail hauberk",
              QualityEnum.AVE, MaterialEnum.MAIL, AL_4,
              COV_Fo | COV_El | COV_Ua | COV_Sh | COV_Tx | COV_Ab | COV_Hp | \
              COV_Gr | COV_Th),
    ItemEnum.ARMOR_LEGGINGS_MAIL:
        Armor("chainmail leggings",
              QualityEnum.AVE, MaterialEnum.MAIL, AL_4_5,
              COV_Hp | COV_Gr | COV_Th | COV_Kn | COV_Ca | COV_Ft),
    ItemEnum.ARMOR_MITTENS_MAIL:
        Armor("chainmail mittens",
              QualityEnum.AVE, MaterialEnum.MAIL, AL_4, COV_Ha),
    # ARMOR [SCALE]
    ItemEnum.ARMOR_VEST_SCALE:
        Armor("scale armor vest",
              QualityEnum.AVE, MaterialEnum.SCALE, AL_3 | AL_4 | AL_5,
              COV_Sh | COV_Tx | COV_Ab),
    ItemEnum.ARMOR_BYRNIE_SCALE:
        Armor("scale armor byrnie",
              QualityEnum.AVE, MaterialEnum.SCALE, AL_3 | AL_4 | AL_5,
              COV_Ua | COV_Sh | COV_Tx | COV_Ab | COV_Hp | COV_Gr),
    ItemEnum.ARMOR_HAUBERK_SCALE:
        Armor("scale armor hauberk",
              QualityEnum.AVE, MaterialEnum.SCALE, AL_3 | AL_4 | AL_5,
              COV_Fo | COV_El | COV_Ua | COV_Sh | COV_Tx | COV_Ab | COV_Hp | \
              COV_Gr | COV_Th),
    # ARMOR [STEEL]
    ItemEnum.ARMOR_HALFHELM_STEEL:
        Armor("steel halfhelm",
              QualityEnum.AVE, MaterialEnum.STEEL, AL_5,
              COV_Sk),
    ItemEnum.ARMOR_GREAT_HELM_STEEL:
        Armor("steel great helm",
              QualityEnum.AVE, MaterialEnum.STEEL, AL_5,
              COV_Sk | COV_Fa | COV_Nk),
    ItemEnum.ARMOR_BREASTPLATE_STEEL:
        Armor("steel breastplate",
              QualityEnum.AVE, MaterialEnum.STEEL, AL_5,
              COV_Ch),
    ItemEnum.ARMOR_BACKPLATE_STEEL:
        Armor("steel backplate",
              QualityEnum.AVE, MaterialEnum.STEEL, AL_5,
              COV_Bk),
    ItemEnum.ARMOR_AILETTES_STEEL:
        Armor("steel ailettes",
              QualityEnum.AVE, MaterialEnum.STEEL, AL_5,
              COV_Sh),
    ItemEnum.ARMOR_REREBRACES_STEEL:
        Armor("steel rerebraces",
              QualityEnum.AVE, MaterialEnum.STEEL, AL_5,
              COV_Ua),
    ItemEnum.ARMOR_COUDES_STEEL:
        Armor("steel coudes",
              QualityEnum.AVE, MaterialEnum.STEEL, AL_5,
              COV_El),
    ItemEnum.ARMOR_VAMBRACES_STEEL:
        Armor("steel vambraces",
              QualityEnum.AVE, MaterialEnum.STEEL, AL_5,
              COV_Fo),
    ItemEnum.ARMOR_KNEECOPS_STEEL:
        Armor("steel kneecops",
              QualityEnum.AVE, MaterialEnum.STEEL, AL_5_5,
              COV_Kn),
    ItemEnum.ARMOR_GREAVES_STEEL:
        Armor("steel greaves",
              QualityEnum.AVE, MaterialEnum.STEEL, AL_5_5,
              COV_Ca),
    # MISC ARMOR
    ItemEnum.ARMOR_STAINED_QUILT_TUNIC:
        Armor("stained quilt tunic",
              QualityEnum.TER, MaterialEnum.QUILT, AL_2,
              COV_Ua | COV_Sh | COV_Tx | COV_Ab | COV_Hp | COV_Gr),
    ItemEnum.ARMOR_STAINED_QUILT_COWL:
        Armor("stained quilt cowl",
              QualityEnum.TER, MaterialEnum.QUILT, AL_2,
              COV_Sk | COV_Nk),
    ItemEnum.ARMOR_STAINED_QUILT_LEGGINGS:
        Armor("stained quilt leggings",
              QualityEnum.TER, MaterialEnum.QUILT, AL_2_5,
              COV_Hp | COV_Gr | COV_Th | COV_Kn | COV_Ca | COV_Ft),

    # RING

    ItemEnum.RING_ATTACK_SILVER:
        Ring("silver ring", QualityEnum.SUP, MaterialEnum.SILVER, 0.1, 1500,
             flags=IFLAG_MAGIC, eff=[Effect(EffectTypeEnum.DEX, 1)]),

    ItemEnum.RING_HP_GOLD:
        Ring("gold ring", QualityEnum.SUP, MaterialEnum.GOLD, 0.1, 2500,
             flags=IFLAG_MAGIC, eff=[Effect(EffectTypeEnum.HP_MAX, 5)]),

    # MISC

    ItemEnum.MISC_STONE:
        Item(ItemTypeEnum.MISC, "stone", QualityEnum.TER,
             MaterialEnum.STONE, 1),
    ItemEnum.MISC_RAT_FUR:
        Item(ItemTypeEnum.MISC, "rat fur", QualityEnum.AVE,
             MaterialEnum.FUR_LT, 2,
             onDrop=[
                 Trigger(TriggerTypeEnum.MESSAGE, ["With a sigh of relief you drop a rat fur."]),
             ],
             onGet=[
                 Trigger(TriggerTypeEnum.MESSAGE, ["You pinch your nose trying to pick up the rat fur, "
                                                   "wondering if this time you'll be successful."]),
                 Trigger(TriggerTypeEnum.DENY, chance=90),
             ]),
    ItemEnum.MISC_TORCH:
        Item(ItemTypeEnum.MISC, "torch",
             QualityEnum.AVE, MaterialEnum.WOOD, 0.5,
             flags=IFLAG_LIGHT),

    # QUEST

    ItemEnum.QUEST_WEATHERED_PACKAGE:
        Item(ItemTypeEnum.QUEST, "weathered package", QualityEnum.AVE,
             MaterialEnum.LEATHER, 0.1, flags=IFLAG_QUEST),

    # KEYS

    ItemEnum.KEY_WAREHOUSE_DBL_DOOR:
        Item(ItemTypeEnum.MISC, "a large bronze key", QualityEnum.AVE,
             MaterialEnum.BRONZE, 1),
    ItemEnum.KEY_CORPORAL_APPT:
        Item(ItemTypeEnum.MISC, "a small iron key on a chain", QualityEnum.AVE,
             MaterialEnum.STEEL, 1),
}

# vim: tabstop=2 shiftwidth=2 expandtab:
