#!/usr/bin/env bash

# Setup python environment
. ./work_env.sh
. paths



# Install bazel if it is missing
if [[ $(ls -1 $BAZEL_BIN | wc -l) -eq 0 ]]; then
    echo "Installing bazel"
    wget https://github.com/bazelbuild/bazel/releases/download/0.22.0/bazel-0.22.0-installer-linux-x86_64.sh
    bash bazel-0.22.0-installer-linux-x86_64.sh --user
    rm bazel-0.22.0-installer-linux-x86_64.sh
    echo "Installation done"
fi

# Build mscoco data
cd $ROOT_PATH/im2txt
$BAZEL_BIN build //im2txt:download_and_preprocess_mscoco
./bazel-bin/im2txt/download_and_preprocess_mscoco "${MSCOCO_DIR}"

# Install the rest of the items
cd $ROOT_PATH/im2txt
$BAZEL_BIN build -c opt //im2txt/...

# Download and unpack inception pre-trained model
cd $ROOT_PATH
if [[ $(ls $INCEPTION_CHECKPOINT | wc -l) -eq 0 ]]; then
    wget "http://download.tensorflow.org/models/inception_v3_2016_08_28.tar.gz"
    mkdir -p $INCEPTION_CHECKPOINT_PATH
    tar -xf "inception_v3_2016_08_28.tar.gz" -C "$INCEPTION_CHECKPOINT_PATH"
    rm inception_v3_2016_08_28.tar.gz
fi

# Prepare coco captioning library
cd $ROOT_PATH/coco-caption
./get_stanford_models.sh
