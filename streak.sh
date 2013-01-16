#!/bin/bash

current="Mon Jan 1 02:00:00 1900"
counter=1

while [ $counter -le 1000000 ]; do
    export GIT_AUTHOR_DATE="$current -0700"
    export GIT_COMMITTER_DATE=$GIT_AUTHOR_DATE
    git commit --allow-empty -m "HTTP 418 I'm a teapot"

    echo $GIT_AUTHOR_DATE

    current=$(date -d "$current 1 days")

    counter=$(( $counter + 1 ))
done

# make things smaller
git gc
