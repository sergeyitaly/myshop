#!/bin/bash
echo"$ENV_ARGS" | jq -r 'to_entries | .[] | "\(.key)=\(.value)"' > .env
