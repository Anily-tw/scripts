cd ~/ddnet
git pull
mkdir build
cd build
cmake -DMYSQL=ON -DCLIENT=OFF ..
make -j$(nproc)
cp DDNet-Server ~/servers/server
