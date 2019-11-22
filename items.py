# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

from global_defines import (MaterialEnum, QualityEnum, CoverageEnum,
                            Effect, EffectTypeEnum, ItemFlagEnum, ItemTypeEnum,
                            ItemEnum, Item, Weapon, Shield, Armor, Ring,
                            DamageTypeEnum, SkillEnum, item_flags)


# Coverage Abbreviations

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

# Item Flag Abbreviations

IFLAG_NO_SELL = item_flags[ItemFlagEnum.NO_SELL].Bit
IFLAG_NO_DROP = item_flags[ItemFlagEnum.NO_DROP].Bit
IFLAG_NO_GET = item_flags[ItemFlagEnum.NO_GET].Bit
IFLAG_LIGHT = item_flags[ItemFlagEnum.LIGHT].Bit
IFLAG_MAGIC = item_flags[ItemFlagEnum.MAGIC].Bit
IFLAG_HIDDEN = item_flags[ItemFlagEnum.HIDDEN].Bit
IFLAG_INVIS = item_flags[ItemFlagEnum.INVIS].Bit


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

AL_1 = 1 << ARMOR_LAYER1
AL_1_5 = 1 << ARMOR_LAYER1_5
AL_2 = 1 << ARMOR_LAYER2
AL_2_5 = 1 << ARMOR_LAYER2_5
AL_3 = 1 << ARMOR_LAYER3
AL_3_5 = 1 << ARMOR_LAYER3_5
AL_4 = 1 << ARMOR_LAYER4
AL_4_5 = 1 << ARMOR_LAYER4_5
AL_5 = 1 << ARMOR_LAYER5


items = {
    # WEAPON [UNARMED]
    ItemEnum.WEAPON_HAND:
        Weapon("punch", QualityEnum.AVE, MaterialEnum.BONE, 0,
               SkillEnum.UNARMED, 0, 5, 0, 1, 2, 0, DamageTypeEnum.BLUNT,
               flags=IFLAG_NO_SELL | IFLAG_NO_DROP),
    ItemEnum.WEAPON_FOOT:
        Weapon("kick", QualityEnum.AVE, MaterialEnum.BONE, 0,
               SkillEnum.UNARMED, 5, 5, 0, 1, 2, 1, DamageTypeEnum.BLUNT,
               flags=IFLAG_NO_SELL | IFLAG_NO_DROP),
    ItemEnum.WEAPON_BITE_SMALL:
        Weapon("bite", QualityEnum.AVE, MaterialEnum.BONE, 0,
               SkillEnum.UNARMED, 0, 0, 0, 1, 2, 0, DamageTypeEnum.PIERCE,
               flags=IFLAG_NO_SELL | IFLAG_NO_DROP),
    ItemEnum.WEAPON_BITE_MED:
        Weapon("bite", QualityEnum.AVE, MaterialEnum.BONE, 0,
               SkillEnum.UNARMED, 0, 0, 0, 1, 4, 0, DamageTypeEnum.PIERCE,
               flags=IFLAG_NO_SELL | IFLAG_NO_DROP),
    ItemEnum.WEAPON_BITE_LARGE:
        Weapon("large bite", QualityEnum.AVE, MaterialEnum.BONE, 0,
               SkillEnum.UNARMED, 0, 0, 0, 1, 6, 0, DamageTypeEnum.PIERCE,
               flags=IFLAG_NO_SELL | IFLAG_NO_DROP),
    ItemEnum.WEAPON_CLAW_SMALL:
        Weapon("small sharp claws", QualityEnum.INF, MaterialEnum.BONE, 0,
               SkillEnum.UNARMED, 0, 0, 0, 1, 2, 0, DamageTypeEnum.EDGE,
               flags=IFLAG_NO_SELL | IFLAG_NO_DROP),
    ItemEnum.WEAPON_CLAW_MED:
        Weapon("long claws", QualityEnum.INF, MaterialEnum.BONE, 0,
               SkillEnum.UNARMED, 0, 0, 0, 1, 4, 0, DamageTypeEnum.EDGE,
               flags=IFLAG_NO_SELL | IFLAG_NO_DROP),
    ItemEnum.WEAPON_CLAW_LARGE:
        Weapon("razor-sharp claws", QualityEnum.INF, MaterialEnum.BONE, 0,
               SkillEnum.UNARMED, 0, 0, 0, 1, 6, 0, DamageTypeEnum.EDGE,
               flags=IFLAG_NO_SELL | IFLAG_NO_DROP),
    # WEAPON [DAGGER]
    ItemEnum.WEAPON_KNIFE:
        Weapon("hunting knife", QualityEnum.POR, MaterialEnum.STEEL_WOOD, 1,
               SkillEnum.DAGGER, 5, 0, 0, 1, 4, 0, DamageTypeEnum.PIERCE),
    ItemEnum.WEAPON_DAGGER:
        Weapon("sharp dagger", QualityEnum.AVE, MaterialEnum.STEEL, 1.2,
               SkillEnum.DAGGER, 5, 5, 0, 1, 6, 0, DamageTypeEnum.PIERCE),
    ItemEnum.WEAPON_MAIN_GAUCHE:
        Weapon("small parrying blade", QualityEnum.SUP, MaterialEnum.STEEL, 1.2,
               SkillEnum.DAGGER, 5, 10, 0, 1, 6, 0, DamageTypeEnum.PIERCE),
    # WEAPON [SWORD]
    ItemEnum.WEAPON_SHORTSWORD:
        Weapon("steel shortsword", QualityEnum.SUP, MaterialEnum.STEEL, 2.5,
               SkillEnum.SWORD, 10, 5, 0, 1, 6, 1, DamageTypeEnum.EDGE),
    ItemEnum.WEAPON_FALCHION:
        Weapon("steel falchion", QualityEnum.SUP, MaterialEnum.STEEL, 4,
               SkillEnum.SWORD, 15, 5, 0, 1, 6, 1, DamageTypeEnum.EDGE),
    ItemEnum.WEAPON_BROADSWORD:
        Weapon("steel broadsword", QualityEnum.SUP, MaterialEnum.STEEL, 5,
               SkillEnum.SWORD, 15, 10, 0, 1, 6, 2, DamageTypeEnum.EDGE),
    ItemEnum.WEAPON_BASTARD_SWORD:
        Weapon("steel bastard sword", QualityEnum.SUP, MaterialEnum.STEEL, 6,
               SkillEnum.SWORD, 20, 10, -10, 1, 6, 2, DamageTypeEnum.EDGE),
    ItemEnum.WEAPON_BATTLESWORD:
        Weapon("steel battlesword", QualityEnum.SUP, MaterialEnum.STEEL, 9,
               SkillEnum.SWORD, 25, 10, -20, 2, 6, 1, DamageTypeEnum.EDGE),
    # WEAPON [CLUB]
    ItemEnum.WEAPON_STICK:
        Weapon("wooden stick", QualityEnum.TER, MaterialEnum.WOOD, 5,
               SkillEnum.CLUB, 10, 5, 0, 0, 0, 2, DamageTypeEnum.BLUNT,
               flags=IFLAG_NO_SELL),
    ItemEnum.WEAPON_CLUB:
        Weapon("wooden club", QualityEnum.AVE, MaterialEnum.WOOD, 3,
               SkillEnum.CLUB, 15, 5, 0, 1, 4, 0, DamageTypeEnum.BLUNT,
               flags=IFLAG_NO_SELL),
    ItemEnum.WEAPON_MACE:
        Weapon("iron mace", QualityEnum.AVE, MaterialEnum.STEEL, 5,
               SkillEnum.CLUB, 15, 5, 0, 1, 6, 1, DamageTypeEnum.BLUNT),
    ItemEnum.WEAPON_MORNINGSTAR:
        Weapon("steel morningstar",
               QualityEnum.INF, MaterialEnum.STEEL_WOOD, 7,
               SkillEnum.CLUB, 20, 5, -10, 1, 6, 2, DamageTypeEnum.PIERCE),
    ItemEnum.WEAPON_MAUL:
        Weapon("spiked wooden maul", QualityEnum.SUP, MaterialEnum.WOOD, 8,
               SkillEnum.CLUB, 20, 5, -20, 2, 6, 1, DamageTypeEnum.BLUNT),
    # WEAPON [AXE]
    ItemEnum.WEAPON_SICKLE:
        Weapon("sickle", QualityEnum.INF, MaterialEnum.STEEL_WOOD, 1,
               SkillEnum.AXE, 5, 5, 0, 1, 4, 0, DamageTypeEnum.EDGE),
    ItemEnum.WEAPON_HATCHET:
        Weapon("hatchet", QualityEnum.INF, MaterialEnum.STEEL_WOOD, 2,
               SkillEnum.AXE, 5, 5, 0, 1, 6, 0, DamageTypeEnum.EDGE),
    ItemEnum.WEAPON_HANDAXE:
        Weapon("handaxe", QualityEnum.AVE, MaterialEnum.STEEL, 4,
               SkillEnum.AXE, 10, 5, 0, 1, 6, 1, DamageTypeEnum.EDGE),
    ItemEnum.WEAPON_WARHAMMER:
        Weapon("warhammer", QualityEnum.SUP, MaterialEnum.STEEL_WOOD, 6,
               SkillEnum.AXE, 15, 5, -5, 1, 6, 1, DamageTypeEnum.BLUNT),
    ItemEnum.WEAPON_BATTLEAXE:
        Weapon("battleaxe", QualityEnum.SUP, MaterialEnum.STEEL_WOOD, 7,
               SkillEnum.AXE, 20, 10, -15, 1, 6, 2, DamageTypeEnum.EDGE),
    # WEAPON [FLAIL]
    ItemEnum.WEAPON_GRAINFLAIL:
        Weapon("grainflail", QualityEnum.AVE, MaterialEnum.WOOD, 6,
               SkillEnum.FLAIL, 20, 5, 0, 1, 6, 0, DamageTypeEnum.BLUNT),
    ItemEnum.WEAPON_BALL_AND_CHAIN:
        Weapon("ball and chain", QualityEnum.AVE, MaterialEnum.STEEL_WOOD, 6,
               SkillEnum.FLAIL, 20, 10, 0, 1, 6, 2, DamageTypeEnum.BLUNT),
    ItemEnum.WEAPON_WARFLAIL:
        Weapon("warflail", QualityEnum.AVE, MaterialEnum.STEEL_WOOD, 6,
               SkillEnum.FLAIL, 20, 10, -20, 2, 6, 0, DamageTypeEnum.BLUNT),

    # SHIELD
    ItemEnum.SHIELD_BUCKLER_WOOD:
        Shield("wooden buckler", QualityEnum.SUP, MaterialEnum.WOOD, 3,
               SkillEnum.SHIELD, 5, 15),
    ItemEnum.SHIELD_BUCKLER_BANDED:
        Shield("reinforced wooden buckler",
               QualityEnum.AVE, MaterialEnum.STEEL_WOOD, 3,
               SkillEnum.SHIELD, 5, 15),
    ItemEnum.SHIELD_BUCKLER_STEEL:
        Shield("steel buckler", QualityEnum.AVE, MaterialEnum.STEEL_WOOD, 4,
               SkillEnum.SHIELD, 5, 15),
    ItemEnum.SHIELD_KNIGHT_STEEL:
        Shield("steel knight shield", QualityEnum.AVE,
               MaterialEnum.STEEL_WOOD, 6,
               SkillEnum.SHIELD, 5, 20),
    ItemEnum.SHIELD_ROUND_WOOD:
        Shield("wooden round shield", QualityEnum.SUP, MaterialEnum.WOOD, 6,
               SkillEnum.SHIELD, 5, 20),
    ItemEnum.SHIELD_ROUND_BANDED:
        Shield("reinforced wooden round shield",
               QualityEnum.AVE, MaterialEnum.STEEL_WOOD, 6,
               SkillEnum.SHIELD, 5, 20),
    ItemEnum.SHIELD_KITE_STEEL:
        Shield("steel kite shield", QualityEnum.AVE,
               MaterialEnum.STEEL_WOOD, 8.5,
               SkillEnum.SHIELD, 5, 25),
    ItemEnum.SHIELD_TOWER_WOOD:
        Shield("wooden tower shield", QualityEnum.SUP, MaterialEnum.WOOD, 8,
               SkillEnum.SHIELD, 5, 25),
    ItemEnum.SHIELD_TOWER_BANDED:
        Shield("reinforced wooden tower shield",
               QualityEnum.AVE, MaterialEnum.STEEL_WOOD, 8,
               SkillEnum.SHIELD, 5, 25),

    # ARMOR [CLOTH]
    ItemEnum.ARMOR_CAP_CLOTH:
        Armor("cloth cap",
              QualityEnum.AVE, MaterialEnum.CLOTH_HAIR, AL_1,
              COV_Sk),
    ItemEnum.ARMOR_HOOD_CLOTH:
        Armor("cloth hood",
              QualityEnum.AVE, MaterialEnum.CLOTH_HAIR, AL_1,
              COV_Sk | COV_Nk),
    ItemEnum.ARMOR_VEST_CLOTH:
        Armor("cloth vest",
              QualityEnum.AVE, MaterialEnum.CLOTH_HAIR, AL_1,
              COV_Sh | COV_Tx | COV_Ab),
    ItemEnum.ARMOR_TUNIC_CLOTH:
        Armor("cloth tunic",
              QualityEnum.AVE, MaterialEnum.CLOTH_HAIR, AL_1,
              COV_Ua | COV_Sh | COV_Tx | COV_Ab | COV_Hp | COV_Gr),
    ItemEnum.ARMOR_SURCOAT_CLOTH:
        Armor("cloth surcoat",
              QualityEnum.AVE, MaterialEnum.CLOTH_HAIR, AL_1,
              COV_Sh | COV_Tx | COV_Ab | COV_Hp | COV_Gr | COV_Th),
    ItemEnum.ARMOR_ROBE_CLOTH:
        Armor("cloth robe",
              QualityEnum.AVE, MaterialEnum.CLOTH_HAIR, AL_1,
              COV_Ua | COV_Sh | COV_Tx | COV_Ab | COV_Hp | COV_Gr | COV_Fo | \
              COV_El | COV_Th | COV_Kn | COV_Ca),
    ItemEnum.ARMOR_LEGGINGS_CLOTH:
        Armor("cloth leggings",
              QualityEnum.AVE, MaterialEnum.CLOTH_HAIR, AL_1_5,
              COV_Hp | COV_Gr | COV_Th | COV_Kn | COV_Ca | COV_Ft),
    # ARMOR [QUILT]
    ItemEnum.ARMOR_CAP_QUILT:
        Armor("quilt cap",
              QualityEnum.AVE, MaterialEnum.QUILT_FUR, AL_2,
              COV_Sk),
    ItemEnum.ARMOR_COWL_QUILT:
        Armor("quilt cowl",
              QualityEnum.AVE, MaterialEnum.QUILT_FUR, AL_2,
              COV_Sk | COV_Nk),
    ItemEnum.ARMOR_TUNIC_QUILT:
        Armor("quilt tunic",
              QualityEnum.AVE, MaterialEnum.QUILT_FUR, AL_2,
              COV_Ua | COV_Sh | COV_Tx | COV_Ab | COV_Hp | COV_Gr),
    ItemEnum.ARMOR_GAMBESON_QUILT:
        Armor("quilt gambeson",
              QualityEnum.AVE, MaterialEnum.QUILT_FUR, AL_2,
              COV_Fo | COV_El | COV_Ua | COV_Sh | COV_Tx | COV_Ab | COV_Hp | \
              COV_Gr | COV_Th),
    ItemEnum.ARMOR_LEGGINGS_QUILT:
        Armor("quilt leggings",
              QualityEnum.AVE, MaterialEnum.QUILT_FUR, AL_2_5,
              COV_Hp | COV_Gr | COV_Th | COV_Kn | COV_Ca | COV_Ft),
    # ARMOR [LEATHER]
    ItemEnum.ARMOR_CAP_LEATHER:
        Armor("leather cap",
              QualityEnum.AVE, MaterialEnum.LEATHER_HIDE, AL_3,
              COV_Sk),
    ItemEnum.ARMOR_COWL_LEATHER:
        Armor("leather cowl",
              QualityEnum.AVE, MaterialEnum.LEATHER_HIDE, AL_3,
              COV_Sk | COV_Nk),
    ItemEnum.ARMOR_VEST_LEATHER:
        Armor("leather vest",
              QualityEnum.AVE, MaterialEnum.LEATHER_HIDE, AL_3,
              COV_Sh | COV_Tx | COV_Ab),
    ItemEnum.ARMOR_TUNIC_LEATHER:
        Armor("leather tunic",
              QualityEnum.AVE, MaterialEnum.LEATHER_HIDE, AL_3,
              COV_Ua | COV_Sh | COV_Tx | COV_Ab | COV_Hp | COV_Gr),
    ItemEnum.ARMOR_SURCOAT_LEATHER:
        Armor("leather surcoat",
              QualityEnum.AVE, MaterialEnum.LEATHER_HIDE, AL_3,
              COV_Sh | COV_Tx | COV_Ab | COV_Hp | COV_Gr | COV_Th),
    ItemEnum.ARMOR_LEGGINGS_LEATHER:
        Armor("leather leggings",
              QualityEnum.AVE, MaterialEnum.LEATHER_HIDE, AL_3,
              COV_Hp | COV_Gr | COV_Th | COV_Kn | COV_Ca | COV_Ft),
    ItemEnum.ARMOR_SHOES_LEATHER:
        Armor("leather shoes",
              QualityEnum.AVE, MaterialEnum.LEATHER_HIDE, AL_3_5,
              COV_Ft),
    ItemEnum.ARMOR_CALF_BOOTS_LEATHER:
        Armor("leather calf boots",
              QualityEnum.AVE, MaterialEnum.LEATHER_HIDE, AL_3_5,
              COV_Ca | COV_Ft),
    ItemEnum.ARMOR_KNEE_BOOTS_LEATHER:
        Armor("leather knee boots",
              QualityEnum.AVE, MaterialEnum.LEATHER_HIDE, AL_3_5,
              COV_Kn | COV_Ca | COV_Ft),
    ItemEnum.ARMOR_GAUNTLETS_LEATHER:
        Armor("leather gauntlets",
              QualityEnum.AVE, MaterialEnum.LEATHER_HIDE, AL_3,
              COV_Ha),
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
              AL_3_5 | AL_4_5 | AL_5,
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
              QualityEnum.AVE, MaterialEnum.STEEL, AL_5,
              COV_Kn),
    ItemEnum.ARMOR_GREAVES_STEEL:
        Armor("steel greaves",
              QualityEnum.AVE, MaterialEnum.STEEL, AL_5,
              COV_Ca),

    # RING

    ItemEnum.RING_ATTACK_SILVER:
        Ring("silver ring", QualityEnum.SUP, MaterialEnum.SILVER, 0.1, 1500,
             flags=IFLAG_MAGIC, eff=[Effect(EffectTypeEnum.ATK, 2)]),

    ItemEnum.RING_HP_GOLD:
        Ring("gold ring", QualityEnum.SUP, MaterialEnum.GOLD, 0.2, 2500,
             flags=IFLAG_MAGIC, eff=[Effect(EffectTypeEnum.HP_MAX, 5)]),

    # MISC

    ItemEnum.MISC_STONE:
        Item(ItemTypeEnum.MISC, "stone", QualityEnum.TER,
             MaterialEnum.STONE, 1),
    ItemEnum.MISC_RAT_FUR:
        Item(ItemTypeEnum.MISC, "rat fur", QualityEnum.POR,
             MaterialEnum.QUILT_FUR, 1),
}

# vim: tabstop=2 shiftwidth=2 expandtab:
