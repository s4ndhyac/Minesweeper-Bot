

class Neighbour:
    def __init__(self, x, y, needed, unexposed):
        x = x
        y = y
        needed = needed
        unexposed = unexposed


class Free:
    def __init__(self, x, y, exposedCount, unexposed, listEntries):
        x = x
        y = y
        exposedCount = exposedCount
        unexposed = unexposed
        listEntries = listEntries


class CList:
    def __init__(self, x, y, count, tried, num, prob, neighbour):
        x = x
        y = y
        count = count
        tried = tried
        num = num
        prob = prob
        neighbour = []


class BackTrack:
    def __init__(self):
        #   int		neighborNext;						// next neighbor entry to use
        # int		neighborStart[MAX_LISTS];			// starting neighbor for this list
        # int		neighborEnd[MAX_LISTS];				// last neighbor for this list
        # Neighbor neighborArray[MAX_HEIGHT * MAX_WIDTH];		// list of all neighbors
        # int		freeNext;							// number of entries in freeArray
        # Free	freeArray[MAX_HEIGHT * MAX_WIDTH];	// number of non-neighbors we can play in with guess 1 rule
        # List	listArray[MAX_HEIGHT * MAX_WIDTH];	// list entries
        # int		listUsed[MAX_HEIGHT][MAX_WIDTH];	// which list is this entry part of (-1 if none)
        # int		listNext;							// next entry to use
        # int		lists;								// number of lists found
        # int		minesUsed;							// current count of mines used
        # int		listStart[MAX_LISTS];				// starting index for a list
        # int		listEnd[MAX_LISTS];					// last entry for a list
        # int		listSolutions[MAX_LISTS];			// number of possible choices for each list
        # int		listMinMines[MAX_LISTS];			// min number of mines used
        # int		listMaxMines[MAX_LISTS];			// max number of mines used

    def AddNeighbour(self, cList, x, y):
      
