SolDefines module
=================

.. automodule:: SolDefines
    :members:
    :undoc-members:
    :show-inheritance:

This file describes the SOL Objects structure.

==============================
How to add an Object structure
==============================

1. Create an issue with name: "Adding YOUR_OBJECT_NAME structure".
This will create a issue number like #49.

2. Create a new branch with the name: ``develop_<your issue number>``
  ex: `develop_49`
  
3. Add the object type in the list at the top of the SolDefines.py file.

* Prepend the string "SOL_TYPE" to your object name.

* Increment the last number of the list to get an object id

Refer to the other object if you are not sure.

4. Add the object structure at the bottom of the :doc:`SolDefines.py` file.

Refere to the python structure to know which field to set: https://docs.python.org/2/library/struct.html

5. Run the the ``registry_gen.py`` script. That will update the ``registry.md`` file.

6. Commit your changes starting with the issue number.
   Commit message example: "``#49 adding YOUR_OBJECT_NAME structure``".
   
7. Push your changes to the repo: ``git push origin develop_49``

8. Create a merge request on branch develop using GitHub UI.

