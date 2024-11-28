cd $ANILY_DDRACE_SOURCE
git pull
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release -DMYSQL=ON -DCLIENT=OFF -DANTIBOT=ON ..
make -j$(nproc)
cp DDNet-Server $ANILY_DDRACE_ROOT/$ANILY_DDRACE_SERVER_NAME
