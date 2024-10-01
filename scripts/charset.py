import codecs
import chardet

input_file = '/home/mike-pi/Documents/coding/projects/disp/data/dikson/24a04'
output_file = '/home/mike-pi/Documents/coding/projects/disp/data/dikson/24a04_tr'

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    return result['encoding']

def convert_koi8r_to_utf8(input_file, output_file):
    # Detect the encoding of the input file
    detected_encoding = detect_encoding(input_file)
    print(f"Detected encoding: {detected_encoding}")
    
    # Check if the detected encoding is KOI8-R
    if detected_encoding and 'koi8' in detected_encoding.lower():
        # Open the input file with the detected encoding
        with codecs.open(input_file, 'r', encoding=detected_encoding) as infile:
            # Read the content
            content = infile.read()
        
        # Open the output file with UTF-8 encoding
        with codecs.open(output_file, 'w', encoding='utf-8') as outfile:
            # Write the content
            outfile.write(content)
        print(f"Conversion successful. Output saved to {output_file}")
    else:
        print("The detected encoding is not KOI8-R. Conversion aborted.")

# Example usage
# input_file = 'input.txt'  # Replace with your input file name
# output_file = 'output.txt'  # Replace with your output file name

convert_koi8r_to_utf8(input_file, output_file)

# print(detect_encoding('/home/mike-pi/Documents/coding/projects/disp/data/dikson/24a04'))