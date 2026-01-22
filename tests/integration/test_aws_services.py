"""
Integration Tests for AWS Services
Tests interaction with AWS infrastructure components
"""
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import json
from datetime import datetime, timedelta


@pytest.mark.integration
class TestS3Integration:
    """Integration tests for S3 storage operations"""

    @pytest.fixture
    def s3_service(self, mock_s3_client):
        """Create S3 service with mocked client"""
        from src.services.storage.s3_service import S3Service
        service = S3Service()
        service.client = mock_s3_client
        return service

    # ==================== Upload Operations ====================

    @pytest.mark.integration
    async def test_upload_video_file(self, s3_service, mock_s3_client):
        """Test uploading video file to S3"""
        mock_s3_client.put_object.return_value = {"ETag": "abc123"}
        
        result = await s3_service.upload_video(
            file_path="/tmp/video.mp4",
            key="videos/project_001/video.mp4",
            bucket="ai-film-studio-assets"
        )
        
        assert result is not None
        mock_s3_client.put_object.assert_called()

    @pytest.mark.integration
    async def test_upload_with_metadata(self, s3_service, mock_s3_client):
        """Test uploading with custom metadata"""
        mock_s3_client.put_object.return_value = {"ETag": "abc123"}
        
        metadata = {
            "project_id": "proj_001",
            "scene_number": "1",
            "created_by": "system"
        }
        
        result = await s3_service.upload_video(
            file_path="/tmp/video.mp4",
            key="videos/project_001/video.mp4",
            bucket="ai-film-studio-assets",
            metadata=metadata
        )
        
        assert result is not None

    @pytest.mark.integration
    async def test_multipart_upload_large_file(self, s3_service, mock_s3_client):
        """Test multipart upload for large files"""
        mock_s3_client.create_multipart_upload.return_value = {"UploadId": "upload_001"}
        mock_s3_client.upload_part.return_value = {"ETag": "part_etag"}
        mock_s3_client.complete_multipart_upload.return_value = {"Location": "s3://bucket/key"}
        
        result = await s3_service.upload_large_file(
            file_path="/tmp/large_video.mp4",
            key="videos/large_video.mp4",
            bucket="ai-film-studio-assets",
            part_size=5 * 1024 * 1024  # 5MB parts
        )
        
        assert result is not None

    # ==================== Download Operations ====================

    @pytest.mark.integration
    async def test_download_file(self, s3_service, mock_s3_client):
        """Test downloading file from S3"""
        mock_s3_client.get_object.return_value = {
            "Body": MagicMock(read=MagicMock(return_value=b"video_data"))
        }
        
        result = await s3_service.download(
            key="videos/project_001/video.mp4",
            bucket="ai-film-studio-assets",
            destination="/tmp/downloaded.mp4"
        )
        
        assert result is not None

    @pytest.mark.integration
    async def test_generate_presigned_url(self, s3_service, mock_s3_client):
        """Test generating presigned URL"""
        mock_s3_client.generate_presigned_url.return_value = "https://presigned-url"
        
        url = await s3_service.get_presigned_url(
            key="videos/project_001/video.mp4",
            bucket="ai-film-studio-assets",
            expiration=3600
        )
        
        assert url.startswith("https://")

    @pytest.mark.integration
    async def test_stream_download(self, s3_service, mock_s3_client):
        """Test streaming download for large files"""
        mock_body = MagicMock()
        mock_body.iter_chunks.return_value = [b"chunk1", b"chunk2", b"chunk3"]
        mock_s3_client.get_object.return_value = {"Body": mock_body}
        
        chunks = []
        async for chunk in s3_service.stream_download(
            key="videos/large_video.mp4",
            bucket="ai-film-studio-assets"
        ):
            chunks.append(chunk)
        
        assert len(chunks) > 0

    # ==================== Bucket Operations ====================

    @pytest.mark.integration
    async def test_list_objects(self, s3_service, mock_s3_client):
        """Test listing objects in bucket"""
        mock_s3_client.list_objects_v2.return_value = {
            "Contents": [
                {"Key": "videos/video1.mp4", "Size": 1000},
                {"Key": "videos/video2.mp4", "Size": 2000}
            ]
        }
        
        objects = await s3_service.list_objects(
            bucket="ai-film-studio-assets",
            prefix="videos/"
        )
        
        assert len(objects) == 2

    @pytest.mark.integration
    async def test_delete_object(self, s3_service, mock_s3_client):
        """Test deleting object from S3"""
        mock_s3_client.delete_object.return_value = {}
        
        result = await s3_service.delete(
            key="videos/old_video.mp4",
            bucket="ai-film-studio-assets"
        )
        
        assert result is True

    @pytest.mark.integration
    async def test_copy_object(self, s3_service, mock_s3_client):
        """Test copying object within S3"""
        mock_s3_client.copy_object.return_value = {"CopyObjectResult": {"ETag": "new_etag"}}
        
        result = await s3_service.copy(
            source_key="videos/original.mp4",
            dest_key="videos/copy.mp4",
            bucket="ai-film-studio-assets"
        )
        
        assert result is True


@pytest.mark.integration
class TestSQSIntegration:
    """Integration tests for SQS queue operations"""

    @pytest.fixture
    def sqs_service(self, mock_sqs_client):
        """Create SQS service with mocked client"""
        from src.services.queue.sqs_service import SQSService
        service = SQSService()
        service.client = mock_sqs_client
        return service

    # ==================== Message Operations ====================

    @pytest.mark.integration
    async def test_send_message(self, sqs_service, mock_sqs_client, sample_job):
        """Test sending message to queue"""
        mock_sqs_client.send_message.return_value = {"MessageId": "msg_001"}
        
        result = await sqs_service.send_message(
            queue_url="https://sqs.us-east-1.amazonaws.com/123456789/video-processing",
            message=sample_job
        )
        
        assert result.get("MessageId") is not None

    @pytest.mark.integration
    async def test_receive_messages(self, sqs_service, mock_sqs_client):
        """Test receiving messages from queue"""
        mock_sqs_client.receive_message.return_value = {
            "Messages": [
                {
                    "MessageId": "msg_001",
                    "Body": json.dumps({"job_id": "job_001"}),
                    "ReceiptHandle": "handle_001"
                }
            ]
        }
        
        messages = await sqs_service.receive_messages(
            queue_url="https://sqs.us-east-1.amazonaws.com/123456789/video-processing",
            max_messages=10,
            wait_time=20
        )
        
        assert len(messages) == 1

    @pytest.mark.integration
    async def test_delete_message(self, sqs_service, mock_sqs_client):
        """Test deleting message after processing"""
        mock_sqs_client.delete_message.return_value = {}
        
        result = await sqs_service.delete_message(
            queue_url="https://sqs.us-east-1.amazonaws.com/123456789/video-processing",
            receipt_handle="handle_001"
        )
        
        assert result is True

    @pytest.mark.integration
    async def test_batch_send_messages(self, sqs_service, mock_sqs_client):
        """Test batch sending messages"""
        mock_sqs_client.send_message_batch.return_value = {
            "Successful": [{"Id": "1"}, {"Id": "2"}],
            "Failed": []
        }
        
        messages = [
            {"job_id": "job_001"},
            {"job_id": "job_002"}
        ]
        
        result = await sqs_service.send_batch(
            queue_url="https://sqs.us-east-1.amazonaws.com/123456789/video-processing",
            messages=messages
        )
        
        assert len(result.get("Successful", [])) == 2

    # ==================== Queue Management ====================

    @pytest.mark.integration
    async def test_get_queue_attributes(self, sqs_service, mock_sqs_client):
        """Test getting queue attributes"""
        mock_sqs_client.get_queue_attributes.return_value = {
            "Attributes": {
                "ApproximateNumberOfMessages": "5",
                "ApproximateNumberOfMessagesNotVisible": "2"
            }
        }
        
        attrs = await sqs_service.get_queue_stats(
            queue_url="https://sqs.us-east-1.amazonaws.com/123456789/video-processing"
        )
        
        assert "ApproximateNumberOfMessages" in attrs

    @pytest.mark.integration
    async def test_purge_queue(self, sqs_service, mock_sqs_client):
        """Test purging all messages from queue"""
        mock_sqs_client.purge_queue.return_value = {}
        
        result = await sqs_service.purge(
            queue_url="https://sqs.us-east-1.amazonaws.com/123456789/video-processing"
        )
        
        assert result is True


@pytest.mark.integration
class TestRDSIntegration:
    """Integration tests for RDS database operations"""

    @pytest.fixture
    def db_service(self, mock_database):
        """Create database service with mocked connection"""
        from src.services.database.db_service import DatabaseService
        service = DatabaseService()
        service.pool = mock_database
        return service

    # ==================== CRUD Operations ====================

    @pytest.mark.integration
    async def test_create_project(self, db_service, mock_database):
        """Test creating project in database"""
        mock_database.execute.return_value = MagicMock(
            fetchone=MagicMock(return_value={"id": "proj_001"})
        )
        
        project = await db_service.create_project({
            "name": "Test Project",
            "description": "Integration test project",
            "owner_id": "user_001"
        })
        
        assert project.get("id") is not None

    @pytest.mark.integration
    async def test_read_project(self, db_service, mock_database):
        """Test reading project from database"""
        mock_database.fetch_one.return_value = {
            "id": "proj_001",
            "name": "Test Project",
            "status": "active"
        }
        
        project = await db_service.get_project("proj_001")
        
        assert project["id"] == "proj_001"

    @pytest.mark.integration
    async def test_update_project(self, db_service, mock_database):
        """Test updating project in database"""
        mock_database.execute.return_value = MagicMock(rowcount=1)
        
        result = await db_service.update_project(
            project_id="proj_001",
            updates={"status": "completed"}
        )
        
        assert result is True

    @pytest.mark.integration
    async def test_delete_project(self, db_service, mock_database):
        """Test soft deleting project"""
        mock_database.execute.return_value = MagicMock(rowcount=1)
        
        result = await db_service.delete_project("proj_001")
        
        assert result is True

    # ==================== Query Operations ====================

    @pytest.mark.integration
    async def test_list_projects_with_pagination(self, db_service, mock_database):
        """Test listing projects with pagination"""
        mock_database.fetch_all.return_value = [
            {"id": "proj_001", "name": "Project 1"},
            {"id": "proj_002", "name": "Project 2"}
        ]
        
        projects = await db_service.list_projects(
            owner_id="user_001",
            limit=10,
            offset=0
        )
        
        assert len(projects) == 2

    @pytest.mark.integration
    async def test_search_projects(self, db_service, mock_database):
        """Test searching projects"""
        mock_database.fetch_all.return_value = [
            {"id": "proj_001", "name": "Action Film"}
        ]
        
        projects = await db_service.search_projects(
            query="action",
            owner_id="user_001"
        )
        
        assert len(projects) >= 1

    # ==================== Transaction Operations ====================

    @pytest.mark.integration
    async def test_transaction_commit(self, db_service, mock_database):
        """Test transaction with commit"""
        mock_transaction = MagicMock()
        # Make execute an AsyncMock
        mock_transaction.execute = AsyncMock(return_value=None)
        mock_database.transaction.return_value.__aenter__ = AsyncMock(return_value=mock_transaction)
        mock_database.transaction.return_value.__aexit__ = AsyncMock()
        
        async with db_service.transaction() as tx:
            await tx.execute("INSERT INTO projects (name) VALUES (?)", ["Test"])
            await tx.execute("INSERT INTO scenes (project_id) VALUES (?)", ["proj_001"])
        
        # Transaction should complete without error

    @pytest.mark.integration
    async def test_transaction_rollback(self, db_service, mock_database):
        """Test transaction rollback on error"""
        mock_transaction = MagicMock()
        # Make execute an AsyncMock that raises an exception
        mock_transaction.execute = AsyncMock(side_effect=Exception("DB Error"))
        mock_database.transaction.return_value.__aenter__ = AsyncMock(return_value=mock_transaction)
        mock_database.transaction.return_value.__aexit__ = AsyncMock()
        
        with pytest.raises(Exception, match="DB Error"):
            async with db_service.transaction() as tx:
                await tx.execute("INVALID SQL")
        
        # Transaction should be rolled back


@pytest.mark.integration
class TestECSIntegration:
    """Integration tests for ECS task operations"""

    @pytest.fixture
    def ecs_service(self):
        """Create ECS service with mocked client"""
        from src.services.compute.ecs_service import ECSService
        service = ECSService()
        service.client = MagicMock()
        return service

    # ==================== Task Operations ====================

    @pytest.mark.integration
    async def test_run_gpu_task(self, ecs_service):
        """Test running GPU-enabled task"""
        ecs_service.client.run_task.return_value = {
            "tasks": [{"taskArn": "arn:aws:ecs:us-east-1:123456789:task/cluster/task_001"}]
        }
        
        result = await ecs_service.run_gpu_task(
            task_definition="video-generation-gpu",
            cluster="ai-film-studio-cluster",
            environment={
                "JOB_ID": "job_001",
                "INPUT_PATH": "s3://bucket/input.mp4"
            }
        )
        
        assert "taskArn" in result["tasks"][0]

    @pytest.mark.integration
    async def test_get_task_status(self, ecs_service):
        """Test getting task status"""
        ecs_service.client.describe_tasks.return_value = {
            "tasks": [
                {
                    "taskArn": "arn:aws:ecs:...",
                    "lastStatus": "RUNNING",
                    "containers": [{"exitCode": None}]
                }
            ]
        }
        
        status = await ecs_service.get_task_status(
            cluster="ai-film-studio-cluster",
            task_arn="arn:aws:ecs:..."
        )
        
        assert status["lastStatus"] == "RUNNING"

    @pytest.mark.integration
    async def test_stop_task(self, ecs_service):
        """Test stopping running task"""
        ecs_service.client.stop_task.return_value = {
            "task": {"taskArn": "arn:aws:ecs:...", "lastStatus": "STOPPED"}
        }
        
        result = await ecs_service.stop_task(
            cluster="ai-film-studio-cluster",
            task_arn="arn:aws:ecs:...",
            reason="User requested cancellation"
        )
        
        assert result["task"]["lastStatus"] == "STOPPED"

    @pytest.mark.integration
    async def test_list_running_tasks(self, ecs_service):
        """Test listing running tasks"""
        ecs_service.client.list_tasks.return_value = {
            "taskArns": [
                "arn:aws:ecs:...:task1",
                "arn:aws:ecs:...:task2"
            ]
        }
        
        tasks = await ecs_service.list_tasks(
            cluster="ai-film-studio-cluster",
            status="RUNNING"
        )
        
        assert len(tasks) == 2


@pytest.mark.integration
class TestCloudFrontIntegration:
    """Integration tests for CloudFront CDN operations"""

    @pytest.fixture
    def cdn_service(self):
        """Create CDN service with mocked client"""
        from src.services.cdn.cloudfront_service import CloudFrontService
        service = CloudFrontService()
        service.client = MagicMock()
        return service

    # ==================== Distribution Operations ====================

    @pytest.mark.integration
    async def test_create_invalidation(self, cdn_service):
        """Test creating cache invalidation"""
        cdn_service.client.create_invalidation.return_value = {
            "Invalidation": {
                "Id": "inv_001",
                "Status": "InProgress"
            }
        }
        
        result = await cdn_service.invalidate(
            distribution_id="E1234567890",
            paths=["/videos/project_001/*"]
        )
        
        assert result["Invalidation"]["Id"] is not None

    @pytest.mark.integration
    async def test_get_signed_url(self, cdn_service):
        """Test generating signed CloudFront URL"""
        cdn_service.generate_signed_url = MagicMock(return_value="https://d123.cloudfront.net/video.mp4?Signature=...")
        
        url = await cdn_service.get_signed_url(
            resource_path="/videos/project_001/video.mp4",
            expiration=timedelta(hours=24)
        )
        
        assert "cloudfront.net" in url
        assert "Signature" in url

    @pytest.mark.integration
    async def test_get_distribution_metrics(self, cdn_service):
        """Test getting distribution metrics"""
        cdn_service.cloudwatch_client = MagicMock()
        cdn_service.cloudwatch_client.get_metric_statistics.return_value = {
            "Datapoints": [
                {"Sum": 1000000, "Timestamp": datetime.now()}
            ]
        }
        
        metrics = await cdn_service.get_metrics(
            distribution_id="E1234567890",
            metric="BytesDownloaded",
            period=3600
        )
        
        assert len(metrics["Datapoints"]) > 0
