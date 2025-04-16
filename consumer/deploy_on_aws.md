

🧰 Step 1: Prepare Dockerfile for the Consumer

Here’s a sample Dockerfile based on your uploaded files:

# Dockerfile for Consumer Service
FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y gcc && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Run script
CMD ["python", "main.py"]

Save this as Dockerfile in the root of your consumer directory.

⸻

🚀 Step 2: Build and Push Docker Image (Optional)

You can either:
	•	Build and run the Docker image on EC2 directly, or
	•	Push it to ECR, and pull it on EC2.

Let me know your preference. If you’re okay to build on EC2 (easier right now), we’ll proceed.

⸻

☁️ Step 3: Launch and Setup EC2
	1.	Go to AWS Console → EC2 → Launch instance
	2.	Choose Amazon Linux 2 or Ubuntu
	3.	Select a small instance type (e.g., t2.micro)
	4.	Allow SSH (port 22) and outbound internet
	5.	Use a key pair you have access to

⸻

🔑 Step 4: SSH Into EC2 and Setup

ssh -i /path/to/your-key.pem ec2-user@<EC2-Public-IP>

Then run:

# Update and install Docker
sudo apt update && sudo apt install -y docker.io

# Start Docker and add user to docker group
sudo systemctl start docker
sudo usermod -aG docker $USER
newgrp docker



⸻

🐳 Step 5: Clone Your Consumer Repo and Build Docker Image

git clone <your-repo-url> consumer-service
cd consumer-service

# OR copy files manually via SCP if private
# scp -i key.pem ./* ec2-user@<EC2-IP>:~/consumer-service

docker build -t consumer-service .



⸻

🏁 Step 6: Run Consumer Service

docker run -d --name consumer \
  -e AWS_ACCESS_KEY_ID=xxx \
  -e AWS_SECRET_ACCESS_KEY=xxx \
  -e AWS_REGION=ap-south-1 \
  consumer-service

🧠 You can also use a .env file or mount secret_keys.py if needed.

⸻

🔁 Step 7: Make It Auto-Start on Reboot

Create a systemd service (optional but useful):

sudo nano /etc/systemd/system/consumer.service

[Unit]
Description=Consumer Service
After=docker.service
Requires=docker.service

[Service]
Restart=always
ExecStart=/usr/bin/docker start -a consumer
ExecStop=/usr/bin/docker stop -t 2 consumer

[Install]
WantedBy=multi-user.target

sudo systemctl enable consumer
sudo systemctl start consumer



⸻

✅ You’re now running your Consumer 24/7 on EC2 with Docker!

