ls -l | grep -oE '[a-z|A-Z|.]*txt' > tmp
lineNum=`wc -l tmp | awk '{print $1}'`
echo $lineNum
for i in $(seq 1 $lineNum)
do
	ii="$i"p
	bfFileName=`sed -n $ii tmp`
	newFileName=`echo $bfFileName | cut -d '.' -f 1-3`
	mv $bfFileName $newFileName
done
