source paths
. ./work_env.sh
# Uncomment below to evaluate all images
#IMAGE_FILE="$IMAGE_PATH/*.jpg"


# Build the inference binary.
cd $ROOT_PATH/im2txt
bazel build -c opt //im2txt:run_inference

# Ignore GPU devices (only necessary if your GPU is currently memory
# constrained, for example, by running the training script).
export CUDA_VISIBLE_DEVICES=""

tempfile=$(mktemp)
# Run inference to generate captions.
bazel-bin/im2txt/run_inference \
  --checkpoint_path=${MODEL_DIR}/train \
  --vocab_file=${VOCAB_FILE} \
  --input_files=${IMAGE_FILE} > $tempfile

cd $ROOT_PATH
./scripts/jsonifyCaptions.py -i $tempfile > captions.json

