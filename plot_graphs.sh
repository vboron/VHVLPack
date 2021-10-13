set -x

for ((i=10;i<=30;i++)); do
	./log_stats2graph.py /home/veronica/VHVLPack/xray_5A_files_unique_to_af2data/ $i
done
