# TropicalMagic

## Dependencies
* gfan
* Singular
* Python 2.7
* xlsxwriter module for python (if using `./newtondiagrams.py --excel`)
* gnuplot (if using `./newtondiagrams.py --plot`)

## Usage
Place the input files in the _input_ folder, refer to _input/README.md_ for file format

### `./step1and2.py`
This generates the elements inside the cones, to be processed by gfan later in `step3.sh`

* **Input:**  `input/cones`, `input/rays` and `input/reduced_grobner_base`
* **Output:** `output/elements.txt`, `output/elements/x-y-z.step2` (being _x,y,z_ the rays of the cone)

_elements.txt_ contains a list of the generated elements, and the generator cone, with the following format (one per line):
`(a,b,c,d) #(x,y,z)` being _x,y,z_ the rays of the cone, and _a,b,c,d,..._ the coordinates of the element.

_x-y-z.step2_ has __gfan__ format

### `./step3.sh`
This processes the elements generated in the previous step, and generates initial ideals for those elements using `gfan_initialforms --ideal`.

* **Input:**  _output/elements/x-y-z.step2_
* **Output:** *output/initial_ideals/x-y-z.step3*

As this is a slow process, elements that have been already processed and succeeded are not processed again (the input file is copied to _output/success/_).
The time limit for each calculation is 20 minutes, if this is exceeded, the input files is copied into _output/failure/_ and the execution for this particular file stops.

### `./step4.sh`
This converts the gfan output (an initial ideal) from previous step (_x-y-z.step3_) into Singular format (the original file is left intact). And then finds a smaller set of generators for that initial ideal with `step4.singular`

* **Input:**  *output/initial_ideals/x-y-z.step3*
* **Output:** _output/iigen/x-y-z.step4_

### `./newtondiagrams.py`
Prints the Type (1, 2 or 3) for the elements obtained in the beginning, the lower hull, the element and the cone.

`./newtondiagrams.py --plot` (argument is optional)  will output the _output/diagrams/x-y-z.png_ file for each element, generated using `gnuplot < plot.gnuplot`.

`./newtondiagrams.py --excel` (argument is optional) will output the _output/Results.xlsx_ file containing the output described below.

`./newtondiagrams.py --quiet` (argument is optional) suppresses the console output.

* **Input:**  _output/elements.txt_
* **Output:** _stdout_ (console), _output/diagrams/x-y-z.png_ (if `--plot` is used), _output/Results.xlsx_ (if `--excel` is used)

This is reads the _element.txt_ file and outputs (to console) the following information about each element (separated by tabs)
* Type
    * 1, 2 or 3 _(See: [Arithmetics and combinatorics of tropical Severi varieties of univariate polynomials](http://arxiv.org/abs/1601.05479))_
* Hidden Ties
    * Relevant when type is 3, in any other case this is `[]`
    * Example: `[(4, 5)]`
* Lower Hull:
    * List of the x coordinates for forming the hull sides.
    * Example: `[[0, 2], [2, 3, 4], [4, 5, 6]]`
* Points (from the element, enumerated):
    * The coordinates of the points for that newton diagram.
    * Example `[1225, 1564, 600, 300, 0, 0, 0]`
* Rays (the cone)
    * The indexes of the rays generating the cone for this element.
    * Example: `[3, 12, 13]`

Example line:
```
1	[]	[[0, 2], [2, 3, 4], [4, 5, 6]]	[1225, 1564, 600, 300, 0, 0, 0]	[3, 12, 13]
```

Example output _3-12-13.png_:

![3-12-13.png](sample.png)

### `./generators.py`
Reads _input/generators_ which contains cones, and tries to reduce the rays to the generator rays for the cone.

This is done by invoking the Singular commands `containsInSupport` and `containsRelatively`, if a ray is included in the cone determined by other rays, then it's removed.

* **Input:** _input/rays_ and _input/generators_
* **Output:** _output/generators.txt_

The output file _generators.txt_ has the input cone and the result cone separated by tabs and `=>`, one cone per line. And a set of all the generator rays at the end.
```
# Cones	=>	Generators:
{a b c d e}	=>	{a b c}
{x y z}	=>	{x y}
# Generator Rays: [a, b, c, x, y]
```
