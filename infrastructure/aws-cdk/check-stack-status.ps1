# Check CloudFormation Stack Status
# Fixes AWS CLI Python association warning and checks stack status

param(
    [string]$StackName = "AIFilmStudio-dev",
    [string]$Region = "us-east-1"
)

Write-Host "Checking CloudFormation stack status..." -ForegroundColor Cyan
Write-Host "Stack Name: $StackName" -ForegroundColor Yellow
Write-Host "Region: $Region" -ForegroundColor Yellow
Write-Host ""

# Suppress Python association warning by using full path to AWS CLI
$awsCliPath = "C:\Program Files\Amazon\AWSCLIV2\aws.exe"

if (-not (Test-Path $awsCliPath)) {
    Write-Host "AWS CLI not found at expected path. Using 'aws' command." -ForegroundColor Yellow
    $awsCliPath = "aws"
}

# Check if stack exists
Write-Host "Checking if stack exists..." -ForegroundColor Cyan
$stackStatus = & $awsCliPath cloudformation describe-stacks `
    --stack-name $StackName `
    --region $Region `
    --query "Stacks[0].StackStatus" `
    --output text 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "Stack Status: $stackStatus" -ForegroundColor $(if ($stackStatus -like "*COMPLETE" -and $stackStatus -notlike "*ROLLBACK*") { "Green" } else { "Red" })
    
    # Get recent events if stack is in a bad state
    if ($stackStatus -like "*FAILED*" -or $stackStatus -like "*ROLLBACK*") {
        Write-Host "`nFetching recent stack events..." -ForegroundColor Cyan
        & $awsCliPath cloudformation describe-stack-events `
            --stack-name $StackName `
            --region $Region `
            --max-items 10 `
            --query "StackEvents[*].[Timestamp,ResourceStatus,ResourceType,LogicalResourceId,ResourceStatusReason]" `
            --output table 2>&1 | Out-String
    }
} else {
    Write-Host "Stack '$StackName' not found or error occurred." -ForegroundColor Red
    Write-Host "Error: $stackStatus" -ForegroundColor Red
    
    # List all stacks to help identify the correct name
    Write-Host "`nListing all stacks..." -ForegroundColor Cyan
    & $awsCliPath cloudformation list-stacks `
        --region $Region `
        --query "StackSummaries[?StackStatus!='DELETE_COMPLETE'].[StackName,StackStatus]" `
        --output table 2>&1 | Out-String
}
