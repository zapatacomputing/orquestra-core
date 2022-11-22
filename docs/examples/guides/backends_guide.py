# QuantumSimulator creation example
# Example of simulator with no arguments
from orquestra.integrations.cirq.simulator import CirqSimulator

simulator = CirqSimulator()

# Example QiskitSimulator options
from orquestra.integrations.qiskit.simulator import QiskitSimulator

simulator = QiskitSimulator("aer_simulator")
simulator = QiskitSimulator("aer_simulator_statevector")
# End QuantumSimulator creation example


# QuantumSimulator examples
import numpy as np
from orquestra.integrations.cirq.simulator import CirqSimulator
from orquestra.quantum.circuits import CNOT, Circuit, H, X
from orquestra.quantum.operators import PauliSum

initial_state = np.array([0, 1, 0, 0])
circuit = Circuit([H(0), X(1)])

simulator = CirqSimulator()

# wave function
wave_function = simulator.get_wavefunction(circuit, initial_state)

# expectation values

operator = PauliSum("Z0 + 2*Z1")

expectation_values = simulator.get_exact_expectation_values(circuit, operator)
# End QuantumSimulator examples

"""
# QuantumBackend creation example
from orquestra.integrations.qiskit.backend import QiskitBackend

backend = QiskitBackend(
    "ibmq_lima", api_token="LOOKMORTYITURNEDMYSELFINTOANAPITOKEN!I'MAPIRICK"
)
# End QuantumBackend creation example
"""

# QuantumBackend run and measure circuit
circuit = Circuit() + X(0) + X(1)
number_of_samples = 1024

measurements = simulator.run_circuit_and_measure(circuit, number_of_samples)
# End QuantumBackend run and measure circuit

# QuantumBackend run and measure circuitset
circuit1 = Circuit() + X(0) + X(1)
circuit2 = Circuit() + H(0) + CNOT(0, 1)
circuit3 = Circuit() + X(0) + H(0) + CNOT(0, 1)

circuit_set = [circuit1, circuit2, circuit3]
number_of_samples_set = [10, 90, 100]

measurements_set = simulator.run_circuitset_and_measure(
    circuit_set, number_of_samples_set
)
# End QuantumBackend run and measure circuitset


# Quantumbackend measurement distribution
measurement_distribution = simulator.get_measurement_outcome_distribution(
    circuit, n_samples=1000
)
# End Quantumbackend measurement distribution


# TrackingBackend creation example
from orquestra.quantum.backends import MeasurementTrackingBackend, SymbolicSimulator

backend = MeasurementTrackingBackend(SymbolicSimulator(), "tracker_example")
# End TrackingBackend creation example


from orquestra.integrations.cirq.conversions._circuit_conversions import (
    export_to_cirq,
    import_from_cirq,
)

# Importing and Exporting with different frameworks
from orquestra.integrations.forest.conversions import (
    export_to_pyquil,
    import_from_pyquil,
)
from orquestra.integrations.qiskit.conversions import (
    export_to_qiskit,
    import_from_qiskit,
)
from orquestra.integrations.qulacs.conversions import convert_to_qulacs

# end importing/exporting examples
# Inherit QuantumSimulator
from orquestra.quantum.api.backend import QuantumBackend
from orquestra.quantum.measurements import Measurements


class MyBackend(QuantumBackend):
    def __init__(self, simulator_name, noise_model):
        super().__init__()
        self.noise_model = noise_model
        self.simulator = simulator_name

    def run_circuit_and_measure(self, circuit, n_samples):
        my_circ = export_to_my_circ(circuit)  # function to translate circuits
        result = self.simulator.run(
            my_circ, n_samples
        )  # we assume here that your simulator uses the method .run to execute and measure. Also it takes circuit and shots as the only params
        samples = convert_the_results_to_samples(result)

        return Measurements(samples)


# End Inherit QuantumSimulator


def export_to_my_circ(circuit):
    # mock function to translate circuits
    return circuit


def convert_the_results_to_samples(result):
    # mock function to convert the results of your simulator to samples
    return result
