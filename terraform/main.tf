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

# Use existing SSH key from DigitalOcean
data "digitalocean_ssh_key" "default" {
  name = "Imran-ssh-key"
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

# Main droplet
resource "digitalocean_droplet" "quran_hadith" {
  image    = "ubuntu-22-04-x64"
  name     = "quran-hadith-api"
  region   = var.region
  size     = var.droplet_size
  ssh_keys = [data.digitalocean_ssh_key.default.fingerprint]

  tags = ["quran-hadith", "api", "production"]
}
