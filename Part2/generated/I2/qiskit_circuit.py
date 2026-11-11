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

def _function_gate_oracle_4619890720(num_qubits):
    """Custom gate: oracle"""
    qc_func = QuantumCircuit(num_qubits, name='oracle')
    qc_func.append(XGate().control(5, ctrl_state='11101'), [0, 1, 7, 8, 9, 10])
    qc_func.append(XGate().control(4, ctrl_state='1101'), [0, 1, 7, 8, 9])
    qc_func.append(XGate().control(3, ctrl_state='101'), [0, 1, 7, 8])
    qc_func.append(XGate().control(2, ctrl_state='01'), [0, 1, 7])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [0, 1, 7, 8, 9, 10])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [0, 1, 7, 8, 9])
    qc_func.append(XGate().control(3, ctrl_state='110'), [0, 1, 7, 8])
    qc_func.append(XGate().control(2, ctrl_state='10'), [0, 1, 7])
    qc_func.append(XGate().control(6, ctrl_state='111001'), [1, 2, 3, 7, 8, 9, 10])
    qc_func.append(XGate().control(5, ctrl_state='11001'), [1, 2, 3, 7, 8, 9])
    qc_func.append(XGate().control(4, ctrl_state='1001'), [1, 2, 3, 7, 8])
    qc_func.append(XGate().control(3, ctrl_state='001'), [1, 2, 3, 7])
    qc_func.append(XGate().control(5, ctrl_state='11111'), [2, 3, 7, 8, 9, 10])
    qc_func.append(XGate().control(4, ctrl_state='1111'), [2, 3, 7, 8, 9])
    qc_func.append(XGate().control(3, ctrl_state='111'), [2, 3, 7, 8])
    qc_func.append(XGate().control(2, ctrl_state='11'), [2, 3, 7])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [1, 2, 7, 8, 9, 10])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [1, 2, 7, 8, 9])
    qc_func.append(XGate().control(3, ctrl_state='110'), [1, 2, 7, 8])
    qc_func.append(XGate().control(2, ctrl_state='10'), [1, 2, 7])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [1, 3, 7, 8, 9, 10])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [1, 3, 7, 8, 9])
    qc_func.append(XGate().control(3, ctrl_state='110'), [1, 3, 7, 8])
    qc_func.append(XGate().control(2, ctrl_state='10'), [1, 3, 7])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [0, 4, 7, 8, 9, 10])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [0, 4, 7, 8, 9])
    qc_func.append(XGate().control(3, ctrl_state='110'), [0, 4, 7, 8])
    qc_func.append(XGate().control(2, ctrl_state='10'), [0, 4, 7])
    qc_func.append(XGate().control(6, ctrl_state='111001'), [4, 5, 6, 7, 8, 9, 10])
    qc_func.append(XGate().control(5, ctrl_state='11001'), [4, 5, 6, 7, 8, 9])
    qc_func.append(XGate().control(4, ctrl_state='1001'), [4, 5, 6, 7, 8])
    qc_func.append(XGate().control(3, ctrl_state='001'), [4, 5, 6, 7])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [4, 5, 7, 8, 9, 10])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [4, 5, 7, 8, 9])
    qc_func.append(XGate().control(3, ctrl_state='110'), [4, 5, 7, 8])
    qc_func.append(XGate().control(2, ctrl_state='10'), [4, 5, 7])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [4, 6, 7, 8, 9, 10])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [4, 6, 7, 8, 9])
    qc_func.append(XGate().control(3, ctrl_state='110'), [4, 6, 7, 8])
    qc_func.append(XGate().control(2, ctrl_state='10'), [4, 6, 7])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [3, 5, 7, 8, 9, 10])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [3, 5, 7, 8, 9])
    qc_func.append(XGate().control(3, ctrl_state='110'), [3, 5, 7, 8])
    qc_func.append(XGate().control(2, ctrl_state='10'), [3, 5, 7])
    qc_func.append(XGate().control(5, ctrl_state='11111'), [2, 6, 7, 8, 9, 10])
    qc_func.append(XGate().control(4, ctrl_state='1111'), [2, 6, 7, 8, 9])
    qc_func.append(XGate().control(3, ctrl_state='111'), [2, 6, 7, 8])
    qc_func.append(XGate().control(2, ctrl_state='11'), [2, 6, 7])
    qc_func.append(XGate().control(7, ctrl_state='0000011'), [0, 5, 6, 7, 8, 9, 10, 11])
    qc_func.append(XGate().control(2, ctrl_state='11'), [2, 6, 7])
    qc_func.append(XGate().control(3, ctrl_state='111'), [2, 6, 7, 8])
    qc_func.append(XGate().control(4, ctrl_state='1111'), [2, 6, 7, 8, 9])
    qc_func.append(XGate().control(5, ctrl_state='11111'), [2, 6, 7, 8, 9, 10])
    qc_func.append(XGate().control(2, ctrl_state='10'), [3, 5, 7])
    qc_func.append(XGate().control(3, ctrl_state='110'), [3, 5, 7, 8])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [3, 5, 7, 8, 9])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [3, 5, 7, 8, 9, 10])
    qc_func.append(XGate().control(2, ctrl_state='10'), [4, 6, 7])
    qc_func.append(XGate().control(3, ctrl_state='110'), [4, 6, 7, 8])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [4, 6, 7, 8, 9])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [4, 6, 7, 8, 9, 10])
    qc_func.append(XGate().control(2, ctrl_state='10'), [4, 5, 7])
    qc_func.append(XGate().control(3, ctrl_state='110'), [4, 5, 7, 8])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [4, 5, 7, 8, 9])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [4, 5, 7, 8, 9, 10])
    qc_func.append(XGate().control(3, ctrl_state='001'), [4, 5, 6, 7])
    qc_func.append(XGate().control(4, ctrl_state='1001'), [4, 5, 6, 7, 8])
    qc_func.append(XGate().control(5, ctrl_state='11001'), [4, 5, 6, 7, 8, 9])
    qc_func.append(XGate().control(6, ctrl_state='111001'), [4, 5, 6, 7, 8, 9, 10])
    qc_func.append(XGate().control(2, ctrl_state='10'), [0, 4, 7])
    qc_func.append(XGate().control(3, ctrl_state='110'), [0, 4, 7, 8])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [0, 4, 7, 8, 9])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [0, 4, 7, 8, 9, 10])
    qc_func.append(XGate().control(2, ctrl_state='10'), [1, 3, 7])
    qc_func.append(XGate().control(3, ctrl_state='110'), [1, 3, 7, 8])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [1, 3, 7, 8, 9])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [1, 3, 7, 8, 9, 10])
    qc_func.append(XGate().control(2, ctrl_state='10'), [1, 2, 7])
    qc_func.append(XGate().control(3, ctrl_state='110'), [1, 2, 7, 8])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [1, 2, 7, 8, 9])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [1, 2, 7, 8, 9, 10])
    qc_func.append(XGate().control(2, ctrl_state='11'), [2, 3, 7])
    qc_func.append(XGate().control(3, ctrl_state='111'), [2, 3, 7, 8])
    qc_func.append(XGate().control(4, ctrl_state='1111'), [2, 3, 7, 8, 9])
    qc_func.append(XGate().control(5, ctrl_state='11111'), [2, 3, 7, 8, 9, 10])
    qc_func.append(XGate().control(3, ctrl_state='001'), [1, 2, 3, 7])
    qc_func.append(XGate().control(4, ctrl_state='1001'), [1, 2, 3, 7, 8])
    qc_func.append(XGate().control(5, ctrl_state='11001'), [1, 2, 3, 7, 8, 9])
    qc_func.append(XGate().control(6, ctrl_state='111001'), [1, 2, 3, 7, 8, 9, 10])
    qc_func.append(XGate().control(2, ctrl_state='10'), [0, 1, 7])
    qc_func.append(XGate().control(3, ctrl_state='110'), [0, 1, 7, 8])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [0, 1, 7, 8, 9])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [0, 1, 7, 8, 9, 10])
    qc_func.append(XGate().control(2, ctrl_state='01'), [0, 1, 7])
    qc_func.append(XGate().control(3, ctrl_state='101'), [0, 1, 7, 8])
    qc_func.append(XGate().control(4, ctrl_state='1101'), [0, 1, 7, 8, 9])
    qc_func.append(XGate().control(5, ctrl_state='11101'), [0, 1, 7, 8, 9, 10])
    return qc_func.to_instruction()


def _function_gate_diffuser_4623437504(num_qubits):
    """Custom gate: diffuser"""
    qc_func = QuantumCircuit(num_qubits, name='diffuser')
    qc_func.h(0)
    qc_func.h(1)
    qc_func.h(2)
    qc_func.h(3)
    qc_func.h(4)
    qc_func.h(5)
    qc_func.h(6)
    qc_func.append(XGate().control(7, ctrl_state='0000000'), [0, 1, 2, 3, 4, 5, 6, 11])
    qc_func.h(0)
    qc_func.h(1)
    qc_func.h(2)
    qc_func.h(3)
    qc_func.h(4)
    qc_func.h(5)
    qc_func.h(6)
    return qc_func.to_instruction()




# Initialize Registers

q = QuantumRegister(12, 'q')


c = ClassicalRegister(7, 'c')


# Initialize Circuit
qc = QuantumCircuit(q, c)

# Operations

qc.append(HGate(), [q[0]])

qc.append(HGate(), [q[1]])

qc.append(HGate(), [q[2]])

qc.append(HGate(), [q[3]])

qc.append(HGate(), [q[4]])

qc.append(HGate(), [q[5]])

qc.append(HGate(), [q[6]])

qc.append(XGate(), [q[11]])

qc.append(HGate(), [q[11]])

qc.append(_function_gate_oracle_4619890720(12), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11]])

qc.append(_function_gate_diffuser_4623437504(12), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11]])

qc.append(_function_gate_oracle_4619890720(12), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11]])

qc.append(_function_gate_diffuser_4623437504(12), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11]])

qc.append(_function_gate_oracle_4619890720(12), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11]])

qc.append(_function_gate_diffuser_4623437504(12), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11]])

qc.append(_function_gate_oracle_4619890720(12), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11]])

qc.append(_function_gate_diffuser_4623437504(12), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11]])

qc.append(_function_gate_oracle_4619890720(12), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11]])

qc.append(_function_gate_diffuser_4623437504(12), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11]])

qc.append(_function_gate_oracle_4619890720(12), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11]])

qc.append(_function_gate_diffuser_4623437504(12), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11]])

qc.append(_function_gate_oracle_4619890720(12), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11]])

qc.append(_function_gate_diffuser_4623437504(12), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11]])

qc.append(_function_gate_oracle_4619890720(12), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11]])

qc.append(_function_gate_diffuser_4623437504(12), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11]])

qc.measure(q[0], c[0])

qc.measure(q[1], c[1])

qc.measure(q[2], c[2])

qc.measure(q[3], c[3])

qc.measure(q[4], c[4])

qc.measure(q[5], c[5])

qc.measure(q[6], c[6])


# Draw
print(qc.draw())


# Execution (Local Aer Simulator)
print("Simulating circuit with Aer Simulator...")
simulator = AerSimulator()
transpiled_qc = transpile(qc, simulator)
result = simulator.run(transpiled_qc, shots=1024).result()
counts = result.get_counts()
print("Counts:", counts)
