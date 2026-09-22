import requests
from bs4 import BeautifulSoup

def decode_secret_message(url):
    # Fetch the published Google Doc content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract all table rows from the document
    rows = soup.find_all('tr')
    
    data = []
    # Parse table columns, skipping the header row
    for row in rows[1:]:
        cols = [col.text.strip() for col in row.find_all(['td', 'th'])]
        if len(cols) >= 3:
            try:
                x = int(cols[0])
                char = cols[1]
                y = int(cols[2])
                data.append((x, char, y))
            except ValueError:
                continue
                
    if not data:
        print("No valid coordinate data found.")
        return
        
    # Determine the maximum grid boundaries
    max_x = max(item[0] for item in data)
    max_y = max(item[2] for item in data)
    
    # Initialize a 2D grid filled with space characters
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    
    # Populate the grid (using max_y - y for Cartesian coordinate orientation)
    for x, char, y in data:
        grid[max_y - y][x] = char
        
    # Print the final rendered grid
    for row in grid:
        print("".join(row))

# Execute the function with the provided assessment URL
decode_secret_message("https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub")
   