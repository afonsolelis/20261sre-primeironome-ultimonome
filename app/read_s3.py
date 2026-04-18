import os
import boto3


def list_bucket_objects(bucket_name: str) -> list[str]:
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket_name)
    return [obj['Key'] for obj in response.get('Contents', [])] if response.get('Contents') else []


def main() -> None:
    bucket = os.environ.get('PIPELINE_BUCKET')
    if not bucket:
        raise SystemExit('Defina a variável de ambiente PIPELINE_BUCKET com o nome do bucket S3')

    keys = list_bucket_objects(bucket)
    print(f'Bucket S3: {bucket}')
    print(f'Total de objetos: {len(keys)}')
    for key in keys:
        print(f' - {key}')


if __name__ == '__main__':
    main()
