from components.ai import HostileEnemy, NoAI, HauntedTree
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Skills
from entity import Actor, Item, Trap
import color

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    skills=Skills(),
    fighter=Fighter(),
    inventory=Inventory(capacity=26),
)

orc = Actor(
    char="o",
    color=color.orc,
    name="Orc",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    skills=Skills(),
    fighter=Fighter(),
    inventory=Inventory(capacity=0),
    skill_levels={"attack": 2},
)
troll = Actor(
    char="T",
    color=color.troll,
    name="Troll",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    skills=Skills(),
    fighter=Fighter(),
    inventory=Inventory(capacity=0),
)
rubberduck = Actor(
    char="d",
    color=color.duck,
    name="Rubber Duck",
    ai_cls=NoAI,
    equipment=Equipment(),
    skills=Skills(),
    fighter=Fighter(),
    inventory=Inventory(capacity=0),
)

hauntedtree = Trap(
    char="♠",
    color=(34, 139, 34),
    name="Tree",
    blocks_movement=True,
    ai_cls=HauntedTree,
    stops_movement=False,
    damage=1,
)

corpse = Item(
    char="%",
    color=color.corpse,
    name=None,  # f"reamains of {self.parent.name}"
    consumable=consumable.HealingConsumable(amount=1),
)

confusion_scroll = Item(
    char="~",
    color=color.confusion_scroll,
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)
fireball_scroll = Item(
    char="~",
    color=color.fireball_scroll,
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)
health_potion = Item(
    char="!",
    color=color.health_potion,
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
)
lightning_scroll = Item(
    char="~",
    color=color.lightning_scroll,
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)

dagger = Item(
    char="/",
    color=color.weapon,
    name="Dagger",
    equippable=equippable.Dagger(),
)
sword = Item(
    char="/",
    color=color.weapon,
    name="Sword",
    equippable=equippable.Sword(),
)

leather_armor = Item(
    char="[",
    color=color.armor,
    name="Leather Armor",
    equippable=equippable.LeatherArmor(),
)
chain_mail = Item(
    char="[",
    color=color.armor,
    name="Chain Mail",
    equippable=equippable.ChainMail,
)
