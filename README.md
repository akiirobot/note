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

Create firestore

```shell
gcloud alpha firestore databases create \
--database=note \
--location=asia-east1 \
--type=firestore-native
```

## Debug

```shell
python -m venv venv
source venv/bin/activate
pip install functions-framework
pip install -r function/note/requirements.txt
```

```shell
./debug.sh
```

## Deploy

```shell
./deploy.sh
```


