Backward Compatibility
======================

.. currentmodule:: attr

``attrs`` has a very strong backward compatibility policy that is inspired by the one of the `Twisted framework <https://twistedmatrix.com/trac/wiki/CompatibilityPolicy>`_.

Put simply, you shouldn't ever be afraid to upgrade ``attrs`` if you're using its public APIs.
If there will ever be need to break compatibility, it will be announced in the :doc:`changelog`, raise deprecation warning for a year before it's finally really broken.


.. _exemption:

.. warning::

   The structure of the :class:`attr.Attribute` class is exempted from this rule.
   It *will* change in the future since it should be considered read-only, that shouldn't matter.

   However if you intend to build extensions on top of ``attrs`` you have to anticipate that.
