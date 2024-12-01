# Desative o backend remoto temporariamente
# terraform {
#   backend "azurerm" {
#     resource_group_name  = "airbnb-rg"
#     storage_account_name = "airbnbstorageacct"
#     container_name       = "terraform-state"
#     key                  = "terraform.tfstate"
#   }
# }

# Configuração do Provedor Azure
provider "azurerm" {
  features {}
}

# 1. Resource Group
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

# 2. Storage Account (Blob Storage)
resource "azurerm_storage_account" "storage" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# Containers para Camadas de Dados
resource "azurerm_storage_container" "raw" {
  name                  = var.raw_container
  storage_account_id  = azurerm_storage_account.storage.id
  container_access_type = "private"
}

resource "azurerm_storage_container" "bronze" {
  name                  = var.bronze_container
  storage_account_id  = azurerm_storage_account.storage.id
  container_access_type = "private"
}

resource "azurerm_storage_container" "silver" {
  name                  = var.silver_container
  storage_account_id  = azurerm_storage_account.storage.id
  container_access_type = "private"
}

resource "azurerm_storage_container" "gold" {
  name                  = var.gold_container
  storage_account_id  = azurerm_storage_account.storage.id
  container_access_type = "private"
}

# 3. SQL Server (Opcional - Demonstração)
resource "azurerm_mssql_server" "sqlserver" {
  name                         = "airbnbsqlserver"
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = var.location
  administrator_login          = var.sql_admin_user
  administrator_login_password = var.sql_admin_password
  version                      = "12.0"
}

# 4. SQL Database (Opcional - Demonstração)
resource "azurerm_mssql_database" "sqldb" {
  name        = "airbnbdb"
  server_id   = azurerm_mssql_server.sqlserver.id
  sku_name    = "Basic"
  max_size_gb = 2
}

# 5. Configuração do Container para o Estado do Terraform
resource "azurerm_storage_container" "terraform_state" {
  name                  = "terraform-state"
  storage_account_id  = azurerm_storage_account.storage.id
  container_access_type = "private"
}
