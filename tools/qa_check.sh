#!/bin/bash
MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $MY_DIR/..
flake8 .
TMP=`mktemp -t coverage`
coverage erase
coverage run --branch ./manage.py test
coverage report > $TMP
cat $TMP
coverage html
if ! tail -n1 $TMP | grep -q "100%"; then
    open htmlcov/index.html
fi
rm $TMP

PIP_TMP=`mktemp -t pip`
diff <(cat requirements.* | grep -v "^#" | grep -v "^ *$" | sort) <(pip freeze | sort) | grep "^>" > $PIP_TMP
if grep -q "^>" $PIP_TMP; then
    echo
    echo "Packages missing from requirements:"
    cat $PIP_TMP | cut -c3-
fi
rm $PIP_TMP
