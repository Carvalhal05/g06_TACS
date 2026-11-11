import sys
import os
sys.path = [p.strip() for p in sys.path if p]
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit import Instruction

from qiskit_aer import AerSimulator

from qiskit.circuit.library import *
from qiskit.circuit.library.standard_gates import GlobalPhaseGate
import numpy as np










# Function Gate Definitions

def _function_gate_oracle_2170691823392(num_qubits):
    """Custom gate: oracle"""
    qc_func = QuantumCircuit(num_qubits, name='oracle')
    qc_func.append(XGate().control(4, ctrl_state='1101'), [0, 1, 4, 5, 6])
    qc_func.append(XGate().control(3, ctrl_state='101'), [0, 1, 4, 5])
    qc_func.append(XGate().control(2, ctrl_state='01'), [0, 1, 4])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [0, 1, 4, 5, 6])
    qc_func.append(XGate().control(3, ctrl_state='110'), [0, 1, 4, 5])
    qc_func.append(XGate().control(2, ctrl_state='10'), [0, 1, 4])
    qc_func.append(XGate().control(5, ctrl_state='11001'), [1, 2, 3, 4, 5, 6])
    qc_func.append(XGate().control(4, ctrl_state='1001'), [1, 2, 3, 4, 5])
    qc_func.append(XGate().control(3, ctrl_state='001'), [1, 2, 3, 4])
    qc_func.append(XGate().control(4, ctrl_state='1111'), [2, 3, 4, 5, 6])
    qc_func.append(XGate().control(3, ctrl_state='111'), [2, 3, 4, 5])
    qc_func.append(XGate().control(2, ctrl_state='11'), [2, 3, 4])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [1, 2, 4, 5, 6])
    qc_func.append(XGate().control(3, ctrl_state='110'), [1, 2, 4, 5])
    qc_func.append(XGate().control(2, ctrl_state='10'), [1, 2, 4])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [1, 3, 4, 5, 6])
    qc_func.append(XGate().control(3, ctrl_state='110'), [1, 3, 4, 5])
    qc_func.append(XGate().control(2, ctrl_state='10'), [1, 3, 4])
    qc_func.append(XGate().control(5, ctrl_state='00011'), [0, 3, 4, 5, 6, 7])
    qc_func.append(XGate().control(2, ctrl_state='10'), [1, 3, 4])
    qc_func.append(XGate().control(3, ctrl_state='110'), [1, 3, 4, 5])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [1, 3, 4, 5, 6])
    qc_func.append(XGate().control(2, ctrl_state='10'), [1, 2, 4])
    qc_func.append(XGate().control(3, ctrl_state='110'), [1, 2, 4, 5])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [1, 2, 4, 5, 6])
    qc_func.append(XGate().control(2, ctrl_state='11'), [2, 3, 4])
    qc_func.append(XGate().control(3, ctrl_state='111'), [2, 3, 4, 5])
    qc_func.append(XGate().control(4, ctrl_state='1111'), [2, 3, 4, 5, 6])
    qc_func.append(XGate().control(3, ctrl_state='001'), [1, 2, 3, 4])
    qc_func.append(XGate().control(4, ctrl_state='1001'), [1, 2, 3, 4, 5])
    qc_func.append(XGate().control(5, ctrl_state='11001'), [1, 2, 3, 4, 5, 6])
    qc_func.append(XGate().control(2, ctrl_state='10'), [0, 1, 4])
    qc_func.append(XGate().control(3, ctrl_state='110'), [0, 1, 4, 5])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [0, 1, 4, 5, 6])
    qc_func.append(XGate().control(2, ctrl_state='01'), [0, 1, 4])
    qc_func.append(XGate().control(3, ctrl_state='101'), [0, 1, 4, 5])
    qc_func.append(XGate().control(4, ctrl_state='1101'), [0, 1, 4, 5, 6])
    return qc_func.to_instruction()


def _function_gate_diffuser_2170691827376(num_qubits):
    """Custom gate: diffuser"""
    qc_func = QuantumCircuit(num_qubits, name='diffuser')
    qc_func.h(0)
    qc_func.h(1)
    qc_func.h(2)
    qc_func.h(3)
    qc_func.append(XGate().control(4, ctrl_state='0000'), [0, 1, 2, 3, 7])
    qc_func.h(0)
    qc_func.h(1)
    qc_func.h(2)
    qc_func.h(3)
    return qc_func.to_instruction()




# Initialize Registers

q = QuantumRegister(8, 'q')


c = ClassicalRegister(4, 'c')


# Initialize Circuit
qc = QuantumCircuit(q, c)

# Operations

qc.append(HGate(), [q[0]])

qc.append(HGate(), [q[1]])

qc.append(HGate(), [q[2]])

qc.append(HGate(), [q[3]])

qc.append(XGate(), [q[7]])

qc.append(HGate(), [q[7]])

qc.append(_function_gate_oracle_2170691823392(8), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7]])

qc.append(_function_gate_diffuser_2170691827376(8), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7]])

qc.append(_function_gate_oracle_2170691823392(8), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7]])

qc.append(_function_gate_diffuser_2170691827376(8), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7]])

qc.append(_function_gate_oracle_2170691823392(8), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7]])

qc.append(_function_gate_diffuser_2170691827376(8), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7]])

qc.measure(q[0], c[0])

qc.measure(q[1], c[1])

qc.measure(q[2], c[2])

qc.measure(q[3], c[3])


# Draw
print(qc.draw())


# Execution (Local Aer Simulator)
print("Simulating circuit with Aer Simulator...")
simulator = AerSimulator()
transpiled_qc = transpile(qc, simulator)
result = simulator.run(transpiled_qc, shots=1024).result()
counts = result.get_counts()
print("Counts:", counts)
