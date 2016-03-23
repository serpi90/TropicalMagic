set term png
set xzeroaxis
set out 'test.png'
set offset 1,1,1,1
plot 'points.dat' using 1:2:(sprintf("(%d, %d)", $1, $2)) with labels point pt 7 lc rgb 'red' lw 6 offset char 1,1 notitle, 'lower.dat' pt 7 lc rgb 'black' lw 3 with linespoints notitle
