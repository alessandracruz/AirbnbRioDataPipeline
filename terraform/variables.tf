# Variáveis para o Azure
variable "resource_group_name" {
  default = "airbnb-rg"
}

variable "location" {
  default = "brazilsouth"
}

variable "storage_account_name" {
  default = "airbnbstorageacct"
}

variable "sql_admin_user" {
  default = "adminuser"
}

variable "sql_admin_password" {
  description = "Senha para o administrador do SQL Server"
  default     = "P@ssw0rd1234!"
}

# Containers do Blob Storage
variable "raw_container" {
  default = "dataraw"
}

variable "bronze_container" {
  default = "databronze"
}

variable "silver_container" {
  default = "datasilver"
}

variable "gold_container" {
  default = "datagold"
}
