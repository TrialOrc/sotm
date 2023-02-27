from enum import auto, Enum


class EquipmentType(Enum):
    WEAPON = auto()
    MAIN_HAND = auto()  # Replace WEAPON when implemented.
    OFF_HAND = auto()  # Replace WEAPON when implemented.  # ? Implement dual wield (main + off)
    ARMOR = auto()
    HEAD = auto()  # ? Implement items that cover head but not face, and items that cover both.
    BODY_INNER = auto()  # Replace ARMOR when implemented.
    BODY = auto()  # Replace ARMOR when implemented.
    BODY_OUTER = auto()  # Replace ARMOR when implemented.
    HANDS_INNER = auto()
    HANDS = auto()
    LEGS_INNER = auto()
    LEGS = auto()
    LEGS_OUTER = auto()
    FEET_INNER = auto()
    FEET_OUTER = auto()
