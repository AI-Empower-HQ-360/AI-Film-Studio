#!/usr/bin/env python3
"""
Verify all AWS service modules can be imported
"""
import sys

def verify_imports():
    """Verify all AWS service modules can be imported"""
    errors = []
    
    try:
        from src.services.storage.s3_service import S3Service
        print("✓ S3Service imported successfully")
    except Exception as e:
        errors.append(f"S3Service: {e}")
        print(f"✗ S3Service import failed: {e}")
    
    try:
        from src.services.queue.sqs_service import SQSService
        print("✓ SQSService imported successfully")
    except Exception as e:
        errors.append(f"SQSService: {e}")
        print(f"✗ SQSService import failed: {e}")
    
    try:
        from src.services.database.db_service import DatabaseService
        print("✓ DatabaseService imported successfully")
    except Exception as e:
        errors.append(f"DatabaseService: {e}")
        print(f"✗ DatabaseService import failed: {e}")
    
    try:
        from src.services.compute.ecs_service import ECSService
        print("✓ ECSService imported successfully")
    except Exception as e:
        errors.append(f"ECSService: {e}")
        print(f"✗ ECSService import failed: {e}")
    
    try:
        from src.services.cdn.cloudfront_service import CloudFrontService
        print("✓ CloudFrontService imported successfully")
    except Exception as e:
        errors.append(f"CloudFrontService: {e}")
        print(f"✗ CloudFrontService import failed: {e}")
    
    try:
        from src.services.cache.redis_service import CacheService
        print("✓ CacheService imported successfully")
    except Exception as e:
        errors.append(f"CacheService: {e}")
        print(f"✗ CacheService import failed: {e}")
    
    if errors:
        print(f"\n✗ {len(errors)} import error(s) found")
        return 1
    else:
        print("\n✓ All 6 AWS service modules imported successfully - 0 import errors")
        return 0

if __name__ == "__main__":
    sys.exit(verify_imports())
