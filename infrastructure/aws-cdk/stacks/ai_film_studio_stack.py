"""
Main AWS CDK Stack for AI Film Studio
Enterprise Studio Operating System Infrastructure
"""
from aws_cdk import (
    Stack,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_s3 as s3,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_ecr as ecr,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_elasticloadbalancingv2 as elbv2,
    aws_iam as iam,
    aws_logs as logs,
    aws_secretsmanager as secretsmanager,
    aws_elasticache as elasticache,
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as cw_actions,
    CfnOutput,
    Duration,
    RemovalPolicy,
    Tags
)
from constructs import Construct


class AIFilmStudioStack(Stack):
    """
    Main stack for AI Film Studio infrastructure
    
    Components:
    - VPC with public/private subnets
    - ECS Fargate cluster for backend API
    - EC2 GPU instances for AI workers
    - RDS PostgreSQL database
    - S3 buckets for assets
    - SQS queues for job processing
    - CloudFront CDN
    - ECR repositories
    - Security groups and IAM roles
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Environment name
        env_name = self.node.try_get_context("environment") or "production"

        # ==================== VPC ====================
        vpc = ec2.Vpc(
            self,
            "VPC",
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC,
                    name="Public",
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    name="Private",
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    name="Database",
                    cidr_mask=24
                )
            ]
        )

        # ==================== S3 Buckets ====================
        # Assets bucket (character images, videos, audio)
        assets_bucket = s3.Bucket(
            self,
            "AssetsBucket",
            bucket_name=f"ai-film-studio-assets-{env_name}-{self.account}",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.RETAIN if env_name == "production" else RemovalPolicy.DESTROY,
            lifecycle_rules=[
                s3.LifecycleRule(
                    id="TransitionToGlacier",
                    transitions=[
                        s3.Transition(
                            storage_class=s3.StorageClass.GLACIER,
                            transition_after=Duration.days(90)
                        )
                    ]
                )
            ]
        )

        # Characters bucket
        characters_bucket = s3.Bucket(
            self,
            "CharactersBucket",
            bucket_name=f"ai-film-studio-characters-{env_name}-{self.account}",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.RETAIN if env_name == "production" else RemovalPolicy.DESTROY
        )

        # Marketing assets bucket
        marketing_bucket = s3.Bucket(
            self,
            "MarketingBucket",
            bucket_name=f"ai-film-studio-marketing-{env_name}-{self.account}",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            public_read_access=False,
            removal_policy=RemovalPolicy.RETAIN if env_name == "production" else RemovalPolicy.DESTROY
        )

        # ==================== RDS Database ====================
        # Database subnet group
        db_subnet_group = rds.SubnetGroup(
            self,
            "DatabaseSubnetGroup",
            vpc=vpc,
            description="Subnet group for RDS database",
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            )
        )

        # Database security group
        db_security_group = ec2.SecurityGroup(
            self,
            "DatabaseSecurityGroup",
            vpc=vpc,
            description="Security group for RDS database",
            allow_all_outbound=False
        )

        # Database credentials secret
        db_secret = secretsmanager.Secret(
            self,
            "DatabaseSecret",
            description="RDS database credentials",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template='{"username": "aifilmstudio"}',
                generate_string_key="password",
                exclude_characters='"@/\\'
            )
        )

        # RDS PostgreSQL instance
        database = rds.DatabaseInstance(
            self,
            "Database",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_15_4
            ),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.T3,
                ec2.InstanceSize.MICRO if env_name != "production" else ec2.InstanceSize.SMALL
            ),
            vpc=vpc,
            subnet_group=db_subnet_group,
            security_groups=[db_security_group],
            credentials=rds.Credentials.from_secret(db_secret),
            database_name="aifilmstudio",
            allocated_storage=20 if env_name != "production" else 100,
            max_allocated_storage=100 if env_name != "production" else 500,
            backup_retention=Duration.days(7) if env_name == "production" else Duration.days(1),
            deletion_protection=(env_name == "production"),
            removal_policy=RemovalPolicy.RETAIN if env_name == "production" else RemovalPolicy.DESTROY,
            multi_az=(env_name == "production")
        )

        # ==================== SQS Queues ====================
        # Main job queue
        job_queue = sqs.Queue(
            self,
            "JobQueue",
            queue_name=f"ai-film-studio-jobs-{env_name}",
            visibility_timeout=Duration.minutes(15),
            retention_period=Duration.days(14),
            dead_letter_queue=sqs.DeadLetterQueue(
                queue=sqs.Queue(
                    self,
                    "JobQueueDLQ",
                    queue_name=f"ai-film-studio-jobs-dlq-{env_name}",
                    retention_period=Duration.days(14)
                ),
                max_receive_count=3
            )
        )

        # Priority queues for different job types
        video_generation_queue = sqs.Queue(
            self,
            "VideoGenerationQueue",
            queue_name=f"ai-film-studio-video-jobs-{env_name}",
            visibility_timeout=Duration.minutes(30),
            retention_period=Duration.days(14),
            fifo=False
        )

        voice_synthesis_queue = sqs.Queue(
            self,
            "VoiceSynthesisQueue",
            queue_name=f"ai-film-studio-voice-jobs-{env_name}",
            visibility_timeout=Duration.minutes(10),
            retention_period=Duration.days(14)
        )

        backend_sg = ec2.SecurityGroup(
            self,
            "BackendSecurityGroup",
            vpc=vpc,
            description="Security group for backend API",
            allow_all_outbound=True
        )

        # ==================== ElastiCache Redis ====================
        # Redis subnet group
        redis_subnet_group = elasticache.CfnSubnetGroup(
            self,
            "RedisSubnetGroup",
            description="Subnet group for ElastiCache Redis",
            subnet_ids=[subnet.subnet_id for subnet in vpc.private_subnets],
            cache_subnet_group_name=f"ai-film-studio-redis-{env_name}"
        )

        # Redis security group
        redis_sg = ec2.SecurityGroup(
            self,
            "RedisSecurityGroup",
            vpc=vpc,
            description="Security group for ElastiCache Redis",
            allow_all_outbound=False
        )

        # Redis cluster
        redis_cluster = elasticache.CfnCacheCluster(
            self,
            "RedisCluster",
            cache_node_type="cache.t3.micro" if env_name != "production" else "cache.t3.small",
            engine="redis",
            num_cache_nodes=1,
            cache_subnet_group_name=redis_subnet_group.ref,
            vpc_security_group_ids=[redis_sg.security_group_id],
            engine_version="7.0",
            preferred_maintenance_window="sun:05:00-sun:06:00",
            snapshot_retention_limit=7 if env_name == "production" else 1
        )

        # Allow backend access to Redis
        redis_sg.add_ingress_rule(
            backend_sg,
            ec2.Port.tcp(6379),
            "Allow Redis from backend"
        )

        # ==================== SNS Topics ====================
        # Job completion notifications
        job_completion_topic = sns.Topic(
            self,
            "JobCompletionTopic",
            topic_name=f"ai-film-studio-job-completion-{env_name}",
            display_name="AI Film Studio Job Completion"
        )

        # Error notifications
        error_topic = sns.Topic(
            self,
            "ErrorTopic",
            topic_name=f"ai-film-studio-errors-{env_name}",
            display_name="AI Film Studio Errors"
        )

        # System alerts
        system_alerts_topic = sns.Topic(
            self,
            "SystemAlertsTopic",
            topic_name=f"ai-film-studio-system-alerts-{env_name}",
            display_name="AI Film Studio System Alerts"
        )

        # ==================== ECR Repositories ====================
        backend_repo = ecr.Repository(
            self,
            "BackendRepository",
            repository_name=f"ai-film-studio-backend-{env_name}",
            image_scan_on_push=True,
            lifecycle_rules=[
                ecr.LifecycleRule(
                    rule_priority=1,
                    description="Keep last 10 images",
                    max_image_count=10
                )
            ],
            removal_policy=RemovalPolicy.DESTROY if env_name != "production" else RemovalPolicy.RETAIN
        )

        worker_repo = ecr.Repository(
            self,
            "WorkerRepository",
            repository_name=f"ai-film-studio-worker-{env_name}",
            image_scan_on_push=True,
            lifecycle_rules=[
                ecr.LifecycleRule(
                    rule_priority=1,
                    description="Keep last 10 images",
                    max_image_count=10
                )
            ],
            removal_policy=RemovalPolicy.DESTROY if env_name != "production" else RemovalPolicy.RETAIN
        )

        # ==================== ECS Cluster ====================
        cluster = ecs.Cluster(
            self,
            "Cluster",
            vpc=vpc,
            cluster_name=f"ai-film-studio-{env_name}",
            container_insights=True
        )

        # ==================== IAM Roles ====================
        # Backend task role
        backend_task_role = iam.Role(
            self,
            "BackendTaskRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            description="Task role for backend service"
        )

        # Grant permissions
        assets_bucket.grant_read_write(backend_task_role)
        characters_bucket.grant_read_write(backend_task_role)
        marketing_bucket.grant_read_write(backend_task_role)
        job_queue.grant_send_messages(backend_task_role)
        video_generation_queue.grant_consume_messages(backend_task_role)
        voice_synthesis_queue.grant_consume_messages(backend_task_role)
        db_secret.grant_read(backend_task_role)
        job_completion_topic.grant_publish(backend_task_role)
        error_topic.grant_publish(backend_task_role)

        # Backend execution role
        backend_execution_role = iam.Role(
            self,
            "BackendExecutionRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonECSTaskExecutionRolePolicy")
            ]
        )

        db_secret.grant_read(backend_execution_role)

        # ==================== Security Groups ====================
        # Backend security group
        # Allow database access from backend
        db_security_group.add_ingress_rule(
            backend_sg,
            ec2.Port.tcp(5432),
            "Allow PostgreSQL from backend"
        )

        # ALB security group
        alb_sg = ec2.SecurityGroup(
            self,
            "ALBSecurityGroup",
            vpc=vpc,
            description="Security group for Application Load Balancer",
            allow_all_outbound=True
        )

        alb_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(80),
            "Allow HTTP"
        )

        alb_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(443),
            "Allow HTTPS"
        )

        # ==================== Application Load Balancer ====================
        alb = elbv2.ApplicationLoadBalancer(
            self,
            "ALB",
            vpc=vpc,
            internet_facing=True,
            security_group=alb_sg,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC
            )
        )

        # Target group for backend
        backend_target_group = elbv2.ApplicationTargetGroup(
            self,
            "BackendTargetGroup",
            port=8000,
            protocol=elbv2.ApplicationProtocol.HTTP,
            vpc=vpc,
            target_type=elbv2.TargetType.IP,
            health_check=elbv2.HealthCheck(
                path="/api/v1/health",
                interval=Duration.seconds(30),
                timeout=Duration.seconds(5),
                healthy_threshold_count=2,
                unhealthy_threshold_count=3
            )
        )

        # ALB listener
        listener = alb.add_listener(
            "Listener",
            port=80,
            default_target_groups=[backend_target_group]
        )

        # ==================== ECS Fargate Service (Backend) ====================
        backend_task_definition = ecs.FargateTaskDefinition(
            self,
            "BackendTaskDefinition",
            cpu=512 if env_name != "production" else 1024,
            memory_limit_mib=1024 if env_name != "production" else 2048,
            task_role=backend_task_role,
            execution_role=backend_execution_role
        )

        # Backend container
        backend_container = backend_task_definition.add_container(
            "BackendContainer",
            image=ecs.ContainerImage.from_ecr_repository(backend_repo, "latest"),
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix="backend",
                log_group=logs.LogGroup(
                    self,
                    "BackendLogGroup",
                    log_group_name=f"/ecs/ai-film-studio/backend-{env_name}",
                    retention=logs.RetentionDays.ONE_WEEK if env_name != "production" else logs.RetentionDays.ONE_MONTH,
                    removal_policy=RemovalPolicy.DESTROY if env_name != "production" else RemovalPolicy.RETAIN
                )
            ),
            environment={
                "ENVIRONMENT": env_name,
                "API_HOST": "0.0.0.0",
                "API_PORT": "8000",
                "ASSETS_BUCKET": assets_bucket.bucket_name,
                "CHARACTERS_BUCKET": characters_bucket.bucket_name,
                "MARKETING_BUCKET": marketing_bucket.bucket_name,
                "JOB_QUEUE_URL": job_queue.queue_url,
                "VIDEO_QUEUE_URL": video_generation_queue.queue_url,
                "VOICE_QUEUE_URL": voice_synthesis_queue.queue_url,
                # Redis endpoint will be available via service discovery or environment injection
                # Using cluster ID for runtime resolution
                "REDIS_CLUSTER_ID": redis_cluster.ref,
                "JOB_COMPLETION_TOPIC_ARN": job_completion_topic.topic_arn,
                "ERROR_TOPIC_ARN": error_topic.topic_arn
            },
            secrets={
                "DATABASE_URL": ecs.Secret.from_secrets_manager(db_secret, "password")
            }
        )

        backend_container.add_port_mappings(
            ecs.PortMapping(
                container_port=8000,
                protocol=ecs.Protocol.TCP
            )
        )

        # Backend service
        backend_service = ecs.FargateService(
            self,
            "BackendService",
            cluster=cluster,
            task_definition=backend_task_definition,
            desired_count=1 if env_name != "production" else 2,
            security_groups=[backend_sg],
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
            ),
            assign_public_ip=False
        )

        backend_service.attach_to_application_target_group(backend_target_group)

        # Auto-scaling
        scaling = backend_service.auto_scale_task_count(
            min_capacity=1,
            max_capacity=10 if env_name != "production" else 50
        )

        scaling.scale_on_cpu_utilization(
            "CpuScaling",
            target_utilization_percent=70
        )

        scaling.scale_on_memory_utilization(
            "MemoryScaling",
            target_utilization_percent=80
        )

        # ==================== CloudFront Distribution ====================
        # CloudFront for S3 assets
        distribution = cloudfront.Distribution(
            self,
            "AssetsDistribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(assets_bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD,
                cached_methods=cloudfront.CachedMethods.CACHE_GET_HEAD,
                cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED
            ),
            additional_behaviors={
                "/characters/*": cloudfront.BehaviorOptions(
                    origin=origins.S3Origin(characters_bucket),
                    viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                    cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED
                ),
                "/marketing/*": cloudfront.BehaviorOptions(
                    origin=origins.S3Origin(marketing_bucket),
                    viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                    cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED
                )
            },
            default_root_object="index.html",
            comment="AI Film Studio Assets CDN"
        )

        # ==================== GPU Worker Launch Template ====================
        # Worker IAM role
        worker_role = iam.Role(
            self,
            "WorkerRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            description="Role for GPU worker instances"
        )

        assets_bucket.grant_read_write(worker_role)
        characters_bucket.grant_read_write(worker_role)
        marketing_bucket.grant_read_write(worker_role)
        video_generation_queue.grant_consume_messages(worker_role)
        voice_synthesis_queue.grant_consume_messages(worker_role)
        job_queue.grant_consume_messages(worker_role)
        job_completion_topic.grant_publish(worker_role)
        error_topic.grant_publish(worker_role)

        # Worker instance profile
        worker_instance_profile = iam.CfnInstanceProfile(
            self,
            "WorkerInstanceProfile",
            roles=[worker_role.role_name],
            instance_profile_name=f"ai-film-studio-worker-{env_name}"
        )

        # GPU worker launch template
        worker_launch_template = ec2.LaunchTemplate(
            self,
            "WorkerLaunchTemplate",
            launch_template_name=f"ai-film-studio-worker-{env_name}",
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.G4DN,
                ec2.InstanceSize.XLARGE
            ),
            machine_image=ec2.MachineImage.latest_amazon_linux2(
                gpu_support=True
            ),
            role=worker_role,
            security_group=ec2.SecurityGroup(
                self,
                "WorkerSecurityGroup",
                vpc=vpc,
                description="Security group for GPU workers",
                allow_all_outbound=True
            ),
            user_data=ec2.UserData.for_linux(),
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/xvda",
                    volume=ec2.BlockDeviceVolume.ebs(
                        volume_size=100,
                        volume_type=ec2.EbsDeviceVolumeType.GP3,
                        encrypted=True
                    )
                )
            ]
        )

        # ==================== Outputs ====================
        CfnOutput(
            self,
            "BackendURL",
            value=f"http://{alb.load_balancer_dns_name}",
            description="Backend API URL"
        )

        CfnOutput(
            self,
            "AssetsBucketName",
            value=assets_bucket.bucket_name,
            description="S3 bucket for assets"
        )

        CfnOutput(
            self,
            "DistributionDomainName",
            value=distribution.distribution_domain_name,
            description="CloudFront distribution domain"
        )

        CfnOutput(
            self,
            "DatabaseEndpoint",
            value=database.instance_endpoint.hostname,
            description="RDS database endpoint"
        )

        CfnOutput(
            self,
            "BackendRepositoryURI",
            value=backend_repo.repository_uri,
            description="ECR repository URI for backend"
        )

        CfnOutput(
            self,
            "WorkerRepositoryURI",
            value=worker_repo.repository_uri,
            description="ECR repository URI for worker"
        )

        # ==================== CloudWatch Alarms ====================
        # Backend CPU alarm
        backend_cpu_alarm = cloudwatch.Alarm(
            self,
            "BackendCpuAlarm",
            metric=backend_service.metric_cpu_utilization(),
            threshold=80,
            evaluation_periods=2,
            alarm_description="Backend CPU utilization is high"
        )
        backend_cpu_alarm.add_alarm_action(cw_actions.SnsAction(system_alerts_topic))

        # Backend memory alarm
        backend_memory_alarm = cloudwatch.Alarm(
            self,
            "BackendMemoryAlarm",
            metric=backend_service.metric_memory_utilization(),
            threshold=85,
            evaluation_periods=2,
            alarm_description="Backend memory utilization is high"
        )
        backend_memory_alarm.add_alarm_action(cw_actions.SnsAction(system_alerts_topic))

        # Database CPU alarm
        db_cpu_alarm = cloudwatch.Alarm(
            self,
            "DatabaseCpuAlarm",
            metric=database.metric_cpu_utilization(),
            threshold=75,
            evaluation_periods=2,
            alarm_description="Database CPU utilization is high"
        )
        db_cpu_alarm.add_alarm_action(cw_actions.SnsAction(system_alerts_topic))

        # Queue depth alarm
        queue_depth_alarm = cloudwatch.Alarm(
            self,
            "QueueDepthAlarm",
            metric=job_queue.metric_approximate_number_of_messages_visible(),
            threshold=1000,
            evaluation_periods=2,
            alarm_description="Job queue depth is high"
        )
        queue_depth_alarm.add_alarm_action(cw_actions.SnsAction(system_alerts_topic))

        # ==================== Additional Outputs ====================
        CfnOutput(
            self,
            "RedisClusterId",
            value=redis_cluster.ref,
            description="ElastiCache Redis cluster ID (endpoint available via AWS SDK)"
        )

        CfnOutput(
            self,
            "RedisConfigurationEndpoint",
            value=f"{redis_cluster.ref}.cache.amazonaws.com",
            description="ElastiCache Redis configuration endpoint (port 6379)"
        )

        CfnOutput(
            self,
            "JobCompletionTopicARN",
            value=job_completion_topic.topic_arn,
            description="SNS topic for job completion notifications"
        )

        CfnOutput(
            self,
            "ErrorTopicARN",
            value=error_topic.topic_arn,
            description="SNS topic for error notifications"
        )

        # ==================== Tags ====================
        Tags.of(self).add("Project", "AI-Film-Studio")
        Tags.of(self).add("Environment", env_name)
        Tags.of(self).add("ManagedBy", "AWS-CDK")
        Tags.of(self).add("Architecture", "8-Engine-Enterprise-Studio-OS")
