#!/bin/bash
export target="../../../servers/install/ApiLogicServer"
export project=${target}/ApiLogicProject
# ls $target
# ls $project  ../../../servers/install/ApiLogicServer/ApiLogicProject

echo "\n\nCreates ApiLogicProject, tests rebuild-from-database and rebuild-from-model"
echo "... Validates key content of ui/admin/admin-merge.yaml"
echo "... Pre-req: creation tests first, to build servers/install/ApiLogicServer/venv"

if [ $# -eq 0 ]
    then
        echo " "
        echo " IMPORTANT - cd ApiLogicServer/tests/rebuild_tests folder"
        echo " "
        # ls ${project}/database
        echo " "
        echo "  sh rebuild-test.sh [ go ]"
        echo " "
        exit 0
  else
    if [ "$1" = "go" ]
        then
            echo ""
            read -p "Press [Enter] to proceed> "
            echo ""

            set -x
            alias activate='${target}/venv/bin/activate'
            $activate
            set +x
            source ${target}/venv/bin/activate
            set -x
            pwd
            pushd $target
            pwd

            ApiLogicServer create --project_name=ApiLogicProject --db_url=
            if [ -e ${project}/ui/admin/admin-merge.yaml ]
            then
                read -p "Error - file admin-merge.yaml exists in ${project}/ui/admin -- Press [Enter] to proceed> "
                exit 1
            else
                echo "ok... clean create, no admin-merge"
            fi

            ApiLogicServer rebuild-from-database --project_name=ApiLogicProject --db_url=
            if [ -e ${project}/ui/admin/admin-merge.yaml ]
                then
                    echo "rebuild-from-database ok - admin-merge.yaml exists "
                    if grep -q "new_resources: ''" ${project}/ui/admin/admin-merge.yaml
                        then
                            echo 'rebuild-from-database.. null merge properly handled'
                        else
                            echo 'rebuild-from-database.. no new_resources'
                            # more ${project}/ui/admin/admin-merge.yaml
                            # echo '..rebuild-from-database failed - did not see "new_resources: " in admin-merge.yaml'
                            # exit 1
                        fi
                    fi
                else
                    read -p "Error rebuild-from-database - file admin-merge.yaml not in ${project}/ui/admin -- Press [Enter] to proceed> "
                    exit 1
                fi

            popd
            cp models.py ${project}/database
            pushd $target
            ApiLogicServer rebuild-from-model --project_name=ApiLogicProject --db_url=
            if [ -e ${project}/ui/admin/admin-merge.yaml ]
                then
                    echo "rebuild-from-model ok - admin-merge.yaml exists "
                    if grep -q CategoryNew ${project}/ui/admin/admin-merge.yaml
                        then
                            echo '..rebuild-from-model contains new resource'
                        else
                            more ${project}/ui/admin/admin-merge.yaml
                            echo '..rebuild-from-model failed - did not see "new_resources: CategoryNew " in admin-merge.yaml'
                            exit 1
                        fi                    
                else
                    read -p "Error rebuild-from-model - file admin-merge.yaml not in ${project}/ui/admin -- Press [Enter] to proceed> "
                    exit 1
                fi
            
            echo "\nalembic test"
            pushd $project/database
            pwd
            alembic revision --autogenerate -m "Added Tables and Columns"
            alembic upgrade head
            popd

            popd
            pwd
            set +x
            echo "\nSuccess"
            echo "...rebuild-from-model    contains    new resource"
            echo "...rebuild-from-database contains no new resource\n"
    fi