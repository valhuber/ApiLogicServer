export PATH=$PATH:/home/api_logic_server/bin

# cd ~

echo " "
echo "Welcome to ApiLogicServer - Docker container"
echo " "
cat ../../etc/issue

echo " "
echo "printenv..."
echo " "
printenv
echo " "

if [[ -z "${APILOGICSERVER_GIT}" ]]; then
  LOAD_GIT="No APILOGICSERVER_GIT"
else
  echo "Now: sh /home/api_logic_server/bin/run-project.sh ${APILOGICSERVER_GIT} ${APILOGICSERVER_FIXUP}"
  sh /home/api_logic_server/bin/run-project.sh ${APILOGICSERVER_GIT} ${APILOGICSERVER_FIXUP}

fi

ApiLogicServer
