resource "kubernetes_persistent_volume_claim" "msa-es" {

  metadata {
    name = "msa-es"
    labels = {
      service = "msa-es"
    }
  }
  spec {
    access_modes = ["ReadWriteMany"]
    resources {
      requests = {
        storage = var.msa2_es_pvc
      }
    }
    storage_class_name = "azurefile"
  }
}
