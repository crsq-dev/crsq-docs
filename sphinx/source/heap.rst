the qubit Heap component
========================

The qubit heap component provides functions and classes to deal with temporary
qubit allocation and target qubit list creation for custom gate parameters.

Qiskit provides features to combine a sequence of instructions on qubits into a
unit, either as a custom instruction or a custom gate.  The two are similar in
functionality, but custom gates have the additional capability of adding control
bits afterwards, or converting a gate to its inverse.  Here we will refer to
'gate' but the same applies for instructions for what we discuss here.

Custom gates are an effective means to organize complex quantum circuits
hierarchically, and it is used extensively in our development.  It works well
for circuits with a small number of input registers, such as all the arithmetic
operations.  However, when it is applied to larger circuits, such as the gate to
compute potential energy term of the Hamiltonian for all pairs of electrons, we
found it challenging to avoid mistakes when passing argument qubits to the gate.

Custom gates take an array of qubit specifiers for the target of its operation.
A qubit specifier is either an integer or a Qubit object.  A Qubit object is not
the physical qubit device, but a class in the Qiskit SDK which holds information
to identify a physical qubit.  We use Qubit objects exclusively as specifiers.
The handling of the list of target qubit specifiers become error prone as the
number of parameters increase.  Unlike in programming languages of classical
computers, there is no compiler support to check that the caller side arguments
match the callee gate parameters.  Means to ensure that the two match would be
helpful.

Besides qubits for input and output of the intended operation, temporary qubits
required by the gate must be included in the list of parameters as well.  Since
the programmer is interested in the input and output of the gate, but not in the
temporary qubits, the responsibility to supply the exact number of temporary
qubits is a burden.  To make matters worse, the number of required qubits is
sometimes hard to determine.  This is because custom gates can be nested and the
number of temporary qubits depend on the nested inner gates, recursively.  Any
of the inner gates might be modified and change the number of temporary qubits
they require.  A dynamic mechanism for determining the number of temporary
qubits is desired.

The situation is depicted in :numref:`nested-gate-calls`. In the figure, circuit
c invokes gate f, and gate f in turn invokes two gates g and h in sequence.
Arrows represent the passing of target qubits from the caller to the callee.
When circuit c calls gate f, 6 target qubits will be passed.  Gate f will pass 4
target qubits to gate g, and 2 target qubits to gate h.  We classify target
qubits into parameter target qubits and opaque target qubits.  Parameter target
qubits, denoted by white arrows, are target qubits whose meaning is known to the
caller, where opaque target qubits, denoted by shaded arrows, are those whose
meaning or usage is unknown to the caller.  It only matters that the correct
number of opaque qubits are passed, and that their initial state is set to
:math:`\ket{0}`.

Within a gate, the opaque qubits that has been provided by the caller of the
gate, is used for two purposes: for use by the gate itself and for a heap of
temporary qubits from which opaque target qubits can be allocated when calling
other sub-gates.

.. drawio-figure:: heap_img/heap.drawio
  :name: nested-gate-calls
  :page-index: 2

  Nested circuit gates and qubit allocation

The heap size for each gate is non-trivial.  For gate f, the heap size 2 is the
maximum number of opaque qubits that is required at any single moment during the
execution of this gate.  Gate g requires 2 opaque qubits, gate h requires 1, so
the maximum is 2, therefore the heap size for gate f is 2.

To make sure that the order of the parameter qubits match between the caller and
the callee, we make it a rule that the parameter qubits have the same names on
both side.  When the caller passes a qubit named "x1", then the callee will also
refer to that qubit as "x1".  Given this rule, we make it the callee's
responsibility to create a list of parameter qubit names.  The caller will use
that list of names to identify the qubits in the callers set of qubits.  This
will guarantee that the order will not be mistaken.  When creating the target
qubit list at the callers side, information must be provided from the callee.
This interaction according to the scenario in :numref:`nested-gate-calls` is
described in :numref:`target-qubit-preparation`.  At step 1, the callee, gate f
provides information about the expected target qubits.  The parameter qubit list
is ``["x", "y"]`` and the number of opaque qubits is 4.  At step 2, the caller,
circuit c prepares the target qubit list as ``["x", "y", "tmp1", "tmp2", "tmp3",
"tmp4"]``. These are names of qubits that exist in circuit c. Qubits identified
by these names within circuit c will be passed to gate f as qubits to work on.
In step 3 Gate f will receive those 6 qubits and call them as ``["x", "y", "b",
"c", "tmp1", "tmp2"]``, and use them for the computation.  To determine the number
of opaque qubits, this interaction must take place recursively from the deepest
level first order.  Gates g and h must be processed first, then gate f can be
processed.

.. drawio-figure:: heap_img/heap.drawio
  :name: target-qubit-preparation
  :page-index: 3

  Interaction between circuit c and gate f for the preparation of target qubits

To address the above mentioned problems of (a) ensuring that the caller passes
target qubits in the correct order, and (b) automatically calculate the number
of opaque qubits, we introduce some utility classes and a design pattern for the
classes that produce the circuits.  The overall class structure to handle the
above described interactions is shown in the UML class diagram
:numref:`frame-system-pattern`.  This is the set of classes that correspond to
the scenario in :numref:`nested-gate-calls`.  The shaded classes such as
"Frame", "TemporaryQubitAllocator" are utility classes that can be reused for
various circuits, and the white classes such as "FFrame" and "GFrame" are
classes that are specific to the circuit in concern.  The white classes
"FFrame", "GFrame" and "HFrame" corresponds to the gates f,g and h in
:numref:`nested-gate-calls`, and their main responsibility is to hold
QuantumRegister objects that identify the qubits that belong to each of the
gates.  Fframe, for example has member variables x, y, b and c that corresponds
to the qubits belonging to gate f.  These three classes all have a common
superclass "Frame", which provides functionality for temporary qubit management
and target qubit list preparation.  In parallel with the frame classes, there
are three block classes "FBlock", "GBlock" and "HBlock" whose responsibility is
to hold any parameter values that determines the number of qubits for each gate
and the corresponding circuit, and also to generate the gates for the circuits.
These block classes have the information required to create the circuits. These
classes will work on registers held by the corresponding frame classes, which
shall be passed as parameters.  For FBlock, the two methods allocate_registers
and build_circuit both take an FFrame object as the parameter.

Circuit generation for the overall f, g, h gates can be performed by calling those
two methods on the top level block FBlock.  The allocate_registers method will
call the same named method on the lower level blocks GBlock and HBlock, and along
this chain of calls, all Qubit objects (identifiers for physical qubits) that
except for heap qubits are created, and they are registered to the Frame class
as either a qubit belonging to the parameter , or a qubit which is local to the
gate and therefore opaque to the caller of the gate.  The following build_circuit
method is also a recursive method that will cause the circuit for a single
custom gate to be generated, then being converted to a custom gate, then being
applied to the caller's circuit as a single instruction. 

.. drawio-figure:: heap_img/heap.drawio
  :name: frame-system-pattern
  :page-index: 5

  overall structure for target qubit handling


We will describe the sequence  of allocate_registers and build_circuit in detail
using UML sequence diagrams.  The first diagram shown in
:numref:`g-block-allocate-registers` is the allocate_registers method of GBlock
which is a leaf gate, meaning it has no more inner gates.  The diagram shows that
GBlock has the responsibility to create the QuantumRegister objects, and GFrame
stores them, along with registering to its parent class Frame whether the register
is a parameter or a local register.

.. drawio-figure:: heap_img/heap.drawio
  :name: g-block-allocate-registers
  :page-index: 6

  Sequence diagram of GBlock.allocate_registers

The next diagram is one layer above the GBlock that has been explained. The diagram
:numref:`f-block-allocate-registers` shows the sequence of the allocate_registers
method of FBlock.  This method calls allocate_registers on GBlock and HBlock to
process the inner blocks first, then prepare qubit objects for itself. For qubits
that are passed as parameters to GBlock or HBlock, qubit objects with the same name
have already been created on GFrame or HFrame.  Sharing the qubit objects in this way
ensures that the qubit name on both the caller and callee will be identical.

.. drawio-figure:: heap_img/heap.drawio
  :name: f-block-allocate-registers
  :page-index: 7

  Sequence diagram of FBlock.allocate_registers

Upon completion of the allocate_registers method, each frame will have complete
information of the parameters it accepts, but the heap size that each frame
require is not determined. This will be computed along generating the circuit
with the generate_circuit call. The generate_circuit of the FBlock is shown on
:numref:`f-block-generate-circuit`. The purpose of this method is to add
instructions to the QuantumCircuit object that belongs to FFrame.  At some point
of that process, the GBlock and HBlock needs to be added to the circuit as a
custom instruction.  When that timing arrives, generate_circuit on GBlock or
HBlock is called to fill the quantum circuit with instructions on those frame
objects, then an apply method on the FFrame is called with GFrame or HFrame
object as the parameter.  Generating circuits on GFrame and HFrame has the
effect of determining the required heap sizes of those frames.

.. drawio-figure:: heap_img/heap.drawio
  :name: f-block-generate-circuit
  :page-index: 8

  Sequence diagram of FBlock.allocate_registers

The apply method will convert the frame content into a custom gate and prepare
the target qubit list and invoke the custom gate.  The detailed sequence of
FFrame.apply(gf) is shown on :numref:`f-frame-apply-gf`.  The content of the
QuantumCircuit for GFrame is converted into a custom gate.  Then the opaque bit
count is queried.  This is answered by adding the size of the free qubit pool
held by the TemporaryQubitAllocator for GFrame and the number of qubits of local
registers. The opaque qubits are prepared by calling the TemporaryQubitAllocator
for FFrame. If the allocator does not have enough free qubits in the pool, new
qubits will be added to the quantum circuit and the pool.  That will increase
the total qubit count of FFrame. Along with the heap qubits, the parameter
register list is obtained from FFrame. The parameter list and the opaque qubits
are added together to form the target qubit list. This list is used to apply the
custom gate to the quantum circuit of FFrame.

.. drawio-figure:: heap_img/heap.drawio
  :name: f-frame-apply-gf
  :page-index: 9

  Sequence diagram of FFrame.apply(gf)


The class diagram of the utility class ``TemporaryQubitAllocator``
(:py:class:`API <crsq.heap.TemporaryQubitAllocator>`), is shown in
:numref:`qubit-allocator-structure`. This class maintains a list of pooled
qubits that can be borrowed from (allocated) for temporary use and returned
after use. The number of qubits pooled in the list will grow to the maximum
number of qubits that are simultaneously allocated during circuit generation.
It provides two methods ``allocate`` and ``free``.  The allocator will have an
associated QuantumCircuit object, and when qubits are added to the pool, they
are also added to the circuit.

.. drawio-figure:: heap_img/heap.drawio
  :name: qubit-allocator-structure
  :page-index: 4

  the TemporaryQubitAllocator class
