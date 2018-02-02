for a in 10 20 40; do
	for b in 20; do
		time(./shell_pyprism.py 3 5 $a $b >> dump_.txt) &>>time.txt
		mv image.png images/image_${a}_$b.png
		done
	done

