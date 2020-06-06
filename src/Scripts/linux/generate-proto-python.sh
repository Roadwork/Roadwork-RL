# if [ -z $1 -o -z $2 ]; then
#   echo "Usage: ./generate-proto.sh <LOCATION_PROTO> <OUTPUT_FOLDER>"
#   echo "Example: ./generate-proto.sh Proto/ Server/Proto/"
#   exit 1
# fi

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROTO_FILE_LOCATION="$CURRENT_DIR/../../Proto/roadwork"
PROTO_FILE_NAME="roadwork.proto"
PROTO_OUTPUT_LOCATION="$CURRENT_DIR/../../Lib/python/roadwork/roadwork/proto"

mkdir -p $PROTO_OUTPUT_LOCATION

python3 -m grpc_tools.protoc --proto_path=$PROTO_FILE_LOCATION --python_out=$PROTO_OUTPUT_LOCATION --grpc_python_out=$PROTO_OUTPUT_LOCATION $PROTO_FILE_LOCATION/$PROTO_FILE_NAME
