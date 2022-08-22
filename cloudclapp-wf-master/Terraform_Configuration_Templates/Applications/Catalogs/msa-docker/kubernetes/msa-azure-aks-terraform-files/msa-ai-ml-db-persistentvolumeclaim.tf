resource "kubernetes_persistent_volume_claim" "msa-ai-ml-db" {

  metadata {
    name = "msa-ai-ml-db"
    labels = {
      service = "msa-ai-ml-db"
    }
  }
  spec {
    access_modes = ["ReadWriteMany"]
    resources {
      requests = {
        storage = var.msa2_ai_ml_db_pvc
      }
    }
    storage_class_name = "azurefile"
  }
}
