const selectTenant = (tenantName) => {
  cy.get("#msaTenantBtn").click();
  cy.get('.MuiPopover-root').findByText(tenantName).click();
};

export default {
  selectTenant,
};
