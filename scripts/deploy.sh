#!/bin/bash

set -euo pipefail

if [ ! -f .env ]; then
  echo "Arquivo .env não encontrado. Copie .env.example para .env e ajuste os valores."
  exit 1
fi

# Carrega variáveis de ambiente do .env
set -a
source .env
set +a

aws cloudformation deploy \
  --stack-name "${AWS_STACK_NAME}" \
  --template-file cloudformation/template.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    InstanceProfileName="${INSTANCE_PROFILE_NAME}"

echo "Deploy concluído. Use 'aws cloudformation describe-stacks --stack-name ${AWS_STACK_NAME}' para ver o status."