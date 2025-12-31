"""
YouTube Service - Handles YouTube API integration for video uploads
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class YouTubeService:
    """Service for YouTube API integration"""
    
    def __init__(self, db_connection, client_id: str, client_secret: str):
        self.db = db_connection
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_service_name = "youtube"
        self.api_version = "v3"
    
    async def connect_youtube_account(
        self,
        user_id: str,
        authorization_code: str,
        redirect_uri: str
    ) -> Dict:
        """
        Connect user's YouTube account using OAuth 2.0
        
        Args:
            user_id: User ID
            authorization_code: OAuth authorization code from Google
            redirect_uri: OAuth redirect URI
            
        Returns:
            YouTube integration information
        """
        try:
            # Exchange authorization code for tokens
            flow = self._create_oauth_flow(redirect_uri)
            flow.fetch_token(code=authorization_code)
            credentials = flow.credentials
            
            # Get YouTube channel information
            youtube = build(
                self.api_service_name,
                self.api_version,
                credentials=credentials
            )
            
            channel_response = youtube.channels().list(
                part="snippet,contentDetails",
                mine=True
            ).execute()
            
            if not channel_response.get("items"):
                raise ValueError("No YouTube channel found for this account")
            
            channel = channel_response["items"][0]
            channel_id = channel["id"]
            channel_name = channel["snippet"]["title"]
            channel_thumbnail = channel["snippet"]["thumbnails"]["default"]["url"]
            
            # Check if integration already exists
            existing = await self.db.query(
                "SELECT id FROM youtube_integrations WHERE user_id = %s AND channel_id = %s",
                (user_id, channel_id)
            )
            
            integration_data = {
                "user_id": user_id,
                "channel_id": channel_id,
                "channel_name": channel_name,
                "channel_thumbnail_url": channel_thumbnail,
                "access_token": credentials.token,
                "refresh_token": credentials.refresh_token,
                "token_expires_at": datetime.utcnow() + timedelta(seconds=credentials.expiry),
                "scope": " ".join(credentials.scopes) if credentials.scopes else None,
                "is_active": True
            }
            
            if existing:
                # Update existing integration
                await self.db.update(
                    "youtube_integrations",
                    {"id": existing[0]["id"]},
                    integration_data
                )
                integration_id = existing[0]["id"]
            else:
                # Create new integration
                integration_id = await self.db.insert(
                    "youtube_integrations",
                    integration_data
                )
            
            logger.info(f"YouTube account connected: {channel_name} for user {user_id}")
            
            return {
                "integration_id": integration_id,
                "channel_id": channel_id,
                "channel_name": channel_name,
                "channel_thumbnail_url": channel_thumbnail
            }
            
        except Exception as e:
            logger.error(f"Error connecting YouTube account: {str(e)}")
            raise
    
    async def upload_video(
        self,
        user_id: str,
        project_id: str,
        video_file_path: str,
        title: str,
        description: str = "",
        tags: List[str] = None,
        category_id: str = "22",  # People & Blogs
        privacy_status: str = "private",
        playlist_id: Optional[str] = None
    ) -> Dict:
        """
        Upload video to YouTube
        
        Args:
            user_id: User ID
            project_id: Project ID
            video_file_path: Local path to video file
            title: Video title
            description: Video description
            tags: List of tags
            category_id: YouTube category ID
            privacy_status: Privacy status (public, private, unlisted)
            playlist_id: Optional playlist ID to add video to
            
        Returns:
            Upload information including video ID and URL
        """
        try:
            # Get active YouTube integration
            integration = await self._get_active_integration(user_id)
            
            if not integration:
                raise ValueError("No active YouTube integration found")
            
            # Refresh token if needed
            credentials = await self._get_refreshed_credentials(integration)
            
            # Build YouTube service
            youtube = build(
                self.api_service_name,
                self.api_version,
                credentials=credentials
            )
            
            # Prepare video metadata
            body = {
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": tags or [],
                    "categoryId": category_id
                },
                "status": {
                    "privacyStatus": privacy_status,
                    "selfDeclaredMadeForKids": False
                }
            }
            
            # Create media upload
            media = MediaFileUpload(
                video_file_path,
                chunksize=-1,
                resumable=True,
                mimetype="video/mp4"
            )
            
            # Create upload record
            upload_data = {
                "project_id": project_id,
                "user_id": user_id,
                "youtube_integration_id": integration["id"],
                "video_title": title,
                "video_description": description,
                "status": "uploading",
                "upload_progress": 0,
                "privacy_status": privacy_status,
                "category_id": category_id,
                "tags": tags or [],
                "playlist_id": playlist_id
            }
            
            upload_id = await self.db.insert("youtube_uploads", upload_data)
            
            # Perform upload
            request = youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    await self._update_upload_progress(upload_id, progress)
            
            video_id = response["id"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            # Update upload record with video ID
            await self.db.update(
                "youtube_uploads",
                {"id": upload_id},
                {
                    "video_id": video_id,
                    "video_url": video_url,
                    "status": "processing",
                    "upload_progress": 100
                }
            )
            
            # Add to playlist if specified
            if playlist_id:
                await self._add_video_to_playlist(
                    youtube,
                    video_id,
                    playlist_id
                )
            
            # Update last used timestamp
            await self.db.update(
                "youtube_integrations",
                {"id": integration["id"]},
                {"last_used_at": datetime.utcnow()}
            )
            
            logger.info(f"Video uploaded to YouTube: {video_id}")
            
            return {
                "upload_id": upload_id,
                "video_id": video_id,
                "video_url": video_url,
                "status": "processing"
            }
            
        except Exception as e:
            logger.error(f"Error uploading video to YouTube: {str(e)}")
            # Update upload record with error
            if 'upload_id' in locals():
                await self.db.update(
                    "youtube_uploads",
                    {"id": upload_id},
                    {
                        "status": "failed",
                        "error_message": str(e)
                    }
                )
            raise
    
    async def create_playlist(
        self,
        user_id: str,
        title: str,
        description: str = "",
        privacy_status: str = "private"
    ) -> Dict:
        """
        Create a new YouTube playlist
        
        Args:
            user_id: User ID
            title: Playlist title
            description: Playlist description
            privacy_status: Privacy status
            
        Returns:
            Playlist information
        """
        try:
            integration = await self._get_active_integration(user_id)
            
            if not integration:
                raise ValueError("No active YouTube integration found")
            
            credentials = await self._get_refreshed_credentials(integration)
            
            youtube = build(
                self.api_service_name,
                self.api_version,
                credentials=credentials
            )
            
            body = {
                "snippet": {
                    "title": title,
                    "description": description
                },
                "status": {
                    "privacyStatus": privacy_status
                }
            }
            
            response = youtube.playlists().insert(
                part="snippet,status",
                body=body
            ).execute()
            
            playlist_id = response["id"]
            
            logger.info(f"Playlist created: {playlist_id}")
            
            return {
                "playlist_id": playlist_id,
                "title": title,
                "url": f"https://www.youtube.com/playlist?list={playlist_id}"
            }
            
        except Exception as e:
            logger.error(f"Error creating playlist: {str(e)}")
            raise
    
    async def get_upload_status(self, upload_id: str) -> Dict:
        """Get YouTube upload status"""
        try:
            uploads = await self.db.query(
                "SELECT * FROM youtube_uploads WHERE id = %s",
                (upload_id,)
            )
            
            if not uploads:
                raise ValueError("Upload not found")
            
            return uploads[0]
            
        except Exception as e:
            logger.error(f"Error fetching upload status: {str(e)}")
            raise
    
    async def disconnect_youtube_account(
        self,
        user_id: str,
        integration_id: str
    ) -> bool:
        """Disconnect YouTube account"""
        try:
            await self.db.update(
                "youtube_integrations",
                {"id": integration_id, "user_id": user_id},
                {"is_active": False}
            )
            
            logger.info(f"YouTube account disconnected: {integration_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error disconnecting YouTube account: {str(e)}")
            raise
    
    async def _get_active_integration(self, user_id: str) -> Optional[Dict]:
        """Get active YouTube integration for user"""
        integrations = await self.db.query(
            """
            SELECT * FROM youtube_integrations 
            WHERE user_id = %s AND is_active = true
            ORDER BY last_used_at DESC NULLS LAST
            LIMIT 1
            """,
            (user_id,)
        )
        return integrations[0] if integrations else None
    
    async def _get_refreshed_credentials(self, integration: Dict) -> Credentials:
        """Get refreshed OAuth credentials"""
        credentials = Credentials(
            token=integration["access_token"],
            refresh_token=integration["refresh_token"],
            token_uri="https://oauth2.googleapis.com/token",
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        
        # Refresh if expired
        if datetime.utcnow() >= integration["token_expires_at"]:
            credentials.refresh(Request())
            
            # Update tokens in database
            await self.db.update(
                "youtube_integrations",
                {"id": integration["id"]},
                {
                    "access_token": credentials.token,
                    "token_expires_at": datetime.utcnow() + timedelta(seconds=credentials.expiry)
                }
            )
        
        return credentials
    
    async def _update_upload_progress(self, upload_id: str, progress: int) -> None:
        """Update upload progress"""
        await self.db.update(
            "youtube_uploads",
            {"id": upload_id},
            {"upload_progress": progress}
        )
    
    async def _add_video_to_playlist(
        self,
        youtube,
        video_id: str,
        playlist_id: str
    ) -> None:
        """Add video to playlist"""
        body = {
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
        
        youtube.playlistItems().insert(
            part="snippet",
            body=body
        ).execute()
    
    def _create_oauth_flow(self, redirect_uri: str):
        """Create OAuth 2.0 flow"""
        from google_auth_oauthlib.flow import Flow
        
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
            },
            scopes=[
                "https://www.googleapis.com/auth/youtube.upload",
                "https://www.googleapis.com/auth/youtube",
                "https://www.googleapis.com/auth/youtube.readonly"
            ]
        )
        
        flow.redirect_uri = redirect_uri
        return flow
