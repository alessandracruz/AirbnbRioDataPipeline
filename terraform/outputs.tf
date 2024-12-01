output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}

output "storage_account_name" {
  value = azurerm_storage_account.storage.name
}

output "blob_containers" {
  value = [
    azurerm_storage_container.raw.name,
    azurerm_storage_container.bronze.name,
    azurerm_storage_container.silver.name,
    azurerm_storage_container.gold.name
  ]
}

output "sql_server_name" {
  value = azurerm_mssql_server.sqlserver.name
}

output "sql_database_name" {
  value = azurerm_mssql_database.sqldb.name
}
