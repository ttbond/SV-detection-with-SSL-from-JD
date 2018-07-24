ls -l | grep -oE '[a-z|A-Z|.]*info' > tmp
lineNum=`wc -l tmp | awk '{print $1}'`
touch wgs.ALL.info
echo $lineNum
for i in $(seq 1 $lineNum)
do
	ii="$i"p
	fileName=`sed -n $ii tmp`
	cat $fileName >> wgs.ALL.info
done
rm tmp
