#!/bin/bash

pushd ..
ls

if [ $# -eq 0 ]
    then
        echo " "
        echo "Pushes new API Logic Project to new empty (existing) git repository"
        echo " "
        echo "VSCode provide Source Control >> Publish (New Repository - should *not* exist"
        echo " "
        echo "Usage:"
        echo "  cd devops                                 # this folder"
        echo "  git_push_new_project.sh <git repos name>  # copy this from GitHub"
        echo " "
        echo " "
        echo "For subsequent pushes, use IDE support"
        echo " "
        exit 0
    fi

echo ""
read -p "Press [Enter] to push new API Logic Project to new git repository > "

git init
git branch -m main
git add .
git commit -m 'First commit'
git remote add origin $1
git remote -v
git remote set-url origin "$1"
git push origin main
git branch --set-upstream-to=origin/main
popd
