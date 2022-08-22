resource "kubernetes_persistent_volume_claim" "msa-api" {

  metadata {
    name = "msa-api"
    labels = {
      service = "msa-api"
    }
  }
  spec {
    access_modes = ["ReadWriteMany"]
    resources {
      requests = {
        storage = var.msa2_api_pvc
      }
    }
    storage_class_name = "azurefile"
  }
}
