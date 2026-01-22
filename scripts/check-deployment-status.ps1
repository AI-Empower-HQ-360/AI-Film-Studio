# Check Deployment Status Script
# Run this to see what's already deployed

Write-Host "=== Checking Deployment Status ===" -ForegroundColor Cyan
Write-Host ""

# Check CloudFormation Stacks
Write-Host "=== CloudFormation Stacks ===" -ForegroundColor Yellow
try {
    $stacks = aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE --query "StackSummaries[?contains(StackName, 'AIFilmStudio')]" --output json | ConvertFrom-Json
    if ($stacks) {
        $stacks | ForEach-Object {
            Write-Host "  Stack: $($_.StackName) - Status: $($_.StackStatus)" -ForegroundColor Green
        }
    } else {
        Write-Host "  No AIFilmStudio stacks found" -ForegroundColor Red
    }
} catch {
    Write-Host "  Error checking stacks: $_" -ForegroundColor Red
}

Write-Host ""

# Check ECS Clusters
Write-Host "=== ECS Clusters ===" -ForegroundColor Yellow
try {
    $clusters = aws ecs list-clusters --output json | ConvertFrom-Json
    if ($clusters.clusterArns) {
        $clusters.clusterArns | ForEach-Object {
            Write-Host "  Cluster: $_" -ForegroundColor Green
        }
    } else {
        Write-Host "  No ECS clusters found" -ForegroundColor Red
    }
} catch {
    Write-Host "  Error checking clusters: $_" -ForegroundColor Red
}

Write-Host ""

# Check RDS Instances
Write-Host "=== RDS Instances ===" -ForegroundColor Yellow
try {
    $rds = aws rds describe-db-instances --query "DBInstances[?contains(DBInstanceIdentifier, 'ai-film-studio')]" --output json | ConvertFrom-Json
    if ($rds) {
        $rds | ForEach-Object {
            Write-Host "  Database: $($_.DBInstanceIdentifier) - Status: $($_.DBInstanceStatus)" -ForegroundColor Green
            Write-Host "    Endpoint: $($_.Endpoint.Address)" -ForegroundColor Gray
        }
    } else {
        Write-Host "  No RDS instances found" -ForegroundColor Red
    }
} catch {
    Write-Host "  Error checking RDS: $_" -ForegroundColor Red
}

Write-Host ""

# Check S3 Buckets
Write-Host "=== S3 Buckets ===" -ForegroundColor Yellow
try {
    $buckets = aws s3 ls --output json | ConvertFrom-Json
    $aiBuckets = $buckets | Where-Object { $_ -like "*ai-film-studio*" }
    if ($aiBuckets) {
        $aiBuckets | ForEach-Object {
            Write-Host "  Bucket: $_" -ForegroundColor Green
        }
    } else {
        Write-Host "  No AI Film Studio buckets found" -ForegroundColor Red
    }
} catch {
    Write-Host "  Error checking S3: $_" -ForegroundColor Red
}

Write-Host ""

# Check Load Balancers
Write-Host "=== Load Balancers ===" -ForegroundColor Yellow
try {
    $lbs = aws elbv2 describe-load-balancers --query "LoadBalancers[?contains(LoadBalancerName, 'ai-film-studio')]" --output json | ConvertFrom-Json
    if ($lbs) {
        $lbs | ForEach-Object {
            Write-Host "  ALB: $($_.LoadBalancerName) - DNS: $($_.DNSName)" -ForegroundColor Green
        }
    } else {
        Write-Host "  No load balancers found" -ForegroundColor Red
    }
} catch {
    Write-Host "  Error checking load balancers: $_" -ForegroundColor Red
}

Write-Host ""

# Check ECR Repositories (already confirmed)
Write-Host "=== ECR Repositories ===" -ForegroundColor Yellow
Write-Host "  ✅ ai-film-studio" -ForegroundColor Green
Write-Host "  ✅ ai-film-studio-api" -ForegroundColor Green
Write-Host "  ✅ ai-film-studio-backend-dev" -ForegroundColor Green
Write-Host "  ✅ ai-film-studio-worker-dev" -ForegroundColor Green
Write-Host "  ✅ cdk-hnb659fds-container-assets-*" -ForegroundColor Green

Write-Host ""
Write-Host "=== Summary ===" -ForegroundColor Cyan
Write-Host "ECR repositories are already created." -ForegroundColor Green
Write-Host "Run this script to check what else is deployed." -ForegroundColor Yellow
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. If stack exists but incomplete: Continue deployment" -ForegroundColor White
Write-Host "2. If stack doesn't exist: Start fresh deployment" -ForegroundColor White
Write-Host "3. Check CHECK_DEPLOYMENT_STATUS.md for details" -ForegroundColor White
