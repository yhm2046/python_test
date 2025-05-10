from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
import time

def rational_to_float(r):
    try:
        return float(r)
    except Exception:
        return r[0] / r[1]

def dms_to_decimal(dms, ref):
    degrees = rational_to_float(dms[0])
    minutes = rational_to_float(dms[1])
    seconds = rational_to_float(dms[2])
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

start_time = time.time()
print("Current working directory:", os.getcwd())
image_path = "C:\\Users\\yhm20\\Pictures\\250421\\t3.jpg"  # Update as needed

try:
    with Image.open(image_path) as img:
        print("Image successfully opened!")
        print("Image size:", img.size)
        exif_data = img._getexif()
        if exif_data is None:
            print("No EXIF data found in the image.")
        else:
            gps_found = False
            gps_info = {}
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == "GPSInfo":
                    gps_found = True
                    print("GPS Information:")
                    for key in value:
                        sub_tag_name = GPSTAGS.get(key, key)
                        print(f"{sub_tag_name}: {value[key]}")
                        gps_info[sub_tag_name] = value[key]
            if not gps_found:
                print("No GPS information found in the EXIF data.")
            else:
                try:
                    lat_ref = gps_info.get('GPSLatitudeRef')
                    lat_dms = gps_info.get('GPSLatitude')
                    lon_ref = gps_info.get('GPSLongitudeRef')
                    lon_dms = gps_info.get('GPSLongitude')
                    if lat_ref and lat_dms and lon_ref and lon_dms:
                        latitude = dms_to_decimal(lat_dms, lat_ref)
                        longitude = dms_to_decimal(lon_dms, lon_ref)
                        google_maps_coords = f"{latitude}, {longitude}"
                        print("\nGoogle Maps Coordinates (copy-paste this):")
                        print(google_maps_coords)
                    else:
                        print("Missing GPS coordinate data.")
                except Exception as e:
                    print(f"Error: Could not process GPS coordinates. Details: {e}")
except FileNotFoundError:
    print(f"Error: The file '{image_path}' was not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

end_time = time.time()
elapsed = end_time - start_time
minutes = int(elapsed // 60)
seconds = int(elapsed % 60)
print(f"\nthis code overtime is {minutes} minutes {seconds} seconds")
