#!/bin/bash

cd function/note
GCP_PROJECT="$GOOGLE_CLOUD_PROJECT" functions-framework --target entrypoint --debug
