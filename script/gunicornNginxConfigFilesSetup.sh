#!/bin/bash

# PURPOSE
# Automate the error-prone process of setting up the necessary configuration files needed by Gunicorn
# and Nginx.

# USAGE
#     bash /absolute/path/from/literally/anywhere/to/script/gunicornNginxConfigFilesSetup.sh
#     or
#     bash ../relative/path/from/literally/anywhere/to/script/gunicornNginxConfigFilesSetup.sh

PROJECT_PATH=$(readlink -f "${BASH_SOURCE}" | xargs dirname | xargs dirname)
CONFIG_PATH="${PROJECT_PATH}/config"
ENVIRONMENT_VARIABLES_PATH="${CONFIG_PATH}/environmentVariables"

GUNICORN="gunicorn"
GUNICORN_SERVICE_NAME="${GUNICORN}.service"
GUNICORN_SERVICE="${CONFIG_PATH}/${GUNICORN_SERVICE_NAME}"
GUNICORN_SOCKET_NAME="${GUNICORN}.socket"
GUNICORN_SOCKET="${CONFIG_PATH}/${GUNICORN_SOCKET_NAME}"

NGINX_CONF_NAME="makeIdeasMakeRealityNginx.conf"
NGINX_CONF="${CONFIG_PATH}/${NGINX_CONF_NAME}"

DEFAULT_PORT="8000"
NEW_PORT="80"

printAndExecuteCommand()
{
    echo "---> Command: ${@}"
    eval "${@}"
}

restartGunicorn()
{
    sudo systemctl daemon-reload

    # sudo systemctl stop "${GUNICORN_SERVICE_NAME}"
    # sudo systemctl stop "${GUNICORN_SOCKET_NAME}"
    # sudo systemctl start "${GUNICORN_SERVICE_NAME}"
    # sudo systemctl start "${GUNICORN_SOCKET_NAME}"

    sudo systemctl restart "${GUNICORN_SERVICE_NAME}" # Stop and start, or just start if not running yet
    sudo systemctl restart "${GUNICORN_SOCKET_NAME}"
}

restartNginx()
{
    sudo systemctl daemon-reload

    # sudo systemctl stop "${MIMR_NGINX}"
    # sudo systemctl start "${MIMR_NGINX}"

    sudo systemctl restart "${MIMR_NGINX}"
}

setupGunicorn()
{
    printAndExecuteCommand "sudo ln -s -f ${GUNICORN_SERVICE} ${MIMR_SYSTEMD_PATH}"
    printAndExecuteCommand "sudo ln -s -f ${GUNICORN_SOCKET} ${MIMR_SYSTEMD_PATH}"
    echo "Done linking config files of ${GUNICORN}"

    printAndExecuteCommand "sudo systemctl enable --now ${GUNICORN_SOCKET_NAME}" # --now starts the units
    echo "Done enabling ${GUNICORN} to automatically start on boot"

    restartGunicorn # Not necessary, but to always be sure that all changes would reflect
    echo "Done restarting ${GUNICORN}"

    printAndExecuteCommand "systemctl show --value -p MainPID ${GUNICORN_SERVICE_NAME}"
    echo "Done processing service of ${GUNICORN}"
}

setupNginx()
{
    printAndExecuteCommand "sudo ln -s -f ${NGINX_CONF} ${MIMR_NGINX_SITES_AVAILABLE_PATH}"
    printAndExecuteCommand "sudo ln -s -f ${MIMR_NGINX_SITES_AVAILABLE_PATH}/${NGINX_CONF_NAME} ${MIMR_NGINX_SITES_ENABLED_PATH}"
    echo "Done linking config files of ${MIMR_NGINX}"

    printAndExecuteCommand "sudo systemctl enable --now ${MIMR_NGINX_SERVICE}"
    echo "Done enabling ${MIMR_NGINX} to automatically start on boot"

    echo "Use port ${NEW_PORT}? [y/n]"
    echo -n "---> Input: "
    read shouldUseNewPort

    # if [[ $# -eq 1 && "${1}" == "--changedefault" ]]; then
    if [[ "${shouldUseNewPort}" == "y" || "${shouldUseNewPort}" == "Y" ]]; then
        echo "Port ${NEW_PORT} would be used"
        printAndExecuteCommand "sed -i 's/listen '${DEFAULT_PORT}';/listen '${NEW_PORT}';/' ${NGINX_CONF}"
        printAndExecuteCommand "sudo rm -rf ${MIMR_NGINX_ENABLED_DEFAULT_CONF}"
    else
        echo "Port ${DEFAULT_PORT} would be used"
        printAndExecuteCommand "sed -i 's/listen '${NEW_PORT}';/listen '${DEFAULT_PORT}';/' ${NGINX_CONF}"
        printAndExecuteCommand "sudo ln -s -f ${MIMR_NGINX_AVAILABLE_DEFAULT_CONF} ${MIMR_NGINX_ENABLED_DEFAULT_CONF}"
    fi

    restartNginx
    echo "Done restarting ${MIMR_NGINX}"

    echo "Done processing service of ${MIMR_NGINX}"
}

displayStatus()
{
    printAndExecuteCommand "sudo systemctl status ${GUNICORN_SERVICE_NAME} | head -n 5"
    printAndExecuteCommand "sudo systemctl status ${GUNICORN_SOCKET_NAME} | head -n 5"
    printAndExecuteCommand "sudo systemctl status ${MIMR_NGINX} | head -n 5"

    printAndExecuteCommand "ls -al ${MIMR_SYSTEMD_PATH} | grep ${GUNICORN}"

    AVAILABLE_DEFAULT_CONF_NAME=$(basename "${MIMR_NGINX_AVAILABLE_DEFAULT_CONF}")
    ENABLED_DEFAULT_CONF_NAME=$(basename "${MIMR_NGINX_ENABLED_DEFAULT_CONF}")
    printAndExecuteCommand "ls -al ${MIMR_NGINX_SITES_AVAILABLE_PATH} | grep '${NGINX_CONF_NAME}\|${AVAILABLE_DEFAULT_CONF_NAME}'"
    printAndExecuteCommand "ls -al ${MIMR_NGINX_SITES_ENABLED_PATH} | grep '${NGINX_CONF_NAME}\|${ENABLED_DEFAULT_CONF_NAME}'"
}

source ${ENVIRONMENT_VARIABLES_PATH}
setupGunicorn
setupNginx
displayStatus
