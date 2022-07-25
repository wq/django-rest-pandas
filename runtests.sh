set -e
python -m unittest discover -s tests -t . -v
flake8 tests rest_pandas --exclude migrations
npm run test
