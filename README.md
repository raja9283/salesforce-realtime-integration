# Salesforce Real-time Integration using AWS S3 and Lambda

## Project Overview
This project demonstrates how to send data to Salesforce in real-time using AWS S3 and Lambda. The use case for this approach arises from a limitation in AWS AppFlow, which, while capable of integrating Salesforce with AWS services, does not support event-driven triggers when Salesforce is set as the destination. To overcome this, we utilize S3 events and a Lambda function to push data into Salesforce.

The project currently handles **Contacts**, **Leads**, and **Opportunities**. It can create new records or update existing ones based on the input data. The implementation uses the `simple-salesforce` package to interact with the Salesforce API.

## Architecture Overview

1. **S3 Events**: When a new file is uploaded to the S3 bucket, it triggers an event.
2. **AWS Lambda**: The Lambda function is invoked by the S3 event, which processes the file and sends the data to Salesforce.
3. **Salesforce Integration**: The function uses `simple-salesforce` to either create or update records in Salesforce.

## Prerequisites

- AWS account with permissions to create Lambda functions, S3 buckets, and Lambda layers.
- Salesforce account with API access.
- `simple-salesforce` package added as a Lambda layer.

## AWS Setup

1. **Create an S3 Bucket**: Create an S3 bucket to hold the input files.
2. **Create a Lambda Function**: Create a Lambda function and attach the S3 trigger to it.
3. **Add Layers to Lambda**:
   - Include the `simple-salesforce` layer from the repository.
   - Attach the AWSSDKPandas-Python312 built-in layer for Python dependencies.

## Setting Up Salesforce

In Salesforce, create connected app credentials to allow API access. Update the Lambda function environment variables with your Salesforce credentials:

- `SALESFORCE_USERNAME`
- `SALESFORCE_PASSWORD`
- `SALESFORCE_SECURITY_TOKEN`

## How to Run

1. Upload the sample data file to the S3 bucket.
2. This triggers the Lambda function.
3. The function reads the S3 file, processes the data, and uses `simple-salesforce` to create or update records in Salesforce.

## Repository Contents

- **`lambda_function.py`**: The core Lambda function code.
- **`layers/simple_salesforce/`**: Pre-packaged Lambda layer for the `simple-salesforce` library.
- **`sample_data/`**: Sample input files for new and updated Salesforce records.
- **`README.md`**: Documentation file.

## Lambda Layer Information

### 1. `simple-salesforce` Custom Layer
- Folder: `layers/simple_salesforce/`
- Include this layer in your Lambda function for Salesforce integration.

### 2. AWS Built-in Layer
- ARN: `arn:aws:lambda:ap-south-1:336392948345:layer:AWSSDKPandas-Python312:13`


## Sample Data

The repository contains sample data files for each of the following scenarios:

1. **New Contact Record**: `sample_data/contact.csv`
2. **Updated Lead Record**: `sample_data/leads_update.csv`
3. **New Opportunity Record**: `sample_data/opportunity_new.csv`

## How to Use the S3 Bucket

When uploading data files to the S3 bucket, follow the folder structure below:

- **`<bkt_name>`**: Replace this with your S3 bucket name.
- **`sfdc/contact/`**: This path corresponds to Salesforce Contacts data. Use the following paths based on the data type:
  - For **Leads**: `s3://<bkt_name>/sfdc/lead/<file_name>.csv`
  - For **Opportunities**: `s3://<bkt_name>/sfdc/opportunity/<file_name>.csv`
- **`<file_name>.csv`**: Your data file name. Each file should be in CSV format.

### Example Paths

- `s3://my-s3-bucket/sfdc/contact/contact_data.csv`
- `s3://my-s3-bucket/sfdc/lead/lead_data.csv`
- `s3://my-s3-bucket/sfdc/opportunity/opportunity_data.csv`

Make sure that the Lambda function has the correct permissions to access this S3 bucket and read files from the specified paths.

## Troubleshooting & Debugging

- Check the CloudWatch logs for Lambda function errors.
- Ensure Salesforce API credentials are correctly configured.
- Validate the input data format matches the expected structure.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
