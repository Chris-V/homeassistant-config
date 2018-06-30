#!/bin/bash

function get_file {
  DOWNLOAD_PATH=${2}?raw=true
  FILE_NAME=$1
  if [ "${FILE_NAME:0:1}" = "/" ]; then
    SAVE_PATH=$FILE_NAME
  else
    SAVE_PATH=$3$FILE_NAME
  fi
  TMP_NAME=${1}.tmp
  echo "Getting $1"
  # wget $DOWNLOAD_PATH -q -O $TMP_NAME
  curl -s -q -L -o $TMP_NAME $DOWNLOAD_PATH
  rv=$?
  if [ $rv != 0 ]; then
    rm $TMP_NAME
    echo "Download failed with error $rv"
    exit
  fi
  diff ${SAVE_PATH} $TMP_NAME &>/dev/null
  if [ $? == 0 ]; then
    echo "File up to date."
    rm $TMP_NAME
    return 0
  else
    mv $TMP_NAME ${SAVE_PATH}
    if [ $1 == $0 ]; then
      chmod u+x $0
      echo "Restarting"
      $0
      exit $?
    else
      return 1
    fi
  fi
}

function check_dir {
  if [ ! -d $1 ]; then
    read -p "$1 dir not found. Create? (y/n): [n] " r
    r=${r:-n}
    if [[ $r == 'y' || $r == 'Y' ]]; then
      mkdir -p $1
    else
      exit
    fi
  fi
}

if [ ! -f configuration.yaml ]; then
  echo "There is no configuration.yaml in current dir. 'update.sh' should run from Homeassistant config dir"
  read -p "Are you sure you want to continue? (y/n): [n] " r
  r=${r:-n}
  if [[ $r == 'n' || $r == 'N' ]]; then
    exit
  fi
fi


check_dir "www/custom_ui/floorplan"
check_dir "www/custom_ui/floorplan/lib"
check_dir "panels"


get_file ha-floorplan.html https://github.com/Chris-V/ha-floorplan/blob/multiple_Actions/www/custom_ui/floorplan/ha-floorplan.html www/custom_ui/floorplan/
get_file state-card-floorplan.html https://github.com/Chris-V/ha-floorplan/blob/multiple_Actions/www/custom_ui/state-card-floorplan.html www/custom_ui/
get_file floorplan.html https://github.com/Chris-V/ha-floorplan/blob/multiple_Actions/panels/floorplan.html panels/
get_file jquery-3.2.1.min.js https://github.com/Chris-V/ha-floorplan/blob/multiple_Actions/www/custom_ui/floorplan/lib/jquery-3.2.1.min.js www/custom_ui/floorplan/lib/
get_file moment.min.js https://github.com/Chris-V/ha-floorplan/blob/multiple_Actions/www/custom_ui/floorplan/lib/moment.min.js www/custom_ui/floorplan/lib/
get_file svg-pan-zoom.min.js https://github.com/Chris-V/ha-floorplan/blob/multiple_Actions/www/custom_ui/floorplan/lib/svg-pan-zoom.min.js www/custom_ui/floorplan/lib/

