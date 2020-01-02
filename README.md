# Registry-Cleaner

Registry Cleaner is singular or multiple tag deletion tool from private docker registry.

Libraries that must be pre-installed to run the program :
- requests
- argparse

## Parameters
|Parameter                         |Description                                                                            |
|----------------------------------|---------------------------------------------------------------------------------------|
|`--host/-host "value"`            |'Registry URL'                                                                         |
|`--username/-u "value"`           |"Registry username"                                                                    |
|`--password/-p "value"`           |"Registry user password"                                                               |
|`--get-repos/-get-repos`          |"For list all repos in registry"                                                       |
|`--get-tags/-get-tags "repo-name"`|"For list all tags of written repo"                                                    |
|`--tag/-t "repo:tag"`             |"Repos and tags you want to delete, use like 'repo1:tag1 repo1:tag2 repo2:tag repo3:*'"|
|`--allready-login/-already-login` |"Use if you already login private docker registry"                                     |
|`--config/-c`                     |"If you want to specify config path"                                                   |
|`--yes/-yes`                      |"To delete the listed repos"                                                           |



> If your user is not include docker group, you must run with sudo.

### Example Usages

For listing all repos:
> python3 registry-cleaner.py --host registry.abc.xyz --username foo --password bar --get-repos

For listing all tags from written repo
> python3 registry-cleaner.py --host registry.abc.xyz --username foo --password bar --get-tags repo-name

List specified repo and tag
> python3 registry-cleaner.py --host registry.abc.xyz --username foo --password bar --tag repo1:tag1 repo1:tag2 repo2:tag repo3:*

If you already login private docker registry and you don't want to enter username or password use --already-login. Default config file at /home/user/.docker/config.json.
> python3 registry-cleaner.py --host registry.abc.xyz --get-tags repo-name --already-login

If you want to specify config.json file path, use --config parameter.
> python3 registry-cleaner.py --host registry.abc.xyz --get-tags repo-name --already-login --config /home/user/xyz/config.json

To delete the listed tag add --yes.
> python3 registry-cleaner.py --host registry.abc.xyz --username foo --password bar --tag repo1:tag1 repo1:tag2 repo2:tag --yes


### Example Usages with pip

For listing all repos:
> cleaner --host registry.abc.xyz --username foo --password bar --get-repos

For listing all tags from written repo
> cleaner --host registry.abc.xyz --username foo --password bar --get-tags repo-name

List specified repo and tag
> cleaner --host registry.abc.xyz --username foo --password bar --tag repo1:tag1 repo1:tag2 repo2:tag repo3:*

If you already login private docker registry and you don't want to enter username or password use --already-login. Default config file at /home/user/.docker/config.json.
> cleaner --host registry.abc.xyz --get-tags repo-name --already-login

If you want to specify config.json file path, use --config parameter.
> cleaner --host registry.abc.xyz --get-tags repo-name --already-login --config /home/user/xyz/config.json

To delete the listed tag add --yes.
> cleaner --host registry.abc.xyz --username foo --password bar --tag repo1:tag1 repo1:tag2 repo2:tag --yes
