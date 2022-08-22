resource "kubernetes_persistent_volume_claim" "msa-svn" {

  metadata {
    name = "msa-svn"
    labels = {
      service = "msa-svn"
    }
  }
  spec {
    access_modes = ["ReadWriteMany"]
    resources {
      requests = {
        storage = var.msa2_svn_pvc
      }
    }
    storage_class_name = "azurefile"
  }
}
