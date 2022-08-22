import Auth from "../services/Auth";
import TenantSubtenant from "../services/TenantSubtenant";

describe("Managed Entity user journey", () => {
    it("logs in and selects a subtenant", () => {
        Auth.logInAsManager();
        TenantSubtenant.selectSubtenant("MSA-E2E");
    });

    it('naviagates to Infrastructure tab and click the device', function() {
        cy.get('#PRIMARY_MENU_NAV_BTN_CONFIGURATIONS').click();
        cy.findByTitle('Managed Entity Id: 125').click();
        cy.findByText(/Overview/i);
        cy.findByText(/LinuxLocal/i);
    });

    it('edits the device', function() {
        cy.get('#MANAGED_ENTITY_DETAIL_BTN_EDIT_125').click();
        cy.get('#name').click();
        cy.get('#name').clear()
        cy.get('#name').type('Linux Entity');
    });

    it('checks if name changed', function() {
        cy.get('#ME_TOOLBAR_SAVE_BTN').click();
        cy.findByText(/Linux Entity/i)
    });

    it('change back', function() {
        cy.get('#MANAGED_ENTITY_DETAIL_BTN_EDIT_125').click();
        cy.get('#name').clear()
        cy.get('#name').type('LinuxLocal');
    });

    it('check again', function() {
        cy.get('#ME_TOOLBAR_SAVE_BTN').click();
        cy.findByText(/LinuxLocal/i)
    });
});
