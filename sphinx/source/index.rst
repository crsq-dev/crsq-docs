Welcome to crsq's documentation!
==================================

crsq is a Qiskit based python program for quantum chemistry simulation
to run on quantum computers.  It is part of a research project attempting
to prepare a simulation program targeted for quantum devices of the near future.
As such, it cannot be used today to perform actual simulations.
The hardware requirements exceed the capabilities of current quantum computers.

crsq performs time evolution simulation of the Schrödinger
equation to simulate electron and nuclei motion.
The name "crsq" is a shorthand for first quantization, which differentiates
the generation of simulators that crsq belongs to from the typical quantum
computer based quantum chemistry simulators available today, most of which
are based on second quantization.

crsq also runs a non-hybrid, fully quantum computer based simulation.
To cope with the noise level of current quantum devices, current simulators
must keep the overall circuit compact in term of qubit count and gate depth.
To do so simulators today are typically constructed as a hybrid of classical
code and quantum code, often based on the VQE algorithm.
crsq implements all elements of computation for time evolution on
a quantum computer.

At the time of this writing, there is no quantum computer device nor
software simulator capable of running crsq in its actual form.
However the subcomponents can be run and tested.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   intro
   getting_started
   arithmetic
   ast
   wave_functions
   time_evolution
   heap
   notebooks/notebooks
   api/api
   bibliography


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
