# Advent of Code 2018

## Structure
```
├── 00_template.py
├── 01_frequency.py
├── ...
├── README.md
├── aoc_utils.py
├── data
│   ├── 01.ans
│   ├── 01.txt
│   ├── 01_test.txt
│   ├── ...
├── test_00.py
├── test_01.py -> test_00.py
├── test_02.py -> test_00.py
├── ...
```
Each day's puzzle-solving code is a separate file which contains (at least) two methods: `part1` and `part2`.  To get started on a new day, copy the template `00_template.py` and all the boilerplate is written for you.  The `data` directory contains the test input from the problem description (xx_test.txt), the main input (xx.txt), and the expected answers (xx.ans).  The `.ans` file is four lines long, with the expected output as follows:
```
[line 0]: Part 1, test input
[line 1]: Part 2, test input
[line 2]: Part 1, main input
[line 3]: Part 2, main input
```

## Running the code
I used python 3.5, from the anaconda distribution.  I believe networkx and numpy are the only non-stock libraries used.  To run a specific day:
`python <file>`

## Testing the code
If you follow the structure, making a new test is simply creating a symlink to `test_00.py` with the new number.  To run, use pytest:

```
pytest
```

or green:

```
pip install green
green
```
