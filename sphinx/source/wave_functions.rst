.. _wave-functions-intro:

Wave functions
==============

The wave function is stored in the Hilbert space of the quantum registers that
represent the discretized coordinates of the particles.

We define the simulated space as a cube, with size :math:`L\times L \times L`.

A bit count for discretizing length is chosen as :math:`m`. The space is
discretized into :math:`2^m` points for each dimension with interval
:math:`\delta q = \frac{L}{2^m}`.

The coordinates of an electron with index :math:`i` is :math:`\boldsymbol{q}_i`.
The discretized integer indices for coordinate values :math:`(x_i, y_i, z_i)`
are defined as :eq:`wf_1`.

.. math::
    :label: wf_1

    (x_i, y_i, z_i) = \frac{\boldsymbol{q}_i}{\delta q}

Electrons will also need a variable for the spin.  We will denote the electron
coordinate including the spin as :math:`\boldsymbol{x}_i=(q_i,\xi_i)`. The spin
variable :math:`\xi_i` for electron :math:`i` will be represented by an integer
index :math:`w_i` such that:

.. math::
    :label: wf_2

    w_i = \frac{1}{2} - \xi_i

Sometimes it is convenient to treat the four integers :math:`(x_i, y_i, z_i, w_i)`
as a unit. For such cases, we use the variable :math:`q_i = x_i + 2^m y_i +
2^{2m} z_i + 2^{3m} w_i` . The bits in :math:`q_i` will include all the bits in :math:`x_i,
y_i, z_i` and :math:`w_i`.

In the same manner coordinates of a nucleus with index :math:`i` is
:math:`\boldsymbol{Q}_i` and is mapped to integer indices :math:`(X_i, Y_i,
Z_i)`.  As with the electron coordinates we will use the variable :math:`Q_i =
X_i + 2^m Y_i + 2^{2m} Z_i`.

Following conventions the expression :math:`Z_i` will also be used to denote the
electric charge of nucleus i, which should be distinguishable by context.

For each integer index, :math:`m` qubits are assigned, and the binary number
represented by the state of the qubits corresponds to the index value. The wave
function for a system with :math:`N_e` electrons and :math:`N_a` nuclei is
stored in the Hilbert space of the tensor product of all the index registers:

.. math::
    :label: wf_3

    \def\bx{\boldsymbol{x}} \def\bQ{\boldsymbol{Q}}
    \ket{\Psi} =\sum_{q_i,Q_j}
                \Psi(\bx_1,...,\bx_{Ne};\bQ_1,...,\bQ_{N_a})
                \ket{q_1,...,q_{N_e};Q_1,...,Q_{N_a}}


When the wave function is represented in the frequency domain, momentum vectors
are used in place of coordinates.  The momentum of electron :math:`i` is
:math:`\boldsymbol{p}_i` are mapped to the same integer indices that was used
for coordinates, such that:

.. math::
    :label: wf_4

    (x_i, y_i, z_i) = \frac{\boldsymbol{p}_i}{\delta p}

The collection of all the qubits for the integer indices including spin, will be
denoted as :math:`A`. We will use expressions such as :math:`\ket{A}`.

Shuffling algorithm for the Slater determinant
----------------------------------------------

:math:`\Psi` will be prepared by initializing the state of the qubits for each
particle with pre-computed orbital distributions.

.. math::
    :label: wf_5

    \ket{A} = \ket{\Psi(\sigma_0)}
     = \prod_{i=0}^{N_e-1}\ket{\phi_i(i)}
     = \prod_{i=0}^{N_e-1}\sum_{q_i=0}^{2^{3m+1}-1}\phi_i(q_i)\ket{q_i}, \sigma_0=(0,1,...,N_e-1)

Then the registers will be entangled and shuffled (permuted) to form an
equivalent of the Slater determinant.

We use a set of additional qubits :math:`B` to control the shuffling of the
coordinate registers.  :math:`B` is an array of :math:`n` bit registers
:math:`\{b_1,b_2,...,b_{N_e}\}` each corresponding to an orbital index.
:math:`n` must be large enough to store the number of electrons minus 1.
Therefore, we choose :math:`n = \lceil log_2{N_e} \rceil`.

The shuffling consists of two steps: the preparation of the sum state, and the
permutation of the register :math:`A`.

The first step is the preparation of the sum state. The registers :math:`b_k`
are initialized to the entangled value:

.. math::
    :label: wf_6
    
    \ket{b_k} = \frac{1}{\sqrt{k}} \sum_{j=0}^{k-1}\ket{j}

The value set to the overall :math:`B` register will be:

.. math::
    :label: wf_7

    \ket{B} = \frac{1}{\sqrt{N_e !}} \left( \sum_{j=0}^{N_e-1}\ket{j} \right) \otimes
              \left( \sum_{j=0}^{N_e-2}\ket{j} \right) \otimes \cdots \otimes
              \left( \ket{1}+\ket{0} \right) \otimes \ket{0}

The second step of shuffling is the permutation of the register :math:`A` based
on the register :math:`B`. In this step the register :math:`B` is converted from
a tensor product of sums into a superposition of all possible permutations.

.. math::
    :label: wf_8

    \ket{B} = \frac{1}{\sqrt{N_e !}} \sum_{\sigma \in S_{N_e}}\rm{sgn}(\sigma)\ket{\sigma}

Along this conversion, the content of register :math:`A` will be entangled with
values of register :math:`B` and permuted correspondingly.

.. math::
    :label: wf_9

    \def\sgn{\rm{sgn}}
    \ket{B}\ket{A} = \frac{1}{\sqrt{N_e !}} \sum_{\sigma \in S_{N_e}}\sgn(\sigma)\ket{\sigma}\ket{\Psi(\sigma)}

State preparation of initial orbital data
-----------------------------------------

To initialize a set of qubits so that the Hilbert space of the qubits will
follow a desired distribution provided by data, one must build a circuit to
distribute amplitude values to match the data.  A function
``crsq.setdistribution.setv`` (:py:func:`API<crsq.setdistribution.setdist>`) is
provided to set an array of complex number amplitudes to a list of qubits.

Design and implementation of the wave function representation
-------------------------------------------------------------

Wave function and the Slater determinant
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The two major entities register A and register B were decided to be implemented
by dedicated classes 'ARegister' and 'BRegister'. They belong to the
``crsq.slater`` module (:py:mod:`API <crsq.slater>`).

For reasons discussed in :doc:`heap` section, it has been decided to let
the ``RegisterSet`` class to hold the ``QuantumCircuit`` and all
``QuantumRegister`` objects that appear in the simulator. As such, all
QuantumRegisters are pointed from ``RegisterSet``, and ``ARegister`` and
``BRegister`` also have references to the registers they need access to. The
structure of register sets is shown in :numref:`register-set-structure`

.. drawio-figure:: wave_functions_img/wave_functions.drawio
    :name: register-set-structure
    :page-index: 0

    The structure of register sets

The ``ARegister`` and ``BRegister`` objects are held by the simulator's
main class ``FirstQIntegrator`` as shown in :numref:`A-B-registers`.

.. drawio-figure:: wave_functions_img/wave_functions.drawio
    :name: A-B-registers
    :page-index: 1

    The structure of FirstQIntegrator and register classes

The preparation of the sum state is implemented as ``BRegister.build_sums``
(:py:func:`API<crsq.slater.BRegister.build_sums>`) and the shuffling is
implemented as ``BRegister.build_permutations``
(:py:func:`API<crsq.slater.BRegister.build_permutations>`).

State preparation for orbitals
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A function for state preparation is provided as a function ``crsq.setdistribution.setdist``
(:py:func:`API<crsq.setdistribution.setdist>`) and as a gate ``crsq.setdistribution.SetdGate``
(:py:class:`API<crsq.setdistribution.SetdGate>`).

See also
--------

- :doc:`/notebooks/wave_functions` for circuit diagrams of the gates and usage examples.
- :ref:`wave-functions-api` for APIs.
