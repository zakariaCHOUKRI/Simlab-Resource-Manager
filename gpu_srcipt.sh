#!/bin/sh

(squeue -t RUNNING -o "%N %b %C" | awk "NR>1 {split(\$2, gpuArray, \":\"); nodes[\$1]+=\$2; gpus[\$1]+=gpuArray[2]; cpus[\$1]+=\$3} END {for (node in nodes) print node, 1-gpus[node], 44-cpus[node]}" && sinfo -p gpu --noheader -o "%n %G %c" | awk "{gsub(/[^0-9]/, \"\", \$2); print \$1, \$2, \$3}") | grep -F " $(sinfo -o "%n %G" | grep "gpu" | awk "{print \$1}")" | column -t