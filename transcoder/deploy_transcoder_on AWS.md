⸻

🚀 Deployment Guide: Transcoder Service on AWS (Web Console & CLI)

⸻

🧱 Prerequisites

Ensure you have the following:
	•	AWS Account with necessary permissions for ECR, ECS, and IAM.
	•	AWS CLI installed and configured:

aws configure

Provide your AWS Access Key ID, Secret Access Key, default region (e.g., ap-south-1), and output format (json).

	•	Docker installed and running on your local machine.
	•	Dockerized Transcoder Application with a Dockerfile.

⸻

📦 Step 1: Dockerize Your Application

Ensure your Dockerfile is set up correctly. Here’s an example:

FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]

Build the Docker image:

docker build -t video-transcoder .



⸻

🗃️ Step 2: Create an ECR Repository

🔹 Using AWS Console:
	1.	Navigate to the Amazon ECR Console.
	2.	Click “Create repository”.
	3.	Enter Repository name: video-transcode.
	4.	Leave other settings as default and click “Create repository”.

🔹 Using AWS CLI:

aws ecr create-repository --repository-name video-transcode

Note the repository URI from the output, e.g., 954976332532.dkr.ecr.ap-south-1.amazonaws.com/video-transcode.

⸻

🔐 Step 3: Authenticate Docker to ECR

🔹 Using AWS CLI:

aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 954976332532.dkr.ecr.ap-south-1.amazonaws.com



⸻

📤 Step 4: Tag and Push Docker Image to ECR

Tag the image:

docker tag video-transcoder:latest 954976332532.dkr.ecr.ap-south-1.amazonaws.com/video-transcode:latest

Push the image:

docker push 954976332532.dkr.ecr.ap-south-1.amazonaws.com/video-transcode:latest



⸻

🧾 Step 5: Register an ECS Task Definition

🔹 Using AWS Console:
	1.	Navigate to the Amazon ECS Console.
	2.	Click “Task Definitions” > “Create new Task Definition”.
	3.	Select “FARGATE” as the launch type and click “Next step”.
	4.	Configure the task:
	•	Family: video-transcoder
	•	Task role: ecsTaskExecutionRole (create if not existing)
	•	Network mode: awsvpc
	•	Task memory: 3 GB
	•	Task CPU: 1 vCPU
	5.	Add container:
	•	Container name: video-transcoder
	•	Image: 954976332532.dkr.ecr.ap-south-1.amazonaws.com/video-transcode:latest
	•	Port mappings: Container port 80
	6.	Configure logging:
	•	Log driver: awslogs
	•	Log group: /ecs/video-transcoder
	•	Region: ap-south-1
	•	Stream prefix: ecs
	7.	Click “Add”, then “Create”.

🔹 Using AWS CLI:

Create a JSON file transcoder-task.json with the task definition:

{
  "family": "video-transcoder",
  "requiresCompatibilities": ["FARGATE"],
  "networkMode": "awsvpc",
  "cpu": "1024",
  "memory": "3072",
  "executionRoleArn": "arn:aws:iam::954976332532:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "video-transcoder",
      "image": "954976332532.dkr.ecr.ap-south-1.amazonaws.com/video-transcode:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 80,
          "hostPort": 80,
          "protocol": "tcp"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/video-transcoder",
          "awslogs-region": "ap-south-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}

Register the task definition:

aws ecs register-task-definition --cli-input-json file://transcoder-task.json



⸻

🛰️ Step 6: Create an ECS Cluster

🔹 Using AWS Console:
	1.	Navigate to the Amazon ECS Console.
	2.	Click “Clusters” > “Create Cluster”.
	3.	Select “Networking only” (for Fargate) and click “Next step”.
	4.	Enter Cluster name: video-transcoder-cluster.
	5.	Click “Create”.

🔹 Using AWS CLI:

aws ecs create-cluster --cluster-name video-transcoder-cluster



⸻

🚀 Step 7: Run the Task

🔹 Using AWS Console:
	1.	Navigate to your cluster: Clusters > video-transcoder-cluster.
	2.	Click “Run new Task”.
	3.	Configure the task:
	•	Launch type: FARGATE
	•	Task definition: video-transcoder
	•	Platform version: LATEST
	•	Number of tasks: 1
	4.	Configure networking:
	•	Cluster VPC: select your VPC
	•	Subnets: select at least one subnet
	•	Security groups: select or create a security group
	•	Auto-assign public IP: ENABLED
	5.	Click “Run Task”.

🔹 Using AWS CLI:

aws ecs run-task \
  --cluster video-transcoder-cluster \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-abc123],securityGroups=[sg-abc123],assignPublicIp=ENABLED}" \
  --task-definition video-transcoder

Replace subnet-abc123 and security group IDs: