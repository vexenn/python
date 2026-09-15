import requests
from bs4 import BeautifulSoup

def decode_secret_message(doc_url: str) -> None:
    # Fetch the published Google Doc HTML content
    response = requests.get(doc_url)
    response.raise_for_status()

    # Parse HTML table elements
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    if not table:
        print("No table found in document.")
        return

    rows = table.find_all('tr')
    if not rows:
        print("No rows found in table.")

    # Match column indices from header row
    headers = [th.get_text(strip=True).lower() for th in rows[0].find_all(['td', 'th'])]
    x_idx, char_idx, y_idx = 0, 1, 2
    for i, header in enumerate(headers):
        if 'x' in header:
            x_idx = i
        elif 'char' in header:
            char_idx = i
        elif 'y' in header:
            y_idx = i

    # Parse coordinates and characters from data rows
    parsed_data = []
    for row in rows[1:]:
        cols = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
        if len(cols) > max(x_idx, char_idx, y_idx):
            try:
                x = int(cols[x_idx])
                char = cols[char_idx]
                y = int(cols[y_idx])
                parsed_data.append((x, y, char))
            except ValueError:
                continue

    if not parsed_data:
        print("No valid character data found.")
        return

    # Determine maximum dimensions to construct grid
    max_x = max(x for x, y, char in parsed_data)
    max_y = max(y for x, y, char in parsed_data)

    # Initialize grid with spaces
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # Place characters into grid (inverting y-axis so y=max_y is printed at the top)
    for x, y, char in parsed_data:
        grid[max_y - y][x] = char

    # Print the reconstructed grid
    for row in grid:
        print(''.join(row))

decode_secret_message('https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub')