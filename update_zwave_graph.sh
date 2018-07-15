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


check_dir "bin"
check_dir "www"
check_dir "packages/ui"

echo "Installing Python requirements"

source /var/lib/homeassistant/bin/activate
pip3 install --upgrade networkx
deactivate

get_file z-wave-graph.py https://github.com/OmenWild/home-assistant-z-wave-graph/blob/master/bin/z-wave-graph.py bin/
chmod u+x,g+x bin/z-wave-graph.py
get_file z-wave-graph.html https://github.com/OmenWild/home-assistant-z-wave-graph/blob/master/config/www/z-wave-graph.html www/


echo "Assembling packages/ui/z_wave_graph.yaml"

tmp_dir="$(mktemp -d)"
tmp_config="$tmp_dir/z_wave_graph.yaml"
dest_config="packages/ui/z_wave_graph.yaml"
> "$tmp_config"

get_file automation.yaml https://github.com/OmenWild/home-assistant-z-wave-graph/blob/master/config/automations/z-wave-graph.yaml "$tmp_dir/"
sed -i 's/\(.*\)/  \1/' "$tmp_dir/automation.yaml"
echo "automation:" >> "$tmp_config"
cat "$tmp_dir/automation.yaml" >> "$tmp_config"

get_file panel_iframe.yaml https://github.com/OmenWild/home-assistant-z-wave-graph/blob/master/config/panel_iframe/z-wave-graph.yaml "$tmp_dir/"
sed -i 's/\(.*\)/  \1/' "$tmp_dir/panel_iframe.yaml"
echo "panel_iframe:" >> "$tmp_config"
cat "$tmp_dir/panel_iframe.yaml" >> "$tmp_config"

# Better to write our own shell cmd
# Otherwise, sample is here: https://github.com/OmenWild/home-assistant-z-wave-graph/blob/master/config/shell_commands/z-wave-graph.yaml
echo "shell_command:" >> "$tmp_config"
echo "  z_wave_graph: \"/var/lib/homeassistant/bin/python /home/hass/.homeassistant/bin/z-wave-graph.py --config /home/hass/.homeassistant/configuration_z_wave_graph.yaml\"" >> "$tmp_config"

diff "$dest_config" "$tmp_config" &>/dev/null
if [ $? == 0 ]; then
  echo "Config up to date."
else
  mv "$tmp_config" "$dest_config"
fi

rm -rf "$tmp_dir"

