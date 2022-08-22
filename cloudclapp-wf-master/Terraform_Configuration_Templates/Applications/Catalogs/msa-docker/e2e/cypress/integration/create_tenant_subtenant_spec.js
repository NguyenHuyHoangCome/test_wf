import Auth from "../services/Auth";

describe("Create tenant user journey", ()=> {
    it("logs in and selects a subtenant", () => {
        Auth.logInAsManager();
    });

    it("navigates to Admin tab", function() {
        cy.findAllByText(/Admin/).eq(1).click();
        cy.findByText(/No Administrators found/);
    });

    it("navigates to tentant tab and create", function() {
        cy.findByText(/Tenants/).click();
        cy.get("#TENANT_BTN_CREATE_LINK").click();
        cy.get("#TENANT_CREATE_PREFIX").type("NewE2E");
        cy.get("#TENANT_CREATE_NAME").type("NewE2EName");
        cy.get("#DIALOG_ACTIONS_BTN_SAVE").click();
        cy.findByText(/Tenant Prefix must be three characters long/);
        cy.get("#TENANT_CREATE_PREFIX").clear();
        cy.get("#TENANT_CREATE_PREFIX").type("N2E");
        cy.get("#DIALOG_ACTIONS_BTN_SAVE").click();
        cy.findByText(/Tenant created/i);
    });

    // it("navigates to subtentant tab and create", function() {
    //     cy.findByText(/Subtenants/).click();
    //     cy.get("#SUBTENANT_CREATE_NAME").type("NewE2ESubName");
    //     cy.get("#SUBTENANT_BTN_CREATE_LINK").click();
    //     cy.get("#SUBTENANT_CREATE_PREFIX").type("NewE2E");
    //     cy.get("#DIALOG_ACTIONS_BTN_SAVE").click();
    //     cy.findByText(/Tenant Prefix must be three characters long/);
    //     cy.findByText(/Tenant created/i);
    // });
});
