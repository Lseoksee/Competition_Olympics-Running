#!/bin/bash
list=$(docker ps --format "table {{.Names}}")

# 로그 저장 폴더
loc="./log"

# 마지막 최고기록 저장 파일 이름
latest_file="$loc/latest.log"

if [ ! -d $loc ] ; then
 mkdir $loc
fi

echo "" > $latest_file
for item in $list
do
    if [[ "$item" == "competition_run"* ]]; then
        ct_name=$(echo $item | cut -d. -f1-2)
        # 컨테이너 로그 저장
        docker logs $item >& $loc/$ct_name.log
        # 각 컨테이너 별 최고 기록 저장
        echo "[$ct_name]" $(docker logs $item 2> /dev/null | grep "현재 최고기록" | tail -n1) >> $latest_file
    fi
done