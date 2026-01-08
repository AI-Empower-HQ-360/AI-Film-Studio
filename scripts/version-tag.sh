#!/bin/bash
# Version and Tag Management Script
# This script helps manage versions and tags across the repository

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VERSION_FILE="$REPO_ROOT/VERSION"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
function info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

function success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

function warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

function error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Get current version
function get_current_version() {
    if [ -f "$VERSION_FILE" ]; then
        cat "$VERSION_FILE" | tr -d '\n'
    else
        error "VERSION file not found at $VERSION_FILE"
    fi
}

# Update version in all files
function update_version() {
    local new_version=$1
    
    info "Updating version to $new_version in all files..."
    
    # Update VERSION file
    echo "$new_version" > "$VERSION_FILE"
    success "Updated VERSION file"
    
    # Update setup.py
    sed -i "s/version=\"[0-9.]*\"/version=\"$new_version\"/" "$REPO_ROOT/setup.py"
    success "Updated setup.py"
    
    # Update src/__init__.py
    sed -i "s/__version__ = \"[0-9.]*\"/__version__ = \"$new_version\"/" "$REPO_ROOT/src/__init__.py"
    success "Updated src/__init__.py"
    
    # Update Dockerfile
    sed -i "s/LABEL version=\"[0-9.]*\"/LABEL version=\"$new_version\"/" "$REPO_ROOT/Dockerfile"
    sed -i "s/LABEL org.opencontainers.image.version=\"[0-9.]*\"/LABEL org.opencontainers.image.version=\"$new_version\"/" "$REPO_ROOT/Dockerfile"
    success "Updated Dockerfile"
    
    # Update Terraform
    if [ -f "$REPO_ROOT/infrastructure/terraform/environments/dev/main.tf" ]; then
        sed -i "s/Version     = \"[0-9.]*\"/Version     = \"$new_version\"/" "$REPO_ROOT/infrastructure/terraform/environments/dev/main.tf"
        success "Updated Terraform configuration"
    fi
    
    success "All version references updated to $new_version"
}

# Create a git tag
function create_tag() {
    local version=$1
    local message=$2
    
    info "Creating tag v$version..."
    
    # Check if tag already exists
    if git rev-parse "v$version" >/dev/null 2>&1; then
        error "Tag v$version already exists!"
    fi
    
    # Create annotated tag
    git tag -a "v$version" -m "$message"
    success "Created tag v$version"
    
    info "To push the tag, run: git push origin v$version"
}

# List all version tags
function list_tags() {
    info "All version tags:"
    git tag -l "v*" --sort=-v:refname
}

# Show current version
function show_version() {
    local current=$(get_current_version)
    info "Current version: $current"
    
    # Show git tag if exists
    if git rev-parse "v$current" >/dev/null 2>&1; then
        success "Git tag v$current exists"
    else
        warning "Git tag v$current does not exist yet"
    fi
}

# Bump version
function bump_version() {
    local bump_type=$1
    local current=$(get_current_version)
    
    # Parse current version
    IFS='.' read -r -a version_parts <<< "$current"
    local major="${version_parts[0]}"
    local minor="${version_parts[1]}"
    local patch="${version_parts[2]}"
    
    # Calculate new version
    case $bump_type in
        major)
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        minor)
            minor=$((minor + 1))
            patch=0
            ;;
        patch)
            patch=$((patch + 1))
            ;;
        *)
            error "Invalid bump type. Use: major, minor, or patch"
            ;;
    esac
    
    local new_version="$major.$minor.$patch"
    
    info "Bumping version from $current to $new_version ($bump_type)"
    update_version "$new_version"
    
    success "Version bumped to $new_version"
    info "Next steps:"
    info "  1. Review changes: git diff"
    info "  2. Commit changes: git add . && git commit -m 'Bump version to $new_version'"
    info "  3. Create tag: $0 tag $new_version 'Release version $new_version'"
    info "  4. Push changes: git push origin main"
    info "  5. Push tag: git push origin v$new_version"
}

# Show usage
function usage() {
    cat << EOF
Version and Tag Management Script

Usage:
    $0 <command> [options]

Commands:
    version             Show current version
    list                List all version tags
    bump <type>         Bump version (type: major, minor, patch)
    update <version>    Update to specific version
    tag <version> [msg] Create a git tag for version
    help                Show this help message

Examples:
    $0 version                               # Show current version
    $0 list                                  # List all tags
    $0 bump patch                            # Bump patch version (0.1.0 -> 0.1.1)
    $0 bump minor                            # Bump minor version (0.1.0 -> 0.2.0)
    $0 bump major                            # Bump major version (0.1.0 -> 1.0.0)
    $0 update 1.2.3                          # Update to version 1.2.3
    $0 tag 0.1.0 "Initial release"           # Create tag v0.1.0

EOF
}

# Main script
case ${1:-} in
    version)
        show_version
        ;;
    list)
        list_tags
        ;;
    bump)
        if [ -z "${2:-}" ]; then
            error "Bump type required (major, minor, or patch)"
        fi
        bump_version "$2"
        ;;
    update)
        if [ -z "${2:-}" ]; then
            error "Version number required"
        fi
        update_version "$2"
        ;;
    tag)
        if [ -z "${2:-}" ]; then
            error "Version number required"
        fi
        local tag_message="${3:-Release version $2}"
        create_tag "$2" "$tag_message"
        ;;
    help|--help|-h)
        usage
        ;;
    *)
        error "Unknown command: ${1:-}"
        usage
        ;;
esac
