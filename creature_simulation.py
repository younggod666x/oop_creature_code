import unittest
from contextlib import redirect_stdout
from io import StringIO


class Creature:
    def __init__(self, name, hp, attack_power):
        self.name = name
        self.hp = hp
        self.attack_power = attack_power

    def attack(self, target):
        if not self.is_alive():
            print(f"{self.name} cannot attack because it is defeated.")
            return

        print(f"{self.name} attacks {target.name} for {self.attack_power} damage!")
        target.hp -= self.attack_power

    def is_alive(self):
        return self.hp > 0

    def __str__(self):
        return f"{self.name} (HP: {self.hp})"


class FlyingCreature(Creature):
    def __init__(self, name, hp, attack_power):
        super().__init__(name, hp, attack_power)
        self.altitude = 0

    def fly_to(self, new_altitude):
        self.altitude = new_altitude
        print(f"{self.name} flies to altitude {self.altitude} meters.")

    def attack(self, target):
        if not self.is_alive():
            print(f"{self.name} cannot attack because it is defeated.")
            return

        print(f"{self.name} swoops down from altitude {self.altitude}!")
        print(
            f"{self.name} performs an aerial attack on {target.name} "
            f"for {self.attack_power} damage!"
        )
        target.hp -= self.attack_power
        if target.hp < 0:
            target.hp = 0
        print(f"{target.name} HP is now {target.hp}")


class SwimmingCreature(Creature):
    def __init__(self, name, hp, attack_power):
        super().__init__(name, hp, attack_power)
        self.depth = 0

    def dive_to(self, new_depth):
        self.depth = new_depth
        print(f"{self.name} dives to depth {self.depth} meters.")

    def attack(self, target):
        if not self.is_alive():
            print(f"{self.name} cannot attack because it is defeated.")
            return

        print(f"{self.name} attacks from underwater at depth {self.depth}!")
        print(f"It splashes {target.name} for {self.attack_power} damage!")
        target.hp -= self.attack_power
        if target.hp < 0:
            target.hp = 0
        print(f"{target.name} HP is now {target.hp}")


class FireCreature(Creature):
    def __init__(self, name, hp, attack_power, fire_level=0):
        super().__init__(name, hp, attack_power)
        self.fire_level = fire_level

    @property
    def fire_level(self):
        return self._fire_level

    @fire_level.setter
    def fire_level(self, value):
        if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 100:
            raise ValueError("fire_level must be an integer from 0 to 100")
        self._fire_level = value

    def emit_fire(self):
        print(f"{self.name} emits fire at level {self.fire_level}!")

    def attack(self, target):
        if not self.is_alive():
            print(f"{self.name} cannot attack because it is defeated.")
            return

        damage = self.attack_power + self.fire_level
        self.emit_fire()
        print(f"{self.name} attacks {target.name} with fire for {damage} damage!")
        target.hp = max(0, target.hp - damage)
        print(f"{target.name} HP is now {target.hp}")


class CreatureTests(unittest.TestCase):
    def test_base_attack_and_life_status(self):
        attacker = Creature("Goblin", 20, 7)
        target = Creature("Target", 10, 4)

        with redirect_stdout(StringIO()):
            attacker.attack(target)

        self.assertEqual(target.hp, 3)
        self.assertTrue(attacker.is_alive())
        attacker.hp = 0
        self.assertFalse(attacker.is_alive())

    def test_flying_creature_altitude_and_attack(self):
        flyer = FlyingCreature("Hawk", 30, 8)
        target = Creature("Target", 5, 0)

        with redirect_stdout(StringIO()):
            flyer.fly_to(120)
            flyer.attack(target)

        self.assertEqual(flyer.altitude, 120)
        self.assertEqual(target.hp, 0)

    def test_swimming_creature_depth_and_attack(self):
        swimmer = SwimmingCreature("Serpent", 30, 7)
        target = Creature("Target", 20, 0)

        with redirect_stdout(StringIO()):
            swimmer.dive_to(30)
            swimmer.attack(target)

        self.assertEqual(swimmer.depth, 30)
        self.assertEqual(target.hp, 13)

    def test_fire_level_is_limited_to_zero_through_one_hundred(self):
        for level in (0, 100):
            with self.subTest(level=level):
                self.assertEqual(FireCreature("Phoenix", 30, 5, level).fire_level, level)

        for level in (-1, 101, 1.5, True):
            with self.subTest(level=level):
                with self.assertRaises(ValueError):
                    FireCreature("Phoenix", 30, 5, level)

    def test_fire_attack_adds_fire_level_and_stops_at_zero_hp(self):
        attacker = FireCreature("Phoenix", 30, 8, 5)
        target = Creature("Target", 20, 0)

        with redirect_stdout(StringIO()):
            attacker.attack(target)

        self.assertEqual(target.hp, 7)

        target.hp = 2
        with redirect_stdout(StringIO()):
            attacker.attack(target)
        self.assertEqual(target.hp, 0)

    def test_defeated_fire_creature_cannot_attack(self):
        attacker = FireCreature("Phoenix", 0, 8, 5)
        target = Creature("Target", 20, 0)

        with redirect_stdout(StringIO()):
            attacker.attack(target)

        self.assertEqual(target.hp, 20)


if __name__ == "__main__":
    unittest.main()
