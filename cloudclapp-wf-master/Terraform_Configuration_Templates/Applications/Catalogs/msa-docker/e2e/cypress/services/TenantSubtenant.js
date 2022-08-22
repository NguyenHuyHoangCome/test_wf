const selectSubtenant = (subtenantName) => {
  cy.get("#msaSubtenantBtn").click();
  cy.get('.MuiPopover-root').findByText(subtenantName).click();
};

export default {
  selectSubtenant,
};
