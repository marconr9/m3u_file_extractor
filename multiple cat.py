import os


def extract_category_from_m3u(file_path, categories, output_file):
    """
    Extracts URLs from an M3U file by searching for partial matches in the #EXTINF lines
    for multiple categories, and writes the result to a new M3U file.

    :param file_path: Path to the M3U file.
    :param categories: List of partial category strings to search for.
    :param output_file: Path to the output M3U file where the results will be saved.
    """
    extracted_entries = []

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as m3u_file:
            lines = m3u_file.readlines()

        for idx, line in enumerate(lines):
            if line.startswith("#EXTINF"):
                try:
                    category_info = line.split(",", 1)[1].strip()  # Extract text after first comma
                    # Check if any category matches (case insensitive)
                    if any(cat.lower() in category_info.lower() for cat in categories):
                        url = lines[idx + 1].strip() if idx + 1 < len(lines) else None
                        if url and url.startswith(("http", "rtmp", "rtsp")):  # Ensure it's a valid URL
                            extracted_entries.append((line.strip(), url))
                except IndexError:
                    print(f"Warning: No URL found after metadata line {idx + 1}. Skipping.")

        if extracted_entries:
            with open(output_file, 'w', encoding='utf-8') as output:
                output.write("#EXTM3U\n")
                for metadata, url in extracted_entries:
                    output.write(f"{metadata}\n{url}\n")
            print(f"Filtered results saved to '{output_file}'.")
        else:
            print("No matching entries found.")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"Unexpected error: {e}")


# User Input Handling
file_path = input("Enter the path to the input M3U file: ").strip()

if not file_path.lower().endswith('.m3u'):
    file_path += '.m3u'

if not os.path.exists(file_path):
    print(f"Error: File '{file_path}' does not exist.")
else:
    categories = []
    while True:
        category = input("Enter a category to filter (e.g., 'rock', 'pop'): ").strip()
        if category:
            categories.append(category)
        else:
            print("Invalid input. Please enter a valid category.")
            continue

        add_more = input("Do you want to add another category? (yes/no): ").strip().lower()
        if add_more not in ('yes', 'y'):
            break  # Exit the loop if the user doesn't want to add more categories

    if not categories:
        print("Error: No valid categories entered. Exiting.")
    else:
        output_file = input("Enter the name for the output M3U file (e.g., 'filtered_results'): ").strip()

        if not output_file.lower().endswith('.m3u'):
            output_file += '.m3u'

        extract_category_from_m3u(file_path, categories, output_file)
