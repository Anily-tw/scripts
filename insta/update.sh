cd $ANILY_INSTA_ROOT
git pull
mkdir build
cd build
cmake -DCLIENT=OFF ..
make -j$(nproc)
cp teeworlds_srv $ANILY_INSTA_ROOT/$ANILY_INSTA_SERVER_NAME
