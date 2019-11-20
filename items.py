# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

from global_defines import *

items = {
  # WEAPON [UNARMED]
  ItemEnum.WEAPON_HAND:
    Weapon("hand", QualityEnum.AVERAGE, MaterialEnum.BONE, 0, SkillEnum.UNARMED, 0, 5, 0, 0, 0, 1, DamageTypeEnum.BLUNT,
    flags=ITEM_NoSell|ITEM_NoDrop),
  ItemEnum.WEAPON_FOOT:
    Weapon("foot", QualityEnum.AVERAGE, MaterialEnum.BONE, 0, SkillEnum.UNARMED, 5, 5, 0, 0, 0, 2, DamageTypeEnum.BLUNT,
    flags=ITEM_NoSell|ITEM_NoDrop),
  ItemEnum.WEAPON_BITE:
    Weapon("bite", QualityEnum.AVERAGE, MaterialEnum.BONE, 0, SkillEnum.UNARMED, 0, 0, 0, 0, 0, 2, DamageTypeEnum.PIERCE,
    flags=ITEM_NoSell|ITEM_NoDrop),
  # WEAPON [DAGGER]
  ItemEnum.WEAPON_KNIFE:
    Weapon("hunting knife", QualityEnum.POOR, MaterialEnum.STEEL_WOOD, 1, SkillEnum.DAGGER, 5, 0, 0, 1, 4, 0, DamageTypeEnum.PIERCE),
  ItemEnum.WEAPON_DAGGER:
    Weapon("sharp dagger", QualityEnum.AVERAGE, MaterialEnum.STEEL, 1, SkillEnum.DAGGER, 5, 5, 0, 1, 6, 0, DamageTypeEnum.PIERCE),
  ItemEnum.WEAPON_MAIN_GAUCHE:
    Weapon("small parrying blade", QualityEnum.SUPERIOR, MaterialEnum.STEEL, 1, SkillEnum.DAGGER, 5, 10, 0, 1, 6, 0, DamageTypeEnum.PIERCE),
  # WEAPON [SWORD]
  ItemEnum.WEAPON_SHORTSWORD:
    Weapon("steel shortsword", QualityEnum.SUPERIOR, MaterialEnum.STEEL, 2.5, SkillEnum.SWORD, 10, 5, 0, 1, 6, 1, DamageTypeEnum.EDGE),
  ItemEnum.WEAPON_FALCHION:
    Weapon("steel falchion", QualityEnum.SUPERIOR, MaterialEnum.STEEL, 3, SkillEnum.SWORD, 15, 5, 0, 1, 6, 1, DamageTypeEnum.EDGE),
  ItemEnum.WEAPON_BROADSWORD:
    Weapon("steel broadsword", QualityEnum.SUPERIOR, MaterialEnum.STEEL, 4, SkillEnum.SWORD, 15, 10, 0, 1, 6, 2, DamageTypeEnum.EDGE),
  ItemEnum.WEAPON_BASTARD_SWORD:
    Weapon("steel bastard sword", QualityEnum.SUPERIOR, MaterialEnum.STEEL, 5, SkillEnum.SWORD, 20, 10, -10, 1, 6, 2, DamageTypeEnum.EDGE),
  ItemEnum.WEAPON_BATTLESWORD:
    Weapon("steel battlesword", QualityEnum.SUPERIOR, MaterialEnum.STEEL, 9, SkillEnum.SWORD, 25, 10, -20, 2, 6, 1, DamageTypeEnum.EDGE),
  # WEAPON [CLUB]
  ItemEnum.WEAPON_STICK:
    Weapon("wooden stick", QualityEnum.TERRIBLE, MaterialEnum.WOOD, 5, SkillEnum.CLUB, 10, 5, 0, 0, 0, 2, DamageTypeEnum.BLUNT,
    flags=ITEM_NoSell),
  ItemEnum.WEAPON_CLUB:
    Weapon("wooden club", QualityEnum.AVERAGE, MaterialEnum.WOOD, 3, SkillEnum.CLUB, 15, 5, 0, 1, 4, 0, DamageTypeEnum.BLUNT,
    flags=ITEM_NoSell),
  ItemEnum.WEAPON_MACE:
    Weapon("iron mace", QualityEnum.AVERAGE, MaterialEnum.STEEL, 4, SkillEnum.CLUB, 15, 5, 0, 1, 6, 1, DamageTypeEnum.BLUNT),
  ItemEnum.WEAPON_MORNINGSTAR:
    Weapon("steel morningstar", QualityEnum.INFERIOR, MaterialEnum.STEEL_WOOD, 7, SkillEnum.CLUB, 20, 5, -10, 1, 6, 2, DamageTypeEnum.PIERCE),
  ItemEnum.WEAPON_MAUL:
    Weapon("spiked wooden maul", QualityEnum.SUPERIOR, MaterialEnum.WOOD, 8, SkillEnum.CLUB, 20, 5, -20, 2, 6, 1, DamageTypeEnum.BLUNT),
  # WEAPON [AXE]
  ItemEnum.WEAPON_SICKLE:
    Weapon("sickle", QualityEnum.INFERIOR, MaterialEnum.STEEL_WOOD, 1, SkillEnum.AXE, 5, 5, 0, 1, 4, 0, DamageTypeEnum.EDGE),
  ItemEnum.WEAPON_HATCHET:
    Weapon("hatchet", QualityEnum.INFERIOR, MaterialEnum.STEEL_WOOD, 2, SkillEnum.AXE, 5, 5, 0, 1, 6, 0, DamageTypeEnum.EDGE),
  ItemEnum.WEAPON_HANDAXE:
    Weapon("handaxe", QualityEnum.AVERAGE, MaterialEnum.STEEL, 3, SkillEnum.AXE, 10, 5, 0, 1, 6, 1, DamageTypeEnum.EDGE),
  ItemEnum.WEAPON_WARHAMMER:
    Weapon("warhammer", QualityEnum.SUPERIOR, MaterialEnum.STEEL_WOOD, 6, SkillEnum.AXE, 15, 5, -5, 1, 6, 1, DamageTypeEnum.BLUNT),
  ItemEnum.WEAPON_BATTLEAXE:
    Weapon("battleaxe", QualityEnum.SUPERIOR, MaterialEnum.STEEL_WOOD, 7, SkillEnum.AXE, 20, 10, -15, 1, 6, 2, DamageTypeEnum.EDGE),
  # WEAPON [FLAIL]
  ItemEnum.WEAPON_GRAINFLAIL:
    Weapon("grainflail", QualityEnum.AVERAGE, MaterialEnum.WOOD, 6, SkillEnum.FLAIL, 20, 5, 0, 1, 6, 0, DamageTypeEnum.BLUNT),
  ItemEnum.WEAPON_BALL_AND_CHAIN:
    Weapon("ball and chain", QualityEnum.AVERAGE, MaterialEnum.STEEL_WOOD, 6, SkillEnum.FLAIL, 20, 10, 0, 1, 6, 2, DamageTypeEnum.BLUNT),
  ItemEnum.WEAPON_WARFLAIL:
    Weapon("warflail", QualityEnum.AVERAGE, MaterialEnum.STEEL_WOOD, 6, SkillEnum.FLAIL, 20, 10, -20, 2, 6, 0, DamageTypeEnum.BLUNT),

  # SHIELD
  ItemEnum.SHIELD_BUCKLER_WOOD:
    Shield("wooden buckler", QualityEnum.SUPERIOR, MaterialEnum.WOOD, 3, SkillEnum.SHIELD, 5, 15),
  ItemEnum.SHIELD_BUCKLER_BANDED:
    Shield("reinforced wooden buckler", QualityEnum.AVERAGE, MaterialEnum.STEEL_WOOD, 3, SkillEnum.SHIELD, 5, 15),
  ItemEnum.SHIELD_BUCKLER_STEEL:
    Shield("steel buckler", QualityEnum.AVERAGE, MaterialEnum.STEEL, 3, SkillEnum.SHIELD, 5, 15),
  ItemEnum.SHIELD_KNIGHT_STEEL:
    Shield("steel knight shield", QualityEnum.AVERAGE, MaterialEnum.STEEL, 5, SkillEnum.SHIELD, 5, 20),
  ItemEnum.SHIELD_ROUND_WOOD:
    Shield("wooden round shield", QualityEnum.SUPERIOR, MaterialEnum.WOOD, 6, SkillEnum.SHIELD, 5, 20),
  ItemEnum.SHIELD_ROUND_BANDED:
    Shield("reinforced wooden round shield", QualityEnum.AVERAGE, MaterialEnum.STEEL_WOOD, 6, SkillEnum.SHIELD, 5, 20),
  ItemEnum.SHIELD_KITE_STEEL:
    Shield("steel kite shield", QualityEnum.AVERAGE, MaterialEnum.STEEL, 7, SkillEnum.SHIELD, 5, 25),
  ItemEnum.SHIELD_TOWER_WOOD:
    Shield("wooden tower shield", QualityEnum.SUPERIOR, MaterialEnum.WOOD, 8, SkillEnum.SHIELD, 5, 25),
  ItemEnum.SHIELD_TOWER_BANDED:
    Shield("reinforced wooden tower shield", QualityEnum.AVERAGE, MaterialEnum.STEEL_WOOD, 8, SkillEnum.SHIELD, 5, 25),

  # ARMOR [CLOTH]
  ItemEnum.ARMOR_CAP_CLOTH:
    Armor("cloth cap", QualityEnum.AVERAGE, MaterialEnum.CLOTH_HAIR, AL_1, COV_Sk),
  ItemEnum.ARMOR_HOOD_CLOTH:
    Armor("cloth hood", QualityEnum.AVERAGE, MaterialEnum.CLOTH_HAIR, AL_1, COV_Sk|COV_Nk),
  ItemEnum.ARMOR_VEST_CLOTH:
    Armor("cloth vest", QualityEnum.AVERAGE, MaterialEnum.CLOTH_HAIR, AL_1, COV_Sh|COV_Tx|COV_Ab),
  ItemEnum.ARMOR_TUNIC_CLOTH:
    Armor("cloth tunic", QualityEnum.AVERAGE, MaterialEnum.CLOTH_HAIR, AL_1, COV_Ua|COV_Sh|COV_Tx|COV_Ab|COV_Hp|COV_Gr),
  ItemEnum.ARMOR_SURCOAT_CLOTH:
    Armor("cloth surcoat", QualityEnum.AVERAGE, MaterialEnum.CLOTH_HAIR, AL_1, COV_Sh|COV_Tx|COV_Ab|COV_Hp|COV_Gr|COV_Th),
  ItemEnum.ARMOR_ROBE_CLOTH:
    Armor("cloth robe", QualityEnum.AVERAGE, MaterialEnum.CLOTH_HAIR, AL_1, COV_Ua|COV_Sh|COV_Tx|COV_Ab|COV_Hp|COV_Gr|COV_Fo|COV_El|COV_Th|COV_Kn|COV_Ca),
  ItemEnum.ARMOR_LEGGINGS_CLOTH:
    Armor("cloth leggings", QualityEnum.AVERAGE, MaterialEnum.CLOTH_HAIR, AL_1_5, COV_Hp|COV_Gr|COV_Th|COV_Kn|COV_Ca|COV_Ft),
  # ARMOR [QUILT]
  ItemEnum.ARMOR_CAP_QUILT:
    Armor("quilt cap", QualityEnum.AVERAGE, MaterialEnum.QUILT_FUR, AL_2, COV_Sk),
  ItemEnum.ARMOR_COWL_QUILT:
    Armor("quilt cowl", QualityEnum.AVERAGE, MaterialEnum.QUILT_FUR, AL_2, COV_Sk|COV_Nk),
  ItemEnum.ARMOR_TUNIC_QUILT:
    Armor("quilt tunic", QualityEnum.AVERAGE, MaterialEnum.QUILT_FUR, AL_2, COV_Ua|COV_Sh|COV_Tx|COV_Ab|COV_Hp|COV_Gr),
  ItemEnum.ARMOR_GAMBESON_QUILT:
    Armor("quilt gambeson", QualityEnum.AVERAGE, MaterialEnum.QUILT_FUR, AL_2, COV_Fo|COV_El|COV_Ua|COV_Sh|COV_Tx|COV_Ab|COV_Hp|COV_Gr|COV_Th),
  ItemEnum.ARMOR_LEGGINGS_QUILT:
    Armor("quilt leggings", QualityEnum.AVERAGE, MaterialEnum.QUILT_FUR, AL_2_5, COV_Hp|COV_Gr|COV_Th|COV_Kn|COV_Ca|COV_Ft),
  # ARMOR [LEATHER]
  ItemEnum.ARMOR_CAP_LEATHER:
    Armor("leather cap", QualityEnum.AVERAGE, MaterialEnum.LEATHER_HIDE, AL_3, COV_Sk),
  ItemEnum.ARMOR_COWL_LEATHER:
    Armor("leather cowl", QualityEnum.AVERAGE, MaterialEnum.LEATHER_HIDE, AL_3, COV_Sk|COV_Nk),
  ItemEnum.ARMOR_VEST_LEATHER:
    Armor("leather vest", QualityEnum.AVERAGE, MaterialEnum.LEATHER_HIDE, AL_3, COV_Sh|COV_Tx|COV_Ab),
  ItemEnum.ARMOR_TUNIC_LEATHER:
    Armor("leather tunic", QualityEnum.AVERAGE, MaterialEnum.LEATHER_HIDE, AL_3, COV_Ua|COV_Sh|COV_Tx|COV_Ab|COV_Hp|COV_Gr),
  ItemEnum.ARMOR_SURCOAT_LEATHER:
    Armor("leather surcoat", QualityEnum.AVERAGE, MaterialEnum.LEATHER_HIDE, AL_3, COV_Sh|COV_Tx|COV_Ab|COV_Hp|COV_Gr|COV_Th),
  ItemEnum.ARMOR_LEGGINGS_LEATHER:
    Armor("leather leggings", QualityEnum.AVERAGE, MaterialEnum.LEATHER_HIDE, AL_3, COV_Hp|COV_Gr|COV_Th|COV_Kn|COV_Ca|COV_Ft),
  ItemEnum.ARMOR_SHOES_LEATHER:
    Armor("leather shoes", QualityEnum.AVERAGE, MaterialEnum.LEATHER_HIDE, AL_3_5, COV_Ft),
  ItemEnum.ARMOR_CALF_BOOTS_LEATHER:
    Armor("leather calf boots", QualityEnum.AVERAGE, MaterialEnum.LEATHER_HIDE, AL_3_5, COV_Ca|COV_Ft),
  ItemEnum.ARMOR_KNEE_BOOTS_LEATHER:
    Armor("leather knee boots", QualityEnum.AVERAGE, MaterialEnum.LEATHER_HIDE, AL_3_5, COV_Kn|COV_Ca|COV_Ft),
  ItemEnum.ARMOR_GAUNTLETS_LEATHER:
    Armor("leather gauntlets", QualityEnum.AVERAGE, MaterialEnum.LEATHER_HIDE, AL_3, COV_Ha),
  # ARMOR [KURBUL]
  ItemEnum.ARMOR_HALFHELM_KURBUL:
    Armor("hardened leather halfhelm", QualityEnum.AVERAGE, MaterialEnum.KURBUL, AL_3|AL_4|AL_5, COV_Sk),
  ItemEnum.ARMOR_BREASTPLATE_KURBUL:
    Armor("hardened leather breastplate", QualityEnum.AVERAGE, MaterialEnum.KURBUL, AL_3|AL_4|AL_5, COV_Ch),
  ItemEnum.ARMOR_BACKPLATE_KURBUL:
    Armor("hardened leather backplate", QualityEnum.AVERAGE, MaterialEnum.KURBUL, AL_3|AL_4|AL_5, COV_Bk),
  ItemEnum.ARMOR_AILETTES_KURBUL:
    Armor("hardened leather ailettes", QualityEnum.AVERAGE, MaterialEnum.KURBUL, AL_3|AL_4|AL_5, COV_Sh),
  ItemEnum.ARMOR_REREBRACES_KURBUL:
    Armor("hardened leather rerebraces", QualityEnum.AVERAGE, MaterialEnum.KURBUL, AL_3|AL_4|AL_5, COV_Ua),
  ItemEnum.ARMOR_COUDES_KURBUL:
    Armor("hardened leather coudes", QualityEnum.AVERAGE, MaterialEnum.KURBUL, AL_3|AL_4|AL_5, COV_El),
  ItemEnum.ARMOR_VAMBRACES_KURBUL:
    Armor("hardened leather vambraces", QualityEnum.AVERAGE, MaterialEnum.KURBUL, AL_3|AL_4|AL_5, COV_Fo),
  ItemEnum.ARMOR_KNEECOPS_KURBUL:
    Armor("hardened leather kneecops", QualityEnum.AVERAGE, MaterialEnum.KURBUL, AL_3_5|AL_4|AL_5, COV_Kn),
  ItemEnum.ARMOR_GREAVES_KURBUL:
    Armor("hardened leather greaves", QualityEnum.AVERAGE, MaterialEnum.KURBUL, AL_3_5|AL_4|AL_5, COV_Ca),
  # ARMOR [LEATHER+RING]
  ItemEnum.ARMOR_HALFHELM_LEATHER_RING:
    Armor("studded leather halfhelm", QualityEnum.AVERAGE, MaterialEnum.LEATHER_RING, AL_3|AL_4|AL_5, COV_Sk),
  ItemEnum.ARMOR_VEST_LEATHER_RING:
    Armor("studded leather vest", QualityEnum.AVERAGE, MaterialEnum.LEATHER_RING, AL_3|AL_4|AL_5, COV_Sh|COV_Tx|COV_Ab),
  ItemEnum.ARMOR_BYRNIE_LEATHER_RING:
    Armor("studded leather byrnie", QualityEnum.AVERAGE, MaterialEnum.LEATHER_RING, AL_3|AL_4|AL_5, COV_Ua|COV_Sh|COV_Tx|COV_Ab|COV_Hp|COV_Gr),
  ItemEnum.ARMOR_HAUBERK_LEATHER_RING:
    Armor("studded leather hauberk", QualityEnum.AVERAGE, MaterialEnum.LEATHER_RING, AL_3|AL_4|AL_5, COV_Fo|COV_El|COV_Ua|COV_Sh|COV_Tx|COV_Ab|COV_Hp|COV_Gr|COV_Th),
  ItemEnum.ARMOR_LEGGINGS_LEATHER_RING:
    Armor("studded leather leggings", QualityEnum.AVERAGE, MaterialEnum.LEATHER_RING, AL_3_5|AL_4_5|AL_5, COV_Hp|COV_Gr|COV_Th|COV_Kn|COV_Ca|COV_Ft),
  ItemEnum.ARMOR_GAUNTLETS_LEATHER_RING:
    Armor("studded leather gauntlets", QualityEnum.AVERAGE, MaterialEnum.LEATHER_RING, AL_3|AL_4|AL_5, COV_Ha),
  # ARMOR [MAIL]
  ItemEnum.ARMOR_COWL_MAIL:
    Armor("chainmail cowl", QualityEnum.AVERAGE, MaterialEnum.MAIL, AL_4, COV_Sk),
  ItemEnum.ARMOR_BYRNIE_MAIL:
    Armor("chainmail byrnie", QualityEnum.AVERAGE, MaterialEnum.MAIL, AL_4, COV_Ua|COV_Sh|COV_Tx|COV_Ab|COV_Hp|COV_Gr),
  ItemEnum.ARMOR_HAUBERK_MAIL:
    Armor("chainmail hauberk", QualityEnum.AVERAGE, MaterialEnum.MAIL, AL_4, COV_Fo|COV_El|COV_Ua|COV_Sh|COV_Tx|COV_Ab|COV_Hp|COV_Gr|COV_Th),
  ItemEnum.ARMOR_LEGGINGS_MAIL:
    Armor("chainmail leggings", QualityEnum.AVERAGE, MaterialEnum.MAIL, AL_4_5, COV_Hp|COV_Gr|COV_Th|COV_Kn|COV_Ca|COV_Ft),
  ItemEnum.ARMOR_MITTENS_MAIL:
    Armor("chainmail mittens", QualityEnum.AVERAGE, MaterialEnum.MAIL, AL_4, COV_Ha),
  # ARMOR [SCALE]
  ItemEnum.ARMOR_VEST_SCALE:
    Armor("scale armor vest", QualityEnum.AVERAGE, MaterialEnum.SCALE, AL_3|AL_4|AL_5, COV_Sh|COV_Tx|COV_Ab),
  ItemEnum.ARMOR_BYRNIE_SCALE:
    Armor("scale armor byrnie", QualityEnum.AVERAGE, MaterialEnum.SCALE, AL_3|AL_4|AL_5, COV_Ua|COV_Sh|COV_Tx|COV_Ab|COV_Hp|COV_Gr),
  ItemEnum.ARMOR_HAUBERK_SCALE:
    Armor("scale armor hauberk", QualityEnum.AVERAGE, MaterialEnum.SCALE, AL_3|AL_4|AL_5, COV_Fo|COV_El|COV_Ua|COV_Sh|COV_Tx|COV_Ab|COV_Hp|COV_Gr|COV_Th),
  # ARMOR [STEEL]
  ItemEnum.ARMOR_HALFHELM_STEEL:
    Armor("steel halfhelm", QualityEnum.AVERAGE, MaterialEnum.STEEL, AL_5, COV_Sk),
  ItemEnum.ARMOR_GREAT_HELM_STEEL:
    Armor("steel great helm", QualityEnum.AVERAGE, MaterialEnum.STEEL, AL_5, COV_Sk|COV_Fa|COV_Nk),
  ItemEnum.ARMOR_BREASTPLATE_STEEL:
    Armor("steel breastplate", QualityEnum.AVERAGE, MaterialEnum.STEEL, AL_5, COV_Ch),
  ItemEnum.ARMOR_BACKPLATE_STEEL:
    Armor("steel backplate", QualityEnum.AVERAGE, MaterialEnum.STEEL, AL_5, COV_Bk),
  ItemEnum.ARMOR_AILETTES_STEEL:
    Armor("steel ailettes", QualityEnum.AVERAGE, MaterialEnum.STEEL, AL_5, COV_Sh),
  ItemEnum.ARMOR_REREBRACES_STEEL:
    Armor("steel rerebraces", QualityEnum.AVERAGE, MaterialEnum.STEEL, AL_5, COV_Ua),
  ItemEnum.ARMOR_COUDES_STEEL:
    Armor("steel coudes", QualityEnum.AVERAGE, MaterialEnum.STEEL, AL_5, COV_El),
  ItemEnum.ARMOR_VAMBRACES_STEEL:
    Armor("steel vambraces", QualityEnum.AVERAGE, MaterialEnum.STEEL, AL_5, COV_Fo),
  ItemEnum.ARMOR_KNEECOPS_STEEL:
    Armor("steel kneecops", QualityEnum.AVERAGE, MaterialEnum.STEEL, AL_5, COV_Kn),
  ItemEnum.ARMOR_GREAVES_STEEL:
    Armor("steel greaves", QualityEnum.AVERAGE, MaterialEnum.STEEL, AL_5, COV_Ca),

  # RING

  ItemEnum.RING_ATTACK_SILVER:
    Ring("silver ring", QualityEnum.SUPERIOR, MaterialEnum.SILVER, 0.1, 1500,
    flags=ITEM_Magic, eff=[ Effect(EffectTypeEnum.ATK, 2) ]),

  ItemEnum.RING_HP_GOLD:
    Ring("gold ring", QualityEnum.SUPERIOR, MaterialEnum.GOLD, 0.2, 2500,
    flags=ITEM_Magic, eff=[ Effect(EffectTypeEnum.HP_MAX, 5) ]),

  # MISC

  ItemEnum.MISC_STONE:
    Item(ItemTypeEnum.MISC, "stone", QualityEnum.TERRIBLE, MaterialEnum.STONE, 1),
}
