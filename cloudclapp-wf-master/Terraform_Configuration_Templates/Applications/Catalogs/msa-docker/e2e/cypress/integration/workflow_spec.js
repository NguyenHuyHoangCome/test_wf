import Auth from "../services/Auth";
import TenantSubtenant from "../services/TenantSubtenant";

describe("WorkFlow user journey", () => {
    it("logs in and selects a subtenant", () => {
        Auth.logInAsDeveloper();
        TenantSubtenant.selectSubtenant("MSA-E2E");
    });

    it('naviagates to Automation tab and click the device', function() {
        cy.findByText("Automation").click();
        cy.findByText(/Workflows/i).click();
        cy.get('#AUTOMATION_TABLE_CELL_WORKFLOW_NAME_0').click();
        cy.findByText(/This is the description of Test/i)
    });

    it('edits workflow and save', function() {
        cy.get('#AUTOMATION_DETAILS_BTN_EDIT').click();
        cy.get('input[id="information.description"]').clear();
        cy.get('input[id="information.description').type('New description for E2E');
        cy.get('#AUTOMATION_DETAILS_EDIT_SAVE_BTN').click()
        cy.get('#AUTOMATION_DETAILS_BTN_EDIT').click();
        cy.get('input[id="information.description').should('have.value', 'New description for E2E');
        cy.get('#AUTOMATION_DETAILS_EDIT_SAVE_BTN').click()
        cy.findByText(/New description for E2E/i)
    });

    it('create variable', function() {
        cy.get('#AUTOMATION_DETAILS_BTN_EDIT').click();
        cy.get('#WORKFLOWS_VARIABLES_SIDEBAR_TAB').click();
        cy.findByText(/params.name/i)
        cy.get('#VARIABLES_EDIT_CREATE_VARIABLE').click();
        cy.get('#VARIABLES_VARIABLE_1_VARIABLES_EDIT_CREATE_NAME').type('e2e_variable')
        cy.get('input[name="variables.variable.1.displayName"]').type('E2E variable')
        cy.get('#MICROSERVICE_VARIABLES_EDIT_DETAILS_BTN_SAVE').click()
        cy.get('#AUTOMATION_DETAILS_EDIT_SAVE_BTN').click()
        cy.findByText(/All instances/i)
    });
});
