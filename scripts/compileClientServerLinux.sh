#!bin/bash

cd src/
bash creategameprojects
cd game/client/
make -f client_linux32_custom.mak CFG=debug
mv obj_client_custom_linux32/debug/client.so ../../../bin/
cd ../../
cd game/server/
make -f server_linux32_custom.mak CFG=debug
mv obj_server_custom_linux32/debug/server.so ../../../bin/
