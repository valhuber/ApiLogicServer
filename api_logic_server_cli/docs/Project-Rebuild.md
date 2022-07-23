## Preserving Customizations over Iterations
Your customizations are made to the files in the following sections.  These are separate files from the core model and api files, so that (if you wish) you can recreate the system from a revised schema, then simply copy over the files described below.

&nbsp;


## Rebuilding

Ignoring the boxes labeled "rebuild", the key elements of the creation process are illustrated below:

* the system reads the database schema to create `models.py`


* `models.py` drives the creation process


* you customize the created project, mainly by altering the files on the far right

As shown in the diagram, creation is always driven from `models.py.`  Models differ from physical schemas in important ways:

* the system ensure that class names are capitalized and singular


* there are good reasons to customize `models.py`:
   * to add foreign keys missing in the database - these are critical for multi-table apis and applications
   * to provide better naming

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/extended_builder/rebuild-from.png?raw=true"></figure>

You can rebuild your project, preserving customizations (including any additional files you have created).  You have 2 alternatives, depending on where you choose the _"source of truth"_ for your database:

| Source of Truth | Means | Use `rebuild` option |
| :--- |:---|:---|
| Database | The schema is the source of truth<br><br>It includes all the foreign keys | `rebuild-from-datatabase:` rebuilds the files shown in blue and purple. |
| Model | Model is the source of truth<br><br>Use SQLAlchemy services to drive changes into the database |`rebuild-from-model:` rebuilds the files shown in blue |

Note that `ui/admin/admin.yaml` is never overwritten (the dotted line 
means it is written on only on `create` commands).  After rebuilds, merge the new `ui/admin/admin-created.yaml` into your customized `admin.yaml.`

&nbsp;

### API and Admin App merge updates

As of release 5.02.03, ```rebuild``` services provide support for updating customized API and Admin:

| System Object | Support |
| :---  | :--- |
| API | `api/expose_api_models_created.py` created with new `database/models.py` classes |
| Admn App | `ui/admin/admin-merge.yaml` is the merge of `ui/admin/admin.yaml` and new `database/models.py` classes |

Review the altered files, edit (if required), and copy them over the original files.

&nbsp;
