set -e
if [ "$LINT" ]; then
    flake8 tests rest_pandas --exclude migrations
else
    python setup.py test
fi
