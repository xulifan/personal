find . -type d | sort | awk '$0 !~ last "/" {print last} {last=$0} END {print last}'
