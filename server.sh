#!/bin/bash

CUR_FILE=${BASH_SOURCE[0]}
CUR_DIR=$(cd `dirname $CUR_FILE`;pwd)

SERVER_FILE="server.py"
SERVER_PATH=$CUR_DIR/$SERVER_FILE


process_num(){
    process_num=$(ps -ef | grep $SERVER_FILE | grep -v grep | wc -l)
    echo $process_num
}

start(){
    process_num=$(process_num)

    if [[ ${process_num} -ne 0 ]]; then
        echo "服务已启动, 请使用重启命令"
        return 1
    else
        echo "正在启动服务"
        nohup python -u $SERVER_PATH &> $CUR_DIR/log/log.out 2>&1 &
        sleep 1
        process_num=$(process_num)
        if [[ ${process_num} -ne 0 ]]; then
            echo "服务启动成功"
        else
            echo "服务启动失败"
        fi
    fi
}

stop(){
    process_num=$(ps -ef | grep $SERVER_FILE | grep -v grep | wc -l)

    if [[ ${process_num} -eq 0 ]]; then
        echo "服务未启动,不用停止"
        return 1
    else
        echo "正在停止服务"
        ps -ef | grep $SERVER_FILE | grep -v grep | awk '{print $2}' | xargs kill -9
        sleep 1
        process_num=$(process_num)
        if [[ ${process_num} -eq 0 ]]; then
            echo "服务停止成功"
        else
            echo "服务停止失败"
        fi
    fi
}

restart(){
    stop
    sleep 1
    start
}

status(){
    ps -ef | grep $SERVER_FILE | grep -v grep
}

help(){
    echo "bash $CUR_FILE start: start the server"
    echo "bash $CUR_FILE stop: stop the server"
    echo "bash $CUR_FILE restart: restart the server"
    echo "bash $CUR_FILE status: check server status"
    echo "bash $CUR_FILE process_num: get server process number"
}

case $1 in
    start|stop|restart|status|process_num)
    $1
    ;;
    *)
    help
    exit
esac
