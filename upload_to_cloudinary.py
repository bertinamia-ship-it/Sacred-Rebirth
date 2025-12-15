#!/usr/bin/env python3
"""
Script to upload all images to Cloudinary with optimization
"""
import cloudinary
import cloudinary.uploader
import os
import json
from pathlib import Path

# Configure Cloudinary
cloudinary.config(
    cloud_name="dpmozdkfh",
    api_key="159722641187121",
    api_secret="NO-XAc4ikqKN5Vm1r08NS5ItYRg"
)

# Get all image files
image_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.JPG', '.JPEG', '.PNG', '.jgp']
workspace_path = Path('/workspaces/Sacred-Rebirth')

# Find all images
images = []
for ext in image_extensions:
    images.extend(workspace_path.glob(f'*{ext}'))
    images.extend(workspace_path.glob(f'video-photos/*{ext}'))

# Dictionary to store old path -> new URL mapping
url_mapping = {}

print(f"Found {len(images)} images to upload\n")

# Upload each image
for img_path in images:
    try:
        # Get relative path and create public_id
        rel_path = img_path.relative_to(workspace_path)
        
        # Clean public_id (remove extension and special chars)
        public_id = str(rel_path.with_suffix('')).replace(' ', '_').replace('.', '_')
        public_id = f"sacred-rebirth/{public_id}"
        
        print(f"Uploading: {rel_path} -> {public_id}")
        
        # Upload with optimization
        result = cloudinary.uploader.upload(
            str(img_path),
            public_id=public_id,
            folder="sacred-rebirth",
            quality="auto:good",
            fetch_format="auto",
            overwrite=True,
            resource_type="image"
        )
        
        # Store mapping
        url_mapping[str(rel_path)] = result['secure_url']
        
        print(f"  ✓ Uploaded: {result['secure_url']}\n")
        
    except Exception as e:
        print(f"  ✗ Error uploading {rel_path}: {str(e)}\n")

# Save mapping to JSON file
with open('cloudinary_mapping.json', 'w') as f:
    json.dump(url_mapping, f, indent=2)

print(f"\n✅ Upload complete! {len(url_mapping)} images uploaded")
print(f"📄 URL mapping saved to cloudinary_mapping.json")
