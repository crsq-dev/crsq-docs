Abstract Syntax Tree API
========================

See :doc:`../ast` for an introduction.

Module crsq.ast
-----------------

.. automodule:: crsq.arithmetic.ast
  :members: new_scope

.. autoclass:: crsq.arithmetic.ast.Scope
  :members:

.. autoclass:: crsq.arithmetic.ast.Value
  :members:

.. autoclass:: crsq.arithmetic.ast.Constant
  :members:

.. autoclass:: crsq.arithmetic.ast.QuantumValue
  :members: adjust_precision
  :special-members: __iadd__, __isub__, __mul__, __truediv__
