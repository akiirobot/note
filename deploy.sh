#!/bin/bash

pushd function/note

gcloud functions deploy note \
--gen2 \
--runtime=python310 \
--region=asia-east1 \
--source=. \
--entry-point=entrypoint \
--trigger-http \
--allow-unauthenticated

popd

