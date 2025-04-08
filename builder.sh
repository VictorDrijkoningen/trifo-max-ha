#!/bin/bash

ARCH='aarch64'
ENTRYPOINT='trifomaxha.py'
HIDDEN_IMPORTS=""
IMPORTS=""


run_docker() {
        echo -e "\e[34mBuilding for $ARCH with entrypoint $ENTRYPOINT and imports $IMPORTS...\e[0m\c"

        docker run --rm --privileged multiarch/qemu-user-static --reset -p yes > /dev/null 2>&1

        ENTRYPOINT_FILE=$(basename $ENTRYPOINT)
        ELF_FILE=$(echo $ENTRYPOINT_FILE | sed 's/.py//g')

        docker run --platform "linux/arm64" --rm -t -v $(pwd):/root/ $2 /bin/bash -c "apt -qq update 2> /dev/null > /dev/null; \
        apt -qq install gcc zlib1g-dev -y 2> /dev/null > /dev/null; \
        pip3 -q install --upgrade pip; \
        pip3 install pyinstaller $IMPORTS; \
        pyinstaller /root/$ENTRYPOINT --distpath /root/ --onefile --clean $HIDDEN_IMPORTS > /dev/null; \
        mv /root/$ELF_FILE /root/$ENTRYPOINT_FILE-$ARCH"

        if [ $? -ne 0 ]; then
                echo -e "[\e[31mERROR\e[0m] Build failed"
                exit 1
        fi

        echo -e "[\e[32mOK\e[0m] Build completed successfully"
        rm -rf ./.cache
}

run_docker "linux/arm64" "arm64v8/python:3.7.11-stretch" ;;

