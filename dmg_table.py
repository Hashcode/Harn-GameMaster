# Copyright (c) 2019 Michael Scott
#
# SPDX-License-Identifier: Apache-2.0

# Damage Table Definitions

from global_defines import (CoverageEnum, DamageTypeEnum,
                            ImpactResult, ImpactActionEnum, ImpactAction)

dmg_table_melee = {
    DamageTypeEnum.BLUNT: {
        CoverageEnum.SKULL: [
            ImpactResult(4,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.SHOCK, 2),
                         ]),
            ImpactResult(8,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.SHOCK, 3),
                         ]),
            ImpactResult(12,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 3),
                         ]),
            ImpactResult(16,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.KILL_CHECK, 4),
                             ImpactAction(ImpactActionEnum.SHOCK, 100),
                             ImpactAction(ImpactActionEnum.FUMBLE, 100),
                         ]),
            ImpactResult(100,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.KILL_CHECK, 5),
                             ImpactAction(ImpactActionEnum.BLEED, 1),
                             ImpactAction(ImpactActionEnum.SHOCK, 100),
                             ImpactAction(ImpactActionEnum.FUMBLE, 100),
                         ]),
        ],
        CoverageEnum.FACE: [
            ImpactResult(4,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.SHOCK, 2),
                         ]),
            ImpactResult(8,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 2),
                         ]),
            ImpactResult(12,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 3),
                         ]),
            ImpactResult(16,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 4),
                             ImpactAction(ImpactActionEnum.FUMBLE, 100),
                         ]),
            ImpactResult(100,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.KILL_CHECK, 4),
                             ImpactAction(ImpactActionEnum.BLEED, 1),
                             ImpactAction(ImpactActionEnum.SHOCK, 100),
                             ImpactAction(ImpactActionEnum.FUMBLE, 100),
                         ]),
        ],
        CoverageEnum.NECK: [
            ImpactResult(4,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.SHOCK, 1),
                         ]),
            ImpactResult(8,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.SHOCK, 2),
                         ]),
            ImpactResult(10,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 2),
                         ]),
            ImpactResult(12,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 2),
                             ImpactAction(ImpactActionEnum.FUMBLE, 100),
                         ]),
            ImpactResult(16,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.KILL_CHECK, 3),
                             ImpactAction(ImpactActionEnum.SHOCK, 100),
                             ImpactAction(ImpactActionEnum.FUMBLE, 100),
                         ]),
            ImpactResult(100,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.KILL_CHECK, 4),
                             ImpactAction(ImpactActionEnum.BLEED, 1),
                             ImpactAction(ImpactActionEnum.SHOCK, 100),
                             ImpactAction(ImpactActionEnum.FUMBLE, 100),
                         ]),
        ],
        CoverageEnum.SHOULDERS: [
            ImpactResult(4,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.FUMBLE, 1),
                         ]),
            ImpactResult(8,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.FUMBLE, 2),
                         ]),
            ImpactResult(11,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.FUMBLE, 2),
                         ]),
            ImpactResult(14,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 1),
                             ImpactAction(ImpactActionEnum.FUMBLE, 3),
                         ]),
            ImpactResult(19,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 2),
                             ImpactAction(ImpactActionEnum.FUMBLE, 100),
                         ]),
            ImpactResult(100,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.KILL_CHECK, 3),
                             ImpactAction(ImpactActionEnum.BLEED, 1),
                             ImpactAction(ImpactActionEnum.SHOCK, 100),
                             ImpactAction(ImpactActionEnum.FUMBLE, 100),
                         ]),
        ],
        CoverageEnum.UPPER_ARMS: [
            ImpactResult(4,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.FUMBLE, 1),
                         ]),
            ImpactResult(8,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.FUMBLE, 2),
                         ]),
            ImpactResult(11,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.FUMBLE, 2),
                         ]),
            ImpactResult(14,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 1),
                             ImpactAction(ImpactActionEnum.FUMBLE, 3),
                         ]),
            ImpactResult(100,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.BLEED, 1),
                             ImpactAction(ImpactActionEnum.SHOCK, 2),
                             ImpactAction(ImpactActionEnum.FUMBLE, 100),
                         ]),
        ],
        CoverageEnum.ELBOWS: [
            ImpactResult(4,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.FUMBLE, 3),
                         ]),
            ImpactResult(8,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.FUMBLE, 4),
                         ]),
            ImpactResult(10,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.FUMBLE, 4),
                         ]),
            ImpactResult(13,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 1),
                             ImpactAction(ImpactActionEnum.FUMBLE, 5),
                         ]),
            ImpactResult(16,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 2),
                             ImpactAction(ImpactActionEnum.FUMBLE, 100),
                         ]),
            ImpactResult(100,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.AMPUTATE_CHECK, 3),
                             ImpactAction(ImpactActionEnum.BLEED, 1),
                             ImpactAction(ImpactActionEnum.SHOCK, 100),
                             ImpactAction(ImpactActionEnum.FUMBLE, 100),
                         ]),
        ],
        CoverageEnum.FOREARMS: [
            ImpactResult(4,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.FUMBLE, 2),
                         ]),
            ImpactResult(8,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.FUMBLE, 3),
                         ]),
            ImpactResult(11,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.FUMBLE, 3),
                         ]),
            ImpactResult(14,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 1),
                             ImpactAction(ImpactActionEnum.FUMBLE, 4),
                         ]),
            ImpactResult(100,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.BLEED, 1),
                             ImpactAction(ImpactActionEnum.SHOCK, 2),
                             ImpactAction(ImpactActionEnum.FUMBLE, 100),
                         ]),
        ],
        CoverageEnum.HANDS: [
            ImpactResult(4,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.FUMBLE, 3),
                         ]),
            ImpactResult(7,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.FUMBLE, 4),
                         ]),
            ImpactResult(9,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.FUMBLE, 4),
                         ]),
            ImpactResult(12,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 1),
                             ImpactAction(ImpactActionEnum.FUMBLE, 5),
                         ]),
            ImpactResult(16,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 2),
                             ImpactAction(ImpactActionEnum.FUMBLE, 100),
                         ]),
            ImpactResult(100,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.AMPUTATE_CHECK, 3),
                             ImpactAction(ImpactActionEnum.BLEED, 1),
                             ImpactAction(ImpactActionEnum.SHOCK, 100),
                             ImpactAction(ImpactActionEnum.FUMBLE, 100),
                         ]),
        ],
        CoverageEnum.THORAX_FRONT: [
            ImpactResult(4,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.SHOCK, 1),
                         ]),
            ImpactResult(8,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.SHOCK, 2),
                         ]),
            ImpactResult(12,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 2),
                         ]),
            ImpactResult(16,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 2),
                             ImpactAction(ImpactActionEnum.FUMBLE, 100),
                         ]),
            ImpactResult(100,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.KILL_CHECK, 4),
                             ImpactAction(ImpactActionEnum.BLEED, 1),
                             ImpactAction(ImpactActionEnum.SHOCK, 100),
                             ImpactAction(ImpactActionEnum.FUMBLE, 100),
                         ]),
        ],
        CoverageEnum.THORAX_REAR: [
            ImpactResult(4,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.SHOCK, 1),
                         ]),
            ImpactResult(8,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.SHOCK, 2),
                         ]),
            ImpactResult(12,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 2),
                         ]),
            ImpactResult(16,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 3),
                             ImpactAction(ImpactActionEnum.FUMBLE, 100),
                         ]),
            ImpactResult(100,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.KILL_CHECK, 4),
                             ImpactAction(ImpactActionEnum.BLEED, 1),
                             ImpactAction(ImpactActionEnum.SHOCK, 100),
                             ImpactAction(ImpactActionEnum.FUMBLE, 100),
                         ]),
        ],
        CoverageEnum.ABDOMEN_FRONT: [
            ImpactResult(4,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.SHOCK, 1),
                         ]),
            ImpactResult(8,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 1),
                         ]),
            ImpactResult(12,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 2),
                         ]),
            ImpactResult(16,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 3),
                             ImpactAction(ImpactActionEnum.FUMBLE, 100),
                         ]),
            ImpactResult(100,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.KILL_CHECK, 4),
                             ImpactAction(ImpactActionEnum.BLEED, 1),
                             ImpactAction(ImpactActionEnum.SHOCK, 100),
                             ImpactAction(ImpactActionEnum.FUMBLE, 100),
                         ]),
        ],
        CoverageEnum.ABDOMEN_REAR: [
            ImpactResult(4,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.SHOCK, 1),
                         ]),
            ImpactResult(8,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.SHOCK, 2),
                         ]),
            ImpactResult(11,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 2),
                         ]),
            ImpactResult(16,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 3),
                             ImpactAction(ImpactActionEnum.FUMBLE, 100),
                         ]),
            ImpactResult(100,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.KILL_CHECK, 4),
                             ImpactAction(ImpactActionEnum.BLEED, 1),
                             ImpactAction(ImpactActionEnum.SHOCK, 100),
                             ImpactAction(ImpactActionEnum.FUMBLE, 100),
                         ]),
        ],
        CoverageEnum.GROIN: [
            ImpactResult(4,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.SHOCK, 2),
                         ]),
            ImpactResult(8,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 2),
                         ]),
            ImpactResult(12,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 3),
                         ]),
            ImpactResult(16,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 3),
                             ImpactAction(ImpactActionEnum.STUMBLE, 100),
                         ]),
            ImpactResult(100,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.BLEED, 1),
                             ImpactAction(ImpactActionEnum.SHOCK, 4),
                             ImpactAction(ImpactActionEnum.STUMBLE, 100),
                         ]),
        ],
        CoverageEnum.HIPS: [
            ImpactResult(4,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.STUMBLE, 1),
                         ]),
            ImpactResult(8,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.STUMBLE, 2),
                         ]),
            ImpactResult(12,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.STUMBLE, 2),
                             ImpactAction(ImpactActionEnum.SHOCK, 1),
                         ]),
            ImpactResult(16,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 2),
                             ImpactAction(ImpactActionEnum.STUMBLE, 100),
                         ]),
            ImpactResult(19,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 3),
                             ImpactAction(ImpactActionEnum.STUMBLE, 100),
                         ]),
            ImpactResult(100,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.KILL_CHECK, 3),
                             ImpactAction(ImpactActionEnum.BLEED, 1),
                             ImpactAction(ImpactActionEnum.SHOCK, 100),
                             ImpactAction(ImpactActionEnum.STUMBLE, 100),
                         ]),
        ],
        CoverageEnum.THIGHS: [
            ImpactResult(4,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.STUMBLE, 1),
                         ]),
            ImpactResult(9,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.STUMBLE, 2),
                         ]),
            ImpactResult(11,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.STUMBLE, 2),
                         ]),
            ImpactResult(13,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.STUMBLE, 3),
                             ImpactAction(ImpactActionEnum.SHOCK, 1),
                         ]),
            ImpactResult(17,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 2),
                             ImpactAction(ImpactActionEnum.STUMBLE, 100),
                         ]),
            ImpactResult(100,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.BLEED, 1),
                             ImpactAction(ImpactActionEnum.SHOCK, 3),
                             ImpactAction(ImpactActionEnum.STUMBLE, 100),
                         ]),
        ],
        CoverageEnum.KNEES: [
            ImpactResult(4,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.STUMBLE, 3),
                         ]),
            ImpactResult(8,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.STUMBLE, 4),
                         ]),
            ImpactResult(10,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.STUMBLE, 4),
                         ]),
            ImpactResult(12,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.STUMBLE, 5),
                             ImpactAction(ImpactActionEnum.SHOCK, 1),
                         ]),
            ImpactResult(16,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 2),
                             ImpactAction(ImpactActionEnum.STUMBLE, 100),
                         ]),
            ImpactResult(100,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.AMPUTATE_CHECK, 3),
                             ImpactAction(ImpactActionEnum.BLEED, 1),
                             ImpactAction(ImpactActionEnum.SHOCK, 100),
                             ImpactAction(ImpactActionEnum.STUMBLE, 100),
                         ]),
        ],
        CoverageEnum.CALVES: [
            ImpactResult(4,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.STUMBLE, 2),
                         ]),
            ImpactResult(8,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.STUMBLE, 3),
                         ]),
            ImpactResult(10,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.STUMBLE, 3),
                         ]),
            ImpactResult(12,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.STUMBLE, 4),
                             ImpactAction(ImpactActionEnum.SHOCK, 1),
                         ]),
            ImpactResult(16,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 2),
                             ImpactAction(ImpactActionEnum.STUMBLE, 100),
                         ]),
            ImpactResult(100,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.BLEED, 1),
                             ImpactAction(ImpactActionEnum.SHOCK, 3),
                             ImpactAction(ImpactActionEnum.STUMBLE, 100),
                         ]),
        ],
        CoverageEnum.FEET: [
            ImpactResult(4,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.STUMBLE, 3),
                         ]),
            ImpactResult(7,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_MILD),
                             ImpactAction(ImpactActionEnum.STUMBLE, 4),
                         ]),
            ImpactResult(11,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_SERIOUS),
                             ImpactAction(ImpactActionEnum.STUMBLE, 4),
                         ]),
            ImpactResult(15,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.SHOCK, 2),
                             ImpactAction(ImpactActionEnum.STUMBLE, 100),
                         ]),
            ImpactResult(100,
                         [
                             ImpactAction(ImpactActionEnum.WOUND_GRIEVOUS),
                             ImpactAction(ImpactActionEnum.AMPUTATE_CHECK, 3),
                             ImpactAction(ImpactActionEnum.BLEED, 1),
                             ImpactAction(ImpactActionEnum.SHOCK, 100),
                             ImpactAction(ImpactActionEnum.STUMBLE, 100),
                         ]),
        ],
    },
    DamageTypeEnum.EDGE: {
    },
    DamageTypeEnum.PIERCE: {
    },
    DamageTypeEnum.ELEMENTAL: {
    },
}

# vim: tabstop=2 shiftwidth=2 expandtab:
