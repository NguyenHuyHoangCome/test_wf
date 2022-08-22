resource "kubernetes_persistent_volume_claim" "msa-bulkfiles" {

  metadata {
    name = "msa-bulkfiles"
    labels = {
      service = "msa-bulkfiles"
    }
  }
  spec {
    access_modes = ["ReadWriteMany"]
    resources {
      requests = {
        storage = "100Mi"
      }
    }
    storage_class_name = "azurefile"
  }
}
