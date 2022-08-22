import "./commands";
import "cypress-jest-adapter";

Cypress.Screenshot.defaults({
  screenshotOnRunFailure: false,
});

// Clear indexedDB state before each test suite runs
beforeEach(() => {
  indexedDB.deleteDatabase("keyval-store");
});
