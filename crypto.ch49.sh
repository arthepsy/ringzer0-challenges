#/bin/sh
tar -xzf ch49.tar
cd ./flag || exit 0
openssl rsautl -decrypt -in flag.enc -out flag.dec -inkey private.pem
cat flag.dec
cd ..
rm -rf ./flag
