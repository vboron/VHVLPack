set -x

for ((i=10;i<=30;i++)); do
	./log_stats2graph.py /home/veronica/VHVLPack/xray_5A_pdbs/ $i
done
