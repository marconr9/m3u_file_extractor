def extract_category_from_m3u(file_path, partial_category, output_file):
    """
    Extracts URLs from an M3U file by searching for a partial match in the #EXTINF lines
    and writes the result to a new M3U file.

    :param file_path: Path to the M3U file.
    :param partial_category: Partial category string to search for (e.g., 'Rock').
    :param output_file: Path to the output M3U file where the results will be saved.
    :return: None
    """
    extracted_urls = []
    try:
        # Open the input M3U file with 'utf-8' encoding or 'latin1' to handle special characters
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as m3u_file:
            lines = m3u_file.readlines()
            for i in range(len(lines)):
                if lines[i].startswith("#EXTINF"):
                    # Extract category information from the #EXTINF metadata line
                    category_info = lines[i].split(",")[1].strip()  # Get text after comma
                    # Search for partial match (case-insensitive)
                    if partial_category.lower() in category_info.lower():
                        # The URL is in the next line, so we grab it
                        if i + 1 < len(lines):
                            url = lines[i + 1].strip()
                            extracted_urls.append((lines[i].strip(), url))  # Store both the metadata and URL

        # Write filtered content to the output M3U file
        with open(output_file, 'w', encoding='utf-8') as output:
            output.write("#EXTM3U\n")  # Write the header
            for metadata, url in extracted_urls:
                output.write(f"{metadata}\n{url}\n")
        print(f"Filtered results saved to '{output_file}'.")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"Error: {e}")


# Get user input for the input M3U file
file_path = input("Enter the path to the input M3U file: ").strip()

# Automatically add the .m3u extension if it doesn't already exist
if not file_path.lower().endswith('.m3u'):
    file_path += '.m3u'

# Get user input for the partial category to filter
partial_category = input("Enter a partial category to filter (e.g., 'rock', 'pop'): ").strip()

# Get user input for the output file name
output_file = input("Enter the name for the output M3U file (e.g., 'new_filtered_result'): ").strip()

# Automatically add the .m3u extension if it doesn't already exist
if not output_file.lower().endswith('.m3u'):
    output_file += '.m3u'

# Run the function to filter and save to the new user-specified M3U file
extract_category_from_m3u(file_path, partial_category, output_file)
