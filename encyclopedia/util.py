import os

def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title.
    If no such entry exists, returns None.
    """
    # Ensure the title is properly capitalized
    title = title.capitalize()
    
    # Construct the file path for the entry
    file_path = f"entries/{title}.md"
    
    # Check if the file exists
    if os.path.exists(file_path):
        # Open the file and read its content
        with open(file_path, "r") as file:
            return file.read()
    
    # Return None if the file does not exist
    return None


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    entries_dir = "entries" # Specifyingthe directory in which we will look.
    filenames = []

    # Walk the directory and get the list of filenames
    for root, dirs, files in os.walk(entries_dir):
        for file in files:
            if file.endswith(".md"):
                filenames.append(file[:-3])  # Remove the .md extension and add to the list
        break  # Exit after the first directory

    return filenames

## Utility Function for the search functionality

def search_entries(query):
    """
    Returns a list of all entries that match the query.
    """
    entries = list_entries()
    matches = []
    
    for entry in entries:
        if query.lower() in entry.lower():
            matches.append(entry)
    
    return matches

# Thesave utility function:
def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown content.If an entry with the same title already exists, it is replaced. But we are handling that requirement in encyclopedia.view.
    """
    file_path = f"entries/{title}.md"
    with open(file_path, "w") as file:
        file.write(content)