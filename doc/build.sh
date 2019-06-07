rm -rf build/doctrees/*
rm -rf build/html/*
rm -rf source/_build/*

export NANOME_DOC_BUILD
NANOME_DOC_BUILD="sh"

rm -f source/nanome.*

sphinx-apidoc -M -l -f -e -o source/ ../nanome
./make.bat html

sed -i 's/\".nanome.*\./">/g' build/html/api.html