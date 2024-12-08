#!/bin/bash
list=$(docker ps --format "table {{.Names}}")

# 로그 저장 폴더
loc="./log"

if [ ! -d $loc ] ; then
 mkdir $loc
fi

for item in $list
do
    if [[ "$item" == "competition_run"* ]]; then
        ct_name=$(echo $item | cut -d. -f1-2)
        # 컨테이너 로그 저장
        docker logs $item >& $loc/$ct_name.log
        # 각 컨테이너 별 최고 기록 저장
        echo "[$ct_name]" $(docker logs $item 2> /dev/null | grep "현재 최고기록" | tail -n1)
    fi
done