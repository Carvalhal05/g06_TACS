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

def _function_gate_oracle_4632538544(num_qubits):
    """Custom gate: oracle"""
    qc_func = QuantumCircuit(num_qubits, name='oracle')
    qc_func.append(XGate().control(6, ctrl_state='111101'), [0, 1, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(5, ctrl_state='11101'), [0, 1, 11, 12, 13, 14])
    qc_func.append(XGate().control(4, ctrl_state='1101'), [0, 1, 11, 12, 13])
    qc_func.append(XGate().control(3, ctrl_state='101'), [0, 1, 11, 12])
    qc_func.append(XGate().control(2, ctrl_state='01'), [0, 1, 11])
    qc_func.append(XGate().control(6, ctrl_state='111110'), [0, 1, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [0, 1, 11, 12, 13, 14])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [0, 1, 11, 12, 13])
    qc_func.append(XGate().control(3, ctrl_state='110'), [0, 1, 11, 12])
    qc_func.append(XGate().control(2, ctrl_state='10'), [0, 1, 11])
    qc_func.append(XGate().control(7, ctrl_state='1111001'), [1, 2, 3, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(6, ctrl_state='111001'), [1, 2, 3, 11, 12, 13, 14])
    qc_func.append(XGate().control(5, ctrl_state='11001'), [1, 2, 3, 11, 12, 13])
    qc_func.append(XGate().control(4, ctrl_state='1001'), [1, 2, 3, 11, 12])
    qc_func.append(XGate().control(3, ctrl_state='001'), [1, 2, 3, 11])
    qc_func.append(XGate().control(6, ctrl_state='111111'), [2, 3, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(5, ctrl_state='11111'), [2, 3, 11, 12, 13, 14])
    qc_func.append(XGate().control(4, ctrl_state='1111'), [2, 3, 11, 12, 13])
    qc_func.append(XGate().control(3, ctrl_state='111'), [2, 3, 11, 12])
    qc_func.append(XGate().control(2, ctrl_state='11'), [2, 3, 11])
    qc_func.append(XGate().control(6, ctrl_state='111110'), [1, 2, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [1, 2, 11, 12, 13, 14])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [1, 2, 11, 12, 13])
    qc_func.append(XGate().control(3, ctrl_state='110'), [1, 2, 11, 12])
    qc_func.append(XGate().control(2, ctrl_state='10'), [1, 2, 11])
    qc_func.append(XGate().control(6, ctrl_state='111110'), [1, 3, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [1, 3, 11, 12, 13, 14])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [1, 3, 11, 12, 13])
    qc_func.append(XGate().control(3, ctrl_state='110'), [1, 3, 11, 12])
    qc_func.append(XGate().control(2, ctrl_state='10'), [1, 3, 11])
    qc_func.append(XGate().control(6, ctrl_state='111101'), [3, 4, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(5, ctrl_state='11101'), [3, 4, 11, 12, 13, 14])
    qc_func.append(XGate().control(4, ctrl_state='1101'), [3, 4, 11, 12, 13])
    qc_func.append(XGate().control(3, ctrl_state='101'), [3, 4, 11, 12])
    qc_func.append(XGate().control(2, ctrl_state='01'), [3, 4, 11])
    qc_func.append(XGate().control(6, ctrl_state='111110'), [3, 4, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [3, 4, 11, 12, 13, 14])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [3, 4, 11, 12, 13])
    qc_func.append(XGate().control(3, ctrl_state='110'), [3, 4, 11, 12])
    qc_func.append(XGate().control(2, ctrl_state='10'), [3, 4, 11])
    qc_func.append(XGate().control(6, ctrl_state='111110'), [3, 5, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [3, 5, 11, 12, 13, 14])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [3, 5, 11, 12, 13])
    qc_func.append(XGate().control(3, ctrl_state='110'), [3, 5, 11, 12])
    qc_func.append(XGate().control(2, ctrl_state='10'), [3, 5, 11])
    qc_func.append(XGate().control(6, ctrl_state='111110'), [3, 6, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [3, 6, 11, 12, 13, 14])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [3, 6, 11, 12, 13])
    qc_func.append(XGate().control(3, ctrl_state='110'), [3, 6, 11, 12])
    qc_func.append(XGate().control(2, ctrl_state='10'), [3, 6, 11])
    qc_func.append(XGate().control(6, ctrl_state='111110'), [3, 7, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [3, 7, 11, 12, 13, 14])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [3, 7, 11, 12, 13])
    qc_func.append(XGate().control(3, ctrl_state='110'), [3, 7, 11, 12])
    qc_func.append(XGate().control(2, ctrl_state='10'), [3, 7, 11])
    qc_func.append(XGate().control(6, ctrl_state='111110'), [0, 8, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [0, 8, 11, 12, 13, 14])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [0, 8, 11, 12, 13])
    qc_func.append(XGate().control(3, ctrl_state='110'), [0, 8, 11, 12])
    qc_func.append(XGate().control(2, ctrl_state='10'), [0, 8, 11])
    qc_func.append(XGate().control(7, ctrl_state='1111001'), [8, 9, 10, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(6, ctrl_state='111001'), [8, 9, 10, 11, 12, 13, 14])
    qc_func.append(XGate().control(5, ctrl_state='11001'), [8, 9, 10, 11, 12, 13])
    qc_func.append(XGate().control(4, ctrl_state='1001'), [8, 9, 10, 11, 12])
    qc_func.append(XGate().control(3, ctrl_state='001'), [8, 9, 10, 11])
    qc_func.append(XGate().control(6, ctrl_state='111110'), [8, 9, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [8, 9, 11, 12, 13, 14])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [8, 9, 11, 12, 13])
    qc_func.append(XGate().control(3, ctrl_state='110'), [8, 9, 11, 12])
    qc_func.append(XGate().control(2, ctrl_state='10'), [8, 9, 11])
    qc_func.append(XGate().control(6, ctrl_state='111110'), [8, 10, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [8, 10, 11, 12, 13, 14])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [8, 10, 11, 12, 13])
    qc_func.append(XGate().control(3, ctrl_state='110'), [8, 10, 11, 12])
    qc_func.append(XGate().control(2, ctrl_state='10'), [8, 10, 11])
    qc_func.append(XGate().control(6, ctrl_state='111110'), [3, 9, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [3, 9, 11, 12, 13, 14])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [3, 9, 11, 12, 13])
    qc_func.append(XGate().control(3, ctrl_state='110'), [3, 9, 11, 12])
    qc_func.append(XGate().control(2, ctrl_state='10'), [3, 9, 11])
    qc_func.append(XGate().control(6, ctrl_state='111111'), [2, 10, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(5, ctrl_state='11111'), [2, 10, 11, 12, 13, 14])
    qc_func.append(XGate().control(4, ctrl_state='1111'), [2, 10, 11, 12, 13])
    qc_func.append(XGate().control(3, ctrl_state='111'), [2, 10, 11, 12])
    qc_func.append(XGate().control(2, ctrl_state='11'), [2, 10, 11])
    qc_func.append(XGate().control(11, ctrl_state='00000011111'), [0, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16])
    qc_func.append(XGate().control(2, ctrl_state='11'), [2, 10, 11])
    qc_func.append(XGate().control(3, ctrl_state='111'), [2, 10, 11, 12])
    qc_func.append(XGate().control(4, ctrl_state='1111'), [2, 10, 11, 12, 13])
    qc_func.append(XGate().control(5, ctrl_state='11111'), [2, 10, 11, 12, 13, 14])
    qc_func.append(XGate().control(6, ctrl_state='111111'), [2, 10, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(2, ctrl_state='10'), [3, 9, 11])
    qc_func.append(XGate().control(3, ctrl_state='110'), [3, 9, 11, 12])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [3, 9, 11, 12, 13])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [3, 9, 11, 12, 13, 14])
    qc_func.append(XGate().control(6, ctrl_state='111110'), [3, 9, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(2, ctrl_state='10'), [8, 10, 11])
    qc_func.append(XGate().control(3, ctrl_state='110'), [8, 10, 11, 12])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [8, 10, 11, 12, 13])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [8, 10, 11, 12, 13, 14])
    qc_func.append(XGate().control(6, ctrl_state='111110'), [8, 10, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(2, ctrl_state='10'), [8, 9, 11])
    qc_func.append(XGate().control(3, ctrl_state='110'), [8, 9, 11, 12])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [8, 9, 11, 12, 13])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [8, 9, 11, 12, 13, 14])
    qc_func.append(XGate().control(6, ctrl_state='111110'), [8, 9, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(3, ctrl_state='001'), [8, 9, 10, 11])
    qc_func.append(XGate().control(4, ctrl_state='1001'), [8, 9, 10, 11, 12])
    qc_func.append(XGate().control(5, ctrl_state='11001'), [8, 9, 10, 11, 12, 13])
    qc_func.append(XGate().control(6, ctrl_state='111001'), [8, 9, 10, 11, 12, 13, 14])
    qc_func.append(XGate().control(7, ctrl_state='1111001'), [8, 9, 10, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(2, ctrl_state='10'), [0, 8, 11])
    qc_func.append(XGate().control(3, ctrl_state='110'), [0, 8, 11, 12])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [0, 8, 11, 12, 13])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [0, 8, 11, 12, 13, 14])
    qc_func.append(XGate().control(6, ctrl_state='111110'), [0, 8, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(2, ctrl_state='10'), [3, 7, 11])
    qc_func.append(XGate().control(3, ctrl_state='110'), [3, 7, 11, 12])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [3, 7, 11, 12, 13])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [3, 7, 11, 12, 13, 14])
    qc_func.append(XGate().control(6, ctrl_state='111110'), [3, 7, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(2, ctrl_state='10'), [3, 6, 11])
    qc_func.append(XGate().control(3, ctrl_state='110'), [3, 6, 11, 12])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [3, 6, 11, 12, 13])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [3, 6, 11, 12, 13, 14])
    qc_func.append(XGate().control(6, ctrl_state='111110'), [3, 6, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(2, ctrl_state='10'), [3, 5, 11])
    qc_func.append(XGate().control(3, ctrl_state='110'), [3, 5, 11, 12])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [3, 5, 11, 12, 13])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [3, 5, 11, 12, 13, 14])
    qc_func.append(XGate().control(6, ctrl_state='111110'), [3, 5, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(2, ctrl_state='10'), [3, 4, 11])
    qc_func.append(XGate().control(3, ctrl_state='110'), [3, 4, 11, 12])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [3, 4, 11, 12, 13])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [3, 4, 11, 12, 13, 14])
    qc_func.append(XGate().control(6, ctrl_state='111110'), [3, 4, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(2, ctrl_state='01'), [3, 4, 11])
    qc_func.append(XGate().control(3, ctrl_state='101'), [3, 4, 11, 12])
    qc_func.append(XGate().control(4, ctrl_state='1101'), [3, 4, 11, 12, 13])
    qc_func.append(XGate().control(5, ctrl_state='11101'), [3, 4, 11, 12, 13, 14])
    qc_func.append(XGate().control(6, ctrl_state='111101'), [3, 4, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(2, ctrl_state='10'), [1, 3, 11])
    qc_func.append(XGate().control(3, ctrl_state='110'), [1, 3, 11, 12])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [1, 3, 11, 12, 13])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [1, 3, 11, 12, 13, 14])
    qc_func.append(XGate().control(6, ctrl_state='111110'), [1, 3, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(2, ctrl_state='10'), [1, 2, 11])
    qc_func.append(XGate().control(3, ctrl_state='110'), [1, 2, 11, 12])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [1, 2, 11, 12, 13])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [1, 2, 11, 12, 13, 14])
    qc_func.append(XGate().control(6, ctrl_state='111110'), [1, 2, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(2, ctrl_state='11'), [2, 3, 11])
    qc_func.append(XGate().control(3, ctrl_state='111'), [2, 3, 11, 12])
    qc_func.append(XGate().control(4, ctrl_state='1111'), [2, 3, 11, 12, 13])
    qc_func.append(XGate().control(5, ctrl_state='11111'), [2, 3, 11, 12, 13, 14])
    qc_func.append(XGate().control(6, ctrl_state='111111'), [2, 3, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(3, ctrl_state='001'), [1, 2, 3, 11])
    qc_func.append(XGate().control(4, ctrl_state='1001'), [1, 2, 3, 11, 12])
    qc_func.append(XGate().control(5, ctrl_state='11001'), [1, 2, 3, 11, 12, 13])
    qc_func.append(XGate().control(6, ctrl_state='111001'), [1, 2, 3, 11, 12, 13, 14])
    qc_func.append(XGate().control(7, ctrl_state='1111001'), [1, 2, 3, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(2, ctrl_state='10'), [0, 1, 11])
    qc_func.append(XGate().control(3, ctrl_state='110'), [0, 1, 11, 12])
    qc_func.append(XGate().control(4, ctrl_state='1110'), [0, 1, 11, 12, 13])
    qc_func.append(XGate().control(5, ctrl_state='11110'), [0, 1, 11, 12, 13, 14])
    qc_func.append(XGate().control(6, ctrl_state='111110'), [0, 1, 11, 12, 13, 14, 15])
    qc_func.append(XGate().control(2, ctrl_state='01'), [0, 1, 11])
    qc_func.append(XGate().control(3, ctrl_state='101'), [0, 1, 11, 12])
    qc_func.append(XGate().control(4, ctrl_state='1101'), [0, 1, 11, 12, 13])
    qc_func.append(XGate().control(5, ctrl_state='11101'), [0, 1, 11, 12, 13, 14])
    qc_func.append(XGate().control(6, ctrl_state='111101'), [0, 1, 11, 12, 13, 14, 15])
    return qc_func.to_instruction()


def _function_gate_diffuser_4632667648(num_qubits):
    """Custom gate: diffuser"""
    qc_func = QuantumCircuit(num_qubits, name='diffuser')
    qc_func.h(0)
    qc_func.h(1)
    qc_func.h(2)
    qc_func.h(3)
    qc_func.h(4)
    qc_func.h(5)
    qc_func.h(6)
    qc_func.h(7)
    qc_func.h(8)
    qc_func.h(9)
    qc_func.h(10)
    qc_func.append(XGate().control(11, ctrl_state='00000000000'), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 16])
    qc_func.h(0)
    qc_func.h(1)
    qc_func.h(2)
    qc_func.h(3)
    qc_func.h(4)
    qc_func.h(5)
    qc_func.h(6)
    qc_func.h(7)
    qc_func.h(8)
    qc_func.h(9)
    qc_func.h(10)
    return qc_func.to_instruction()




# Initialize Registers

q = QuantumRegister(17, 'q')


c = ClassicalRegister(11, 'c')


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

qc.append(HGate(), [q[7]])

qc.append(HGate(), [q[8]])

qc.append(HGate(), [q[9]])

qc.append(HGate(), [q[10]])

qc.append(XGate(), [q[16]])

qc.append(HGate(), [q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_oracle_4632538544(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.append(_function_gate_diffuser_4632667648(17), [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16]])

qc.measure(q[0], c[0])

qc.measure(q[1], c[1])

qc.measure(q[2], c[2])

qc.measure(q[3], c[3])

qc.measure(q[4], c[4])

qc.measure(q[5], c[5])

qc.measure(q[6], c[6])

qc.measure(q[7], c[7])

qc.measure(q[8], c[8])

qc.measure(q[9], c[9])

qc.measure(q[10], c[10])


# Draw
print(qc.draw())


# Execution (Local Aer Simulator)
print("Simulating circuit with Aer Simulator...")
simulator = AerSimulator()
transpiled_qc = transpile(qc, simulator)
result = simulator.run(transpiled_qc, shots=1024).result()
counts = result.get_counts()
print("Counts:", counts)
