resource "kubernetes_persistent_volume_claim" "msa-repository" {

  metadata {
    name = "msa-repository"
    labels = {
      service = "msa-repository"
    }
  }
  spec {
    access_modes = ["ReadWriteMany"]
    resources {
      requests = {
        storage = var.msa2_repository_pvc
      }
    }
    storage_class_name = "azurefile"
  }
}
