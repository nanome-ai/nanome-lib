if [ $# -eq 0 ]
then
	echo "No version bump. To bump version, pass major/minor/patch "
else
	bump2version $1
fi

echo "Zipping plugin template "
rm -f nanome/plugin-template.zip
(cd plugin-template && zip -9r ../nanome/plugin-template.zip .)

rm -rf build
rm -rf dist
rm -rf *.egg-info

python setup.py sdist
python setup.py bdist_wheel --universal

read -rp "Upload? [yes/no] "

if [[ $REPLY =~ ^yes$ ]]; then
	twine upload dist/*
else
	echo "Upload canceled "
fi
