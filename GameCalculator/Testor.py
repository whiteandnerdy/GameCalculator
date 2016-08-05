from Cell import Cell
from Cell import Generator
from Cell import Circulator

import GeneratorType
import CellType

# Testing
# g = Generator(3, 10000000000000000, 0, 0, 0)
f2 = Cell(CellType.fusion, 2, 14)
t = Cell(CellType.thorium, 1, 0)
g2 = Generator(GeneratorType.generatorThree, 25, 86, 45)

print("\r\nGenerator")
print("max heat: {:,}".format(g2.show_max_heat()), " effectiveness: {:,}".format(g2.show_effectiveness()),
      " max water: {:,}".format(g2.show_max_water()),
      " max water with circulator: {:,}".format(g2.show_max_water(None, 2)),
      "water bonus: {:,}".format(g2.show_water_bonus()))

print("Remaining Water: {:,}".format(GeneratorType.calculate_water_remaining(f2, g2, 2, 2)),
      "Total heat per generator: {:,}".format(GeneratorType.calculate_total_heat_per_generator(f2, g2, 2)))

print("\r\nCell")
# print(f.name, "cell has heat production of: {:,}".format(f.cell_heat_production()))
print(f2.name, "cell at level", f2.cell_level, "has heat production of: {0:,}".format(f2.cell_heat_production()))
# print(t.name, "cell has heat production of: {:,}".format(t.cell_heat_production()))

next_level = 15
print("Cost to upgrade ", f2.name, "cell to level", next_level, "is: ", f2.calculate_level_upgrade(next_level))

# print(f.cell_net_production())