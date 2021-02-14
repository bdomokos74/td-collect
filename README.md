## Function app to get 

### How to run

1. Init python env (make sure python3 is installed and on the path)
```
python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt

python test/yfinance_test.py
```

2. Experiment with Jupyter Notebook
```
jupyter notebook notebooks/
```

3. Run function app locally

From VS Code press F5

### Setting up dev env

1. Create service principal for development
```
az ad sp create-for-rbac --name dev-sp-rbac --skip-assignment --sdk-auth > tmpdata/local-sp.json
```
2. Based on tmpdata/local-sp.json, add env variables to thee local.settings.json, Variables section:
```
"STORAGE_ACCOUNT_NAME": "...",
"BLOB_CONTAINER_NAME": "...",
"AZURE_CLIENT_ID": "...",
"AZURE_CLIENT_SECRET": "...",
"AZURE_SUBSCRIPTION_ID": "...",
"AZURE_TENANT_ID": "..."
```

3. Authorize the service principal to be able to access the test storage blob
```
az ad sp list --all --query "[].{displayName:displayName, objectId:objectId}" --output tsv
az ad sp list --display-name dev-sp-rbac
az ad sp list --filter "appid eq '...'"

az role definition list --query "[].{name:name, roleType:roleType, roleName:roleName}" --output tsv

az role assignment create --assignee "..." \
--role "Storage Blob Data Contributor" \
--scope "/subscriptions/5624ad56-ba19-4366-b73f-7d1a242ea122/resourceGroups/aztrdalertfunction/providers/Microsoft.Storage/storageAccounts/aztrdteststorage"
```

### Notes

#### Set up local env

https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-authenticate?tabs=cmd#identity-when-running-the-app-on-azure

https://docs.microsoft.com/en-us/azure/developer/python/configure-local-development-environment?tabs=bash

https://docs.microsoft.com/en-gb/azure/azure-functions/functions-run-local?tabs=macos%2Ccsharp%2Cbash#local-settings-file

https://code.visualstudio.com/docs/editor/tasks

#### Create service principal, and add roles:

https://docs.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli#create-a-service-principal

https://docs.microsoft.com/en-us/azure/role-based-access-control/role-assignments-steps

https://github.com/Azure/azure-sdk-for-python/blob/master/sdk/storage/azure-storage-blob/samples/blob_samples_service.py