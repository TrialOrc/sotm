from __future__ import annotations

import random
from typing import TYPE_CHECKING, Optional, Tuple

import numpy as np

import color
import exceptions

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity, Item


class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in.

        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class PickupAction(Action):
    """Pick up an item and add it to the inventory, if there is room for it."""

    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        actor_location_x = self.entity.x
        actor_location_y = self.entity.y
        inventory = self.entity.inventory

        for item in self.engine.game_map.items:
            if actor_location_x == item.x and actor_location_y == item.y:
                if len(inventory.items) >= inventory.capacity:
                    raise exceptions.Impossible("Your inventory is full.")

                self.engine.game_map.entities.remove(item)
                item.parent = self.entity.inventory
                inventory.items.append(item)

                self.engine.message_log.add_message(f"You picked up the {item.name}")
                return

        raise exceptions.Impossible("there is nothing here to pick up.")


class SearchAction(Action):
    def __init__(self, entity: Actor) -> None:
        super().__init__(entity)

    def perform(self) -> None:
        actor_location_x = self.entity.x
        actor_location_y = self.entity.y
        inventory = self.entity.inventory
        # Add a `checked map` (np.bool((height, width)) where `True` = Checked tiles, `False` = Unchecked tile)
        # `checked map` should have a method to regenerate checked tiles after time. (More checked tiles = shorter regeneration time)
        # Add a method to check all spaces surrounding the player. scipy.signal.convolve2d?
        # The following line is used to remove errors, remove when class is built:
        tiles_surrounding_player, tile_not_searched, luck_modifier, random_item = None

        for tile in tiles_surrounding_player:
            if tile_not_searched:
                pass
                # pick a random tile
                if (
                    np.random.random() < 0.5 + luck_modifier
                ):  # Chance to find an item, modified by player's luck.
                    found_item = (
                        random_item()
                    )  # Roll from a list of items able to be searched for.
                    found_item.parent = self.entity.inventory  # Add item to inventory.
                    inventory.items.append(found_item)
                    # Update `checked map`
                    self.engine.message_log.add_message(
                        f"You found a {found_item.name}"
                    )
                else:
                    # Update `checked map`
                    raise exceptions.Impossible("You find nothing.")
            else:  # If all tiles have been checked
                raise exceptions.Impossible("You've searched everywhere.")


class ChopTreeAction(Action):
    def __init__(self, entity: Actor) -> None:
        super().__init__(entity)


class ItemAction(Action):
    def __init__(
        self, entity: Actor, item: Item, target_xy: Optional[Tuple[int, int]] = None
    ):
        super().__init__(entity)
        self.item = item
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this action's destination."""
        return self.engine.game_map.get_actor_at_location(*self.target_xy)

    def perform(self) -> None:
        """Invoke the item's ability, this cation will be given to provide context."""
        if self.item.consumable:
            self.item.consumable.activate(self)


class DropItem(ItemAction):
    def perform(self) -> None:
        if self.entity.equipment.item_is_equipped(self.item):
            self.entity.equipment.toggle_equip(self.item)
        self.entity.inventory.drop(self.item)


class EquipAction(Action):
    def __init__(self, entity: Actor, item: Item):
        super().__init__(entity)

        self.item = item

    def perform(self) -> None:
        self.entity.equipment.toggle_equip(self.item)


class WaitAction(Action):
    def perform(self) -> None:
        pass


class TakeStairsAction(Action):
    def perform(self) -> None:
        """
        Take the stairs, if any exist at the entity's location.
        """
        if (self.entity.x, self.entity.y) == self.engine.game_map.downstairs_location:
            self.engine.game_world.generate_floor()
            self.engine.message_log.add_message(
                "You descend the staircase.", color.descend
            )
        else:
            raise exceptions.Impossible("There are no stairs here.")


class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns this action's destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking entity at this action's destination."""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this action's destination."""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("Nothing to attack.")
        damage_dealt = random.randint(0, self.entity.fighter.power + 1)
        # logging.debug(f"damage_dealt={damage_dealt}")
        damage_received = max(0, damage_dealt - target.fighter.defense)
        # logging.debug(f"damage_received={damage_received}")
        defense_xp = min(
            (damage_dealt - damage_received), target.fighter.defense
        )  # TODO: Fix, if the player blocks more damage than is dealt, receive blocked damage XP

        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk

        if damage_dealt == 0:
            self.engine.message_log.add_message(
                f"{attack_desc} but misses.", attack_color
            )
        else:
            if damage_received > 0:
                self.engine.message_log.add_message(
                    f"{attack_desc} for {damage_received} hp.", attack_color
                )

                target.fighter.hp -= damage_received

            if self.entity is not self.engine.player:
                if not defense_xp == 0:
                    self.engine.player.skills.add_xp("defense", defense_xp)
                    self.engine.player.skills.add_xp("hp", damage_dealt)
            if self.entity is self.engine.player:
                if not damage_dealt == 0:
                    self.engine.player.skills.add_xp("attack", damage_dealt)

            else:
                self.engine.message_log.add_message(
                    f"{attack_desc} but does no damage.", attack_color
                )


class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            # Destination is out of bounds.
            raise exceptions.Impossible("That way is blocked.")
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            # Destination is blocked by a tile.
            raise exceptions.Impossible("That way is blocked.")
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            # Destination is blocked by an entity
            raise exceptions.Impossible("That way is blocked.")

        self.entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()

        # TODO: handle if the player moves into another chunk.

        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()
