from __future__ import annotations

from typing import TYPE_CHECKING

import color
import entity_factories
from components.base_components import BaseComponent
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor


class Fighter(BaseComponent):
    parent: Actor

    def __init__(self) -> None:
        pass

    def set_init_hp(self) -> None:
        self.max_hp = self.parent.skills.get_level("hp") * 10
        self._hp = self.parent.skills.get_level("hp") * 10

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.die()

    @property
    def defense(self) -> int:
        return self.parent.skills.get_level("defence") + self.defense_bonus

    @property
    def power(self) -> int:
        return self.parent.skills.get_level("attack") + self.power_bonus

    @property
    def defense_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.defense_bonus
        else:
            return 0

    @property
    def power_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.power_bonus
        else:
            return 0

    def die(self) -> None:
        if self.engine.player is self.parent:
            death_message = "You died!"
            death_message_color = color.player_die

            # Kill the player.
            self.parent.char = "%"
            self.parent.color = (191, 0, 0)
            self.parent.blocks_movement = False
            self.parent.ai = None
            self.parent.name = f"remains of {self.parent.name}"
            self.parent.render_order = RenderOrder.CORPSE

        else:
            death_message = f"{self.parent.name} is dead!"
            death_message_color = color.enemy_die

            # 'Kill' the entity. (Removes the entity and replaces it with an item.)
            entity_factories.corpse.spawn(
                self.parent.gamemap, self.parent.x, self.parent.y
            ).name = f"remains of {self.parent.name}"
            self.parent.gamemap.entities.remove(self.parent)

        self.engine.message_log.add_message(death_message, death_message_color)

    def heal(self, amount: int) -> int:
        if self.hp == self.max_hp:
            return 0

        new_hp_value = self.hp + amount

        if new_hp_value > self.max_hp:
            new_hp_value = self.max_hp

        amount_recovered = new_hp_value - self.hp

        self.hp = new_hp_value

        return amount_recovered

    def take_damage(self, amount: int) -> None:
        self.hp -= amount
