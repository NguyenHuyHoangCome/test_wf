import Auth from "../services/Auth";
import Tenant from "../services/Tenant";
import TenantSubtenant from "../services/TenantSubtenant";

describe("BPM user journey", () => {
  it("logs in and selects a subtenant", () => {
    Auth.logInAsManager();
    TenantSubtenant.selectSubtenant("MSA-E2E");
  });

  it("navigates to BPM tab and begins creating a new BPM diagram", () => {
    cy.get("#PRIMARY_MENU_NAV_BTN_AUTOMATION").click();
    cy.findByText(/Create BPM/i).click();
  });

  it("drags a workflow element onto the BPM canvas", () => {
    // Force clicking as each elements are out of screen because of a bug in cypress
    cy.get('[data-element-id="StartEvent_1"]').click({ force: true });
    cy.get('[data-action="append.append-task"]').click({ force: true });
  });

  it("attaches a workflow, process name, and variables", () => {
    cy.get("#BPM_PROPERTIES_PANEL_WORKFLOW_SELECT").click();
    cy.findByText("Sample Firewall").click();
    cy.get("#BPM_PROPERTIES_PANEL_PROCESS_SELECT").click();
    cy.findAllByText("Create Firewall").click();
    cy.findByText("Saved").click();
    cy.get("#BPM_PROPERTIES_PANEL_EDIT").click({ force: true });
    cy.findAllByText(/Firewall name/);
    cy.get("#VARIABLE_FIELD_TEXT_FW_NAME").type("test-fw-name");
    cy.get("input#VARIABLE_FIELD_INTEGER_SLEEP").type("1");
    cy.get("#DIALOG_ACTIONS_BTN_SAVE").click();
    cy.get('[data-action="append.end-event"]').click({ force: true });
  });

  it("creates the BPM diagram and saves it with a name", () => {
    cy.get("#MODAL_TOOLBAR_SAVE_BTN").click();
    cy.get("#bpm-name-field").type("My BPM diagram");
    cy.findAllByText(/Create BPM/i)
      .last()
      .click();
    cy.findByText(/Discard Changes/i).should("not.exist");
  });

  it("finds the BPM that was just created and edits it", () => {
    cy.findByText("My BPM diagram").click({ force: true });
    cy.get("#BPM_DETAILS_EXECUTE_BPM").click();
    cy.findByText(/Create Firewall/i).click({ force: true });
    cy.findAllByText(/Firewall name/);
    cy.get("#BPM_PROPERTIES_PANEL_EDIT").click({ force: true });
    cy.get("#VARIABLE_FIELD_TEXT_FW_NAME").click();
    cy.get("#VARIABLE_FIELD_TEXT_FW_NAME").should("have.value", "test-fw-name");
    cy.get("#VARIABLE_FIELD_TEXT_FW_NAME").clear();
    cy.get("#VARIABLE_FIELD_TEXT_FW_NAME").type("test-fw-name-updated");
    cy.get("#DIALOG_ACTIONS_BTN_SAVE").click();
  });

  it("executes the BPM and sees execution results", () => {
    cy.get("#MODAL_TOOLBAR_EXECUTE_BTN").click();
    cy.get("#DIALOG_ACTIONS_BTN_SAVE").click();
    cy.get(".bjs-container").click();
    cy.findByText(/Latest Execution Result/i);
    cy.get("#MODAL_TOOLBAR_CLOSE_BTN").click();
    cy.get("#BPM_DETAILS_LINK_BACK_TO_BPM_LIST").click();
  });

  it("detaches the BPM from Subtenant", () => {
    Tenant.selectTenant("MSAE2E");
    // force clicking as cypress trigger("mouseover") ignores CSS effect
    cy.findAllByText(/Add to/i)
      .first()
      .click({ force: true });
    cy.get("#ATTACHMENT_BOARD_DETACH_ALL").click();
    cy.findByText(/Save/i).click();
  });

  it("deletes the BPM", () => {
    // wait for the dialog to be closed as force clicking in the next step
    cy.findByText(/ATTACH MY BPM DIAGRAM/i).should("not.exist");
    // force clicking as cypress trigger("mouseover") ignores CSS effect
    cy.get("#BPM_TABLE_BTN_DELETE_0").click({ force: true });
    cy.findByText(/Are you sure you want to delete/i);
    cy.findByText(/OK/i).click();
    cy.findByText("My BPM diagram").should("not.exist");
  });
});
