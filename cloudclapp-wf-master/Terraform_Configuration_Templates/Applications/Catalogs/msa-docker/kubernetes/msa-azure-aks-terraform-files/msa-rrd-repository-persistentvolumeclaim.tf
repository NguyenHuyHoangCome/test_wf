resource "kubernetes_persistent_volume_claim" "rrd-repository" {

  metadata {
    name = "rrd-repository"
    labels = {
      service = "rrd-repository"
    }
  }
  spec {
    access_modes = ["ReadWriteMany"]
    resources {
      requests = {
        storage = var.msa2_rrd_repository_pvc
      }
    }
    storage_class_name = "azurefile"
  }
}
