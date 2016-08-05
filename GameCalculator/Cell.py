import locale
from collections import namedtuple
import CellType
import GeneratorType

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

    def __init__(self, cell_type, life_level, cell_level):
        self.name = cell_type['name']
        self.cell_cost = cell_type['baseCost']
        self.base_life = cell_type['baseLife']
        self.base_upgrade_price = cell_type['baseUpgradePrice']
        self.base_heat = cell_type['baseHeat']
        self.life_level = life_level
        self.lifetime = self.base_life * (2 ** life_level)
        self.cell_level = cell_level
        self.current_cost = self.base_upgrade_price * (1.78 ** cell_level)
        self.current_heat = self.base_heat * (1.25 ** cell_level)
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

class Circulator:
    level = -1
    base_cost = -1
    base_boost = -1

    def __init__(self, c_level):
        self.level = c_level
        self.base_cost = 1000000000000000000
        self.base_boost = 1.9

    def calculate_water_boost(self, c_level=None):
        if c_level is None:
            c_level = self.level

        return 1.9 + (.225 * c_level)

    def calculate_upgrade_cost(self, desired_level):
        total_cost = 0
        for i in range(self.level, desired_level):
            total_cost += self.base_cost * (2.10 ** i)

        return locale.currency(total_cost, grouping=True)


class Generator:
    level = -1
    base_cost = -1
    base_upgrade_price = -1
    base_effectiveness = -1
    max_heat = -1
    max_water = -1
    effectiveness = -1
    water_bonus = -1

    def __init__(self, gen_type, max_heat_level, effectiveness, max_water):
        self.level = gen_type['type']
        self.base_cost = gen_type['baseCost']
        self.base_max_heat = gen_type['baseMaxHeat']
        self.base_max_water = gen_type['baseMaxWater']
        self.base_effectiveness = gen_type['baseEffectiveness']
        self.max_heat = max_heat_level
        self.max_water = max_water
        self.effectiveness = effectiveness
        self.water_bonus = 100 * (2 ** (gen_type['type'] - 2))

    def show_max_heat(self, max_heat_level=None):
        if max_heat_level is None:
            max_heat_level = self.max_heat

        return self.base_max_heat * (2 ** max_heat_level)

    def show_max_water(self, max_water_level=None, circulator_level=None):
        if max_water_level is None:
            max_water_level = self.max_water
        if circulator_level is None:
            max_water = self.base_max_water * (1.25 ** max_water_level)
        else:
            c = Circulator(circulator_level)
            max_water = (self.base_max_water * (1.25 ** max_water_level)) * \
                        c.calculate_water_boost()
        return max_water

    def show_effectiveness(self, effectiveness_level=None):
        if effectiveness_level is None:
            effectiveness_level = self.effectiveness

        return self.base_effectiveness * (1.25 ** effectiveness_level)

    def show_water_bonus(self):

        return self.water_bonus

