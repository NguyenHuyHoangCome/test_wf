describe("Login user journey", () => {
  it("sees the login UI when visiting the homepage as a logged out user", () => {
    cy.visit("/");

    cy.findByLabelText(/Username/i);
    cy.findAllByLabelText(/Password/i).first();
    cy.findByText(/Log In/i);
  });

  it("logs in", () => {
    cy.findByLabelText(/Username/i).type("ncroot");
    cy.findAllByLabelText(/Password/i)
      .first()
      .type("ubiqube");
    cy.findByText(/Log In/i).click();
  });

  it("is redirected to the Dashboard tab", () => {
    cy.findByText(/Dashboard/i);
    cy.findByText(/Managed Entities/i);
  });

  it("logs out and is redirected back to the login UI", () => {
    cy.findByText(/Logout/i).click();

    cy.findByLabelText(/Username/i);
    cy.findAllByLabelText(/Password/i).first();
    cy.findByText(/Log In/i);
  });
});
