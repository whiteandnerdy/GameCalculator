import locale
from collections import namedtuple


locale.setlocale(locale.LC_ALL, '')


class Cell:
    name = ""
    cell_cost = -1
    base_life = -1
    base_upgrade_price = -1
    base_heat = -1
    lifetime = -1
    cell_level = -1
    life_level = -1
    current_cost = -1
    current_heat = -1
    level_price_increase = -1
    level_heat_increase = -1

    def __init__(self, name, cell_cost, base_life, base_upgrade_price, base_heat, life_level, cell_level):
        self.name = name
        self.cell_cost = cell_cost
        self.base_life = base_life
        self.base_upgrade_price = base_upgrade_price
        self.base_heat = base_heat
        self.life_level = life_level
        self.lifetime = base_life * (2 ** life_level)
        self.cell_level = cell_level
        self.current_cost = base_upgrade_price * (1.78 ** cell_level)
        self.current_heat = base_heat * (1.25 ** cell_level)
        self.grossRevenue = self.current_heat * self.lifetime

    def calculate_level_upgrade(self, desired_level):
        # iterate through from current to desired level and return total amount for upgrade
        total_cost = 0
        for i in range(self.cell_level, desired_level):
            total_cost += self.base_upgrade_price * (1.78 ** i)

        return locale.currency(total_cost, grouping=True)

    def calculate_cell_heat_upgrade(self, desired_level):
        return self.base_heat * (1.25 ** desired_level)

    def cell_heat_production(self):
        return self.current_heat

    def cell_net_production(self):
        return self.current_heat - (self.cell_cost / self.lifetime)


class Generator:
    level = -1
    base_cost = -1
    base_upgrade_price = -1
    max_heat = -1
    max_water = -1
    effectiveness = -1
    water_bonus = -1

    def __init__(self, level, base_cost, max_heat_level, effectiveness, max_water):
        self.level = level
        self.base_cost = base_cost
        self.max_heat = max_heat_level
        self.effectiveness = effectiveness
        self.max_water = max_water
        self.water_bonus = 100 * (2 ** (level - 2))

    def show_max_heat(self, max_heat_level=None):
        if max_heat_level is None:
            max_heat_level = self.max_heat

        return 900*(2 ** max_heat_level)

    def show_max_water(self,max_water_level=None):
        if max_water_level is None:
            max_water_level = self.max_water

        return 8000*(1.25 ** max_water_level)

    def show_effectiveness(self, effectiveness_level=None):
        if effectiveness_level is None:
            effectiveness_level = self.effectiveness

        return 32 * (1.25 ** effectiveness_level)

    def show_water_bonus(self):

        return self.water_bonus


def calculate_water_remaining(cell, generator, number_of_generators):

    return -1*((((cell.current_heat / number_of_generators) - generator.show_effectiveness()) / generator.water_bonus) - generator.show_max_water())


def calculate_total_heat_per_generator(cell, generator, number_of_generators):

    # ((max_water - remaining_water) * water_bonus) + effectiveness
    max_water = generator.show_max_water()
    remaining_water = calculate_water_remaining(cell,generator,number_of_generators)
    water_bonus = generator.show_water_bonus()
    effectiveness = generator.show_effectiveness()

    return ((max_water - remaining_water) * water_bonus) + effectiveness

# Testing
# nuclear = Cell("Nuclear", 500000000, 800, 10000000000, 1200000, 1, 0)
f = Cell("Fusion", 800000000000, 800, 100000000000000, 2500000000, 1, 3)

g = Generator(3, 10000000000000000, 23, 77, 45)

print("Generator")
print("max heat: {:,}".format(g.show_max_heat()), " effectiveness: {:,}".format(g.show_effectiveness()),
      " max water: {:,}".format(g.show_max_water()), "water bonus: {:,}".format(g.show_water_bonus()))

print("Remaining Water: {:,}".format(calculate_water_remaining(f, g, 1)),
      "Total heat per generator: {:,}".format(calculate_total_heat_per_generator(f, g, 1)))

# print("Cell")
# print(nuclear.calculate_level_upgrade(3))
# print(nuclear.cell_heat_production())
# print(nuclear.calculate_cell_heat_upgrade(3))
# print(nuclear.cell_net_production())
# print(f.calculate_level_upgrade(3))
print(f.name, "cell has heat production of: {:,}".format(f.cell_heat_production()))
# print(f.cell_net_production())