import Auth from "../services/Auth";
import TenantSubtenant from "../services/TenantSubtenant";

describe("WorkFlow user journey", () => {
    it("logs in and selects a subtenant", () => {
        Auth.logInAsManager();
        TenantSubtenant.selectSubtenant("UBI-E2E");
    });

    it('naviagates to Automation tab and click the device', function() {
        cy.get('#PRIMARY_MENU_NAV_BTN_AUTOMATION').click();
        cy.findByText(/Workflows/i).click();
        cy.get('#AUTOMATION_TABLE_CELL_WORKFLOW_NAME_0').click();
    });

    it('runs a python workflow', function() {
        cy.get('#AUTOMATION_DETAILS_BTN_CREATE').click();
        cy.get('#VARIABLE_FIELD_TEXT_NAME').type('WFE2E');
        cy.get('#AUTOMATION_DETAILS_PROCESS_RUN').click();
        cy.findByText("Task OK");
        cy.get('#AUTOMATION_PROCESS_EXECUTION_DIALOG_BTN_CLOSE').click();
        cy.get('#AUTOMATION_DETAIL_DRAWER_BTN_CLOSE').click();
    });

});
