Qubit Arithmetics
=================

The time evolution algorithm requires certain arithmetic operations on numbers
represented as a set of qubit states.

These operations work on entangled states, thus performing arithmetic for
multiple values on one execution of the circuits.  The design of such circuits
are shown in :cite:p:`RefWorks:RefID:48-vedral1996quantum` .

Such circuits are provided here as reusable functions.  The functions come in
two forms, instruction emitting functions and gate creating functions, described
as follows:

- Instruction emitting functions

  These functions will emit instructions to a given QuantumCircuit. They are
  named such as ``signed_adder``. They use qiskit QuantumRegisters to group the
  bits for input value and return value, and this interface form is often easier
  to notice parameter mismatch mistakes compared to the Gate creating functions.

- Gate creating functions

  These functions will create a qiskit Gate that implements a specific
  arithmetic operation. They are given names such as ``signed_adder_gate``.
  Qiskit Gates are a feature rich construct, and they can have extra control
  bits attached, or converted to an inverse operation.  So sometimes you need to
  use Gates, but the input and output values are specified as a list of qubit
  objects, and you have to make sure that the bit count and order is correct.
  This makes it harder to use than the instruction emitting functions.

Either form of functions can be used on QuantumCircuits without relying on any
other features of crsq.

In the context of the time evolution calculation of the Schrödinger equation,
arithmetic operations are required for the computation of the potential term of
the Hamiltonian which computes the inverse of the distance between two coordinates.
This will require subtraction, multiplication, addition, square root and
division.  For a simplified one-dimensional model, the norm calculation can be
replaced with an absolute value function.  Based on these needs, the set of
operations we have implemented is the following:

- Adders

  - unsigned adder
  - signed adder
  - signed constant value adder (Adds a constant value to a register)

- Subtractors

  - unsigned subtractor
  - signed subtractor

- Multipliers

  - unsigned multiplier
  - signed multiplier

- Dividers

  - unsigned divider

- Single operand functions

  - signed square
  - square root
  - absolute value

Design and Implementation of arithmetic functions
-------------------------------------------------

Simple functions, not classes, were chosen as the implementation structure for
quantum circuit generators for arithmetic functions.

The functions are provided in the ``crsq.arithmetic`` module
(:py:mod:`API<crsq.arithmetic>`).

A function is provided for each supported arithmetic function. Each function
takes a QuantumCircuit as a target to emit gates to, and QuantumRegisters for
the operands.  Many functions require additional registers for carry bits or
other work registers.

Most of those additional registers require that they are passed in
:math:`\ket{0}` and at will be set to :math:`\ket{0}` after usage. However, in
some specific cases certain non-zero value will remain stored in the registers.
They can be returned to :math:`\ket{0}` by running an inverse operation of the
arithmetic function.

For each arithmetic function, two styles of functions are provided. One will
emit gates to the given circuit, and the other will create a Gate object that
can be handled and visualized as an atomic instruction.  The Gate version is
handy when graphically inspecting circuits that contain many arithmetic
operations.

All functions work on arbitrary length of bits as operands. For addition and
subtraction, a simple version of the generator function requires that the bit
length of the two operands match, but a variable-length version will accept
inputs of different bit length.

Most of the operations work on input numbers represented as qubit states, but
exceptionally, there is an "add constant value" function the takes a
compile-time constant as one of the operands.

See Also
--------

- :doc:`/notebooks/arithmetic` for circuit diagrams of the gates and usage examples.
- :ref:`arithmetic-api` for APIs.
