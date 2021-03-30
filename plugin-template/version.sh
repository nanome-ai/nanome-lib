if [ $# -eq 0 ]; then
	echo "To bump version, pass major/minor/patch "
else
	bump2version $1
fi
