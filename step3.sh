#!/bin/sh

TIME_OUT="20m"

mkdir -p output/initial_ideal output/success output/failure

# Process 
for input in $(ls output/elements | egrep '[0-9]+\.step2' | sort -h)
do
	# Do not recalculate if already succeeded	
	if [ ! -f output/success/$input ]
	then
		echo "Processing" $input
		output=${input%.step2}.step3

		# Execute take $input.step2 and generate $output.step3, fail if execution exceeds timeout
		timeout $TIME_OUT gfan_initialforms --ideal --stdin output/elements/$input --stdout output/initial_ideal/$output

		# If no output, or output is empty then we failed.
		if [ ! -f output/initial_ideal/$output ] || [ `stat -c %s output/initial_ideal/$output` -eq 0 ]
		then
			echo $input "Failed"
			rm -f output/initial_ideal/$output
			cp output/elements/$input output/failure/$input
		else
			cp output/elements/$input output/success/$input
		fi
	fi
done
