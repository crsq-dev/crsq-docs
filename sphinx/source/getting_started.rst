Getting Started
===============

Why should you want to setup a simulator that cannot run?
---------------------------------------------------------

This software package uses too many qubits to run successfully
on any real quantum computer hardware that is available at the
time of this writing.  So why should you ever want to set it up
on you computer?

Here are some reasons that you might want to actually download
this software and set it up for running some part of it.

- Run just the python code, not the quantum circuits it produces

  You can run all the python code that produces the quantum
  circuits.  You can investigate the circuits that it generates,
  or check the sizes of the registers that might be of your
  interest.

  You can also adjust the configuration parameters and see how the size
  of the circuit grows.
  Parameters include things like bit number for spatial
  resolution, number of electrons or nuclei (atoms).

- Use it as a tool for your research project

  You might be working on a new type of integrator algorithm for the
  Schrödinger equation.  You can leverage this code for the common
  parts like arithmetics and temporary qubit allocation.


How to set up
-------------

If you want to run the tests on your computer, here is how to do the setup.

Install python and packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^

crsq is tested with python 3.11.
The minimum required python version is not confirmed.
Install python if you have not yet.

crsq requires several python packages, including qiskit.
Prepare a virtual python environment such as venv or conda.

After activating your virtual environment run pip.:

    $ pip install
