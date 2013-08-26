IN_DIREC="$1/*"
OUT_DIREC=$2

echo $IN_DIREC
echo $OUT_DIREC

for filename in $IN_DIREC
do
    output=${filename/.jpg/.ppm}
    echo $filename $output
    djpeg -outfile $output $filename
    mv $output $OUT_DIREC
done
