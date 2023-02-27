from __future__ import annotations

from typing import TYPE_CHECKING, Dict, TypeVar, Union

from components.base_components import BaseComponent

if TYPE_CHECKING:
    from entity import Actor

T = TypeVar("T", bound="Skill")


class Skill(BaseComponent):
    parent: Actor

    name: str
    current_level: int
    current_xp: int
    level_up_base: int
    level_up_factor: int
    xp_given: int

    def __init__(
        self,
        name: str,
        current_level: int = 1,
        current_xp: int = 0,
        level_up_base: int = 50,
        level_up_factor: int = 10,
        xp_given: int = 0,
    ):
        self.name = name
        self.current_level = current_level
        self.current_xp = current_xp
        self.level_up_base = level_up_base
        self.level_up_factor = level_up_factor
        self.xp_given = xp_given

    @property
    def experience_to_next_level(self) -> int:
        return self.level_up_base + self.current_level * self.level_up_factor

    @property
    def requires_level_up(self) -> bool:
        return self.current_xp > self.experience_to_next_level

    def add_xp(self, xp: int) -> None:
        if xp == 0 or self.level_up_base == 0:
            return

        self.current_xp += xp

    def increase_level(self) -> None:
        self.current_xp -= self.experience_to_next_level

        self.current_level += 1


class Skills(BaseComponent):
    parent: Actor

    def __init__(self):
        skills: Dict[str, Skill] = {
            "attack": Skill("Attack"),
            "strength": Skill("Strength"),
            "defense": Skill("Defense"),
            "hp": Skill("HP"),
            "woodcutting": Skill("Woodcutting"),
            "cooking": Skill("Cooking"),
            "scavenging": Skill("Scavenging"),
        }
        self.skills = skills
        self.skills = {name: cls for name, cls in self.skills.items()}

    def __getitem__(self, key: str) -> Union[Skill, None]:
        return self.skills.get(key)

    def get_level(self, skill_name: str) -> int:
        skill = self.skills.get(skill_name)
        return skill.current_level if skill else 0

    def list_skill_names(self):
        return list(self.skills.keys())

    def add_xp(self, skill_name: str, xp: int):
        skill = self.skills.get(skill_name)
        if skill:
            skill.add_xp(xp)
            self.engine.message_log.add_message(
                f"You gain {xp} {skill.name} experience points."
            )

            if skill.requires_level_up:
                self.engine.message_log.add_message(
                    f"Your {skill.name} skill advances to level {skill.current_level + 1}!"
                )
                if not skill.current_level == 20:
                    skill.increase_level()
