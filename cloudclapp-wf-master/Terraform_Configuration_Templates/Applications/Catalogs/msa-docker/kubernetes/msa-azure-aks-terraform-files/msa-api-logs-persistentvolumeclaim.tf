resource "kubernetes_persistent_volume_claim" "msa-api-logs" {

  metadata {
    name = "msa-api-logs"
    labels = {
      service = "msa-api-logs"
    }
  }
  spec {
    access_modes = ["ReadWriteMany"]
    resources {
      requests = {
        storage = var.msa2_api_logs_pvc
      }
    }
    storage_class_name = "azurefile"
  }
}
