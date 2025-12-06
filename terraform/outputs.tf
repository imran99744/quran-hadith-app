output "droplet_ip" {
  value = digitalocean_droplet.quran_hadith.ipv4_address
  description = "The public IP address of the Quran Hadith API droplet"
}

output "droplet_name" {
  value = digitalocean_droplet.quran_hadith.name
  description = "The name of the created droplet"
}

output "ssh_command" {
  value = "ssh root@${digitalocean_droplet.quran_hadith.ipv4_address}"
  description = "SSH command to connect to the droplet"
}

output "api_url" {
  value = "http://${digitalocean_droplet.quran_hadith.ipv4_address}:8000"
  description = "URL to access the Quran Hadith API"
}

output "docs_url" {
  value = "http://${digitalocean_droplet.quran_hadith.ipv4_address}:8000/docs"
  description = "URL to access the API documentation"
}
