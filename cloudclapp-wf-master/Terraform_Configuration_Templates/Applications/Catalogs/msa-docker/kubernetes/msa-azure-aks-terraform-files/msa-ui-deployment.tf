resource "kubernetes_deployment" "msa-ui" {

  metadata {
    name = "msa-ui"
    labels = {
      service = "msa-ui"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        service = "msa-ui"
      }
    }
    strategy {
      type = "Recreate"
    }
    template {
      metadata {
        labels = {
          network_quickstart-default = "true"
          service                    = "msa-ui"
        }
      }
      spec {
        container {
          image = var.msa2_ui_img
          name  = "msa-ui"
          env {
            name  = "FEATURE_ADMIN"
            value = "true"
          }
          env {
            name  = "FEATURE_AI_ML"
            value = "true"
          }
          env {
            name  = "FEATURE_ALARMS"
            value = "true"
          }
          env {
            name  = "FEATURE_CONNECTION_STATUS"
            value = "true"
          }
          env {
            name  = "FEATURE_LICENCE"
            value = "true"
          }
          env {
            name  = "FEATURE_MONITORING_PROFILES"
            value = "true"
          }
          env {
            name  = "FEATURE_PERMISSION_PROFILES"
            value = "true"
          }
          env {
            name  = "FEATURE_PROFILE_AUDIT_LOGS"
            value = "true"
          }
          env {
            name  = "FEATURE_SCHEDULE_WORKFLOWS"
            value = "true"
          }
          env {
            name  = "FEATURE_TOPOLOGY"
            value = "true"
          }
          env {
            name  = "FEATURE_WORKFLOW_OWNER"
            value = "false"
          }
          port {
            container_port = 8080
          }
          liveness_probe {
            exec {
              command = ["curl --fail http://localhost:8080"]
            }
          }
        }
        restart_policy = "Always"
      }
    }
  }
}
