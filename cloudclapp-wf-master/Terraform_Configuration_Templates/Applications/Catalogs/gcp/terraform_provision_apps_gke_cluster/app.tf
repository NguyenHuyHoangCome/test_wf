resource "kubernetes_deployment" "app_deploy" {
  metadata {
    name = "app_name"
    labels = {
      App = "app_label"
    }
  }

  spec {
    replicas = app_replicas 
    selector {
      match_labels = {
        App = "app_label"
      }
    }
    template {
      metadata {
        labels = {
          App = "app_label"
        }
      }
      spec {
        container {
          image = "app_image"
          name  = "app_container_name"
          port {
            container_port = "app_port"
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "app_service" {
  depends_on = [
    kubernetes_deployment.app_deploy,
  ]
  metadata {
    name = "app-service"
  }
  spec {
    selector = {
      App = kubernetes_deployment.app_deploy.spec.0.template.0.metadata[0].labels.App
    }
    port {
      port        = "app_port"
      #node_port   = "app_node_port"
    }

    type = "LoadBalancer"
  }
}

output "app_lb_ip" {
  value = kubernetes_service.app_service.status.0.load_balancer.0.ingress.0.ip
}
