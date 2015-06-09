# Edit distance

# Function: edit_distance
# ------------------------
# This function is a recursive function that calculates the 
# Levenshtein distance between two strings. It stops functioning
# properly after the edit distance exceeds Max.

def edit_distance_naive(s1, s2, l1, l2, Max):
	if l1 == 0:
		return l2
	if l2 == 0:
		return l1
	if s1[0] == s2[0]:
		return edit_distance_naive(s1[1:], s2[1:], l1-1, l2-1, Max)
	else:
		if Max == 0: return 1

		ed1 = edit_distance_naive(s1[1:], s2, l1-1, l2, Max-1)
		ed2 = edit_distance_naive(s1, s2[1:], l1, l2-1, Max-1)
		ed3 = edit_distance_naive(s1[1:], s2[1:], l1-1, l2-1, Max-1)
		return 1 + min(ed1, ed2, ed3) # Concerned only with the minimum edit distance


def edit_distance_dynamic(s1, s2, l1, l2, Max):
	if l1 == 0:
		return l2
	if l2 == 0:
		return l1
	if s1[0] == s2[0]:
		return edit_distance_naive(s1[1:], s2[1:], l1-1, l2-1, Max)
	else:
		if Max == 0: return 1

		ed1 = edit_distance_naive(s1[1:], s2, l1-1, l2, Max-1)
		ed2 = edit_distance_naive(s1, s2[1:], l1, l2-1, Max-1)
		ed3 = edit_distance_naive(s1[1:], s2[1:], l1-1, l2-1, Max-1)
		return 1 + min(ed1, ed2, ed3) # Concerned only with the minimum edit distance


# Strings of size m and n are passed.
# Construct the Table for X[0...m, m+1], Y[0...n, n+1]
def EditDistanceDP(X, Y):
	# Cost of alignment
	cost = 0
	# leftCell, topCell, cornerCell
 
	m = len(X) + 1
	n = len(Y) + 1
 
	T = []
   
	# Initialize table
	for i in xrange(m):
		T.append([])
		for j in xrange(n):
			T[i].append(-1)

	print T
 
	# Set up base cases

	# T[i][0] = i
	for i in xrange(m):
		T[i][0] = i
 
	for j in xrange(n):
		T[0][j] = j
 
	# Build the T in top-down fashion
	for i in xrange(m):
		for j in xrange(n):

			left = T[i][j-1] + 1 # deletion
 
			top = T[i-1][j] + 1 # insertion
			if (X[i-1] != Y[j-1]):
				extraCost = 1
			else:
				extraCost = 0 
			# edit[(i-1), (j-1)] = 0 if X[i] == Y[j], 1 otherwise
			corner = T[i-1][j-1] + extraCost # may be replace

			# Minimum cost of current cell
			# Fill in the next cell T[i][j]
			T[i][j] = min(left, top, corner)
	# Cost is in the cell T[m][n]
	cost = T[m-1][n-1]
	print "DP cost", cost
	return cost



a = "abcd"
b = "ad"

# naive_cost = edit_distance_naive(a, b, len(a), len(b), 100)
# dpCost = EditDistanceDP(a, b)
# if naive_cost - dpCost == 0:
# 	print "Good"
# else:
# 	print "Problem"
# 	print naive_cost, dpCost
