import Auth from "../services/Auth";
import TenantSubtenant from "../services/TenantSubtenant";

const DATA = {
  subtenant: "MSA-E2E",
  workflowName: "E2E Workflow",
  processName: "E2E Process",
  actionName: "E2E Action",
  initialStateName: "E2E Initial State",
  finalStateName: "E2E Final State",
  bpmName: "E2E BPM",
};

describe("AI/ML Create states, create action and generate BPM user journey", () => {
  it("Logs in as developer and navigates to Automation -> Workflows", () => {
    Auth.logInAsDeveloper();
    cy.get("#PRIMARY_MENU_NAV_BTN_AUTOMATION").click();
    cy.findByText("Workflows").click();
  });

  /* CREATING WORKFLOW */
  it("Creates workflow", () => {
    cy.get("#AUTOMATION_BTN_ADD_WORKFLOW").click();
    cy.get('input[id="information.displayName').type(DATA.workflowName);
    cy.get("#WORKFLOWS_PROCESS_ADD").click();
    cy.findByText(/Create process/i);
    cy.get("#AUTOMATON_PROCESS_NAME").type(DATA.processName);
    cy.get("#AUTOMATON_PROCESS_TYPE").click();
    cy.get("#AUTOMATION_PROCESS_TYPE_CREATE").click();
    cy.get("#DIALOG_ACTIONS_BTN_SAVE").click();
    cy.get("#AUTOMATION_DETAILS_EDIT_SAVE_BTN").click();
    cy.findByText(DATA.workflowName);
  })

  /* CREATING STATES */
  it("Navigates to Automation -> Intent-based -> States tab", () => {
    cy.get("#PRIMARY_MENU_NAV_BTN_AUTOMATION").click();
    cy.get("#PRIMARY_MENU_NAV_BTN_AUTOMATION_INTENT_BASED").click();
    cy.findByText("States").click();
  });

  it("Creates initial state", () => {
    cy.get("#AI_STATE_BTN_CREATE_LINK").click();
    cy.get("#AI_STATE_CREATE_NAME").type(DATA.initialStateName);
    cy.get("#AI_STATE_CREATE_INITIAL_CHECKBOX").check();
    cy.get("#DIALOG_ACTIONS_BTN_SAVE").click();
    cy.findByText(DATA.initialStateName);
  });

  it("Creates final state", () => {
    cy.get("#AI_STATE_BTN_CREATE_LINK").click();
    cy.get("#AI_STATE_CREATE_NAME").type(DATA.finalStateName);
    cy.get("#AI_STATE_CREATE_FINAL_CHECKBOX").check();
    cy.get("#DIALOG_ACTIONS_BTN_SAVE").click();
  });

  it("Finds newly created states in the list", () => {
    cy.findByText(DATA.initialStateName);
    cy.findByText(DATA.finalStateName);
  });

  /* CREATING ACTION */
  it("Navigates to Automation -> Intent-based -> Actions tab", () => {
    cy.get("#PRIMARY_MENU_NAV_BTN_AUTOMATION").click();
    cy.get("#PRIMARY_MENU_NAV_BTN_AUTOMATION_INTENT_BASED").click();
    cy.findByText("Actions").click();
  });

  it("Creates action", () => {
    cy.get("#AI_ACTION_BTN_CREATE_LINK").click();
    cy.get('input[id="name').type(DATA.actionName);
    cy.get("#AI_ACTION_CREATE_WORKFLOW_SELECT").click();
    cy.get('[id*="option-0"]').click();
    cy.get("#AI_ACTION_CREATE_PROCESS_SELECT").click();
    cy.get('[id*="option-0"]').click();
    cy.get("#AI_ACTION_CREATE_STATE_SELECT").click();
    cy.get('[id*="option-1"]').click();
    cy.get("#DIALOG_ACTIONS_BTN_SAVE").click();
  });

  it("Finds newly created action in the list", () => {
    cy.findByText(DATA.actionName);
  });

  /* SELECTING SUBTENANT */
  it("Selects subtenant", () => {
    TenantSubtenant.selectSubtenant(DATA.subtenant);
  });

  /* GENERATING BPM BASED ON STATES CREATED */
  it("Navigates to Automation -> Intent-based -> Generate BPM", () => {
    cy.get("#PRIMARY_MENU_NAV_BTN_AUTOMATION").click();
    cy.get("#PRIMARY_MENU_NAV_BTN_AUTOMATION_INTENT_BASED").click();
  });

  it("Selects Final state and Initial state", () => {
    cy.get("#AI_FINAL_STATE_SELECT").click();
    cy.get('[id*="option-1"]').first().click();
    cy.get("#AI_INITIAL_STATE_SELECT").click();
    cy.get('[id*="option-0"]').click();
  });

  it("Generates BPM", () => {
    cy.get("#AI_GENERATE_WF_BTN").click();
    cy.get("#MODAL_TOOLBAR_SAVE_BTN").click();
    cy.get("#bpm-name-field").type(DATA.bpmName);
    cy.get("#DIALOG_ACTIONS_BTN_SAVE").click();
    cy.findByText(DATA.bpmName);
  });

  it("Opens newly created BPM for edit", () => {
    cy.findByText(DATA.bpmName).click({ force: true });
    cy.get("#BPM_DETAILS_BTN_EDIT").click();
  });

  it("Saves BPM after edit and finds it in the list", () => {
    cy.get("#MODAL_TOOLBAR_SAVE_BTN").click();
    cy.findByText(DATA.bpmName);
  });
});