from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class AllotropeData:
    name: str
    properties: Dict[str, str]


PROPERTY_LABELS = {
    "density": "标准状况密度 (kg/m³)",
    "melting_point": "熔点 (K)",
    "boiling_point": "沸点 (K)",
    "electronegativity": "电负性 (鲍林)",
    "vdw_radius": "范德华半径 (Å)",
    "speed_of_sound": "声速",
    "triple_point": "三相点",
    "critical_point": "临界点",
    "electrical_conductivity": "电导率",
    "thermal_conductivity": "热导率",
    "mohs_hardness": "莫氏硬度",
    "crystal_structure": "晶体结构",
}

PROPERTY_ORDER = list(PROPERTY_LABELS.keys())

WIKIPEDIA_ALLOTROPES: Dict[str, List[AllotropeData]] = {
    "H": [
        AllotropeData(
            name="氢气 (H₂)",
            properties={
                "density": "0.08988",
                "melting_point": "13.99",
                "boiling_point": "20.271",
                "electronegativity": "2.20",
                "vdw_radius": "1.20",
                "speed_of_sound": "1310 m/s",
                "triple_point": "13.8033 K, 7.042 kPa",
                "critical_point": "33.145 K, 1.296 MPa",
                "electrical_conductivity": "0 S/m",
                "thermal_conductivity": "0.1805 W/(m·K)",
            },
        ),
    ],
    "C": [
        AllotropeData(
            name="石墨",
            properties={
                "density": "2267",
                "melting_point": "3823",
                "boiling_point": "4300",
                "electronegativity": "2.55",
                "vdw_radius": "1.70",
                "speed_of_sound": "21000 m/s",
                "electrical_conductivity": "2.5 × 10⁵ S/m",
                "thermal_conductivity": "119–165 W/(m·K)",
                "mohs_hardness": "1–2",
                "crystal_structure": "六方晶系",
            },
        ),
        AllotropeData(
            name="金刚石",
            properties={
                "density": "3515",
                "melting_point": "3823",
                "boiling_point": "4300",
                "electronegativity": "2.55",
                "vdw_radius": "1.70",
                "speed_of_sound": "12000 m/s",
                "electrical_conductivity": "≈0 S/m",
                "thermal_conductivity": "2200 W/(m·K)",
                "mohs_hardness": "10",
                "crystal_structure": "立方晶系 (金刚石型)",
            },
        ),
    ],
    "O": [
        AllotropeData(
            name="氧气 (O₂)",
            properties={
                "density": "1.429",
                "melting_point": "54.36",
                "boiling_point": "90.20",
                "electronegativity": "3.44",
                "vdw_radius": "1.52",
                "speed_of_sound": "317.5 m/s",
                "triple_point": "54.361 K, 0.1463 kPa",
                "critical_point": "154.59 K, 5.043 MPa",
                "electrical_conductivity": "0 S/m",
                "thermal_conductivity": "0.02658 W/(m·K)",
            },
        ),
    ],
    "Fe": [
        AllotropeData(
            name="α-铁 (体心立方)",
            properties={
                "density": "7874",
                "melting_point": "1811",
                "boiling_point": "3134",
                "electronegativity": "1.83",
                "vdw_radius": "2.04",
                "speed_of_sound": "5120 m/s",
                "electrical_conductivity": "10.0 × 10⁶ S/m",
                "thermal_conductivity": "80.4 W/(m·K)",
                "mohs_hardness": "4.0",
                "crystal_structure": "体心立方",
            },
        ),
    ],
}


def get_allotropes(symbol: str) -> List[AllotropeData]:
    return WIKIPEDIA_ALLOTROPES.get(symbol, [])
