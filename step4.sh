#!/bin/sh

TIME_OUT="20m"

mkdir -p output/iigen output/success output/failure
for input in $(ls output/initial_ideal | egrep '[0-9-]+\.step3' | sort -h)
do
	# Do not recalculate if already succeeded
	if [ ! -f output/success/$input ]
	then
		output=${input%.step3}.step4
		echo "Processing:" $input "into" $output

		cp output/initial_ideal/$input input.txt
		# 4.1 converts input.txt -> output.txt with singular format.
		./step4.1.py
		# 4.2 reads output.txt and generates iigen/file.step4
		timeout $TIME_OUT Singular -q < step4.2.singular > output/iigen/$output
		rm -f input.txt output.txt
		
		# If no output, or output is empty then we failed.
		if [ ! -f output/iigen/$output ] || [ `stat -c %s output/iigen/$output` -eq 0 ]
		then
			echo $input "Failed"
			rm -f output/iigen/$output
			cp output/initial_ideal/$input output/failure/$input
		else
			cp output/initial_ideal/$input output/success/$input
		fi
	fi
done
