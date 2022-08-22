const fillCredentials = () => {
  cy.findByLabelText(/Username/i).type("ncroot");
  cy.findAllByLabelText(/Password/i)
    .first()
    .type("ubiqube");
  cy.findByText(/Log In/i).click();
};

const logInAsManager = () => {
  cy.visit("/");
  fillCredentials();
  // Login normally takes time so extend the wait time from default (10sec) to 30sec
  cy.findAllByText(/MANAGED ENTITIES/i, { timeout: 30000 });
};
const logInAsDeveloper = () => {
  cy.visit("/");
  cy.get("#LOGIN_TAB_SELECT_DEV").click();
  fillCredentials();
  cy.findAllByText(/Explore our/i, { timeout: 30000 });
};

export default {
  logInAsManager,
  logInAsDeveloper,
};
