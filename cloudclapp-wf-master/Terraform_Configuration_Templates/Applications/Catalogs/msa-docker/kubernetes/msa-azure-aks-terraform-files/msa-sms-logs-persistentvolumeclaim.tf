resource "kubernetes_persistent_volume_claim" "msa-sms-logs" {

  metadata {
    name = "msa-sms-logs"
    labels = {
      service = "msa-sms-logs"
    }
  }
  spec {
    access_modes = ["ReadWriteMany"]
    resources {
      requests = {
        storage = var.msa2_sms_logs_pvc
      }
    }
    storage_class_name = "azurefile"
  }
}
