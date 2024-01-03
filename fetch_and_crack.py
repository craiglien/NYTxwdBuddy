import json
import os
import shutil
import urllib.request


def ascii_board(jdata):
    """
    Build board and add the answers.

    With game JSON data. Extract cells and dimension.

    Parameters:
    jdata: The JSON data from the game.

    Returns:
    ASCII representation of the board.
    """
    # Extracting cells and dimensions from JSON data
    cells = jdata['body'][0]['cells']
    board_width = jdata['body'][0]['dimensions']['width']
    board_height = jdata['body'][0]['dimensions']['height']

    # Initialize an empty board
    board = [['*' for _ in range(board_width)] for _ in range(board_height)]

    # Add answers to board
    for cell in cells:
        if 'answer' in cell:
            cell_index = cells.index(cell)
            row = cell_index // board_height
            col = cell_index % board_width
            board[row][col] = cell['answer']

    return '\n'.join([''.join(row) for row in board])


def process_template(template, out_file, params):
    """
    Process a template file and replace the key values from params.

    Will open the template as the file to read and open the out_file as the file to write to.
    The keys are mapped via the Python "dunder" __key__.

    Parameters:
    template: Template file
    out_file: The file to write the processed template to.
    params: The Key Values to write into the out_file.

    Returns:
    None
    """
    with open(template, encoding='utf-8') as rf, open(out_file, "w", encoding='utf-8') as wf:
        for ln in rf.readlines():
            for fill_k, fill_v in params.items():
                rstr = f"__{fill_k}__"
                ln = ln.replace(rstr, fill_v)
            wf.write(ln)


def main():
    """
    Main function tying the program logic together.

    This function preforms the following steps.
    1. Setup the variables.
    2. Fetch the game board JSON.
    3. Run the game board JSON through ascii_board.
    4. Calculate name and store the daily data with the ascii board.
    5. Start output with the board and the file the data was stored.
    6. Rotate the daily files, leaving no 'daily.txt'.
    7. Process the daily_template with the fill_in parameters,
       this writes the new 'daily.txt' file.
    8. Finally, print out the files that have been added to the repo.
       The push action will use this line for "git add".
    """
    # Setup varaibles
    add_files = []
    pastdir = "data"
    url = os.environ.get("URL", "https://www.nytimes.com/svc/crosswords/v6/puzzle/mini.json")
    daily_template_fn = os.environ.get("DAILY_FILE_TEMPLATE", "daily_Template.txt")
    daily_file_seq = os.environ.get("DAILY_FILE_SEQ", "daily.txt,yesterday.txt").split(",")

    # Fetch content from URL
    content = urllib.request.urlopen(url).read().decode('utf-8')
    out = dict(json=json.loads(content))

    out['board'] = ascii_board(out['json'])

    # Store daily info
    day_parts = out['json']['publicationDate'].split('-')
    day_dir = '/'.join([pastdir] + day_parts[0:2])
    day_fn = f"{day_dir}/{day_parts[-1]}.json"

    # Create a directory named after the date
    os.makedirs(day_dir, exist_ok=True)

    # Store the json data.
    with open(day_fn, "w", encoding='utf-8') as f:
        f.write(json.dumps(out, indent=2, sort_keys=True))
    add_files.append(day_fn)

    print(out['board'])
    print(f"Content fetched and stored in {day_fn}")

    # Rotate the dailies
    fls = daily_file_seq
    idx = len(fls) - 1

    while idx > 0:
        if os.path.exists(fls[idx - 1]):
            shutil.move(fls[idx - 1], fls[idx])
            add_files.append(fls[idx])
        idx -= 1

    fill_in = dict(board=out['board'])
    fill_in['date'] = out['json']['publicationDate']

    # Create new daily
    process_template(daily_template_fn, fls[0], fill_in)

    add_files.append(fls[0])
    print(json.dumps(add_files))


if __name__ == "__main__":
    main()
