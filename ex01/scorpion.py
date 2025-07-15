
import argparse
from PIL import Image, ExifTags

def get_exif_data(image_path) :
    try:
       img = Image.open(image_path)
       exifdata = img.getexif()
       if exifdata:
        for tag_id in exifdata:
           tag_name = ExifTags.TAGS.get(tag_id, tag_id)
           value = exifdata.get(tag_id)
           
           if isinstance(value, bytes):
              value = value.decode(errors="ignore")

           print(f"{tag_name}: {value}")

       else:
            print(f"No EXIF data found for {image_path}")
    except FileNotFoundError:
        print(f"Error Image file not found at {image_path}")
    except Exception as e:
        print(f"An error")
def main() :
    parser = argparse.ArgumentParser(usage='%(prog)s FILE1 [FILE2 ...]')
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()
    #print(args.files[0])\
    for i in range(len(args.files)):
        print(f"Image_name : {args.files[i]}")
        get_exif_data(args.files[i])
        if i < len(args.files) - 1 :
            print("------------------")


if __name__ == "__main__":
   main()