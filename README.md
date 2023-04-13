# Note

```shell
pip install google-cloud-firestore
```

## GCP

Init GCP

```shell
gcloud auth login
gcloud config set project PROJECT_ID

# enable service (for new project and only first time)
gcloud services enable run.googleapis.com

# setup key for debugging
# change path if needed
export GOOGLE_APPLICATION_CREDENTIALS="path/to/xxxxxx-xxxxxx-xxxxxxxxxxxx.json"
```

## Debug

```shell
cd function/note
functions-framework --target entrypoint --debug
```

## Deploy

```shell
./deploy.sh
```


