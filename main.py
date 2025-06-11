import streamlit as st
import time 
from collections import deque
import heapq

st.markdown("# Pathfinding Visualizer")
st.markdown("Click cells to toggle walls 🧱 or set start/end points. Then run an algorithm!")

st.markdown("""
**Legend**  
🟩 Start | 🟥 End | ⬛ Wall | 🟨 Visited | 🔵 Path | ⬜ Empty
""")

ROWS, COLS = 7, 7

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


st.title("Path Finding Visualizer")

## Grid Display
with st.sidebar:
    st.header("Controls")
    mode = st.radio("Mode", ["Wall", "Set Start", "Set End"], key="mode")
    speed = st.slider("⏱️ Animation Speed", 0.001, 0.1, 0.02)

def get_cell_emoji(r, c):
    if (r, c) == st.session_state['start']:
        return "🟩"  
    elif (r, c) == st.session_state['end']:
        return "🟥"  
    elif st.session_state.grid[r][c] == 1:
        return "⬛"  
    elif st.session_state.grid[r][c] == 2:
        return "🟨"  
    elif st.session_state.grid[r][c] == 3:
        return "🔵"  
    else:
        return "⬜"  

for r in range(ROWS):
    cols = st.columns(COLS)
    for c in range(COLS):
        cell_label = get_cell_emoji(r, c)
        if cols[c].button(cell_label, key=f'cell_{r}_{c}'):
            if mode == 'Wall':
                if (r, c) != st.session_state['start'] and (r, c) != st.session_state['end']:
                    st.session_state.grid[r][c] = 0 if st.session_state.grid[r][c] == 1 else 1
            elif mode == 'Set Start':
                if (r, c) != st.session_state['end']:
                    st.session_state['start'] = (r, c)
            elif mode == 'Set End':
                if (r, c) != st.session_state['start']:
                    st.session_state['end'] = (r, c)
            st.rerun()

##BFS
def bfs():
    q = st.session_state["bfs_queue"]
    visited = st.session_state["bfs_visited"]
    parent = st.session_state["bfs_parent"]
    end = st.session_state['end']

    if st.session_state['bfs_mode'] == 'search':
        if not q:
            st.session_state['bfs_mode'] = None
            return 

        r, c = q.popleft()

        if(r, c) != st.session_state['start'] and (r, c) != end:
            st.session_state.grid[r][c] = 2

        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            x, y = r + dr, c + dc

            if 0 <= x < ROWS and 0 <= y < COLS and not visited[x][y] and st.session_state.grid[x][y] != 1:
                visited[x][y] = True
                parent[x][y] = (r, c)
                q.append((x, y))
                if (x, y) == end:
                    st.session_state['bfs_mode'] = 'backtrack'
                    st.session_state['bfs_found'] = True
                    st.rerun()
                    return 
        time.sleep(speed)
        st.rerun()


    elif st.session_state['bfs_mode'] == 'backtrack' and st.session_state['bfs_found']:
        parent = st.session_state["bfs_parent"]
        start = st.session_state["start"]
        end = st.session_state["end"]
        
        r, c = end  # ✅ Fix: initialize r, c to start from the end
        path = []

        while (r, c) != start:
            if parent[r][c] is None:
                break
            r, c = parent[r][c]
            if (r, c) != start:
                path.append((r, c))

        for r, c in reversed(path):
            st.session_state.grid[r][c] = 3
            time.sleep(speed)

        st.session_state['bfs_mode'] = None
        st.rerun()



if st.button("Run BFS"):
    reset_path()
    st.session_state['bfs_queue'] = deque([st.session_state['start']])
    st.session_state['bfs_visited'] = [[False] * COLS for _ in range(ROWS)]
    st.session_state['bfs_visited'][st.session_state['start'][0]][st.session_state['start'][1]] = True
    st.session_state["bfs_parent"] = [[None]*COLS for _ in range(ROWS)]
    st.session_state["bfs_mode"] = 'search'
    st.session_state["bfs_found"] = False
    st.rerun()

if 'bfs_mode' in st.session_state and st.session_state.bfs_mode:
    bfs()


##DFS 
def dfs():
    stack = st.session_state["dfs_stack"]
    visited = st.session_state["dfs_visited"]
    parent = st.session_state["dfs_parent"]
    end = st.session_state['end']


    if st.session_state["dfs_mode"] == 'search':
        if not stack:
            st.session_state['dfs_mode'] = None
            return 
        
        r, c = stack.pop()

        if(r, c) != st.session_state['start'] and (r, c) != end:
            st.session_state.grid[r][c] = 2

        for dr, dc in [(0,1), (1,0), (0,-1),(-1,0)]:
            x, y = r + dr, c + dc
            if 0 <= x < ROWS and 0 <= y < COLS and not visited[x][y] and st.session_state.grid[x][y] != 1:
                visited[x][y] = True
                parent[x][y] = (r, c)
                stack.append((x, y))
                if(x, y) == end:
                    st.session_state['dfs_mode'] = 'backtrack'
                    st.session_state['dfs_found'] = True
                    st.rerun()
                    return 
                
        time.sleep(speed)
        st.rerun()

    elif st.session_state['dfs_mode'] == 'backtrack' and st.session_state['dfs_found'] :
        r, c = end
        path = []
        while (r, c) != st.session_state['start']:
            if parent[r][c] == None:
                break
            r, c = parent[r][c]
            if (r, c) != st.session_state['start']:
                path.append((r, c))

        for r, c in reversed(path):
            st.session_state.grid[r][c] = 3
            time.sleep(speed)
        st.session_state['dfs_mode'] = None
        st.rerun()


if st.button("Run DFS"):
    reset_path()
    st.session_state['dfs_stack'] = [st.session_state['start']]
    st.session_state['dfs_visited'] = [[False] * COLS for _ in range(ROWS)]
    st.session_state['dfs_visited'][st.session_state['start'][0]][st.session_state['start'][1]] = True
    st.session_state['dfs_mode'] = 'search'
    st.session_state["dfs_parent"] = [[None]*COLS for _ in range(ROWS)]
    st.session_state['dfs_found'] = False
    st.rerun()

if 'dfs_mode' in st.session_state and st.session_state['dfs_mode']:
    dfs()



## Dijstras
def dijkstra():
    pq = st.session_state['dij_pq']
    distance = st.session_state['dij_dis']
    parent = st.session_state['dij_parent']
    end = st.session_state['end']

    if st.session_state['dij_mode'] == 'search':
        if not pq:
            st.session_state['dij_mode'] = None
            return 
        dist, r, c = heapq.heappop(pq)

        if (r, c) != st.session_state['start'] and (r, c) != end:
            st.session_state.grid[r][c] = 2

        for dr, dc in  [(0,1), (1, 0), (0, -1),(-1,0)]:
            x, y = r + dr, c + dc
            if 0 <= x < ROWS and 0 <= y < COLS and st.session_state.grid[x][y] != 1:
                new_dist = dist + 1
                if new_dist < distance[x][y]:
                    distance[x][y] = new_dist
                    parent[x][y] = (r, c)
                    heapq.heappush(pq, (new_dist, x, y))
                    if(x, y) == end:
                        st.session_state['dij_mode'] = 'backtrack'
                        st.session_state['dij_found'] = True
                        st.rerun()
                        return 
                    
        time.sleep(speed)
        st.rerun()

    elif st.session_state['dij_mode'] == 'backtrack' and st.session_state['dij_found']:
        r, c = end
        path = []
        while(r, c) != st.session_state['start']:
            if parent[r][c] is None:
                break
            r, c = parent[r][c]
            if (r, c) != st.session_state['start']:
                path.append((r, c))
        for r, c in reversed(path):
            st.session_state.grid[r][c] = 3
            time.sleep(speed)
        st.session_state['dij_mode'] = None
        st.rerun()


if st.button("Run Dijkstra"):
    reset_path()
    st.session_state["dij_pq"] = [(0, *st.session_state["start"])]
    st.session_state["dij_dis"] = [[float("inf")] * COLS for _ in range(ROWS)]
    st.session_state["dij_dis"][st.session_state["start"][0]][st.session_state["start"][1]] = 0
    st.session_state["dij_parent"] = [[None] * COLS for _ in range(ROWS)]
    st.session_state["dij_mode"] = "search"
    st.session_state["dij_found"] = False
    st.rerun()


if 'dij_mode' in st.session_state and st.session_state['dij_mode']:
    dijkstra()


## A- Star
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar():
    pq = st.session_state['astar_pq']
    g_cost = st.session_state['astar_g']
    parent = st.session_state['astar_parent']
    end = st.session_state['end']

    if st.session_state['astar_mode'] == 'search':
        if not pq:
            st.session_state['astar_mode'] = None
            return
        
        f, g, r, c = heapq.heappop(pq)

        if (r, c) != st.session_state['start'] and (r, c) != end:
            st.session_state.grid[r][c] = 3

        for dr, dc in [(0,1), (1, 0), (0, -1), (-1, 0)]:
            x, y = r + dr, c + dc
            if 0 <= x < ROWS and 0 <= y < COLS and st.session_state.grid[x][y] != 1:
                new_g = g + 1
                if new_g < g_cost[x][y]:
                    g_cost[x][y] = new_g
                    f_score = new_g + heuristic((x, y), end)
                    parent[x][y] = (r, c)
                    heapq.heappush(pq, (f_score, new_g, x, y))
                    if (x, y) == end:
                        st.session_state['astar_mode'] = 'backtrack'
                        st.session_state['astar_found'] = True
                        st.rerun()
                        return

        time.sleep(speed)
        st.rerun()

    elif st.session_state['astar_mode'] == 'backtrack' and st.session_state['astar_found']:
        r, c = end
        path = []
        while (r, c) != st.session_state['start']:
            if parent[r][c] is None:
                break
            r,c = parent[r][c]
            if (r, c) != st.session_state['start']:
                path.append((r, c))
        for r, c in reversed(path):
            st.session_state.grid[r][c] = 3
            time.sleep(speed)
        st.session_state['astar_mode'] = None
        st.rerun()

if st.button("Run A*"):
    reset_path()
    st.session_state['astar_pq'] = [(0 + heuristic(st.session_state["start"], st.session_state["end"]), 0, *st.session_state["start"])]
    st.session_state['astar_g'] = [[float("inf")] * COLS for _ in range(ROWS)]
    st.session_state['astar_g'][st.session_state["start"][0]][st.session_state["start"][1]] = 0
    st.session_state['astar_parent'] = [[None] * COLS for _ in range(ROWS)]
    st.session_state['astar_mode'] = 'search'
    st.session_state['astar_found'] = False
    st.rerun()

if 'astar_mode' in st.session_state and st.session_state['astar_mode']:
    astar()

if st.button("Reset Grid"):
    st.session_state.grid = [[0]*COLS for _ in range(ROWS)]
    st.session_state['start'] = (0, 0)
    st.session_state['end'] = (ROWS-1, COLS-1)
    for key in ['bfs_queue', 'bfs_visited', 'bfs_parent', 'bfs_mode', 'bfs_found']:
        st.session_state.pop(key, None)
    st.rerun()
