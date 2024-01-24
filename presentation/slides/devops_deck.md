---
theme: gaia
<!-- _class: invert -->
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


<!--

Welcome back after the reboot! We used to have a lot of fun at these meetings, I hope this first talk represents that.

I have been Programming Computers since I was a kid. I went to college for computer science and got into computer networking. Since, I have always been curious about computers and networks. I have always stayed up to date on the latest technologies. When I see something it is easy to think... if I were to implement this how would I do it?

I am bad with these computer related things. The game turns out to bea computer programming project.

-->

---


<!--

Google searched for nyt mini and got right to it.

-->


This NYT mini crossword game is on my phone.

One day I wondered if there was a web version. 

Sure enough!

Demo -- Firefox Developer Tools


I searched for a unique word in a clue and found mini.json

There is no authentication required to get this file!


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


### I could write a program to solve this

- Run it manually?

### Or, Automate it!

- cron on a linux host
- Github actions manually or scheduled!


---


Demo -- new repo and create an action.

```
ps
set
arp -an
```


---


<!-- Show it running locally. -->

The output needed to have the filenames in JSON, use ```jq``` again.

```
ACIDS
SUNUP
PLUTO
CLICK
ASTHE
Content fetched and stored in data/2024/01/24.json
["data/2024/01/24.json", "yesterday.txt", "daily.txt"]
```


---

### This is used in the ```git add```

```
$ echo '["data/2024/xx/yy.json", "yesterday.txt", "daily.txt"]' | jq
[
  "data/2024/xx/yy.json",
  "yesterday.txt",
  "daily.txt"
]
```

---

### This will be simple using GitHub Actions.
#### These are the first steps

```
jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
        with:
          persist-credentials: false
      - name: Set up Python
        uses: actions/setup-python@v3
        with:
          python-version: '3.x'
          architecture: 'x64'
```

---


### After the first couple they start becoming unique.
#### Next steps are to run the python script and commit the changes.

```
      - name: Run the Python script
        run: |
          python fetch_and_crack.py > output.txt
      - name: Commit changes
        run: |
          echo $GITHUB_REPOSITORY
          git config --global user.name 'github-actions[bot]'
          git config --global user.email 'github-actions[bot]@users.noreply.github.com'
          cat output.txt
          git add -v $(cat output.txt | tail -1 | jq -r 'join(" ")')
          git commit -m "xwdBuddy $(date +'%m/%d/%Y')"
          git push https://oauth2:${{ secrets.PUSH_TOKEN }}@github.com/$GITHUB_REPOSITORY ${{ github.ref }}

```

---

### Name and when the jobs are ran.

```
name: Fetch and Process Game JSON with Python

on:
  workflow_dispatch:
  schedule:
    - cron: '45 6 * * *'  # Runs at 6:45 AM UTC every day
        
jobs:
  build:
    runs-on: ubuntu-latest
```

---


# Questions?

---

# Thanks!

Craig Lien
Your Email: craig@lien.com
LinkedIn: https://www.linkedin.com/in/craiglien
GitHub: https://github.com/craiglien
