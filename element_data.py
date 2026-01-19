from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class Element:
    number: int
    symbol: str
    name_cn: str
    period: int
    group: int
    series: str


GROUP_COLORS_IUPAC: Dict[int, Tuple[int, int, int]] = {
    1: (244, 208, 63),
    2: (243, 156, 18),
    3: (189, 195, 199),
    4: (149, 165, 166),
    5: (39, 174, 96),
    6: (93, 109, 126),
    7: (142, 68, 173),
    8: (160, 64, 0),
    9: (31, 97, 141),
    10: (20, 143, 119),
    11: (212, 172, 13),
    12: (127, 140, 141),
    13: (200, 214, 229),
    14: (52, 73, 94),
    15: (52, 152, 219),
    16: (231, 76, 60),
    17: (0, 200, 83),
    18: (108, 92, 231),
}

GROUP_LABELS = {
    "iupac": [str(i) for i in range(1, 19)],
    "cas": [
        "ⅠA",
        "ⅡA",
        "ⅢB",
        "ⅣB",
        "ⅤB",
        "ⅥB",
        "ⅦB",
        "ⅧB",
        "ⅧB",
        "ⅧB",
        "ⅠB",
        "ⅡB",
        "ⅢA",
        "ⅣA",
        "ⅤA",
        "ⅥA",
        "ⅦA",
        "ⅧA",
    ],
    "cn": [
        "ⅠA",
        "ⅡA",
        "ⅢB",
        "ⅣB",
        "ⅤB",
        "ⅥB",
        "ⅦB",
        "Ⅷ",
        "Ⅷ",
        "Ⅷ",
        "ⅠB",
        "ⅡB",
        "ⅢA",
        "ⅣA",
        "ⅤA",
        "ⅥA",
        "ⅦA",
        "0",
    ],
}

PERIOD_NOBLE_GAS_SHELLS = {
    1: (["2"], ["K"]),
    2: (["8", "2"], ["L", "K"]),
    3: (["8", "8", "2"], ["M", "L", "K"]),
    4: (["8", "18", "8", "2"], ["N", "M", "L", "K"]),
    5: (["8", "18", "18", "8", "2"], ["O", "N", "M", "L", "K"]),
    6: (["8", "18", "32", "18", "8", "2"], ["P", "O", "N", "M", "L", "K"]),
    7: (
        ["8", "18", "32", "32", "18", "8", "2"],
        ["Q", "P", "O", "N", "M", "L", "K"],
    ),
}

METALLOID_LINE = {"B", "Si", "Ge", "As", "Sb", "Te", "Po", "At"}
NON_METALS = {
    "H",
    "He",
    "C",
    "N",
    "O",
    "F",
    "Ne",
    "P",
    "S",
    "Cl",
    "Ar",
    "Se",
    "Br",
    "Kr",
    "I",
    "Xe",
    "Rn",
    "Og",
    "At",
    "Ts",
}

RADIOACTIVE = {43, 61} | set(range(84, 119))

ELEMENT_SYMBOLS = [
    "H",
    "He",
    "Li",
    "Be",
    "B",
    "C",
    "N",
    "O",
    "F",
    "Ne",
    "Na",
    "Mg",
    "Al",
    "Si",
    "P",
    "S",
    "Cl",
    "Ar",
    "K",
    "Ca",
    "Sc",
    "Ti",
    "V",
    "Cr",
    "Mn",
    "Fe",
    "Co",
    "Ni",
    "Cu",
    "Zn",
    "Ga",
    "Ge",
    "As",
    "Se",
    "Br",
    "Kr",
    "Rb",
    "Sr",
    "Y",
    "Zr",
    "Nb",
    "Mo",
    "Tc",
    "Ru",
    "Rh",
    "Pd",
    "Ag",
    "Cd",
    "In",
    "Sn",
    "Sb",
    "Te",
    "I",
    "Xe",
    "Cs",
    "Ba",
    "La",
    "Ce",
    "Pr",
    "Nd",
    "Pm",
    "Sm",
    "Eu",
    "Gd",
    "Tb",
    "Dy",
    "Ho",
    "Er",
    "Tm",
    "Yb",
    "Lu",
    "Hf",
    "Ta",
    "W",
    "Re",
    "Os",
    "Ir",
    "Pt",
    "Au",
    "Hg",
    "Tl",
    "Pb",
    "Bi",
    "Po",
    "At",
    "Rn",
    "Fr",
    "Ra",
    "Ac",
    "Th",
    "Pa",
    "U",
    "Np",
    "Pu",
    "Am",
    "Cm",
    "Bk",
    "Cf",
    "Es",
    "Fm",
    "Md",
    "No",
    "Lr",
    "Rf",
    "Db",
    "Sg",
    "Bh",
    "Hs",
    "Mt",
    "Ds",
    "Rg",
    "Cn",
    "Nh",
    "Fl",
    "Mc",
    "Lv",
    "Ts",
    "Og",
]

ELEMENT_NAMES_CN = [
    "氢",
    "氦",
    "锂",
    "铍",
    "硼",
    "碳",
    "氮",
    "氧",
    "氟",
    "氖",
    "钠",
    "镁",
    "铝",
    "硅",
    "磷",
    "硫",
    "氯",
    "氩",
    "钾",
    "钙",
    "钪",
    "钛",
    "钒",
    "铬",
    "锰",
    "铁",
    "钴",
    "镍",
    "铜",
    "锌",
    "镓",
    "锗",
    "砷",
    "硒",
    "溴",
    "氪",
    "铷",
    "锶",
    "钇",
    "锆",
    "铌",
    "钼",
    "锝",
    "钌",
    "铑",
    "钯",
    "银",
    "镉",
    "铟",
    "锡",
    "锑",
    "碲",
    "碘",
    "氙",
    "铯",
    "钡",
    "镧",
    "铈",
    "镨",
    "钕",
    "钷",
    "钐",
    "铕",
    "钆",
    "铽",
    "镝",
    "钬",
    "铒",
    "铥",
    "镱",
    "镥",
    "铪",
    "钽",
    "钨",
    "铼",
    "锇",
    "铱",
    "铂",
    "金",
    "汞",
    "铊",
    "铅",
    "铋",
    "钋",
    "砹",
    "氡",
    "钫",
    "镭",
    "锕",
    "钍",
    "镤",
    "铀",
    "镎",
    "钚",
    "镅",
    "锔",
    "锫",
    "锎",
    "锿",
    "镄",
    "钔",
    "锘",
    "铹",
    "𬬻",
    "𬭊",
    "𬭳",
    "𬭛",
    "𬭶",
    "鿏",
    "𫟼",
    "𬬭",
    "鿔",
    "鿭",
    "𫓧",
    "镆",
    "𫟷",
    "鿬",
    "鿫",
]

PERIOD_LAYOUT = {
    1: [(1, "H"), (18, "He")],
    2: [(1, "Li"), (2, "Be"), (13, "B"), (14, "C"), (15, "N"), (16, "O"), (17, "F"), (18, "Ne")],
    3: [(1, "Na"), (2, "Mg"), (13, "Al"), (14, "Si"), (15, "P"), (16, "S"), (17, "Cl"), (18, "Ar")],
    4: [(1, "K"), (2, "Ca"), (3, "Sc"), (4, "Ti"), (5, "V"), (6, "Cr"), (7, "Mn"), (8, "Fe"), (9, "Co"), (10, "Ni"), (11, "Cu"), (12, "Zn"), (13, "Ga"), (14, "Ge"), (15, "As"), (16, "Se"), (17, "Br"), (18, "Kr")],
    5: [(1, "Rb"), (2, "Sr"), (3, "Y"), (4, "Zr"), (5, "Nb"), (6, "Mo"), (7, "Tc"), (8, "Ru"), (9, "Rh"), (10, "Pd"), (11, "Ag"), (12, "Cd"), (13, "In"), (14, "Sn"), (15, "Sb"), (16, "Te"), (17, "I"), (18, "Xe")],
    6: [(1, "Cs"), (2, "Ba"), (3, "La"), (4, "Hf"), (5, "Ta"), (6, "W"), (7, "Re"), (8, "Os"), (9, "Ir"), (10, "Pt"), (11, "Au"), (12, "Hg"), (13, "Tl"), (14, "Pb"), (15, "Bi"), (16, "Po"), (17, "At"), (18, "Rn")],
    7: [(1, "Fr"), (2, "Ra"), (3, "Ac"), (4, "Rf"), (5, "Db"), (6, "Sg"), (7, "Bh"), (8, "Hs"), (9, "Mt"), (10, "Ds"), (11, "Rg"), (12, "Cn"), (13, "Nh"), (14, "Fl"), (15, "Mc"), (16, "Lv"), (17, "Ts"), (18, "Og")],
}

LANTHANIDES = [
    "La",
    "Ce",
    "Pr",
    "Nd",
    "Pm",
    "Sm",
    "Eu",
    "Gd",
    "Tb",
    "Dy",
    "Ho",
    "Er",
    "Tm",
    "Yb",
    "Lu",
]

ACTINIDES = [
    "Ac",
    "Th",
    "Pa",
    "U",
    "Np",
    "Pu",
    "Am",
    "Cm",
    "Bk",
    "Cf",
    "Es",
    "Fm",
    "Md",
    "No",
    "Lr",
]


def build_elements() -> List[Element]:
    symbol_to_name = dict(zip(ELEMENT_SYMBOLS, ELEMENT_NAMES_CN))
    symbol_to_number = {symbol: idx + 1 for idx, symbol in enumerate(ELEMENT_SYMBOLS)}
    elements: List[Element] = []
    for period, entries in PERIOD_LAYOUT.items():
        for group, symbol in entries:
            elements.append(
                Element(
                    number=symbol_to_number[symbol],
                    symbol=symbol,
                    name_cn=symbol_to_name[symbol],
                    period=period,
                    group=group,
                    series="主族",
                )
            )
    for offset, symbol in enumerate(LANTHANIDES):
        elements.append(
            Element(
                number=symbol_to_number[symbol],
                symbol=symbol,
                name_cn=symbol_to_name[symbol],
                period=8,
                group=3 + offset,
                series="镧系",
            )
        )
    for offset, symbol in enumerate(ACTINIDES):
        elements.append(
            Element(
                number=symbol_to_number[symbol],
                symbol=symbol,
                name_cn=symbol_to_name[symbol],
                period=9,
                group=3 + offset,
                series="锕系",
            )
        )
    return sorted(elements, key=lambda e: e.number)


def is_metal(symbol: str) -> bool:
    if symbol in NON_METALS:
        return False
    if symbol in METALLOID_LINE:
        return False
    return True


F_BLOCK_LANTH_COLOR = (96, 200, 191)
F_BLOCK_ACTIN_COLOR = (85, 107, 47)


def group_color(group: int, mode: str) -> Tuple[float, float, float]:
    if mode in {"cas", "cn"} and group in {8, 9, 10}:
        rgb = (123, 141, 154)
    else:
        rgb = GROUP_COLORS_IUPAC.get(group, (180, 180, 180))
    return tuple(channel / 255.0 for channel in rgb)


def element_color(element: Element, mode: str) -> Tuple[float, float, float]:
    if element.series == "镧系":
        if mode == "iupac" and element.symbol == "La":
            return group_color(3, mode)
        return tuple(channel / 255.0 for channel in F_BLOCK_LANTH_COLOR)
    if element.series == "锕系":
        if mode == "iupac" and element.symbol == "Ac":
            return group_color(3, mode)
        return tuple(channel / 255.0 for channel in F_BLOCK_ACTIN_COLOR)
    return group_color(element.group, mode)


ELEMENTS = build_elements()
