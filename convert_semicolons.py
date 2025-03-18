def convert_semicolons_to_commas(input_filename, output_filename):
    # Open the input file and read its contents
    with open(input_filename, 'r') as file_in:
        contents = file_in.read()
    
    # Replace all semicolons with commas
    updated_contents = contents.replace(";", ",")
    
    # Write the updated contents to the output file
    with open(output_filename, 'w') as file_out:
        file_out.write(updated_contents)

if __name__ == "__main__":
    # Specify your input and output file names
    input_file = "resampled_data1.csv"   # replace with your file name
    output_file = "resampled_data2.csv" # replace with your desired output file name
    convert_semicolons_to_commas(input_file, output_file)
    print(f"Conversion complete. Output written to {output_file}")
