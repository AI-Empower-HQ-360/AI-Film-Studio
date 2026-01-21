# PowerShell script to create and merge PR via GitHub API
# Requires GitHub Personal Access Token with 'repo' scope

param(
    [Parameter(Mandatory=$true)]
    [string]$GitHubToken
)

$owner = "AI-Empower-HQ-360"
$repo = "AI-Film-Studio"
$baseBranch = "main"
$headBranch = "feature/studio-operating-system"

# Read PR description
$prBody = Get-Content "PR_DESCRIPTION.md" -Raw

# Create PR
$prData = @{
    title = "feat: Enterprise Studio Operating System Architecture"
    head = $headBranch
    base = $baseBranch
    body = $prBody
} | ConvertTo-Json -Depth 10

$headers = @{
    "Authorization" = "token $GitHubToken"
    "Accept" = "application/vnd.github.v3+json"
}

Write-Host "Creating Pull Request..."
try {
    $prResponse = Invoke-RestMethod -Uri "https://api.github.com/repos/$owner/$repo/pulls" `
        -Method Post `
        -Headers $headers `
        -Body $prData `
        -ContentType "application/json"
    
    $prNumber = $prResponse.number
    Write-Host "✅ PR created successfully! PR #$prNumber"
    Write-Host "PR URL: $($prResponse.html_url)"
    
    # Merge PR
    Write-Host "`nMerging Pull Request..."
    $mergeData = @{
        commit_title = "feat: Enterprise Studio Operating System Architecture"
        merge_method = "squash"
    } | ConvertTo-Json
    
    Start-Sleep -Seconds 2  # Brief delay
    
    $mergeResponse = Invoke-RestMethod -Uri "https://api.github.com/repos/$owner/$repo/pulls/$prNumber/merge" `
        -Method Put `
        -Headers $headers `
        -Body $mergeData `
        -ContentType "application/json"
    
    if ($mergeResponse.merged) {
        Write-Host "✅ PR merged successfully!"
        Write-Host "Merged commit: $($mergeResponse.sha)"
    } else {
        Write-Host "⚠️ PR merge may have failed or requires review"
    }
    
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)"
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Response: $responseBody"
    }
}
