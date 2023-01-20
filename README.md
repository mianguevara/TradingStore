## Step 1: Create a DynamoDB table**

You use a [DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html) table to store data for your API.

Each item has a unique ID, which we use as the [partition key](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html#HowItWorks.CoreComponents.PrimaryKey) for the table.

**To create a DynamoDB table**

1. Open the DynamoDB console at [https://console.aws.amazon.com/dynamodb/](https://console.aws.amazon.com/dynamodb/).
2. Choose  **Create table**.
3. For  **Table name** , enter  **http-crud-tutorial-items**.
4. For  **Partition key** , enter  **id**.
5. Choose  **Create table**.

## Step 2: Create a Lambda function

You create a [Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html) function for the backend of your API. This Lambda function creates, reads, updates, and deletes items from DynamoDB. The function uses [events from API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html#http-api-develop-integrations-lambda.proxy-format) to determine how to interact with DynamoDB. For simplicity this tutorial uses a single Lambda function. As a best practice, you should create separate functions for each route.

###### To create a Lambda function

1. Sign in to the Lambda console at [https://console.aws.amazon.com/lambda](https://console.aws.amazon.com/lambda).
2. Choose  **Create function**.
3. For  **Function name** , enter  **http-crud-tutorial-function**.
4. Under  **Permissions**  choose  **Change default execution role**.
5. Select  **Create a new role from AWS policy templates**.
6. For  **Role name** , enter  **http-crud-tutorial-role**.
7. For  **Policy templates** , choose  **Simple microservice permissions**. This policy grants the Lambda function permission to interact with DynamoDB.
8. Edit the policy template and add in action **"dynamodb:DescribeTable"**
9. Choose  **Create function**.
10. Add **AWSSDKPandas-Python39** in layer of http-crud-tutorial-function and its allows import pandas
11. Open lamda\_function.py in the console's code editor, and replace its contents with the following code. Choose  **Deploy**  to update your function.


## Step 3: Create an HTTP API

The HTTP API provides an HTTP endpoint for your Lambda function. In this step, you create an empty API. In the following steps, you configure routes and integrations to connect your API and your Lambda function.

###### To create an HTTP API

1. Sign in to the API Gateway console at [https://console.aws.amazon.com/apigateway](https://console.aws.amazon.com/apigateway).
2. Choose  **Create API** , and then for  **HTTP API** , choose  **Build**.
3. For  **API name** , enter  **http-trading-api**.
4. Choose  **Next**.
5. For  **Configure routes** , choose  **Next**  to skip route creation. You create routes later.
6. Review the stage that API Gateway creates for you, and then choose  **Next**.
7. Choose  **Create**.

## Step 4: Create routes

Routes are a way to send incoming API requests to backend resources. Routes consist of two parts: an HTTP method and a resource path, for example, GET /items. For this example API, we create tree routes:

- GET /items
- GET /balance
- PUT /ítems

###### To create routes

1. Sign in to the API Gateway console at [https://console.aws.amazon.com/apigateway](https://console.aws.amazon.com/apigateway).
2. Choose your API.
3. Choose  **Routes**.
4. Choose  **Create**.
5. For  **Method** , choose  **GET**.
6. For the path, enter  **/items**
7. Choose  **Create**.
8. Repeat steps 4-7 for GET /balance and PUT /items.

## Step 5: Create an integration

You create an integration to connect a route to backend resources. For this example API, you create one Lambda integration that you use for all routes.

###### To create an integration

1. Sign in to the API Gateway console at [https://console.aws.amazon.com/apigateway](https://console.aws.amazon.com/apigateway).
2. Choose your API.
3. Choose  **Integrations**.
4. Choose  **Manage integrations**  and then choose  **Create**.
5. Skip  **Attach this integration to a route**. You complete that in a later step.
6. For  **Integration type** , choose  **Lambda function**.
7. For  **Lambda function** , enter  **http-crud-tutorial-function**.
8. Choose  **Create**.

## Step 6: Attach your integration to routes

For this example API, you use the same Lambda integration for all routes. After you attach the integration to all of the API's routes, your Lambda function is invoked when a client calls any of your routes.

###### To attach integrations to routes

1. Sign in to the API Gateway console at [https://console.aws.amazon.com/apigateway](https://console.aws.amazon.com/apigateway).
2. Choose your API.
3. Choose  **Integrations**.
4. Choose a route.
5. Under  **Choose an existing integration** , choose  **http-crud-tutorial-function**.
6. Choose  **Attach integration**.
7. Repeat steps 4-6 for all routes.

All routes show that an AWS Lambda integration is attached.

## Step 7: Test your API

To make sure that your API is working, you use POSTMAN.

###### To get the URL to invoke your API

1. Sign in to the API Gateway console at [https://console.aws.amazon.com/apigateway](https://console.aws.amazon.com/apigateway).
2. Choose your API.
3. Note your API's invoke URL. It appears under  **Invoke URL**  on the  **Details**  page.
4. Copy your API's invoke URL.

The full URL looks like https://_abcdef123_.execute-api._us-west-2_.amazonaws.com.

 **1. Insert items:**

    Method: PUT

    https://abcdef123.execute-api.us-west-2.amazonaws.com/items?ticker=SPY&timenow=1/20/2023&11:45:20&AM&type\_option=CALL&type\_operation=OPEN&prime=500&spot\_price=370&strike\_price=400

    Query Params

    ticker: SPY, timenow: 1/20/2023 11:45:20 AM, type\_option: CALL, type\_operation: OPEN, prime: 500, spot\_price: 370, strike\_price: 400

 **2. Get items:**

    Method: GET

    https://abcdef123.execute-api.us-west-2.amazonaws.com/items?id=1

    Query Params

    id: 1

 **3. Get balance:**

    Method: GET

    https://abcdef123.execute-api.us-west-2.amazonaws.com/items/balance
