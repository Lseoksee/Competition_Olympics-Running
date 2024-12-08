DEVICE = "cuda"

STRATEGY = {
    "default": {
        0: [-100, -30],
        1: [-100, -18],
        2: [-100, -6],
        3: [-100, 6],
        4: [-100, 18],
        5: [-100, 30],
        6: [-40, -30],
        7: [-40, -18],
        8: [-40, -6],
        9: [-40, 6],
        10: [-40, 18],
        11: [-40, 30],
        12: [20, -30],
        13: [20, -18],
        14: [20, -6],
        15: [20, 6],
        16: [20, 18],
        17: [20, 30],
        18: [80, -30],
        19: [80, -18],
        20: [80, -6],
        21: [80, 6],
        22: [80, 18],
        23: [80, 30],
        24: [140, -30],
        25: [140, -18],
        26: [140, -6],
        27: [140, 6],
        28: [140, 18],
        29: [140, 30],
        30: [200, -30],
        31: [200, -18],
        32: [200, -6],
        33: [200, 6],
        34: [200, 18],
        35: [200, 30],
    },
    "strategy1": {
        0: [-50, -30],
        1: [-50, -15],
        2: [-50, -7],
        3: [-50, 7],
        4: [-50, 15],
        5: [-50, 30],
        6: [-50, -30],
        7: [-50, -15],
        8: [-50, -7],
        9: [-50, 7],
        10: [-50, 15],
        11: [-50, 30],
        12: [-50, -30],
        13: [-50, -15],
        14: [-50, -7],
        15: [-50, 7],
        16: [-50, 15],
        17: [-50, 30],
        18: [200, -30],
        19: [200, -15],
        20: [200, -7],
        21: [200, 7],
        22: [200, 15],
        23: [200, 30],
        24: [200, -30],
        25: [200, -15],
        26: [200, -7],
        27: [200, 7],
        28: [200, 15],
        29: [200, 30],
        30: [200, -30],
        31: [200, -15],
        32: [200, -7],
        33: [200, 7],
        34: [200, 15],
        35: [200, 30],
    },
    "strategy2": {
        0: [200, -30],
        1: [200, -27],
        2: [200, -24],
        3: [200, -21],
        4: [200, -18],
        5: [200, -15],
        6: [200, -12],
        7: [200, -9],
        8: [200, -6],
        9: [200, -3],
        10: [200, 0],
        11: [200, 3],
        12: [200, 6],
        13: [200, 9],
        14: [200, 12],
        15: [200, 15],
        16: [200, 18],
        17: [200, 30],
        18: [200, -30],
        19: [200, -27],
        20: [200, -24],
        21: [200, -21],
        22: [200, -18],
        23: [200, -15],
        24: [200, -12],
        25: [200, -9],
        26: [200, -6],
        27: [200, -3],
        28: [200, 0],
        29: [200, 3],
        30: [200, 6],
        31: [200, 9],
        32: [200, 12],
        33: [200, 15],
        34: [200, 18],
        35: [200, 30],
    },
    "strategy3": {
        0: [150, -30],
        1: [150, -15],
        2: [150, -7],
        3: [150, 7],
        4: [150, 15],
        5: [150, 30],
        6: [150, -30],
        7: [150, -15],
        8: [150, -7],
        9: [150, 7],
        10: [150, 15],
        11: [150, 30],
        12: [150, -30],
        13: [150, -15],
        14: [150, -7],
        15: [150, 7],
        16: [150, 15],
        17: [150, 30],
        18: [150, -30],
        19: [150, -15],
        20: [150, -7],
        21: [150, 7],
        22: [150, 15],
        23: [150, 30],
        24: [150, -30],
        25: [150, -15],
        26: [150, -7],
        27: [150, 7],
        28: [150, 15],
        29: [150, 30],
        30: [150, -30],
        31: [150, -15],
        32: [150, -7],
        33: [150, 7],
        34: [150, 15],
        35: [150, 30],
    },
}
"""전략: [힘, 각도]"""

MAP_STRATEGY = {
    1: "strategy2",
    2: "strategy3",
    3: "default",
    4: "default",
    5: "strategy3",
    6: "strategy3",
    7: "default",
    8: "strategy3",
    9: "strategy2",
    10: "strategy3",
    11: "strategy1",
}
"""맵별 전략"""


MAP_MODEL = {
    1: "actor_1500.pth",
    2: "actor_1500.pth",
    3: "actor_map-3_ep-1500.pth",
    4: "actor_1500.pth",
    5: "actor_map-5_ep-1500.pth",
    6: "actor_1500.pth",
    7: "actor_1500.pth",
    8: "actor_1500.pth",
    9: "actor_1500.pth",
    10: "actor_map-10_ep-1500.pth",
    11: "actor_1500.pth",
}
"""맵별 모델 (기본값: actor_1500.pth)"""