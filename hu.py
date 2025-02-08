f r o m c o l l e c t i o n s i m p o r t deque
d e f fi n d L a rg e s t ( g r i d ) :
d i r e c t i o n s = 1 [ 1 , 0 1 , I - 1 , 0 1 , [ 0 , 1 1 , [ 0 , -111
ROWS, COLS = len(grid), len(grid [0])
a r e a = 0
d e f b f s ( r , c ) :
q = d e q u e ()
g r i d [ r ] [ c ] = 0
q-append ( ( r , c ) )
r e s = 1
while q :
r o w, c o l = q - p o p ( )
f o r d r , d e i n directions:
n r , n c = d r + r o w, d e + col
g r i d I n r l I n c ] = 0
i f ( n r < = 0 o r n c < = 0 o r n r > = ROWS o r
n c > = COLS o r g r i d i n r l l n c l = = 1
) :
c o n t i n u e
q. append ( ( n r, nc))
r e s + = 1
r e t u r n r e s
f o r r i n range (ROWS):
f o r c i n range (COLS) :
i f g r i d [ r ] [ c ] == 1 :
a r e a += max(area, b f s ( r , c ) )
r e t u r n a r e a