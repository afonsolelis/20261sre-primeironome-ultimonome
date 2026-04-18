# 20261sre-primeironome-ultimonome

Projeto AWS com CloudFormation para pipeline de leitura S3 usando EC2.

## Estrutura

- `cloudformation/template.yaml` - stack que cria VPC, subnet pública, bucket S3, role `labrole`, instance profile e EC2.
- `scripts/deploy.sh` - script para deploy usando o arquivo `.env`.
- `.env.example` - template de variáveis de ambiente para AWS.
- `app/read_s3.py` - exemplo de script Python que lista objetos em um bucket S3.

## Como usar

1. Copie o arquivo de ambiente:

   ```bash
   cp .env.example .env
   ```

2. Ajuste `.env` conforme sua conta e perfil AWS.
   - `AWS_PROFILE=studentlab`
   - `AWS_DEFAULT_REGION=us-east-1`
   - `AWS_STACK_NAME=studentlab-s3-ec2-pipeline`
   - `INSTANCE_PROFILE_NAME=LabInstanceProfile`

3. Faça deploy da stack:

   ```bash
   bash scripts/deploy.sh
   ```

4. Após o deploy, verifique os outputs do CloudFormation para obter o bucket S3 e o IP público da EC2.

## Observações

- A EC2 utiliza uma role com permissão de leitura no bucket S3.
- O script instalado na instância escreve logs em `/var/log/read_s3.log`.
- Caso queira acessar a instância por SSH, forneça um key pair válido no template ou adicione o parâmetro `KeyName` manualmente no deploy.
