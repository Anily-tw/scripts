cd /home/souly/instagib
git pull
mkdir build
cd build
cmake -DCLIENT=OFF ..
make -j$(nproc)
cp teeworlds_srv /home/souly/insta/insta_server
