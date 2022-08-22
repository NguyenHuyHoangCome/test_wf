resource "kubernetes_persistent_volume_claim" "msa-bud-logs" {

  metadata {
    name = "msa-bud-logs"
    labels = {
      service = "msa-bud-logs"
    }
  }
  spec {
    access_modes = ["ReadWriteMany"]
    resources {
      requests = {
        storage = var.msa2_bud_logs_pvc
      }
    }
    storage_class_name = "azurefile"
  }
}
