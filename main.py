import streamlit as st
import time 
from collections import deque

ROWS, COLS = 10, 10

#Initializing the grid
if 'grid' not in st.session_state:
    st.session_state.grid = [[0] * COLS for _ in range(ROWS)]

if 'start' not in st.session_state:
    st.session_state['start'] = (0,0)

if 'end' not in st.session_state:
    st.session_state['end'] = (ROWS -1, COLS - 1)

if 'mode' not in st.session_state:
    st.session_state['mode'] = "Wall"

def reset_path():
    for r in range(ROWS):
        for c in range(COLS):
            if st.session_state.grid[r][c] == 2 or st.session_state.grid[r][c] == 3:
                st.session_state.grid[r][c] = 0


def bfs(start, end):
    visited = [[False] * COLS for _ in range(ROWS)]
    parent = [[None] * COLS for _ in range(ROWS)]

    q = deque()
    q.append(start)
    visited[start[0]][start[1]] = True

    found = False

    while q:
        r, c = q.popleft()
        if (r, c) != start and (r, c) != end:
            st.session_state.grid[r][c] = 2
            time.sleep(0.05)
            st.rerun()

            return 
        
        for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            x = r + dr
            y = c + dc

            if 0 <= x < ROWS and 0 <= y < COLS:
                if not visited[x][y] and st.session_state.grid[x][y] != 1:
                    visited[x][y] = True
                    parent[x][y] = (r, c)
                    q.append((x, y))

                    if (x, y) == end:
                        found = True
                        break
        if found : 
            break

    if found:
        r, c = end
        while parent[r][c] and (r, c) != start:
            r, c = parent[r][c]
            if (r, c) != start:
                st.session_state.grid[r][c] = 3
                time.sleep(0.05)
             
                return 

st.title("Path Finding Visualizer")
mode = st.radio(
    "Select Mode", 
    ["Wall", "Set Start", "Set End"], key = "mode"
)


for r in range(ROWS):
    cols = st.columns(COLS)
    for c in range(COLS):
        cell_val = st.session_state.grid[r][c]
        cell_label = ""


        if (r, c) == st.session_state['start']:
            cell_label = 'S'
        
        elif (r, c) == st.session_state['end']:
            cell_label = 'E'

        elif cell_val == 1:
            cell_label = 'W'
        
        elif cell_val == 2:
            cell_label = '.'
        
        elif cell_val == 3:
            cell_label = '◉'
        else :
            cell_label = ' '


        if cols[c].button(cell_label, key = f'cell_{r}_{c}'):
            if mode == 'Wall':
                if (r, c) != st.session_state['start'] and (r, c) != st.session_state['end']:
                    st.session_state.grid[r][c] = 0 if cell_val == 1 else 1
            elif mode == 'Set Start':
                if (r, c) != st.session_state['end']:
                    st.session_state['start']= (r, c)
            elif mode == 'Set End':
                if (r, c) != st.session_state['start']:
                    st.session_state['end'] = (r, c)
            st.rerun()
        
if st.button("Run BFS"):
    reset_path()
    bfs(st.session_state['start'], st.session_state['end'])
