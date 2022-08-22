resource "kubernetes_persistent_volume_claim" "db" {

  metadata {
    name = "msa-db"
    labels = {
      service = "msa-db"
    }
  }
  spec {
    access_modes = ["ReadWriteMany"]
    resources {
      requests = {
        storage = var.msa2_db_pvc
      }
    }
    storage_class_name = "azurefile"
  }
}
