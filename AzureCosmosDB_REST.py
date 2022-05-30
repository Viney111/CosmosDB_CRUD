'''
    @Author: Viney Khaneja
    @Date: 2022-05-27 10:13
    @Last Modified by: Viney Khaneja
    @Last Modified time: None
    @Title : IAzure CosmosDB with REST API
'''

# Importing required modules
from flask import Flask, request, make_response
from flask_restful import Api
from werkzeug.exceptions import HTTPException, Aborter
import json
# from cosmos_SQL_API_crud import azure_cosmosdb_SQL_CRUD
from cosmos_Mongo_API_crud import azure_cosmosdb_MONGO_CRUD


# Initializing Flask for implementing API
app = Flask(__name__)
api = Api(app)
# crud_azure = azure_cosmosdb_SQL_CRUD()
crud_azure = azure_cosmosdb_MONGO_CRUD()
abort = Aborter()


@app.route("/empdata", methods=['GET'])
def get():
    """
        Description: This function is to retrieve data from Specified URL
        Parameters: None, just defined router path.
        Returns: A dictionary of requested data and response code to client
    """
    try:
        supporting_data = crud_azure.reading_data()
        return make_response({"emp" :supporting_data}, 200)
    except Exception as ex:
        print(ex)


@app.route("/empdata/<string:emp_id>", methods=['GET'])
def get_by_id(emp_id):
    """
        Description: This function is to retrieve data from Specified URL with employee ID
        Parameters: None, just defined router path.
        Returns: A dictionary of requested data and response code to client
    """
    try:
        supporting_data = crud_azure.reading_data_by_ID(emp_id)
        if supporting_data is None:
            abort(404, description="ID is not valid, Please enter correct ID")
        return make_response({"emp" :supporting_data}, 200)
    except HTTPException as ex:
        return handle_exception(ex)
    except Exception as ex:
        print(ex)


@app.route("/empdata", methods=['POST'])
def post():
    """
        Description: This function is to post data to MSSQL Database
        Parameters: None, just defined router path.
        Returns: A descriptive message of posting and response code to client
    """
    posted_data = json.loads(request.data)
    try:
        crud_azure.adding_data(posted_data)
    except Exception as ex:
        print(ex)
    else:
        return make_response("Posted Successfully", 201)

@app.route("/empdata/<string:emp_id>", methods=['DELETE'])
def delete(emp_id):
    """
        Description: This function is to delete data from AzureCosmosDb
        Parameters: Employee ID
        Returns: A descriptive message of deleting(if id exists) and response code to client
    """
    try:
        del_result = crud_azure.deleting_data(emp_id)
        if del_result != None:
            abort(404, description="ID is not valid, Please enter correct ID")
    except HTTPException as ex:
        return handle_exception(ex)
    except Exception as ex:
        print(ex)
    else:
        return make_response("Deleted Successfully", 202)
    


@app.route("/empdata", methods=['PATCH'])
def update():
    """
        Description: This function is to update data to AzureCosmosDb
        Parameters: None
        Returns: A descriptive message of updating(if id exists) and response code to client
    """
    updated_data = json.loads(request.data)
    print(updated_data)
    try:
        update_msg = crud_azure.updating_data_by_id(updated_data)
        if update_msg is None:
            abort(404, description="ID is not valid, Please enter correct ID")
    except HTTPException as ex:
        return handle_exception(ex)
    except Exception as ex:
        print(ex)
    else:
        return make_response("Updated Successfully", 202)

          
@app.errorhandler(HTTPException)
def handle_exception(e):
    """
        Description: This function is to handle abort statements
        Parameters: Abort Status Code HTTP Exceptions
        Returns: Return JSON instead of HTML for HTTP errors.
    """
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "description": e.description,
    })
    response.content_type = "application/json"
    return response   

      
if __name__ == '__main__':
    app.run(debug=True)