#/bin/sh
cd ./data || exit 1
mkdir ch49 && cd ch49 || exit 1
tar -xzf ../ch49.tar
cd flag || exit 1
openssl rsautl -decrypt -in flag.enc -out flag.dec -inkey private.pem
cat flag.dec
cd ../..
rm -rf ./ch49
cd ..
