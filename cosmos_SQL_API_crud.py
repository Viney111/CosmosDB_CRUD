'''
    @Author: Viney Khaneja
    @Date: 2022-05-26 09:12
    @Last Modified by: Viney Khaneja
    @Last Modified time: None
    @Title : Implementing CRUD in Azure CosmosDB (SQL API)
'''

# Importing Required Modules.
from azure.cosmos import CosmosClient
import os
import json


class azure_cosmosdb_SQL_CRUD():
    
    # Setting up Connection with Azure CosmosDB
    url = os.getenv('Account_URL')
    key = os.getenv('Account_KEY')
    client = CosmosClient(url,credential=key)
    DATABASE_NAME = "ToDoList"
    database = client.get_database_client(DATABASE_NAME)
    CONTAINER_NAME = "tbl_emp"
    container = database.get_container_client(CONTAINER_NAME)


    def adding_dummy_data(self):    
        """
            Description: Adding Dummy Data from json file into Azure CosmosDB
            Parametres: None
            Returns: Just post the successful message of uploading data in Azure CosmosDB
        """
        try:
            with open ('dummydata.json') as read_data:
                dummy_data = json.load(read_data)
            for data in dummy_data:
                self.container.upsert_item(data)
        except Exception as ex:
            print(ex)
        else:
            print("Successfully uploaded the dummy data")

    def adding_data(self,data):
        """
            Description: Adding Data into Azure CosmosDB from PostMan
            Parametres: None
            Returns: Just post the successful message of uploading data in Azure CosmosDB
        """
        try:
            self.container.upsert_item(data)
        except Exception as ex:
            print(ex)
        else:
            print("Successfully uploaded the data")
               
    def deleting_data(self,id):
        """
            Description: Deleting Data from Azure CosmosDB by ID
            Parametres: None
            Returns: Just deleted the data and posts successful message
        """
        try:
            for item in self.container.query_items(
                    query=f'SELECT * FROM c where c.id = {id}',
                    enable_cross_partition_query=True):
                print(item)
                self.container.delete_item(item, partition_key='id')
        except Exception as ex:
            print(ex)
            return "Id does not exist"
        else:
            print("Sucessfully Deleted the data")
            return None
        
    def reading_data(self):
        """
            Description: Reading Data from Azure CosmosDB
            Parametres: None
            Returns: Just prints the items present in CosmosDB Container
        """
        try:
            list_of_items = []
            for item in self.container.query_items(
            query='SELECT * FROM c',
            enable_cross_partition_query=True):
                list_of_items.append(item)
        except Exception as ex:
            print(ex)
        else:
            return list_of_items
