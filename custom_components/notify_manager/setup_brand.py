"""Setup brand icons for Notify Manager.

This script copies the integration icons to the www/brands folder
so Home Assistant can display them in the UI.

Run this once after installation:
  python3 /config/custom_components/notify_manager/setup_brand.py
"""
import shutil
from pathlib import Path

def setup_brands():
    """Copy icons to www/brands folder."""
    # Paths
    config_dir = Path("/config")
    component_dir = Path(__file__).parent
    brands_dir = config_dir / "www" / "brands" / "notify_manager"
    
    # Create brands directory
    brands_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy icons
    for icon_name in ["icon.png", "icon@2x.png", "logo.png"]:
        src = component_dir / icon_name
        dst = brands_dir / icon_name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"✓ Copied {icon_name}")
    
    print(f"\n✓ Brand icons installed to: {brands_dir}")
    print("  Restart Home Assistant to see the icons.")

if __name__ == "__main__":
    setup_brands()
