from abc import ABC, abstractmethod
from queue import SimpleQueue
import math


class Module(ABC):
    def __init__(self, name, targets):
        self.name = name
        self.targets = targets.split(", ")

    @abstractmethod
    def process_pulse(self, source: str, pulse: bool) -> dict:
        pass

    @staticmethod
    def parse_module(value):
        module_type, target = value.split(" -> ")
        if module_type == "broadcaster":
            return BroadCaster(target)
        elif module_type[0] == "%":
            return FlipFlop(module_type[1:], target)
        elif module_type[0] == "&":
            return Conjunction(module_type[1:], target)
        else:
            raise ValueError("Unexpected!")


class BroadCaster(Module):
    def __init__(self, targets):
        super().__init__(self.__class__.__name__.lower(), targets)

    def process_pulse(self, source: str, pulse: bool) -> dict:
        return {t: pulse for t in self.targets}


class FlipFlop(Module):
    def __init__(self, name, targets):
        super().__init__(name, targets)
        self.state = False  # off

    def process_pulse(self, source: str, pulse: bool) -> dict:
        # High incoming value leads to empty output
        if pulse:
            return {}

        self.state = not self.state
        return {t: self.state for t in self.targets}


class Conjunction(Module):
    def __init__(self, name, targets):
        super().__init__(name, targets)
        self.input_states: dict = None

    def ensure_configured(self):
        if self.input_states is None:
            raise ValueError("Conjunction inputs not configured!")

    def unambiguous_state(self):
        self.ensure_configured()
        inp_states = set(self.input_states.values())
        if len(inp_states) == 1:
            return next(iter(inp_states))
        return None

    def set_feeding_inputs(self, inputs):
        self.input_states = {i: False for i in inputs}

    def process_pulse(self, source: str, pulse: bool) -> dict:
        self.ensure_configured()
        self.input_states[source] = pulse

        if self.unambiguous_state():
            output_value = False
        else:
            output_value = True

        return {t: output_value for t in self.targets}


def main():
    with open("input.txt", "r") as f:
        contents = f.read()

    example_input = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""

    example_input2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""

    # contents = example_input2
    lines = contents.splitlines()
    modules = [Module.parse_module(m) for m in lines]
    modules = {m.name: m for m in modules}

    # Configure conjunctions
    conjs = [m for m in modules.values() if isinstance(m, Conjunction)]
    for conj in conjs:
        cn = conj.name
        inputs = [k for k, v in modules.items() if cn in v.targets]
        conj.set_feeding_inputs(inputs)

    cnt_high_pulses = 0
    cnt_low_pulses = 0
    pulse_queue = SimpleQueue()

    part2_rx_input = "vr"
    rx_input_module = modules[part2_rx_input]
    rx_input_inputs = rx_input_module.input_states.keys()
    rx_input_first_high = {i: None for i in rx_input_inputs}

    for cycle in range(100000):
        pulse_queue.put(("button", False, "broadcaster"))
        while not pulse_queue.empty():
            src_module, pulse, tgt_module = pulse_queue.get()
            if pulse:
                cnt_high_pulses += 1
            else:
                cnt_low_pulses += 1

            if tgt_module == "vr" and pulse and rx_input_first_high[src_module] is None:
                rx_input_first_high[src_module] = cycle+1
                if all([v is not None for v in rx_input_first_high.values()]):
                    break

            m = modules.get(tgt_module, None)
            if not m:
                continue

            new_pulses = m.process_pulse(src_module, pulse)
            for new_target, pulse in new_pulses.items():
                pulse_queue.put((tgt_module, pulse, new_target))

        if cycle == 1000-1:
            print(cnt_low_pulses*cnt_high_pulses)

    print(math.lcm(*rx_input_first_high.values()))


if __name__ == "__main__":
    main()
