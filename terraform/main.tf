terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

provider "digitalocean" {
  token = var.do_token
}

# SSH Key for accessing the droplet
resource "digitalocean_ssh_key" "default" {
  name       = "quran-hadith-key"
  public_key = file(var.ssh_public_key_path)
}

# Firewall to allow necessary ports
resource "digitalocean_firewall" "quran_hadith" {
  name = "quran-hadith-firewall"

  inbound_rule {
    protocol         = "tcp"
    port_range        = "22"
    source_addresses = ["0.0.0.0/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range        = "80"
    source_addresses = ["0.0.0.0/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range        = "443"
    source_addresses = ["0.0.0.0/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range        = "8000"
    source_addresses = ["0.0.0.0/0"]
  }

  outbound_rule {
    protocol              = "tcp"
    port_range             = "1-65535"
    destination_addresses = ["0.0.0.0/0"]
  }

  outbound_rule {
    protocol              = "udp"
    port_range             = "1-65535"
    destination_addresses = ["0.0.0.0/0"]
  }
}

# Cloud-init script for initial setup
data "cloudinit_config" "setup" {
  gzip = false
  base64_encode = false

  part {
    content_type = "text/x-shellscript"
    content = file("../scripts/setup.sh")
  }
}

# Main droplet
resource "digitalocean_droplet" "quran_hadith" {
  image    = "ubuntu-22-04-x64"
  name     = "quran-hadith-api"
  region   = var.region
  size     = var.droplet_size
  ssh_keys = [digitalocean_ssh_key.default.fingerprint]
  user_data = data.cloudinit_config.setup.rendered

  tags = ["quran-hadith", "api", "production"]
}
