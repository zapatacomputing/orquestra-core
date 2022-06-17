=========================
Circuits guide
=========================


What this guide covers
======================

This guide is an in-depth dive into the ``Circuit`` class within Orquestra Core. In it, we'll cover advanced capabilities that can be performed using ``Circuit`` s like using symbolic gates, creating your own gates, and building decomposition rules. If you're looking for a place to get started, please see :ref:`the basics tutorial <creating_circuits>` before diving into the advanced capabilities here.


The Problem
===========

In this guide we want to create a QAOA circuit to solve a 3-node, fully-connected maxcut problem. Our :ref:`Basic QAOA Tutorial <qaoa>` walks through using Orquestra Core's built-in QAOA functionality to solve the problem from circuit creation through to a final result. Here, to demonstrate capabilities of ``Circuit`` s, we'll do a simple example and just build the circuit we can use to solve the problem later.

TODO: diagram of the graph we want to to maxcut on w/ short explainer including circuit diagram

General ``Circuit`` Information
===============================

Circuit Architecture
--------------------

Orquestra Core represents quantum circuits with the ``Circuit`` class, which is in turn composed of ``Operation`` s. The most common operation type is a ``GateOperation``, which we'll focus on here, although in some circumstances :ref:`wavefunction operations <wavefunction_operations>` can be useful. Circuits also have a property for the number of qubits, but users don't have to define that themselves.

If you would like to follow along with this guide, please create a new python file and start it with the imports we'll need to ensure the rest of the code examples can be run:

.. literalinclude:: /examples/circuits_guide.py
  :language: python
  :start-at: from orquestra.quantum.circuits import (
  :end-at: N_QUBITS =

Notice we also defined a variable for the number of qubits we'll be working with. This will make some list comprehensions easier later.

.. _creating_circuits:

Creating a circuit
------------------

For this QAOA problem, the first part of the circuit we need to create is the initial state preparation circuit. That can be done by putting a Hadamard gate on each qubit. In the end we want the initial state preparation circuit to look like this:

.. code-block:: text
  
  TODO

We do this in our example using a `list comprehension <https://www.w3schools.com/python/python_lists_comprehension.asp>`_:

.. literalinclude:: /examples/circuits_guide.py
  :language: python
  :start-at: state_prep_circ = Circuit(
  :end-at: state_prep_circ = Circuit(

We could have also explicitly put a Hadamard gate on each qubit index too, as we will see in the section on :ref:`appending circuits <appending_circuits>`.

.. _getting_unitary:

Getting the unitary matrix of a circuit
---------------------------------------

Now let's inspect some aspects of the unitary of the circuit, just as a sanity check to see that everything makes sense. We can convert our circuit to a unitary matrix with the ``.to_unitary()`` method. In this case, we should see that the shape of the unitary is an 8x8 matrix (because we have a circuit that operates on 3 qubits) and the type should be a numpy ndarray.

.. literalinclude:: /examples/circuits_guide.py
  :language: python
  :start-at: unitary = state_prep_circ.to_unitary()
  :end-at: ic(type(unitary))

.. include:: /tutorials/beginner_tutorial.rst
    :start-after: icecream-note:
    :end-before: This will output a text description of the circuit

The output we get from those two ``icecream`` statements should be

.. code-block:: text

  ic| unitary.shape: (8, 8)
  ic| type(unitary): <class 'numpy.ndarray'>

Inverting a circuit
-------------------

**TODO**

.. _appending_circuits:

Appending operations to a circuit
---------------------------------

You don't have to build a whole circuit all at once! Let's see how to append operations to an existing circuit by constructing the next part of our QAOA circuit, the problem hamiltonian circuit. This problem hamiltonian circuit gives a quantum description of the problem and shows how the nodes are connected. In this case, the 3 nodes are all-to-all connected, so our circuit should look like this:

.. code-block:: text

  TODO

We'll build up this circuit one connection at a time, using ``+=`` to append ``Circuit`` objects to the end of our existing ``problem_hamiltonian_circ``

.. literalinclude:: /examples/circuits_guide.py
  :language: python
  :start-at: problem_hamiltonian_circ = Circuit(
  :end-before: unitary = problem_hamiltonian_circ.to_unitary()

For now, don't worry about what the ``beta`` variables mean in these circuits. We'll cover that later when we talk about :ref:`symbolic gates <symbolic_gates>`. For now, just notice that we started with an initial circuit and we were able to append other circuits to it using ``+=``

Let's get the :ref:`unitary matrix <getting_unitary>` again and see if it makes sense for this circuit

.. literalinclude:: /examples/circuits_guide.py
  :language: python
  :start-at: unitary = problem_hamiltonian_circ.to_unitary()
  :end-at: ic(type(unitary))

The output should look like this:

.. code-block:: text

  ic| unitary.shape: (8, 8)
  ic| type(unitary): <class 'sympy.matrices.immutable.ImmutableDenseMatrix'>

For more info on why this is a sympy matrix as opposed to a numpy ndarray, please see the section on :ref:`symbolic gates <symbolic_gates>`.

Appending individual gates to circuits is also possible, as we'll see when we build up the mixing circuit for this QAOA problem. The mixing circuit looks like this:

.. code-block:: text

  TODO

To build up the mixing circuit, we ust need to put parametrized RX gate on each of the qubits. We can do that with a for loop:

.. literalinclude:: /examples/circuits_guide.py
  :language: python
  :start-at: mixing_circ = Circuit()
  :end-at: ic(mixing_circ)

The output of that looks like ``mixing_circ: Circuit(operations=[RX(gamma_0)(0), RX(gamma_1)(1), RX(gamma_2)(2)], n_qubits=3)``. Again, for now don't worry about the ``gamma`` parameters in there, that will be addressed in the :ref:`symbolic gates <symbolic_gates>` section.

.. _inspecting_circuits:

Inspecting circuits and components
----------------------------------

Now that we have all three sub-circuits of our overall QAOA circuit, we can put them all together! We can do this by just adding them and storing the result in a new ``qaoa_circ`` variable

.. literalinclude:: /examples/circuits_guide.py
  :language: python
  :start-at: qaoa_circ =
  :end-at: qaoa_circ =

Now let's look at that QAOA circuit to double-check everything makes sense.

**Printing overall circuit information** can be done by calling ``print()`` or ``ic`` on the ``Circuit`` you want information for

**Getting the number of qubits** in a ``Circuit`` can be done by accessing the ``n_qubits`` property.

The **operations property** is a list containing all the operations, and so it can be iterated over and information about specific operations can be obtained. **Getting the total number of operations** in a ``Circuit`` can be done by calling ``len()`` on the ``operations`` property.

Here are examples of how to get the above information about our ``qaoa_circ``

.. literalinclude:: /examples/circuits_guide.py
  :language: python
  :start-at: ic(qaoa_circ)
  :end-at: ic(op.gate.name,

That will produce this output:

.. code-block:: text

  ic| qaoa_circ: Circuit(operations=[H(0), H(1), H(2), CNOT(0,1), RZ(beta_0)(1), CNOT(0,1), CNOT(0,2), RZ(beta_1)(2), CNOT(0,2), CNOT(1,2), RZ(beta_2)(2), CNOT(1,2), RX(gamma_0)(0), RX(gamma_1)(1), RX(gamma_2)(2)], n_qubits=3)
  ic| qaoa_circ.n_qubits: 3
  ic| len(qaoa_circ.operations): 15
  ic| op.gate.name: 'H', op.qubit_indices: (0,), op.params: ()
  ic| op.gate.name: 'H', op.qubit_indices: (1,), op.params: ()
  ic| op.gate.name: 'H', op.qubit_indices: (2,), op.params: ()
  ic| op.gate.name: 'CNOT', op.qubit_indices: (0, 1), op.params: ()
  ic| op.gate.name: 'RZ', op.qubit_indices: (1,), op.params: (beta_0,)
  ic| op.gate.name: 'CNOT', op.qubit_indices: (0, 1), op.params: ()
  ic| op.gate.name: 'CNOT', op.qubit_indices: (0, 2), op.params: ()
  ic| op.gate.name: 'RZ', op.qubit_indices: (2,), op.params: (beta_1,)
  ic| op.gate.name: 'CNOT', op.qubit_indices: (0, 2), op.params: ()
  ic| op.gate.name: 'CNOT', op.qubit_indices: (1, 2), op.params: ()
  ic| op.gate.name: 'RZ', op.qubit_indices: (2,), op.params: (beta_2,)
  ic| op.gate.name: 'CNOT', op.qubit_indices: (1, 2), op.params: ()
  ic| op.gate.name: 'RX', op.qubit_indices: (0,), op.params: (gamma_0,)
  ic| op.gate.name: 'RX', op.qubit_indices: (1,), op.params: (gamma_1,)
  ic| op.gate.name: 'RX', op.qubit_indices: (2,), op.params: (gamma_2,)

.. _wavefunction_operations:

Gate operations vs Wave Function Operations
-------------------------------------------

While gate operations perform the familiar gates on the qubits of a circuit, `wavefunction operations <https://github.com/zapatacomputing/orquestra-quantum/blob/main/src/orquestra/quantum/circuits/_wavefunction_operations.py>`_ can operate on the wavefunction directly. Currently, the only built-in wavefunction operation in Orquestra is the ``MultiPhaseOperation``, which allows a specific phase (given as an angle theta) to be applied to all 2^N components of the wavefunction for an N-qubit circuit.

Wave function operations can be included in the :ref:`creation of a circuit <creating_circuits>`, :ref:`appended later <appending_circuits>`, and :ref:`inspected <inspecting_circuits>` in the same manner GateOperations can be.


- TODO: include power and exponential classes from new unitaryhack work

.. _symbolic_gates:

Symbolic gates
==============

Symbolic gates allow the user to specify parametric gates in terms of parameters that can be set to a specific value/angle later. This allows for a few benefits: 

1. You can create the circuit once and bind the parameters later. Sometimes this saves on computational cost, and it allows for more easily understandable implementations of certain circuits, like the QAOA circuit in this example. 
2. It gives you a closed formula for the final state of the circuit. This allows users interested in mathematical description and manipulations of the state easier access than could be obtained by varying parameters and running the same circuit multiple times. However, when doing symbolic simulation of the circuit, the performance of the simulation is substantially worse than if the parameters were bound.

Using gates with symbolic parameters
---------------------------------------

In order to use symbols in symbolic gates, you need to ``import sympy`` and define some symbols at the top of the file. We recommend doing so just under where you defined ``N_QUBITS``. In our examples, we'll use the following symbols.

.. literalinclude:: /examples/circuits_guide.py
  :language: python
  :start-at: beta = sympy.symbols
  :end-at: theta = sympy.Symbol

For more info on using sympy, please see the `sympy documentation <https://docs.sympy.org/latest/index.html>`_.

As previously seen in the section on :ref:`appending circuits <appending_circuits>` gates can be added to ``Circuits`` with symbolic parameters in place of "standard" parameters. The syntax for parametric gates is ``GATE(param)(qubit)``. Here is the example from the problem hamiltonian circuit from before

.. literalinclude:: /examples/circuits_guide.py
  :language: python
  :start-at: problem_hamiltonian_circ = Circuit(
  :end-at: problem_hamiltonian_circ += Circuit([CNOT(1, 2)

Sympy returns a list of symbols to the ``beta`` and ``gamma`` variables above, so we access a specific symbol within the list with its index.

Note that when you call ``.to_unitary()`` on a Circuit where some parameters are free symbolic parameters, the resulting matrix is a sympy matrix rather than a numpy matrix, as seen in these lines and their output:

.. literalinclude:: /examples/circuits_guide.py
  :language: python
  :start-at: unitary = problem_hamiltonian_circ.to_unitary()
  :end-at: ic(type(unitary))

.. code-block:: text

  ic| unitary.shape: (8, 8)
  ic| type(unitary): <class 'sympy.matrices.immutable.ImmutableDenseMatrix'>


Binding Parameters
------------------

When you use a symbolic parameter in a gate, that parameter is referred to as a "free parameter" and it has no value. In order to assign it a value, you need to bind the parameter.

Before binding the parameters, lets see what free parameters we have in our ``qaoa_circ`` with ``free_symbols``.

.. literalinclude:: /examples/circuits_guide.py
  :language: python
  :start-at: ic(qaoa_circ.free_symbols)
  :end-at: ic(qaoa_circ.free_symbols)

That should output ``ic| qaoa_circ.free_symbols: [beta_0, beta_1, beta_2, gamma_0, gamma_1, gamma_2]`` because we have 3 beta parameters and 3 gamma parameters that are still free.

We can choose which parameters to bind in our circuit, so first let's just bind the beta parameters:

.. literalinclude:: /examples/circuits_guide.py
  :language: python
  :start-at: bound_beta_circ =
  :end-at: ic(bound_beta_circ.free_symbols)

This should output ``ic| bound_beta_circ.free_symbols: [gamma_0, gamma_1, gamma_2]`` as the ``beta`` parameters have been bound, but the gamma parameters have not.

Now let's bind the gamma parameters and check what the :ref:`resulting unitary's <getting_unitary>` type is.

.. literalinclude:: /examples/circuits_guide.py
  :language: python
  :start-at: bound_all_circ =
  :end-at: ic(type(unitary))

We can see in the output that there are no more free parameters and that when all the parameters are bound, the unitary matrix is again a numpy ndarray, rather than a sympy matrix:

.. code-block:: text

  ic| bound_all_circ.free_symbols: []
  ic| type(unitary): <class 'numpy.ndarray'>

.. attention::
  Please note that ``Circuits`` which still have free parameters are not suited to run on most backends. At this time only Zapata's SymbolicSimulator is able run them


Using custom gates
==================

Custom gates let users define gates that can be re-used multiple times. This is especially useful for common sub-circuits like the ``CNOT, RZ, CNOT`` sequence in our ``problem_hamiltonian_circ``. Lets make a custom gate to implement that

Defining custom gates
---------------------

In order to define a custom gate you need to give 3 things to the ``CustomGateDefinition`` class:

1. the name of the gate
2. the matrix that defines the gate
3. the order of any parameters for the gate

In our case, we want to combine a CNOT, an RZ, and a final CNOT gate into a single gate. We'll call this gate ``ZZ`` and get the matrix by doing the needed matrix multiplications. There's only one parameter in this case (we'll call it ``theta``) so the order doesn't matter.

Here's our ``ZZ`` example all together:

.. literalinclude:: /examples/circuits_guide.py
  :language: python
  :start-at: custom_matrix = sympy.Matrix(
  :end-before: new_problem_ham_circ = Circuit(

Instantiating custom gates
--------------------------

You can use a custom gate in the same way as you would use a standard gate. To show this working, let's re-create the problem hamiltonian circuit, but this time using our new, custom ``ZZ`` gate:

.. literalinclude:: /examples/circuits_guide.py
  :language: python
  :start-at: new_problem_ham_circ =
  :end-at: ic(new_problem_ham_circ.to_unitary() ==

This should give us ``ic| new_problem_ham_circ.to_unitary() == problem_hamiltonian_circ.to_unitary(): True`` because the two circuits are equivalent.

Getting custom gates from a circuit
-----------------------------------

To get a list of all the custom gate definitions in a ``Circuit``, you can use the ``collect_custom_gate_definitions()`` method. Let's do that on our ``new_problem_ham_circ`` circuit:

.. literalinclude:: /examples/circuits_guide.py
  :language: python
  :start-at: ic(new_problem_ham_circ.collect_custom_gate_definitions())
  :end-at: ic(new_problem_ham_circ.collect_custom_gate_definitions())

The output should just show our ``ZZ`` gate:

.. code-block:: text

  [CustomGateDefinition(gate_name='ZZ', matrix=Matrix([
  [1.0*exp(-I*theta/2),                  0,                  0,                   0],
  [                  0, 1.0*exp(I*theta/2),                  0,                   0],
  [                  0,                  0, 1.0*exp(I*theta/2),                   0],
  [                  0,                  0,                  0, 1.0*exp(-I*theta/2)]]), params_ordering=(theta,))]


Decompositions
==============

Decompostion is the process of representing gate operations in (often simpler) different gates. For instance, a SWAP gate can be represented as a series of 3 SWAP gates. Often decomposition is needed to be able to run an algorithm on real hardware as different quantum computers have different sets of gates they can physically accomplish (called native gates).

Creating a ``DecompositionRule``
--------------------------------

In order to create a ``DecompositionRule`` you need a ``predicate`` and a ``production`` method.

``predicate`` tells Orquestra Core what should be decomposed. This should be a method that accepts an operation and returns a boolean (True if it should be decomposed, False otherwise).

``production`` tells Orquestra Core how it should be decomposed. This method accepts an operation and returns a list of operations.

Your custom decomposition rule should implement the `DecompositionRule <https://github.com/zapatacomputing/orquestra-quantum/blob/main/src/orquestra/quantum/decompositions/_decomposition.py#L12=>`_ protocol. We can see an example of that in our QAOA example. Suppose we want to decompose our CNOT gate, here's what that ``CNOTDecompositionRule`` class would look like:

.. literalinclude:: /examples/circuits_guide.py
  :language: python
  :start-at: class CNOTDecompositionRule:
  :end-at: return operation.gate.name == "CNOT"

Using a ``DecompositionRule``
-----------------------------

In order to use a ``DecompositionRule``, use the ``decompose_operations()`` method. This method accepts a list of operations and a ``DecompositionRule`` and returns a new list of operations where the rule has been applied.

Let's apply our ``CNOTDecompositionRule`` to our problem hamiltonian circuit. Because the ``Circuit`` class can accept a list of operations as a constructor argument, we can do this in one line:

.. literalinclude:: /examples/circuits_guide.py
  :language: python
  :start-at: decomposed_ham_circ = Circuit(
  :end-at: ic(decomposed_ham_circ.to_unitary() ==

We can see here that the decomposed circuit is equivalent to the original circuit

Built-in decompositions
-----------------------

There is currently only one built-in decomposition in ``orquestra-quantum`` and that is a `U3GateToRotation <https://github.com/zapatacomputing/orquestra-quantum/blob/main/src/orquestra/quantum/decompositions/_orquestra_decompositions.py>`_ decomposition.