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
 		return edit_distance_naive(s1[1:], s2[1:], l1-1, l2-1, Max);
 	else:
 		if Max == 0: return 1

 		ed1 = edit_distance_naive(s1[1:], s2, l1-1, l2, Max-1);
 		ed2 = edit_distance_naive(s1, s2[1:], l1, l2-1, Max-1);
 		ed3 = edit_distance_naive(s1[1:], s2[1:], l1-1, l2-1, Max-1);
 		return 1 + min(ed1, ed2, ed3); # Concerned only with the minimum edit distance



a = "editdistan"
b = "editdistance"

print edit_distance_naive(a, b, len(a), len(b), 100)


