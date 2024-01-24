---
theme: gaia
marp: true
html: true
paginate: false
backgroundColor: #000
foregroundColor: #fff
---


<!-- _class: lead -->

## "Crossword Cracker with Github Actions"

Craig Lien

[https://github.com/craiglien/NYTxwdBuddy](https://github.com/craiglien/NYTxwdBuddy)


![QR Code](/qr.png)


---


Started with jq


```bash
$ curl -O https://www.nytimes.com/svc/crosswords/v6/puzzle/mini.json

$ cat mini.json | jq keys
$ cat mini.json | jq .body | jq .[] | jq .cells
```


---


Python looping

```python
    for cell_index, cell in enumerate(cells):
        if 'answer' in cell:
            row = cell_index // board_width
            col = cell_index % board_width
            board[row][col] = cell['answer']
```


---



```python
def ascii_board(jdata):
    """
    # Extracting cells and dimensions from JSON data
    cells = jdata['body'][0]['cells']
    board_width = jdata['body'][0]['dimensions']['width']
    board_height = jdata['body'][0]['dimensions']['height']

    # Initialize an empty board
    board = [['*' for _ in range(board_width)] for _ in range(board_height)]

    # Add answers to board
    for cell_index, cell in enumerate(cells):
        if 'answer' in cell:
            row = cell_index // board_width
            col = cell_index % board_width
            board[row][col] = cell['answer']

    return '\n'.join([''.join(row) for row in board])

```



---


In Main setup variables
```python
def main():
    # Setup varaibles
    add_files = []
    pastdir = "data"
    url = os.environ.get("URL", "https://www.nytimes.com/svc/crosswords/v6/puzzle/mini.json")
    daily_template_fn = os.environ.get("DAILY_FILE_TEMPLATE", "daily_Template.txt")
    daily_file_seq = os.environ.get("DAILY_FILE_SEQ", "daily.txt,yesterday.txt").split(",")
```

---

*Later in ```main():```*
Get the JSON, call ascii_board and setup the out variable
```python
    # Fetch content from URL
    content = urllib.request.urlopen(url).read().decode('utf-8')
    out = dict(json=json.loads(content))

    out['board'] = ascii_board(out['json'])
```

---


*Later in ```main():```*
Setup the directory
```python
    # Store daily info
    day_parts = out['json']['publicationDate'].split('-')
    day_dir = '/'.join([pastdir] + day_parts[0:2])
    day_fn = f"{day_dir}/{day_parts[-1]}.json"

    # Create a directory named after the date
    os.makedirs(day_dir, exist_ok=True)
```


---


*Later in ```main():```*
Store the JSON, print the board and date for humans
```python
    # Store the json data.
    with open(day_fn, "w", encoding='utf-8') as f:
        f.write(json.dumps(out, indent=2, sort_keys=True))
    add_files.append(day_fn)

    print(out['board'])
    print(f"Content fetched and stored in {day_fn}")
```


---


*Later in ```main():```*
Way before I automated this I rotated the past puzzles
```python
    # Rotate the dailies
    fls = daily_file_seq
    idx = len(fls) - 1

    while idx > 0:
        if os.path.exists(fls[idx - 1]):
            shutil.move(fls[idx - 1], fls[idx])
            add_files.append(fls[idx])
        idx -= 1
```


---


*Later in ```main():```*
Setup the key values for the template in ```fill_in```
Process the template, which creates the new daily.txt
```python
    fill_in = dict(board=out['board'])
    fill_in['date'] = out['json']['publicationDate']

    # Create new daily
    process_template(daily_template_fn, fls[0], fill_in)

    add_files.append(fls[0])
```

---


# Thanks!

Craig Lien
Your Email: craig@lien.com
LinkedIn: https://www.linkedin.com/in/craiglien
GitHub: https://github.com/craiglien
