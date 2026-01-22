"""
AWS Lambda Handler for AI Film Studio API
Free Tier Backend - Handles API requests from GitHub Pages frontend
"""
import json
import boto3
import uuid
from datetime import datetime
from decimal import Decimal

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

# Table and bucket names (from environment)
import os
PROJECTS_TABLE = os.environ.get('PROJECTS_TABLE', 'ai-film-studio-projects')
ASSETS_BUCKET = os.environ.get('ASSETS_BUCKET', 'ai-film-studio-assets')


def lambda_handler(event, context):
    """Main Lambda handler - routes requests to appropriate functions"""
    
    # CORS headers for GitHub Pages
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': 'https://ai-empower-hq-360.github.io',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
    }
    
    # Handle preflight CORS
    if event.get('requestContext', {}).get('http', {}).get('method') == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}
    
    try:
        http_method = event.get('requestContext', {}).get('http', {}).get('method', 'GET')
        path = event.get('rawPath', '/')
        body = json.loads(event.get('body', '{}')) if event.get('body') else {}
        
        # Route to handlers
        if path == '/api/health':
            return health_check(headers)
        elif path == '/api/projects' and http_method == 'GET':
            return list_projects(event, headers)
        elif path == '/api/projects' and http_method == 'POST':
            return create_project(body, headers)
        elif path.startswith('/api/projects/') and http_method == 'GET':
            project_id = path.split('/')[-1]
            return get_project(project_id, event, headers)
        elif path == '/api/upload-url':
            return get_upload_url(body, headers)
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Not found'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }


def health_check(headers):
    """Health check endpoint"""
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({
            'status': 'healthy',
            'service': 'AI Film Studio API',
            'timestamp': datetime.utcnow().isoformat()
        })
    }


def list_projects(event, headers):
    """List all projects for a user"""
    # Get user ID from auth (simplified for demo)
    user_id = event.get('requestContext', {}).get('authorizer', {}).get('claims', {}).get('sub', 'demo-user')
    
    table = dynamodb.Table(PROJECTS_TABLE)
    response = table.query(
        KeyConditionExpression='userId = :uid',
        ExpressionAttributeValues={':uid': user_id}
    )
    
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({
            'projects': response.get('Items', []),
            'count': response.get('Count', 0)
        }, default=str)
    }


def create_project(body, headers):
    """Create a new project"""
    project_id = str(uuid.uuid4())
    user_id = body.get('userId', 'demo-user')
    
    project = {
        'userId': user_id,
        'projectId': project_id,
        'title': body.get('title', 'Untitled Project'),
        'script': body.get('script', ''),
        'status': 'draft',
        'createdAt': datetime.utcnow().isoformat(),
        'updatedAt': datetime.utcnow().isoformat()
    }
    
    table = dynamodb.Table(PROJECTS_TABLE)
    table.put_item(Item=project)
    
    return {
        'statusCode': 201,
        'headers': headers,
        'body': json.dumps(project)
    }


def get_project(project_id, event, headers):
    """Get a specific project"""
    user_id = event.get('requestContext', {}).get('authorizer', {}).get('claims', {}).get('sub', 'demo-user')
    
    table = dynamodb.Table(PROJECTS_TABLE)
    response = table.get_item(
        Key={'userId': user_id, 'projectId': project_id}
    )
    
    if 'Item' not in response:
        return {
            'statusCode': 404,
            'headers': headers,
            'body': json.dumps({'error': 'Project not found'})
        }
    
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps(response['Item'], default=str)
    }


def get_upload_url(body, headers):
    """Generate a presigned S3 URL for file uploads"""
    filename = body.get('filename', f'{uuid.uuid4()}.mp4')
    content_type = body.get('contentType', 'video/mp4')
    
    key = f"uploads/{datetime.utcnow().strftime('%Y/%m/%d')}/{filename}"
    
    url = s3.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': ASSETS_BUCKET,
            'Key': key,
            'ContentType': content_type
        },
        ExpiresIn=3600  # 1 hour
    )
    
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({
            'uploadUrl': url,
            'key': key,
            'expiresIn': 3600
        })
    }
