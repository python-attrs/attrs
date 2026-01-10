Incorrect Default Factory Execution Order in attrs Causing Validation Errors
----------------------------------------------------------------------------

Brief
-----
Classes defined using `@define` in the attrs library support dynamic default
values via a `factory=` argument and value validation via validators. In
certain cases where a required field, a factory-provided field, and one or more
validators exist together, attrs initializes default values too early. This
causes validators to run on incomplete or incorrect state.

This produces mismatches between user intent and runtime behavior — validators
may see pre-factory values, incorrectly succeed, or incorrectly fail.

Expected Behavior
-----------------
Default factories must run only after all explicitly provided required values
have been:
1. Assigned
2. Validated individually

Validators must always receive:
• The resolved value returned by the default factory
• A fully initialized set of attributes
• Complete cross-field state

Required Functional Behavior
----------------------------
1. Required fields missing → raise a validation error (unchanged behavior).
2. The default factory must execute *only if* the user does not pass a value.
3. The default factory must run *after* successful validation of required fields.
4. All validators — including cross-field validators — must observe the final
   resolved default value.
5. If any validator raises, object initialization must halt without returning
   a partially initialized instance.
6. Classes without factories or cross-field validators must behave identically
   to current releases (no regressions).

Edge Cases to Support
---------------------
• Field B default depends on validated A
• Validators referencing multiple attributes
• Factories returning mutable objects (must not reuse previous instance)
• Missing required fields
• Multiple factories in one class

Success Outcome
---------------
After applying a fix, all validators must execute against final initialized
state, default factories must run in the correct order, and all existing behavior
must remain unchanged unless explicitly addressed in this brief.

Everything described must be testable deterministically, with no randomness,
timers, or network interaction.
