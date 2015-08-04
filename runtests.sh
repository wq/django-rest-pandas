if [ "$LINT" ]; then
    flake8 tests rest_pandas
else
    python setup.py test
fi
