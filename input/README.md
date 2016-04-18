Input files should be here:
* cones
* rays
* reduced_grobner_base
* generators

## cones and generators
format {w x y z}
enclosed with bracket, one per line
### Example:
```
{31 50 65}
{82 115 120}
{82 121 142}
```
## rays
format w x y z # index
one per line
### Example
```
-1 0 0 0 0 0 0  #0
-2 -1 0 0 0 0 0 #1
-1 -1 0 0 0 0 0 #2
0 -1 0 0 0 0 0  #3
```

## reduced_grobner_base
gfan format
### Example
```gfan
Q[x,y,z]
{
    x^3*y*z,
    x*y^2+z*x^3
}
```
