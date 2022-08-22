import Auth from "../services/Auth";
import Tenant from "../services/Tenant";
import TenantSubtenant from "../services/TenantSubtenant";

describe("Activate Managed Entity user journey", () => {
    it("logs in and selects a subtenant", () => {
        Auth.logInAsManager();
        TenantSubtenant.selectSubtenant("UBI-E2E");
    });

    it('navigates to Infrastructure tab and click the device', function() {
        cy.get('#PRIMARY_MENU_NAV_BTN_CONFIGURATIONS').click();
        cy.get('#MANAGED_ENTITIES_BTN_CREATE').click();
    });

    it('edits the device', function() {
        cy.get('#DEVICE_ADAPTER_SELECTOR_VENDOR').click();
        cy.findAllByText(/Linux/).last().click();
        cy.get('#DEVICE_ADAPTER_SELECTOR_MODEL').click();
        cy.findAllByText(/Generic/).last().click();
        cy.findAllByText(/UBIE2E/);
        cy.findAllByText(/UBI-E2E/);
        cy.get("#name").type("LinuxE2EME");
        cy.get("#managementAddress").type("msa_linux");
        cy.get("#managementInterface").type("ssh");
        cy.get("#managementPort").type("22");
        cy.get("#logMoreEnabled").check();
        cy.get("#reporting").check();
        cy.get("#login").type("root");
        cy.get("#password").type("ubiqube");

        cy.get("#ME_TOOLBAR_SAVE_BTN").click();
        cy.findByText(/has been created/);
    });

    it("activate managed entity", function() {
        cy.findByText(/Actions/).click();
        cy.findByText("Activate").click();
        cy.get("#INITIAL_PROVISIONING_DIALOG_ACTIONS_BTN_CONTINUE").click();
        cy.get("#Lock_Provisioning-OK").should('exist');
        cy.get("#Save_Configuration-OK", { timeout: 30000 }).should('exist');
    });
});
