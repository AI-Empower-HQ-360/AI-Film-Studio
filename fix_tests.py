#!/usr/bin/env python3
"""
Test Fix Script
Identifies and fixes common test failures
"""
import os
import sys
import re
from pathlib import Path

def check_imports():
    """Check for missing imports in service files"""
    issues = []
    
    service_files = [
        "src/services/video_generation.py",
        "src/services/voice_synthesis.py",
        "src/services/ai_job_manager.py",
    ]
    
    for file_path in service_files:
        if not os.path.exists(file_path):
            issues.append(f"Missing file: {file_path}")
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for pydantic import
        if 'from pydantic import' in content or 'import pydantic' in content:
            # Check if it's wrapped in try/except
            if 'try:' not in content.split('from pydantic')[0][-50:]:
                issues.append(f"{file_path}: pydantic import not wrapped in try/except")
    
    return issues

def check_methods():
    """Check for missing methods that tests expect"""
    missing_methods = []
    
    # Expected methods by service
    expected = {
        "src/services/video_generation.py": {
            "VideoGenerationService": [
                "estimate_processing_time",
                "get_supported_models",
                "get_job_status"
            ]
        },
        "src/services/voice_synthesis.py": {
            "VoiceSynthesisService": [
                "get_available_voices",
                "get_voice_categories",
                "get_job_status"
            ]
        },
        "src/services/ai_job_manager.py": {
            "AIJobManager": [
                "submit_job",
                "get_job_status",
                "cancel_job",
                "register_worker",
                "update_worker_status",
                "get_queue_stats",
                "get_gpu_recommendations"
            ]
        }
    }
    
    for file_path, classes in expected.items():
        if not os.path.exists(file_path):
            missing_methods.append(f"File not found: {file_path}")
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        for class_name, methods in classes.items():
            for method in methods:
                # Check if method exists
                pattern = rf'def\s+{method}\s*\('
                if not re.search(pattern, content):
                    missing_methods.append(f"{file_path}: {class_name}.{method}() missing")
    
    return missing_methods

def main():
    print("Checking for test issues...")
    
    import_issues = check_imports()
    method_issues = check_methods()
    
    print(f"\nImport issues: {len(import_issues)}")
    for issue in import_issues:
        print(f"  - {issue}")
    
    print(f"\nMissing methods: {len(method_issues)}")
    for issue in method_issues:
        print(f"  - {issue}")
    
    if not import_issues and not method_issues:
        print("\n✓ No issues found!")
    else:
        print(f"\nTotal issues: {len(import_issues) + len(method_issues)}")

if __name__ == "__main__":
    main()
