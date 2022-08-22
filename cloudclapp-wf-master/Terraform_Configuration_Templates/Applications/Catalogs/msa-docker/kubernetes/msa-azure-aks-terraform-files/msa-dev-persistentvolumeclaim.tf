resource "kubernetes_persistent_volume_claim" "msa-dev" {

  metadata {
    name = "msa-dev"
    labels = {
      service = "msa-dev"
    }
  }
  spec {
    access_modes = ["ReadWriteMany"]
    resources {
      requests = {
        storage = var.msa2_dev_pvc
      }
    }
    storage_class_name = "azurefile"
  }
}
