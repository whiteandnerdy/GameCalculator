generatorOne = {}
generatorOne['name'] = "Generator 1"
generatorOne['baseCost'] = 500
generatorOne['type'] = 1
generatorOne['baseEffectiveness'] = 3
generatorOne['baseMaxHeat'] = 25
generatorOne['baseMaxWater'] = 0
generatorOne['waterBonus'] = 0

generatorTwo = {}
generatorTwo['name'] = "Generator 2"
generatorTwo['baseCost'] = 2500000
generatorTwo['type'] = 2
generatorTwo['baseEffectiveness'] = 9
generatorTwo['baseMaxHeat'] = 150
generatorTwo['baseMaxWater'] = 5000
generatorTwo['waterBonus'] = 100

generatorThree = {}
generatorThree['name'] = "Generator 3"
generatorThree['baseCost'] = 10000000000000
generatorThree['type'] = 3
generatorThree['baseEffectiveness'] = 32
generatorThree['baseMaxHeat'] = 900
generatorThree['baseMaxWater'] = 8000
generatorThree['waterBonus'] = 200

generatorFour = {}
generatorFour['name'] = "Generator 4"
generatorFour['baseCost'] = 50000000000000000
generatorFour['type'] = 4
generatorFour['baseEffectiveness'] = 96
generatorFour['baseMaxHeat'] = 2200
generatorFour['baseMaxWater'] = 22000
generatorFour['waterBonus'] = 400

generatorFive = {}
generatorFive['name'] = "Generator 5"
generatorFive['baseCost'] = 12500000000000000000
generatorFive['type'] = 5
generatorFive['baseEffectiveness'] = 288
generatorFive['baseMaxHeat'] = 4400
generatorFive['baseMaxHeat'] = 44000
generatorFive['waterBonus'] = 800


def calculate_water_remaining(cell, generator, number_of_generators, circulator_level=None):

    return -1*((((cell.current_heat / number_of_generators) - generator.show_effectiveness()) / generator.water_bonus) - generator.show_max_water(None,circulator_level))


def calculate_total_heat_per_generator(cell, generator, number_of_generators):

    # ((max_water - remaining_water) * water_bonus) + effectiveness
    max_water = generator.show_max_water()
    remaining_water = calculate_water_remaining(cell, generator, number_of_generators)
    water_bonus = generator.show_water_bonus()
    effectiveness = generator.show_effectiveness()

    return ((max_water - remaining_water) * water_bonus) + effectiveness

# def check_upgrade(current_cell,current_gen,number_of_generators,proposed_cell,water_pump,water_element)
