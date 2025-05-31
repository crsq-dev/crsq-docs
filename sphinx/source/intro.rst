Introduction
============

(Edit docx. this is secondary.)

Quantum chemistry simulation is one of the key applications that are expected to
leverage the full advantage of quantum computers above classical computers.  For
chemical problems that require an explicit representation of the wave function,
quantum computers will aid computations that are intractable with classical
computers.

A straight-forward approach of using quantum computers for quantum simulation is
to perform a Hamiltonian simulation and apply a measurement method, such as the
quantum phase estimation algorithm (QPEA), thus, obtaining values such as
eigen-energies and the eigen states of a system.  However, algorithms of this
category require a error-corrected quantum computer with substantial scale,
which is yet to be achieved.

At present, the quantum computers available are subject to noise, and algorithms
need to be designed to function within the noise level and decoherence time.  As
a result, the most successful current simulation algorithms are hybrid
algorithms, that offload computation to classical computers as much as possible,
thus minimizing the depth of the quantum circuit. These algorithms are based on
second quantization and the variational quantum eigensolver (VQE) algorithm.
This setup works remarkably well for computing the ground state energy of
several simple molecules.  However, it is impossible to compute time evolution
of the time dependent Schrödinger equation, as the straight-forward approach
aims to achieve.

A first quantization based simulator could achieve that, but it would require
quantum computation to continue without measurement for several orders of
magnitude longer than that of VQE based simulations and is far out of reach of
the capabilities of the quantum devices of today.  We must wait for the arrival
of fault-tolerant quantum computers, or FTQC, that will have overcome this noise
problem. Recent research have shown progress in the realization of FTQC, which
combines several redundant noisy qubits to construct one fault tolerant qubit.
If such scheme is successfully implemented, we may see early examples of FTQC
devices in a several years range.

In anticipation of such computers, the author has implemented a quantum
chemistry simulator of the straight-forward approach, a first quantization based
quantum simulator on Qiskit.  The algorithm we use is an improvement on Berry
:cite:p:`RefWorks:RefID:44-berry2018improved`.  Since the resulting simulator
circuit uses more than one hundred qubits and uses entanglement extensively, it
cannot be run on current NISQ devices, nor classical computer simulators.
Nevertheless, it is still possible to test sub-components of the circuits, and
we tested all sub-components that fit on software simulators. Through this
development we have established a scheme for organizing quantum circuit
generating code for complex algorithms, which mirrors the stack-based subroutine
call mechanism for classical computer algorithms. The overall simulator circuit
is not of great use at present, but it has become possible to count the concrete
number of circuit geometry such as qubit count and gate depth and compare the
numbers to those previously been predicted.
