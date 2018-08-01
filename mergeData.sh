ls -l | grep -oE 'ngs[a-z|A-Z|.]*info' > tmp
lineNum=`wc -l tmp | awk '{print $1}'`
touch ngs.ALL.info
echo $lineNum
for i in $(seq 1 $lineNum)
do
	ii="$i"p
	fileName=`sed -n $ii tmp`
	cat $fileName >> ngs.ALL.info
done
rm tmp
