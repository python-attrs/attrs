Title: Correct Factory Validation Execution Ordering in attrs Initialization

Brief:
Classes defined using `@define` in the attrs library support default factories
to generate attribute values when not explicitly passed by users. Currently,
factory execution may occur before required field validation, causing
cross-field validators to observe incomplete state, leading to silent data
corruption.

Intended Behavior:
- Required fields must be validated before any factory executes.
- Factories must only run when user does not supply a value.
- Factory-produced values must be validated before assignment.
- Cross-field and per-field validators must observe fully initialized state.
- Behavior must remain unchanged for attributes without factories.

Edge Cases:
- Required missing → error
- Factory returning invalid value → error
- Cross-field validator inspecting both attributes
- Mutable default returned from factory should not be shared

Success Outcome:
- New tests exercise above cases
- Base tests pass unchanged
- New tests fail before fix and pass after fix
