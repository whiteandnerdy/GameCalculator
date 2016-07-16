import math
import locale

locale.setlocale( locale.LC_ALL, '')


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

    def __init__(self, name, cell_cost, base_life, base_upgrade_price, base_heat, life_level, cell_level,
                 level_price_increase, level_heat_increase):
        self.name = name
        self.cell_cost = cell_cost
        self.base_life = base_life
        self.base_upgrade_price = base_upgrade_price
        self.base_heat = base_heat
        self.life_level = life_level
        self.lifetime = base_life * (2 ** life_level)
        self.cell_level = cell_level
        self.current_cost = base_upgrade_price * (level_price_increase ** cell_level)
        self.current_heat = base_heat * (level_heat_increase ** cell_level)
        self.level_price_increase = level_price_increase
        self.levelHeatIncrease = level_heat_increase
        self.grossRevenue = self.current_heat * self.lifetime

    def calculate_level_upgrade(self,desired_level):
        return locale.currency(self.base_upgrade_price * (self.level_price_increase ** desired_level), grouping=True)

    def calculate_heat_production(self):
        return locale.currency(self.current_heat, grouping=True)

    def calculate_net_production(self):
        return locale.currency(self.current_heat - (self.cell_cost/self.lifetime), grouping=True)

f = Cell("Fusion", 800000000000, 800, 100000000000000, 2500000000, 1, 2, 1.78, 1.25)

print(f.calculate_level_upgrade(3))
print(f.calculate_heat_production())
print(f.calculate_net_production())