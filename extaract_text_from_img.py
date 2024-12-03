from PIL import Image
import pytesseract
import sys


def extract_text_from_image(image_path):
    try:
        # Open the image file
        image = Image.open(image_path)
        # Extract text from the image
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_text.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    extracted_text = extract_text_from_image(image_path)
    print(extracted_text)
