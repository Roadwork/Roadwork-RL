if [ -z $1 -o -z $2 ]; then
  echo "Usage: ./$0 <DEPLOY_NAME> <DESTINATION>"
  echo "Example: ./$0 rw-server-openai ./output-server"
  exit 1
fi

POD_NAME=$(kubectl get pods --selector=app=p-$1 -o jsonpath='{.items[0].metadata.name}')

kubectl cp $POD_NAME:output-server/ $2 -c c-$1