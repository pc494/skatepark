for a in $(seq 5 20 50); do
	for b in $(seq 5 100 905); do
		./GaAs_ED_prism_kinematic.py 3 5 $a $b
		mv image.png images/image_$a$b.png
		rm *.XYZ
		rm *.mrc
		done
	done
