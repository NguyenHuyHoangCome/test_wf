provider "kubernetes" {
  config_path = "./kube_config"
  insecure    = "true"
}

resource "kubernetes_namespace" "my-app" {
  metadata {
    name = var.namespace
    labels = {
      "terraform" = "true"
    }
  }
}

resource "kubernetes_config_map" "nginx-config-cmap" {
  metadata {
    name      = "nginx-config-cmap"
    namespace = kubernetes_namespace.my-app.metadata.0.name
    labels = {
      "app"       = "front"
      "terraform" = "true"
    }
  }

  data = {
    "my-web-app.conf" = templatefile("./src/nginx.tftpl", {
                            FRONTEND_PORT = var.frontend_port,
                            BACKEND_URL   = "http://${kubernetes_service.back-end-svc.metadata.0.name}.${kubernetes_namespace.my-app.metadata.0.name}.svc.cluster.local:${var.backend_port}${var.route}"
                        })
    }
}

resource "kubernetes_config_map" "py-config-cmap" {
  metadata {
    name      = "py-config-cmap"
    namespace = kubernetes_namespace.my-app.metadata.0.name
    labels = {
      "app"       = "back"
      "terraform" = "true"
    }
  }

  data = {
    "main.py" = templatefile("./src/python.tftpl", {
                    MESSAGE           = var.message
                    BACKEND_IFADDRESS = var.backend_ifaddress,
                    BACKEND_PORT      = var.backend_port,
                    ROUTE             = var.route
                })
  }
}

resource "kubernetes_pod" "front-end" {
  metadata {
    name      = "front-end"
    namespace = kubernetes_namespace.my-app.metadata.0.name
    labels = {
      "app"       = "front"
      "terraform" = "true"
    }
  }

  spec {
    container {
      name  = "front-end"
      image = var.front_image

      port {
        container_port = var.frontend_port
      }

      volume_mount {
        mount_path = "/etc/nginx/conf.d/"
        name       = "nginx-config"
      }
    }

    volume {
      name = "nginx-config"
      config_map {
        name = kubernetes_config_map.nginx-config-cmap.metadata.0.name
      }
    }
  }
}

resource "kubernetes_pod" "back-end" {
  metadata {
    name      = "back-end"
    namespace = kubernetes_namespace.my-app.metadata.0.name
    labels = {
      "app"       = "back"
      "terraform" = "true"
    }
  }

  spec {
    container {
      name  = "back-end"
      image = var.back_image

      port {
        container_port = var.backend_port
      }

      volume_mount {
        mount_path = "/home/"
        name       = "python-config"
      }
    }

    volume {
      name = "python-config"
      config_map {
        name         = kubernetes_config_map.py-config-cmap.metadata.0.name
        default_mode = "0755"
      }
    }
  }

}

resource "kubernetes_service" "front-end-svc" {
  metadata {
    name      = "fron-end"
    namespace = kubernetes_namespace.my-app.metadata.0.name
    labels = {
      "app"       = "front"
      "terraform" = "true"
    }
  }

  spec {
    type = "NodePort"

    selector = {
      "app" = "front"
    }

    port {
      name      = "${var.frontend_port}"
      port      = var.frontend_port
      node_port = var.node_port
      protocol  = "TCP"
    }
  }
}

resource "kubernetes_service" "back-end-svc" {
  metadata {
    name      = "back-end"
    namespace = kubernetes_namespace.my-app.metadata.0.name
    labels = {
      "app"       = "back"
      "terraform" = "true"
    }
  }

  spec {
    type = "ClusterIP"

    selector = {
      "app" = "back"
    }

    port {
      name     = "${var.backend_port}"
      port     = var.backend_port
      protocol = "TCP"
    }
  }
}
