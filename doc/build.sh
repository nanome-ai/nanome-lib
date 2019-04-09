rm build/doctrees/*
rm build/html/*
rm source/_build/* -r

if [ $# -ne 0 ]
then
    replace=$1
    sed -i "s/version = .*/version = '${replace}'/g" source/conf.py
fi

sphinx-apidoc -M -l -f -e -o source/ ../nanome
./make.bat html

sed -i 's/\".nanome.*\./">/g' build/html/api.html