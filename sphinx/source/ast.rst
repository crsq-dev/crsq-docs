Abstract Syntax Tree
====================

The abstract syntax tree (AST) module provides a set of classes that lies on top
of the arithmetic module to provide a higher level of abstraction in programming
style for arithmetic formulas. Once an AST is constructed, it can be used to
generate sequences of arithmetic gates to compute the formula on a quantum
device.

An abstract syntax tree is a term used in compiler design. A compiler reads the
source code character by character to recognize the syntactic structure, then as
an intermediate representation of the recognized code, constructs a tree
structure which is called an abstract syntax tree.  A schematic example of an AST
for the expression ``sqrt(dx*dx + dy*dy + dz*dz)`` is shown in
:numref:`schematic-ast`

.. graphviz:: ast_img/schematic.dot
   :name: schematic-ast
   :caption: Schematic example of an AST

ASTs are especially useful for representing arithmetic expressions, since
arithmetic expressions have a recursive tree structure. Once an AST is
constructed, target code generation becomes straightforward.

Here we use just the tree structure to make circuit generation easy. We don't
have a compiler, so the user builds this tree without the help of a compiler.
Instead Python's customized arithmetic operators are used.


Node objects
------------

An AST is a set of node objects, that are tied together in the form of a tree.

If you have to nodes a and b, and write:

  c = a + b

then the `+` is a customized operator, and it is coded to produce a node for and
add operation which points to `a` and `b` as its child nodes.  In memory you
will get the structure in :numref:`ast-a-plus-b`

.. _ast-a-plus-b:

.. mermaid:: ast_img/a_plus_b.mmd
   :caption: AST for A + B


At later circuit generation, the gates for a and b will be emitted, and after
that, the gates for c will be emitted.  You don't have to worry about assigning
the correct qubit registers for passing the results between the gates, and
allocating temporary work registers that the gates require.

The Scope object
----------------

To create the node objects and keeping track of them, a ``Scope`` object is
introduced. The scope object can be obtained from
:py:func:`crsq.ast.new_scope`.

The scope object provides methods to create leaf nodes. You typically have
QuantumRegisters in the circuit that you want to use as input for the formula.
In such case, use the register method to create an AST node that wraps the
QuantumRegister as shown in :numref:`ast-python-example`.

.. code-block:: python
  :name: ast-python-example
  :caption: AST usage example

  from qiskit import QuantumCircuit, QuantumRegister
  import crsq.ast as ast
  import crsq.heap as heap
  qc = QuantumCircuit()
  rega = QuantumRegister(4,'a')
  regb = QuantumRegister(4,'b')
  qc.add_register(rega, regb)

  scope = ast.new_scope(qc)
  ast_a = scope.register(rega)  # create leaf node for A
  ast_b = scope.regitser(regb)  # create leaf node for B
  ast_b += ast_a                # create an in-place add node for B
  scope.build_circuit()         # emit the gates to the circuit qc.


After creating the nodes, you can generate the gates by the :py:func:`build_circuit<crsq.ast.Scope.build_circuit>` method.

You can also generate the inverse of gates by :py:func:`build_inverse_circuit<crsq.ast.Scope.build_inverse_circuit>`.
This is often required in quantum algorithms.

Supported operations
--------------------

The following operators are supported on Node objects:

- ``+=``
- ``-=``
- ``*``
- ``/``

The scope object provides the following functions that take one operand.

- ``abs``
- ``square``
- ``square_root``

Fixed point arithmetic support
------------------------------

All internal arithmetic functions are implemented as integer operations. Integer
operations can be used as fixed point fractional number operations by keeping
track of the decimal point location.  AST nodes have variables to store the
number of fractional bits, and the total bit count is known by the size of the
QuantumRegister. These numbers are used for computing the fractional bit count
of the result of an operation, or checking the compatibility of operands before
an operation.

:numref:`ast-bit-length-spec` shows the checking and the resulting fractional bit count.

.. table:: accepted bit length and checking for operations
  :name: ast-bit-length-spec

  +-------------+----------------+---------------+----------------+---------------+----------------+---------------+------------+
  | Operation   | total bits lhs | frac bits lhs | total bits rhs | frac bits rhs | out total bits | out frac bits |  check     |
  +=============+================+===============+================+===============+================+===============+============+
  | Add, Sub    |     m (>=n)    |      f1       |      n         |     f2        |    n           |    f1         |  f1 == f2  |
  +-------------+----------------+---------------+----------------+---------------+----------------+---------------+------------+
  | Multiply    |     m          |      f1       |      n         |     f2        |    m+n         |    f1 + f2    |            |
  +-------------+----------------+---------------+----------------+---------------+----------------+---------------+------------+
  | Divide      |     m (>=n)    |      f1       |      n         |     f2        |    m           |    f1 - f2    |  f1 >= f2  |
  +-------------+----------------+---------------+----------------+---------------+----------------+---------------+------------+
  | Square      |     m          |      f1       |                |               |    2*m         |    2*f1       |            |
  +-------------+----------------+---------------+----------------+---------------+----------------+---------------+------------+
  | Square root |     m          |      f1       |                |               |    m/2         |    f1/2       | | m % 2 =0 |
  |             |                |               |                |               |                |               | | f1 % 2=0 |
  +-------------+----------------+---------------+----------------+---------------+----------------+---------------+------------+


Precision adjustment
--------------------

In fixed point calculation, you may need to add or remove bits to or from the
result of a calculation step before feeding that value to the next step.  The
``adjust_precision()`` method on AST nodes allows to add bits to or remove bits
from either the LSB end or MSB end of the value represented by the node.

In potential energy calculation, this feature is useful to avoid division by
zero when dividing with particle-to-particle distance.  One way to do so is to
add a :math:`\frac{1}{2}lsb` offset to the distance. That is, to add a '1' bit
to the LSB end (which will increment the total bit count), and increment the
fractional bit count.


Design and implementation of the AST
------------------------------------

The AST module is implemented as a collection of classes that implement AST
nodes, and a Scope class that serves as a factory object for leaf nodes. It also
keeps track of all the created nodes.  The scope object also has access to a
temporary qubit allocator that is used for allocating temporary qubits required
by the arithmetic operations.

The classes are provided by the  ``crsq.ast`` module (:py:mod:`API <crsq.ast>`)

AST nodes
^^^^^^^^^

A node class is created for each type of node.  Some nodes are created as a
result of an operation between AST nodes, and the created node class name is not
visible to the user. There are also some abstract base classes that are visible
to the user, but the user does not need to be aware of.
:numref:`ast-node-hierarchy` shows a class diagram of the AST Node classes:

.. _ast-node-hierarchy:

.. mermaid:: ast_img/ast_node_hierarchy.mmd
  :caption: AST node class hierarchy

The QuantumValue class holds the QuantumRegister that stores the value for the node.
The Constant class does not have a QuantumRegister.

The QuantumValue node defines several custom operator functions such as ``__iadd__``
for "in-place add", i.e. the ``+=`` operator.  Any subclass of the QuantumValue class
will accept these operators.

As leaf classes there are classes that correspond to each operation, such ass
IAdd, ISub and such.  These leaf classes all implement a circuit emitting method
that can be call through a common interface.

The Scope class
^^^^^^^^^^^^^^^

The scope class is separated into a user visible API class ``Scope``, and a
hidden implentation class ``_ScopeImp``.  This separation prevents methods in
the implementation class from appearing in the user's IDE when typing code as
auto-complete candidates.

The scope class keeps track of an array of ``Operator`` nodes. ``Operator``
nodes are nodes that has some code to emit as part of the quantum circuit.  This
array is used to generate the quantum circuit when build_circuit() or
build_inverse_circuit() is called. :numref:`scope-class-structure` shows the
structure of a Scope object.

.. _scope-class-structure:

.. mermaid:: ast_img/scope_structure.mmd
   :caption: Structure of a scope object

When the user calls ``Scope.build_circuit()``, the scope object
loops through all the ``Operator`` objects and calls the ``emit_circuit()``
method, as shown in :numref:`ast-code-gen-sequence`.

Each operator, in turn, calls methods on ``QuantumCircuit`` according
to the class of the node, to add gates to implement the intended operation.

.. drawio-figure:: ast_img/ast.drawio
   :page-index: 0
   :name: ast-code-gen-sequence

   Call sequence of build_circuit()

Work qubit allocation
^^^^^^^^^^^^^^^^^^^^^

To supply temporary work qubits that are required by arithmetic function
circuits, the ``Scope`` object uses the ``TemporaryQubitAllocator`` class that
is held by the ``Frame`` class.  ``TemporaryQubitAllocator``
stocks qubits that can be borrowed from and returned.  Both ``Frame``
and ``TemporaryQubitAllocator`` will be discussed in the :doc:`heap`
section.

See Also
--------

- :doc:`/notebooks/ast` for usage examples.
- :doc:`api/ast_api` for APIs.
