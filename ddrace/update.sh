cd $ANILY_DDRACE_SOURCE
git pull
mkdir build
cd build
cmake -DMYSQL=ON -DCLIENT=OFF ..
make -j$(nproc)
cp DDNet-Server $ANILY_DDRACE_ROOT/$ANILY_DDRACE_SERVER_NAME
