if [ $# -eq 0 ] 
then
	echo "No version bump. To bump version, pass major/minor/patch "
else
	bumpversion $1
fi

rm -rf build
rm -rf dist
rm -rf nanome.egg-info

python setup.py sdist bdist_wheel

read -rp "Upload? [yes/no] "

if [[ ${REPLY,,} =~ ^(yes)$ ]]; then
	twine upload dist/*
else
	echo "Upload canceled "
fi
