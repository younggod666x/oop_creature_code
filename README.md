# Creature Simulation

A small, dependency-free Python project for practicing inheritance and polymorphic
attacks. `creature_simulation.py` defines the base `Creature` and its flying,
swimming, and fire-based variants.

## Requirements

- Python 3.8 or newer

## Run the tests

From the repository root, run:

```shell
python -m unittest creature_simulation -v
```

The test cases are included in `creature_simulation.py`. To run them directly:

```shell
python creature_simulation.py
```

On Windows, use `py` instead of `python` if that is how Python is installed.

## Use the creatures

Import the classes from the module and create creatures with a name, hit points,
and attack power:

```python
from creature_simulation import Creature, FireCreature

target = Creature("Practice Dummy", 40, 0)
phoenix = FireCreature("Phoenix", 30, 8, fire_level=5)

phoenix.emit_fire()
phoenix.attack(target)  # Deals attack_power + fire_level (13 damage).
```

`FlyingCreature.fly_to()` sets its altitude, and `SwimmingCreature.dive_to()`
sets its depth. Their attacks, like `FireCreature.attack()`, do not reduce a
target's hit points below zero. A fire level must be an integer from 0 to 100;
it adds directly to the fire creature's attack power.

## Learning branch history

The repository history keeps the exercise steps separate: `flying_creature` and
`swimming_creature` branch from the base `main` commit, their integration includes
a separate conflict-resolution commit, and `fire_creature` branches from that
integrated result before being merged into `main`.
