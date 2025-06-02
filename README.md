# Video Streaming App

A YouTube-like video streaming platform with user authentication, video upload, transcoding, and playback capabilities.

## Features

- User authentication (signup/login) with AWS Cognito
- Video upload with presigned S3 URLs
- Video processing pipeline with SQS and ECS
- Adaptive bitrate streaming with DASH
- Flutter-based mobile client
- FastAPI backend with PostgreSQL and Redis

## Architecture

```
└── anonymous3017-video-streaming-app/
    ├── backend/ - FastAPI service (user auth, video metadata)
    ├── consumer/ - SQS message processor
    ├── transcoder/ - Video processing service
    └── video_stream_client/ - Flutter mobile app
```

## Getting Started

### Prerequisites

- Docker
- Python 3.11
- Flutter 3.0+
- AWS account with necessary services (Cognito, S3, SQS, ECS)

### Backend Setup

1. Navigate to `backend/`
2. Create `.env` file with your AWS credentials and database URLs
3. Run:
   ```bash
   docker-compose up -d
   ```

### Mobile App Setup

1. Navigate to `video_stream_client/`
2. Run:
   ```bash
   flutter pub get
   flutter run
   ```

## Deployment

See individual deployment guides:
- [Backend Deployment](backend/DEPLOY.md)
- [Consumer Service Deployment](consumer/deploy_on_aws.md)
- [Transcoder Service Deployment](transcoder/deploy_transcoder_on_AWS.md)

## API Documentation

The FastAPI backend provides automatic Swagger UI documentation at `http://localhost:8000/docs` when running locally.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
