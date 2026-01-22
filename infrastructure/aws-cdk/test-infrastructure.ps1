# test-infrastructure.ps1
# Comprehensive infrastructure testing script

param(
    [Parameter(Mandatory=$false)]
    [switch]$Synthesis = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$UnitTests = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$Validation = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$All = $true
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Infrastructure Testing" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

function Write-Info { Write-Host "[INFO] $args" -ForegroundColor Green }
function Write-Warn { Write-Host "[WARN] $args" -ForegroundColor Yellow }
function Write-Error { Write-Host "[ERROR] $args" -ForegroundColor Red }

$testResults = @{
    Synthesis = $false
    UnitTests = $false
    Validation = $false
}

# Step 1: Check prerequisites
Write-Info "Checking prerequisites..."

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python not found"
    exit 1
}

if (-not (Get-Command cdk -ErrorAction SilentlyContinue)) {
    Write-Error "CDK not found. Install with: npm install -g aws-cdk"
    exit 1
}

# Check virtual environment
if (-not (Test-Path ".venv-cdk")) {
    Write-Warn "Virtual environment not found. Creating..."
    py -3.12 -m venv .venv-cdk
}

# Activate virtual environment
if (Test-Path ".venv-cdk\Scripts\Activate.ps1") {
    & .venv-cdk\Scripts\Activate.ps1
    Write-Info "Virtual environment activated"
}

# Install test dependencies
Write-Info "Installing test dependencies..."
pip install -q -r requirements.txt
pip install -q -r requirements-test.txt

# Step 2: Test Stack Synthesis
if ($All -or $Synthesis) {
    Write-Host ""
    Write-Host "=== Testing Stack Synthesis ===" -ForegroundColor Yellow
    
    try {
        Write-Info "Synthesizing CloudFormation template..."
        cdk synth --quiet 2>&1 | Out-Null
        
        if ($LASTEXITCODE -eq 0) {
            Write-Info "Stack synthesis successful"
            $testResults.Synthesis = $true
        } else {
            Write-Error "Stack synthesis failed"
            cdk synth
            exit 1
        }
    } catch {
        Write-Error "Synthesis error: $_"
        exit 1
    }
}

# Step 3: Test Stack Validation
if ($All -or $Validation) {
    Write-Host ""
    Write-Host "=== Testing Stack Validation ===" -ForegroundColor Yellow
    
    try {
        Write-Info "Validating stack structure..."
        cdk synth --quiet 2>&1 | Out-Null
        
        # Check if template file exists
        if (Test-Path "cdk.out\AIFilmStudio.template.json") {
            $template = Get-Content "cdk.out\AIFilmStudio.template.json" | ConvertFrom-Json
            $resources = $template.Resources
            
            Write-Info "Template contains $($resources.Count) resources"
            
            # Check for key resources
            $requiredResources = @(
                "VPC",
                "Cluster",
                "Database",
                "AssetsBucket",
                "JobQueue"
            )
            
            $found = 0
            foreach ($resource in $requiredResources) {
                if ($resources.PSObject.Properties.Name -match $resource) {
                    $found++
                    Write-Info "  ✓ Found: $resource"
                } else {
                    Write-Warn "  ✗ Missing: $resource"
                }
            }
            
            if ($found -eq $requiredResources.Count) {
                Write-Info "All required resources found"
                $testResults.Validation = $true
            } else {
                Write-Warn "Some required resources missing"
            }
        } else {
            Write-Error "Template file not found"
        }
    } catch {
        Write-Error "Validation error: $_"
    }
}

# Step 4: Run Unit Tests
if ($All -or $UnitTests) {
    Write-Host ""
    Write-Host "=== Running Unit Tests ===" -ForegroundColor Yellow
    
    try {
        Write-Info "Running pytest..."
        pytest tests/ -v --tb=short
        
        if ($LASTEXITCODE -eq 0) {
            Write-Info "All unit tests passed"
            $testResults.UnitTests = $true
        } else {
            Write-Warn "Some unit tests failed"
        }
    } catch {
        Write-Error "Unit tests error: $_"
    }
}

# Step 5: Test CDK Diff (if AWS configured)
if ($All) {
    Write-Host ""
    Write-Host "=== Testing CDK Diff ===" -ForegroundColor Yellow
    
    try {
        $accountId = aws sts get-caller-identity --query Account --output text 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Info "AWS configured, running cdk diff..."
            cdk diff --quiet 2>&1 | Out-Null
            Write-Info "CDK diff completed (check output above for changes)"
        } else {
            Write-Warn "AWS not configured, skipping cdk diff"
        }
    } catch {
        Write-Warn "AWS not configured, skipping cdk diff"
    }
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Test Results Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($testResults.Synthesis) {
    Write-Host "  ✓ Stack Synthesis: PASSED" -ForegroundColor Green
} else {
    Write-Host "  ✗ Stack Synthesis: NOT TESTED" -ForegroundColor Yellow
}

if ($testResults.Validation) {
    Write-Host "  ✓ Stack Validation: PASSED" -ForegroundColor Green
} else {
    Write-Host "  ✗ Stack Validation: FAILED" -ForegroundColor Red
}

if ($testResults.UnitTests) {
    Write-Host "  ✓ Unit Tests: PASSED" -ForegroundColor Green
} else {
    Write-Host "  ✗ Unit Tests: FAILED" -ForegroundColor Red
}

Write-Host ""

$allPassed = $testResults.Synthesis -and $testResults.Validation -and $testResults.UnitTests

if ($allPassed) {
    Write-Host "All infrastructure tests PASSED!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "Some tests FAILED. Review output above." -ForegroundColor Yellow
    exit 1
}
