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

2. Preencha `.env` com as credenciais do AWS Academy (aba **AWS Details > AWS CLI** do Learner Lab). Elas rotacionam a cada ~4h, então reabra o `.env` e recole sempre que o deploy começar a falhar com `ExpiredToken`:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_SESSION_TOKEN`
   - `AWS_DEFAULT_REGION=us-east-1`
   - `AWS_STACK_NAME=studentlab-s3-ec2-pipeline`
   - `INSTANCE_PROFILE_NAME=LabInstanceProfile`

3. Faça deploy da stack:

   ```bash
   bash scripts/deploy.sh
   ```

   O script carrega o `.env` e exporta as variáveis — a AWS CLI consome `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` / `AWS_SESSION_TOKEN` automaticamente, sem precisar de `aws configure` ou `~/.aws/credentials`.

### GitHub Codespaces

O fluxo acima funciona tal qual em Codespaces — AWS CLI já vem instalada na imagem default. Basta:

```bash
cp .env.example .env
# edite .env colando as credenciais do Learner Lab
bash scripts/deploy.sh
```

O `.env` está no `.gitignore`, então as credenciais não vão para o repo.

4. Após o deploy, verifique os outputs do CloudFormation para obter o bucket S3 e o IP público da EC2.

## Streamlit de teste

Esta stack também cria uma segunda instância EC2 que executa um app Streamlit simples.

- O Streamlit é exposto via Application Load Balancer público em `http://<StreamlitLoadBalancerDNS>`.
- A instância de Streamlit recebe acesso de `8501` apenas do ALB, não diretamente da internet.
- O app de teste está em `app/streamlit_app.py`

## Observações

- A EC2 utiliza uma role com permissão de leitura no bucket S3.
- O script instalado na instância escreve logs em `/var/log/read_s3.log`.
- Caso queira acessar a instância por SSH, forneça um key pair válido no template ou adicione o parâmetro `KeyName` manualmente no deploy.
