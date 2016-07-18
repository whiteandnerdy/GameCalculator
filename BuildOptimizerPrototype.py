from collections import namedtuple
from itertools import combinations_with_replacement

CurrentState = namedtuple('CurrentState', 'cash total_squares components')


class Windmill:
    WindmillParams = namedtuple('WindmillParams', 'power_output_per_tick total_ticks_lifecycle cost_per_lifecycle')
    AllTypes = {'LVL1': WindmillParams(power_output_per_tick=1, total_ticks_lifecycle=10, cost_per_lifecycle=1),
                'LVL2': WindmillParams(power_output_per_tick=10, total_ticks_lifecycle=10, cost_per_lifecycle=5)}

    @staticmethod
    def create(windmill_type):
        return Windmill(*Windmill.AllTypes[windmill_type])

    def __init__(self, power_output_per_tick, total_ticks_lifecycle, cost_per_lifecycle):
        self.power_output_per_tick = power_output_per_tick
        self.power_output_total_lifecycle = total_ticks_lifecycle
        self.cost_per_lifecycle = cost_per_lifecycle
        self._str = 'Windmill ({}, {}, {})'.format(power_output_per_tick, total_ticks_lifecycle, cost_per_lifecycle)

    def __str__(self):
        return self._str


class PowerCollector:
    PowerCollectorParams = namedtuple('PowerCollectorParams', 'power_collected_per_tick one_time_cost')
    AllTypes = {'LVL1': PowerCollectorParams(power_collected_per_tick=5, one_time_cost=50),
                'LVL2': PowerCollectorParams(power_collected_per_tick=7, one_time_cost=100)}

    @staticmethod
    def create(powercollector_type):
        return PowerCollector(*PowerCollector.AllTypes[powercollector_type])

    def __init__(self, power_collected_per_tick, one_time_cost):
        self.power_collected_per_tick = power_collected_per_tick
        self.one_time_cost = one_time_cost
        self._str = 'PowerCollector ({}, {})'.format(power_collected_per_tick, one_time_cost)

    def __str__(self):
        return self._str


class ResearchCenter:
    ResearchCenterParams = namedtuple('ResearchCenter', 'research_output_per_tick one_time_cost')
    AllTypes = {'LVL1': ResearchCenterParams(research_output_per_tick=1, one_time_cost=50),
                'LVL2': ResearchCenterParams(research_output_per_tick=5, one_time_cost=100)}

    @staticmethod
    def create(researchcenter_type):
        return ResearchCenter(*ResearchCenter.AllTypes[researchcenter_type])

    def __init__(self, research_output_per_tick, one_time_cost):
        self.research_output_per_tick = research_output_per_tick
        self.one_time_cost = one_time_cost
        self._str = 'ResearchCenter ({}, {})'.format(research_output_per_tick, one_time_cost)

    def __str__(self):
        return self._str


class BuildInstance:
    def __init__(self, *components):
        self._components = components
        self._set_total_power()
        self._set_power_collected()
        self._set_total_cost()

    def _set_total_power(self):
        self._total_power_output = 0

        for component in self._components:
            if hasattr(component, 'power_output_per_tick'):
                self._total_power_output += component.power_output_per_tick

    def _set_power_collected(self):
        self._total_power_collected = 0

        for component in self._components:
            if hasattr(component, 'power_collected_per_tick'):
                self._total_power_collected += component.power_collected_per_tick

    def _set_total_cost(self):
        self._cost_total = 0

        for component in self._components:
            if hasattr(component, 'cost_per_lifecycle'):
                self._cost_total += component.cost_per_lifecycle
                continue
            # when we support knowing about the current build, we'll have to conditionally apply one_time_cost
            if hasattr(component, 'one_time_cost'):
                self._cost_total += component.one_time_cost
                continue
            raise AttributeError('component does not have a cost attribute: ' + str(component))

    def is_self_collecting(self):
        return self._total_power_output <= self._total_power_collected

    def costs_less_or_equal(self, amount):
        return self._cost_total <= amount

    def get_total_power_produced(self):
        return self._total_power_output

    def get_total_cost(self):
        return self._cost_total

    def get_total_research_produced(self):
        pass

    def __str__(self):
        #return '\n'.join([str(component) for component in self._components]) + \
        return '\ntotal cost = {}, total power output = {}, total power collected = {}' \
                   .format(self._cost_total, self._total_power_output, self._total_power_collected)


class BuildOptimizer:
    @staticmethod
    def get_highest_power_buildinstance(current_state):
        all_possible_component_types = \
            [Windmill.create(windmill_type) for windmill_type in Windmill.AllTypes
             if Windmill.create(windmill_type).cost_per_lifecycle <= current_state.cash] + \
            [PowerCollector.create(powercollector_type) for powercollector_type in PowerCollector.AllTypes
             if PowerCollector.create(powercollector_type).one_time_cost <= current_state.cash] + \
            [ResearchCenter.create(researchCenter_type) for researchCenter_type in ResearchCenter.AllTypes
             if ResearchCenter.create(researchCenter_type).one_time_cost <= current_state.cash]

        print(current_state)

        build_instances = [BuildInstance(*components) for components in
                           combinations_with_replacement(all_possible_component_types, current_state.total_squares)]

        print('all possible component combinations = ' + str(len(build_instances)))

        build_instances = [buildInstance for buildInstance in build_instances
                           if buildInstance.is_self_collecting() and
                           buildInstance.costs_less_or_equal(current_state.cash)]

        print('viable build instances = ' + str(len(build_instances)))

        build_instances = sorted(sorted(build_instances, key=BuildOptimizer.total_cost),
                                 key=BuildOptimizer.total_power_produced, reverse=True)

        return build_instances[0]

    @staticmethod
    def total_power_produced(build_instance):
        return build_instance.get_total_power_produced()

    @staticmethod
    def total_cost(build_instance):
        return build_instance.get_total_cost()


currentState = CurrentState(cash=1000, total_squares=10, components=None)
optimalBuild = BuildOptimizer.get_highest_power_buildinstance(currentState)
print(optimalBuild)
