resource "kubernetes_persistent_volume_claim" "msa-entities" {

  metadata {
    name = "msa-entities"
    labels = {
      service = "msa-entities"
    }
  }
  spec {
    access_modes = ["ReadWriteMany"]
    resources {
      requests = {
        storage = var.msa2_entities_pvc
      }
    }
    storage_class_name = "azurefile"
  }
}
