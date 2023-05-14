# echo "gh codespace ports -c $CODESPACE_NAME" >> ~/.bashrc

if [ -z "$CODESPACE_NAME" ]
then
    echo "Codespace ready"
else
    echo ".devcontainer/setup: port creation..."
    gh codespace ports visibility 5656:public -c $CODESPACE_NAME
    echo ".devcontainer/setup: port created"
fi
