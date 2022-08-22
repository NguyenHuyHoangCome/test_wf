import "@testing-library/cypress/add-commands";

Cypress.Commands.add("openMuiPicker", (pickerLabel) => {
  cy.findByLabelText(pickerLabel).siblings().first().click({ force: true });
});
