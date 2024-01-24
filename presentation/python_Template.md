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
__DK:CELL_LOOP:o:fetch_and_crack.ascii_board:r'^\s*for.*(?:\n(?!^\s*$).*)*'
__CELL_LOOP__
```


---



```python
__DK:BOARD_BUILD:o:fetch_and_crack.ascii_board:l0,11:
__BOARD_BUILD__
```



---


In Main setup variables
```python
__DK:MAIN_1:o:fetch_and_crack.main:l0,16:22
__MAIN_1__
```

---

*Later in ```main():```*
Get the JSON, call ascii_board and setup the out variable
```python
__DK:MAIN_2:o:fetch_and_crack.main:l23:28
__MAIN_2__
```

---


*Later in ```main():```*
Setup the directory
```python
__DK:MAIN_3:o:fetch_and_crack.main:l29:36
__MAIN_3__
```


---


*Later in ```main():```*
Store the JSON, print the board and date for humans
```python
__DK:MAIN_4:o:fetch_and_crack.main:l37:44
__MAIN_4__
```


---


*Later in ```main():```*
Way before I automated this I rotated the past puzzles
```python
__DK:MAIN_5:o:fetch_and_crack.main:l45:54
__MAIN_5__
```


---


*Later in ```main():```*
Setup the key values for the template in ```fill_in```
Process the template, which creates the new daily.txt
```python
__DK:MAIN_6:o:fetch_and_crack.main:l55:62
__MAIN_6__
```

---


# Thanks!

Craig Lien
Your Email: craig@lien.com
LinkedIn: https://www.linkedin.com/in/craiglien
GitHub: https://github.com/craiglien
