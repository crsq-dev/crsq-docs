Time evolution
==============

The time evolution calculation of the Schrödinger equation is based on the
Hamiltonian of the system. The time independent Hamiltonian of the system is a
sum of Hamiltonians for electrons and nuclei and further into kinetic energy
terms and potential energy terms:

.. math::
    :label: evo_1

    \hat{H} = \hat{H}_e+\hat{H}_a = (\hat{T}_e + \hat{V}_e) +
                                    \hat{V}_{ea} +
                                    (\hat{T}_a + \hat{V}_a)

According to the Suzuki-Trotter formula, the time evolution for a time step of
:math:`\delta t` can be approximated as:

.. math::
    :label: evo_2

    \ket{\Psi(\delta t)} = (
        e^{-T_e\delta t}
        e^{-V_e\delta t}
        e^{-V_{ea}\delta t}
        e^{-T_a\delta t}
        e^{-V_a\delta t}
    )\ket{\Psi_0} + O(\delta t^2)

We will use Fourier transforms and its inverse to convert the wave function from
spatial coordinate representation to and from momentum representation.  The
calculation of the kinetic energy term becomes much simpler in the momentum
space. Using quantum Fourier transforms and its inverse :math:`{\rm QFT}` and
:math:`{\rm QFT}^{\dagger}`, the time evolution formula becomes:

.. math::
    :label: evo_3

    \def\QFT{{\rm QFT}}
    \ket{\Psi(\delta t)} = (
        e^{-T_e\delta t}
        \QFT e^{-V_e\delta t}
        e^{-V_{ea}\delta t}
        \QFT^{\dagger} e^{-T_a\delta t}
        \QFT e^{-V_a\delta t}
    )\ket{\Psi_0} + O(\delta t^2)

Calculation of V
-----------------

Calculation of the potential energy term V is done by calculating the Coulomb
energy for every unique pair of particles.

.. math::
    :label: evo_4

    V_e = \sum_{i>j}\frac{1}{|\boldsymbol{q}_i-\boldsymbol{q}_j|}

.. math::
    :label: evo_5

    V_{en} = -\sum_{i,j}\frac{Z_j}{|\boldsymbol{q}_i-\boldsymbol{Q}_j|}

.. math::
    :label: evo_6

    V_{n} = \sum_{i>j}\frac{Z_i Z_j}{|\boldsymbol{Q}_i-\boldsymbol{Q}_j|}

By applying the arithmetic gates on the coordinate index registers, the energy
is computed for all combination of coordinates in superposition by a single
execution of the circuit.  We first compute the norm of the distance between
two particles based on the integer index values, and take its inverse obtaining
a fixed point fractional number :math:`q` with :math:`m-1` fractional bits.
This number can be represented by its bits as :eq:`evo_7`.

.. math::
    :label: evo_7
    
    q = \sum_{d=0}^{m-1}2^{d-(m-1)}q_d

For each bit :math:`q_d` we apply a phase gate :math:`P(\theta_d)` with the phase value chosen as:

.. math::
    :label: evo_8

    \theta_d = -2^{d-(m-1)}\eta q_d,  \eta = \frac{z_i z_j \delta t}{\delta q}

Where :math:`z_i, z_j` is the charge value of the two particles.

Calculation of T
-----------------

Calculation of the kinetic energy term T is done in the momentum space.

.. math::
    :label: evo_T1

    \exp \left( -i\frac{p^2}{2m_e}\cdot\delta t \right) = 
    \exp \left[ -i\gamma \left(
        \sum_{j=0}^{m-1}p_j^{2} 2^{2j} -
        2p_{m-1}\sum_{k=0}^{m-2}p_k 2^{m-1+k} +
        2\sum_{j,k=0(j>k)}^{m-2} p_j p_k 2^{j+k}
        \right) \right]

This formula can be implemented as a circuit that rotates the phase conditionally based
on the product of two qubits.

Design and implementation of the time evolution calculation
------------------------------------------------------------

Calculation of V
^^^^^^^^^^^^^^^^

We use the abstract syntax tree to generate circuits for the binary arithmetic
required for V.  After each term for a pair of particles is computed, it is
applied to the phase.  We do not sum all the terms with binary arithmetic. Then
the reverse operation for the calculation except for the phase operation, is
executed, and all qubits are returned to its original state.

Calculation of T
^^^^^^^^^^^^^^^^

Since the calculation of :math:`p_i^2` is very simple in momentum space, we do not
use the arithmetic gates to compute the square.  Instead we implement the square
operation directly with bit-wise operations.

Application of Fourier Transforms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See also
--------

- :doc:`/notebooks/time_evolution` for circuit diagrams of the gates and usage examples.
- :ref:`time-evolution-api` for APIs.
