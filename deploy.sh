#!/bin/bash

: ${GOOGLE_CLOUD_PROJECT?: GOOGLE_CLOUD_PROJECT project id is not provided}

pushd function/note

gcloud functions deploy notes \
--gen2 \
--runtime=python310 \
--region=asia-east1 \
--source=. \
--entry-point=entrypoint \
--trigger-http \
--allow-unauthenticated \
--set-env-vars GCP_PROJECT=$GOOGLE_CLOUD_PROJECT

popd

