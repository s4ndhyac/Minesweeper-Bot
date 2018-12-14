# Minesweeper-Bot

### Algorithm

- Rule 1: If the percept number on a cell is zero or is equal to the number of adjacent flagged cells then all remaining covered adjacent cells are safe and can be UNCOVERED

- Rule 2: If the (percept number on a cell - adjacent flagged cells) = no. of adjacent cells, then these remaining covered adjacent cells must be mines and can be FLAGGED

For the 16X30 Expert grid the following two additional rules 3 and 4 were used:
- Rule 3: We consider the cells in pairs and look for the 1-1 pattern or 1-2 pattern. 
If we find the 1-1 pattern then we UNCOVER the 3rd cell adjacent to it. Similarly, if we find the 1-2 pattern then we Flag the 3rd cell adjacent to it.

- Rule 4: If all 3 above rules fail, we use a backtracking algorithm, that selects a list of boundary cells, segregates them into isolated boundaries to consider, orders them in increasing order of size and then performs a recursion on each list, assuming a cell to have a mine or not a mine and looks for contradictions. 

- Rule 5: Finally in the worst case, when we don’t get any results even from the backtracking algorithm, we resort to the following probabilistic method:

a.) If the last cell was UNCOVERED -> then for each cell adjacent to it, the probability of a mine being present in it is = (percept number / no. of adjacent covered cells)

b.) If the last cell was FLAGGED -> the probability of a mine being present on it is 1 

c.) The probability of a mine in all remaining covered cells is = (mines left/ cells left)

d.) The cell with the minimum/least mine probability is UNCOVERED


### Performance

| Board size | Mines       | Sample size           | Solved  |
| ------------- |:-----------:|:-------------:| -----:|
| 5 X 5 | 1      | 1000 | 1000 |
| 8 X 8  | 1    | 1000      |   644 |
| 16 X 16 | 10 | 1000      |    551 |
| 16 X 30 | 99 | 1000      |    70 |
