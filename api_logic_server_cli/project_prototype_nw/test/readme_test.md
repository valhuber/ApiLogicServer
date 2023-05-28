## Notes on Tests

These tests exercise API Server Logic.

They can be re-run.  But, if they fail in the middle, be sure so replace `database/db.sqlite`.

Tests are designed to be run with Security.

The most typical way to run the tests:

1. Start API Logic Server
2. Run `Behave Run`
    * Under VSCode, use of the Debug Console obscures the test summary.  Use the combo box on the Debug Console to select Behave Run (instead of the server log).