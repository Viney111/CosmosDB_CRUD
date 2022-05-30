'''
    @Author: Viney Khaneja
    @Date: 2022-05-28 13:12
    @Last Modified by: Viney Khaneja
    @Last Modified time: None
    @Title : Implementing CRUD in Azure CosmosDB (Mongo API)
'''

from hashlib import new
from pymongo import  MongoClient
import os
import json

class azure_cosmosdb_MONGO_CRUD():
    # Setting up Connection with Azure CosmosDB
    conn_str = os.getenv('PRIMARY_CONN_STR')
    client = MongoClient(conn_str)
    db = client['Employee']
    collection = db['emp_info']
    
    def insert_dummy_data(self):
        """
            Description: Adding Dummy Data from json file into Azure CosmosDB
            Parametres: None
            Returns: Just post the successful message of uploading data in Azure CosmosDB
        """
        try:
            with open ('dummydata.json') as read_data:
                dummy_data = json.load(read_data)
            for data in dummy_data:
                self.collection.insert_one(data)
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
            self.collection.insert_one(data)
        except Exception as ex:
            print(ex)
        else:
            print("Successfully uploaded the data")
    
    
    def reading_data(self):
        """
            Description: Reading Data from Azure CosmosDB
            Parametres: None
            Returns: Just prints the items present in CosmosDB Container
        """
        try:
            list_of_items = []
            for item in self.collection.find():
                list_of_items.append(item)
        except Exception as ex:
            print(ex)
        else:
            return list_of_items
    
    
    def reading_data_by_ID(self,id):
        """
            Description: Reading Data from Azure CosmosDB with specific id
            Parametres: None
            Returns: Just prints the items present in CosmosDB Container
        """
        try:
            item = self.collection.find_one({"_id":id})
            if item is None:
                return None
        except Exception as ex:
            print(ex)
        else:
            return item


    def updating_data_by_id(self,updated_data):
        """
            Description: Updating Data in Azure CosmosDB with specific id
            Parametres: None
            Returns: Just successfull message for updation
        """
        try:
            item_tobe_updated = self.collection.find_one({"_id":updated_data['_id']})
            print (item_tobe_updated['_id'])
            if item_tobe_updated is None:
                return None
        except Exception as ex:
            print(ex)
        else:
            condition = {"_id":updated_data['_id']}
            new_values = {"$set": updated_data}
            self.collection.update_one(condition,new_values)
            return "Updated Successfully"
            
        
        
    def deleting_data(self,id):
        """
            Description: Deleting Data from Azure CosmosDB by ID
            Parametres: None
            Returns: Just deleted the data and posts successful message
        """
        try:
            query = {"_id": id }
            item = self.collection.find_one(query)
            if item is not None:
                self.collection.delete_one(query)
            else:
                return "Id does not exist"
        except Exception as ex:
            print(ex)
        else:
            print("Sucessfully Deleted the data")
            return None

# mongo_obj = azure_cosmosdb_MONGO_CRUD()
# mongo_obj.insert_dummy_data()

