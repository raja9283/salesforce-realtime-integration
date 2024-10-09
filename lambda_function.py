import json
from simple_salesforce import Salesforce, SalesforceMalformedRequest
import boto3
import csv
import io


def get_parameters():
    """
    Retrieve Salesforce credentials from AWS Systems Manager Parameter Store.
    
    Returns:
        dict: A dictionary containing Salesforce credentials.
    """
    # Create an SSM client
    ssm_client = boto3.client('ssm')
    
    # Retrieve multiple parameters from Parameter Store
    response = ssm_client.get_parameters(
        Names=[
            '/salesforce/username',  # Salesforce username
            '/salesforce/password',   # Salesforce password
            '/salesforce/security_token'  # Salesforce security token
        ],
        WithDecryption=True  # Decrypt SecureString parameters
    )
    
    # Create a dictionary of parameter names and their values
    parameters = {param['Name']: param['Value'] for param in response['Parameters']}
    
    return parameters

def upsert_contact(contact_data):
    """
    Upsert a contact record in Salesforce.
    
    Args:
        contact_data (dict): A dictionary containing contact information.
    """
    try:
        if 'Id' in contact_data and contact_data['Id']:
            # Update existing contact
            contact_id = contact_data.pop('Id')  # Remove ID from data to avoid sending it in the update
            sf.Contact.update(contact_id, contact_data)
            print(f"Updated Contact ID: {contact_id}")
        else:
            # Create new contact
            new_contact = sf.Contact.create(contact_data)
            print(f"Created new Contact ID: {new_contact['id']}")
    except SalesforceMalformedRequest as e:
        print(f"Error occurred while processing contact: {e}")

def upsert_lead(lead_data):
    """
    Upsert a lead record in Salesforce.
    
    Args:
        lead_data (dict): A dictionary containing lead information.
    """
    try:
        if 'Id' in lead_data and lead_data['Id']:
            # Update existing lead
            lead_id = lead_data.pop('Id')  # Remove ID from data to avoid sending it in the update
            sf.Lead.update(lead_id, lead_data)
            print(f"Updated Lead ID: {lead_id}")
        else:
            # Create new lead
            new_lead = sf.Lead.create(lead_data)
            print(f"Created new Lead ID: {new_lead['id']}")
    except SalesforceMalformedRequest as e:
        print(f"Error occurred while processing lead: {e}")

def upsert_opportunity(opportunity_data):
    """
    Upsert an opportunity record in Salesforce.
    
    Args:
        opportunity_data (dict): A dictionary containing opportunity information.
    """
    try:
        if 'Id' in opportunity_data and opportunity_data['Id']:
            # Update existing opportunity
            opportunity_id = opportunity_data.pop('Id')  # Remove ID from data to avoid sending it in the update
            sf.Opportunity.update(opportunity_id, opportunity_data)
            print(f"Updated Opportunity ID: {opportunity_id}")
        else:
            # Create new opportunity
            new_opportunity = sf.Opportunity.create(opportunity_data)
            print(f"Created new Opportunity ID: {new_opportunity['id']}")
    except SalesforceMalformedRequest as e:
        print(f"Error occurred while processing opportunity: {e}")

def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    
    Args:
        event (dict): Event data passed to the Lambda function.
        context (object): Runtime information.
    
    Returns:
        dict: Response object indicating success or failure.
    """
    # Initialize the S3 client
    s3_client = boto3.client('s3')
    print(event)
    
    # Get the bucket and object key from the S3 event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    # Retrieve Salesforce credentials from Parameter Store
    parameters = get_parameters()
    
    # Access individual parameters
    salesforce_username = parameters['/salesforce/username']
    salesforce_password = parameters['/salesforce/password']
    salesforce_token = parameters['/salesforce/security_token']

    
    try:
        # Read the object content from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        content = response['Body'].read().decode('utf-8')
        
        # Parse the CSV content
        csv_data = csv.DictReader(io.StringIO(content))
        
        # Process each row in the CSV
        for row in csv_data:
            print("upserting record: ",row)
            # Determine the object type from the S3 key and upsert accordingly
            object_type = object_key.split("/")[1]
            if object_type == 'contact':
                upsert_contact(row)
            elif object_type == 'leads':
                upsert_lead(row)
            elif object_type == 'opportunity':
                upsert_opportunity(row)    
            else:
                print(f"Unsupported object type: {object_type}")
            
        return {
            'statusCode': 200,
            'body': json.dumps('Upsert successfully!')
        }

    except Exception as e:
        print(f"Error reading file {object_key} from bucket {bucket_name}: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }
