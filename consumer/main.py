import json
import boto3
from secret_keys import SecretKeys

secret_keys = SecretKeys()
sqs_client = boto3.client(
    "sqs",
    region_name=secret_keys.REGION_NAME,
)

ecs_client = boto3.client(
    "ecs",
    region_name=secret_keys.REGION_NAME,
)


def poll_sqs():
    while True:
        response = sqs_client.receive_message(
            QueueUrl=secret_keys.AWS_SQS_VIDEO_PROCESSING,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10,
        )
        for message in response.get("Messages", []):
            message_body = json.loads(message.get("Body"))

            if (
                "Service" in message_body
                and "Event" in message_body
                and message_body.get("Event") == "s3:TestEvent"
            ):
                sqs_client.delete_message(
                    QueueUrl=secret_keys.AWS_SQS_VIDEO_PROCESSING,
                    ReceiptHandle=message["ReceiptHandle"],
                )
                continue

            # Extract info from actual S3 event message
            if "Records" in message_body:
                s3_record = message_body["Records"][0]["s3"]
                bucket_name = s3_record["bucket"]["name"]
                s3_key = s3_record["object"]["key"]

                print(f"Bucket: {bucket_name}")
                print(f"Key: {s3_key}")

                # spin up a docker container
                response = ecs_client.run_task(
                    cluster="arn:aws:ecs:ap-south-1:954976332532:cluster/VideoTranscoderCluster",
                    launchType="FARGATE",
                    taskDefinition="arn:aws:ecs:ap-south-1:954976332532:task-definition/video-transcoder:2",
                    overrides={
                        "containerOverrides": [
                            {
                                "name": "video-transcoder",
                                "environment": [
                                    {
                                        "name": "S3_BUCKET",
                                        "value": bucket_name,
                                    },
                                    {
                                        "name": "S3_KEY",
                                        "value": s3_key,
                                    },
                                ],
                            }
                        ]
                    },
                    networkConfiguration={
                        "awsvpcConfiguration": {
                            "subnets": [
                                "subnet-0accff48a61623525",
                                "subnet-061467275ae0e8442",
                                "subnet-0fcfdbffbb4c94633",
                                "subnet-00b062743e282b6a6",
                                "subnet-0bf022766f2b0c6b2",
                            ],
                            "assignPublicIp": "ENABLED",
                            "securityGroups": ["sg-0dd4bada1b632567d"],
                        }
                    },
                )

                print(response)
                sqs_client.delete_message(
                    QueueUrl=secret_keys.AWS_SQS_VIDEO_PROCESSING,
                    ReceiptHandle=message["ReceiptHandle"],
                )


poll_sqs()
