# these are the commands for building a debian package from this python module
rm -rf deb_dist/*
python3 setup.py --command-packages=stdeb.command bdist_deb