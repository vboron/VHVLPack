set -x

for ((i=10;i<=30;i++)); do
	./log_stats2graph.py /home/veronica/VHVLPack/clean_unique_af2/ $i
done
