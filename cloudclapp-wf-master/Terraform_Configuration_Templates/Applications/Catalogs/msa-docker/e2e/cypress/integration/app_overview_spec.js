import Auth from "../services/Auth";

describe("App Overview user journey", () => {
  it("logs in", () => {
    Auth.logInAsManager();
  });

  it("is redirected to the Dashboard tab after login", () => {
    cy.findByText(/Dashboard/i);

    cy.findByText(/Managed Entities/i);
    cy.findByText(/MSA-E2E/i);

    cy.findByText(/Workflow Instances/i).scrollIntoView();
    cy.findAllByText(/Total Instances/i);
  });

  it("sees a header with managed entity states", () => {
    cy.findAllByText(/1/i).first();
    cy.findAllByText(/unreachable/i).first();
  });

  it("sets a selected subtenant", () => {
    cy.get("#msaTenantBtn");
    cy.get("#msaSubtenantBtn").click();
    cy.findAllByText("UBI-E2E").last().click();
  });

  it("navigates to the Infrastructure tab and its sub-sections", () => {
    cy.get("#PRIMARY_MENU_NAV_BTN_CONFIGURATIONS").click();

    cy.findByText(/Managed Entities/i);

    cy.findByText(/AWSME/i).click();
    cy.findByText("Overview").click();
    cy.findAllByText(/Information/i);
    cy.findAllByText(/Monitoring/i);

    cy.findByText("Logs").click();
    cy.findAllByText(/Timestamp/i);

    cy.findByText("Variables").click();
    cy.findAllByText(/No Variables found/i);

    cy.findByText("Configure").click();
    cy.findAllByText(/no Deployment Setting/i);

    cy.findByText("History").click();
    cy.findAllByText(/Backup/i);
    cy.findAllByText(/Restore/i);

    cy.findByText(/Back to Managed Entity List/i).click();

    cy.findByText("Logs").click();
    cy.findAllByText(/Timestamp/i);

    cy.findByText(/Microservices/i).click();
    cy.get("#CONFIGURATION_TABLE_SORT_mod_date").should(
      "have.class",
      "MuiTableSortLabel-active"
    );
    cy.get("#CONFIGURATION_TABLE_SORT_name").click();
    cy.get("#CONFIGURATION_TABLE_SORT_name").should(
      "have.class",
      "MuiTableSortLabel-active"
    );

    cy.findAllByText(/Deployment Settings/i)
      .first()
      .click();
    cy.findByText(/Deployment Setting Name/i);

    cy.findByText("Monitoring Profiles").click();
    cy.findAllByText(/Create Monitoring Profile/i);
  });

  it("navigates to the Automation tab and its sub-sections", () => {
    cy.get("#PRIMARY_MENU_NAV_BTN_AUTOMATION").click();

    cy.findAllByText(/BPM/i).first();
    cy.findByText(/No BPM diagrams found/i);

    cy.findByText(/Workflows/i).click();
    cy.findAllByText(/CreateCustomer/i).last();
  });

  it("navigates to the Settings tab", () => {
    cy.findByText(/Settings/i).click();
    cy.findByText(/Product Information/i);
    cy.findByText(/License Information/i);
    cy.findByText(/MSA Variables/i);
  });

  it("navigates to the Profile tab", () => {
    cy.findByText(/Profile/i).click();
    cy.findByText(/Authentication/i);

    cy.findByText(/Audit Logs/i).click();
    cy.findByText(/Timestamp/i);
  });
});
