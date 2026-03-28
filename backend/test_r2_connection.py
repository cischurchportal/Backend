"""
Test script to verify Cloudflare R2 connection and upload functionality
Run this to ensure R2 is properly configured before deploying
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.r2_storage_service import get_r2_service
from app.config import settings

def test_r2_configuration():
    """Test R2 configuration"""
    print("=" * 60)
    print("Testing Cloudflare R2 Configuration")
    print("=" * 60)
    
    print("\n1. Checking R2 Configuration...")
    print(f"   Account ID: {settings.R2_ACCOUNT_ID}")
    print(f"   Bucket Name: {settings.R2_BUCKET_NAME}")
    print(f"   Access Key ID: {settings.R2_ACCESS_KEY_ID[:10]}...")
    print(f"   Secret Key: {'*' * 20}")
    
    if not settings.R2_ACCOUNT_ID or not settings.R2_BUCKET_NAME:
        print("   ❌ R2 configuration is incomplete!")
        return False
    
    print("   ✅ Configuration looks good")
    return True

def test_r2_connection():
    """Test R2 bucket connection"""
    print("\n2. Testing R2 Bucket Connection...")
    
    try:
        r2_service = get_r2_service()
        
        if r2_service.check_bucket_exists():
            print("   ✅ Successfully connected to R2 bucket!")
            return True
        else:
            print("   ❌ Cannot access R2 bucket. Check permissions.")
            return False
            
    except Exception as e:
        print(f"   ❌ Connection failed: {str(e)}")
        return False

def test_r2_upload():
    """Test R2 upload functionality"""
    print("\n3. Testing R2 Upload...")
    
    try:
        r2_service = get_r2_service()
        
        # Create a test image (1x1 pixel PNG)
        test_image_data = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
            b'\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\x00\x01'
            b'\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        )
        
        # Upload test image
        success, url, error = r2_service.upload_image(
            file_content=test_image_data,
            filename="test.png",
            folder="test",
            content_type="image/png"
        )
        
        if success:
            print(f"   ✅ Upload successful!")
            print(f"   URL: {url}")
            
            # Try to delete the test image
            print("\n4. Testing R2 Delete...")
            delete_success, delete_error = r2_service.delete_image(url)
            
            if delete_success:
                print("   ✅ Delete successful!")
            else:
                print(f"   ⚠️  Delete failed: {delete_error}")
                print("   (Test image may remain in bucket)")
            
            return True
        else:
            print(f"   ❌ Upload failed: {error}")
            return False
            
    except Exception as e:
        print(f"   ❌ Upload test failed: {str(e)}")
        return False

def test_folder_structure():
    """Test folder structure creation"""
    print("\n5. Testing Folder Structure...")
    
    folders = ["images", "logos", "priests", "carousels", "ministries"]
    
    try:
        r2_service = get_r2_service()
        
        # Create a tiny test file for each folder
        test_data = b'test'
        
        for folder in folders:
            success, url, error = r2_service.upload_image(
                file_content=test_data,
                filename="test.txt",
                folder=folder,
                content_type="text/plain"
            )
            
            if success:
                print(f"   ✅ {folder}/ - OK")
                # Clean up
                r2_service.delete_image(url)
            else:
                print(f"   ❌ {folder}/ - Failed: {error}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Folder structure test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n🚀 Starting R2 Connection Tests\n")
    
    results = []
    
    # Run tests
    results.append(("Configuration", test_r2_configuration()))
    results.append(("Connection", test_r2_connection()))
    results.append(("Upload/Delete", test_r2_upload()))
    results.append(("Folder Structure", test_folder_structure()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! R2 is ready to use.")
    else:
        print("⚠️  Some tests failed. Please check configuration.")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())
