export PATH=$PATH:/home/api_logic_server/bin
export PYTHONPATH="$PYTHONPATH:/home/api_logic_server"
# echo PYTHONPATH=$PYTHONPATH

ApiLogicServer welcome

osv=$(cat ../../etc/issue)
echo "     $ printenv       for OS context       information -- $osv"
echo "     $ ApiLogicServer for API Logic Server information"
echo " "

if [[ -z "${CODESPACES}" ]]; then
  LOAD_GIT="Not Codespaces"
else
  echo "Now: gh codespace ports visibility 5656:public -c $CODESPACE_NAME"
  gh codespace ports visibility 5656:public -c $CODESPACE_NAME
fi

if [[ -z "${APILOGICSERVER_GIT}" ]]; then
  LOAD_GIT="No APILOGICSERVER_GIT"
else
  echo "Now: sh /home/api_logic_server/bin/run-project.sh ${APILOGICSERVER_GIT} ${APILOGICSERVER_FIXUP}"
  sh /home/api_logic_server/bin/run-project.sh ${APILOGICSERVER_GIT} ${APILOGICSERVER_FIXUP}
fi
