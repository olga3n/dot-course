
all: build sort_triple sort_prob

build:
	/usr/bin/hadoop-0.20 \
	jar /usr/lib/hadoop-0.20/contrib/streaming/hadoop-streaming-0.20.2-cdh3u6.jar \
	-files 'mapper.py,reducer.py' \
	-input 'text.txt' \
	-mapper 'mapper.py' \
	-reducer 'reducer.py' \
	-output result\

sort_triple:
	cat result/part-00000 | sort -k4,4 -nr >result_triple.txt

sort_prob:
	cat result/part-00000 | sort -k6,6gr -k4,4nr >result_prob.txt

clean:
	rm -rd result