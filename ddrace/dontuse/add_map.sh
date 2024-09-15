#!/bin/bash
[ $# -lt 7 ] && echo "Usage: add_map mapname mappath category mapper points stars timestamp" >&2 && exit 1

base_dir=/home/souly/servers

mapname=$1
mappath=$2
category=$3
mapper=$4
points=$5
stars=$6
timestamp=$7

if [[ -z "$mapname" || -z "$mappath" ]]; then
    echo "Empty string"
    exit
elif [[ ! -e "$base_dir/maps/$mappath.map" ]]; then
    echo "Such map does not exit (it should be in maps/)"
    exit
fi

if [[ $category != "anime" && $category != "souly" && $category != "joni" && $category != "other" ]]; then
    echo "Use 'anime', 'souly', 'joni' or 'other' category"
    exit
fi
echo "add_vote \"$mapname\" \"sv_reset_file types/$category/flexreset.cfg; change_map \\\"$mappath\\\"\"" >> "$base_dir/types/$category/votes.cfg"

echo "USE teeworlds;" >> sql_tmp.sql
echo "INSERT INTO \`record_maps\`(\`Map\`, \`Server\`, \`Points\`, \`Stars\`, \`Mapper\`, \`Timestamp\`) VALUES ('$mappath','$category','$points','$stars','$mapper', '$timestamp');" >> sql_tmp.sql
mysql --user=teeworlds --password=superpass < sql_tmp.sql
rm sql_tmp.sql

echo "Success!"
