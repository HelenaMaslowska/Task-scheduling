# Task scheduling competition
Repository contains project of task scheduling competition. October - December 2023 

Sort tasks on a 1 machine, minimize the number of late tasks. Task have time to be done and end time.
### Comment
I don't know how this program works but I had really complex idea while writing it.
My program won 2nd place in competition to solve this problem, but mine took 44ms on 500 instance (1st place got 1,7sec on the same instance), the difference between our results was 1 element of lateness.

### Example
Input file contains information about number of elements, length of task (measured in time), end time and a table, which contains how long will it take to reload the machine to the next one.
#### Input file
```
50
16 959
61 1780
14 2172
26 880
...
97 2351
72 2072
0 5 3 4 7 4 ... 4 6 3 5 7 6
... x50
4 7 4 0 3 5 ... 2 2 4 4 9 0
```
#### Output file
```
result: 45 : 4, 9, 14, 16, 28, 5, 31, 37, 44, 30, 15, 25, 26, 23, 17, 43, 8, 3, 0, 47, 18, 7, 12, 29, 10, 39, 40, 13, 1, 33, 42, 41, 35, 49, 34, 24, 32, 21, 2, 45, 11, 48, 6, 36, 22

late: 5 : 19, 20, 46, 27, 38
```

Overall complexity: linear
