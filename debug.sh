#!/bin/bash

: ${GOOGLE_CLOUD_PROJECT?: GOOGLE_CLOUD_PROJECT project id is not provided}

cd function/note
GCP_PROJECT="$GOOGLE_CLOUD_PROJECT" functions-framework --target entrypoint --debug
