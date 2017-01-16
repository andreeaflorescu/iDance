#!/bin/bash
echo $#
if [ $# -ne 1 ]; then 
	echo "Error: Illegal number of parameters"
	echo "Usage: ./convert_all_au_to_wav <au_files_directory>"	
fi
cd $1
find . -name "*.au" | xargs awk '{file=FILENAME ;wav=".wav"; new_f=substr(file, 0, length(file) - 2); new_f=new_f wav; print new_f; system("sox "file " " new_f) }'
cd -
