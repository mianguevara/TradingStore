import json
import boto3
import pandas as pd

dynamo = boto3.resource("dynamodb")

tableName = dynamo.Table("http-crud-tutorial-items")

GET_RAW_PATH = "GET /items"
GET_BALANCE = "GET /balance"
CREATE_RAW_PATH = "PUT /items"


def lambda_handler(event, context):
    
    # Return an especific item with id
    def get_item_function():

        items = tableName.get_item(Key={"id": event["queryStringParameters"]["id"]})

        return items["Item"]
        
    #Return the balance of the operations
    def get_balance_function():
        
        items = tableName.scan()
        
        items = items['Items']
        
        df = pd.DataFrame(items)
        
        df = df.sort_values(by=['id']).reset_index(drop = True)
        
        saldo = 0
        
        if df.loc[df.index[-1], "type_operation"] == 'OPEN':
            
            end_df = len(df)-2
            
        else:
            end_df = len(df)
            
        for i in range (0,end_df,2):
            
            saldo += int(df.iloc[i+1]['prime']) - int(df.iloc[i]['prime'])

        return saldo

    # Put the operation data into the dynamodb
    def put_item_function():

        items = tableName.put_item(
            Item={
                "id": str(item_count+1),
                "ticker": event["queryStringParameters"]["ticker"],
                "timenow": event["queryStringParameters"]["timenow"],
                "type_option": event["queryStringParameters"]["type_option"],
                "type_operation": event["queryStringParameters"]["type_operation"],
                "prime": event["queryStringParameters"]["prime"],
                "spot_price": event["queryStringParameters"]["spot_price"],
                "strike_price": event["queryStringParameters"]["strike_price"]
                
            }
        )

        return items["ResponseMetadata"]["HTTPStatusCode"]

    item_count = 0

    response = tableName.scan()

    # Track number of Items read
    item_count += len(response["Items"])

    # First, detect if there are data
    if item_count == 0:

        if (event["routeKey"] == GET_RAW_PATH):

            response = "No data"
            
        elif (event["routeKey"] == GET_BALANCE):

            response = "No data"

        elif event["routeKey"] == CREATE_RAW_PATH:

            if event["queryStringParameters"]["type_operation"] == "OPEN":

                response = put_item_function()

            else:

                response = "No data, you cant"

    else:

        if event["routeKey"] == GET_RAW_PATH:

            response = get_item_function()

        elif event["routeKey"] == CREATE_RAW_PATH:

            items = tableName.get_item(Key={"id": str(item_count)})

            ticker = items["Item"]["ticker"]

            type_operation = items["Item"]["type_operation"]

            type_option = items["Item"]["type_option"]

            if ticker == event["queryStringParameters"]["ticker"]:

                if type_operation == "CLOSE":

                    if event["queryStringParameters"]["type_operation"] == "CLOSE":

                        response = "You must open, the last operation was closing"

                    else:

                        response = put_item_function()

                elif (type_option == "CALL" and type_operation == "OPEN"):

                    if event["queryStringParameters"]["type_option"] == "PUT":

                        response = "You must first close the operation that is open"

                    elif (event["queryStringParameters"]["type_option"] == "CALL"
                        and event["queryStringParameters"]["type_operation"] == "OPEN"):

                        response = "You cannot open another trade"

                    else:

                        response = put_item_function()

                elif (type_option == "PUT" and type_operation == "OPEN"):

                    if event["queryStringParameters"]["type_option"] == "CALL":

                        response = "You must first close the operation that is open"

                    elif (event["queryStringParameters"]["type_option"] == "PUT"
                        and event["queryStringParameters"]["type_option"] == "OPEN"):

                        response = "You cannot open another trade"

                    else:

                        response = put_item_function()

            else:

                if type_operation == "CLOSE":
                    
                    if event["queryStringParameters"]["type_option"] == "OPEN":

                        response = put_item_function()
                    
                    else:
                        
                        response = "You cant close, there are no an open trade with this ticker"

                else:
                    response = "You cant open or close a different ticker"

        elif event["routeKey"] == GET_BALANCE:
            
            response = get_balance_function()

    return {"response": response}
