"""
Admin Service - Handles administrative operations and system management
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class AdminService:
    """Service for administrative operations"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    async def get_system_stats(self) -> Dict:
        """
        Get comprehensive system statistics
        
        Returns:
            Dict containing system metrics
        """
        try:
            # User statistics
            user_stats = await self.db.query(
                """
                SELECT 
                    COUNT(*) as total_users,
                    COUNT(CASE WHEN is_active = true THEN 1 END) as active_users,
                    COUNT(CASE WHEN last_login_at > NOW() - INTERVAL '24 hours' THEN 1 END) as users_last_24h,
                    COUNT(CASE WHEN tier = 'free' THEN 1 END) as free_users,
                    COUNT(CASE WHEN tier = 'pro' THEN 1 END) as pro_users,
                    COUNT(CASE WHEN tier = 'enterprise' THEN 1 END) as enterprise_users
                FROM users
                WHERE deleted_at IS NULL
                """
            )
            
            # Project statistics
            project_stats = await self.db.query(
                """
                SELECT 
                    COUNT(*) as total_projects,
                    COUNT(CASE WHEN status = 'draft' THEN 1 END) as draft_projects,
                    COUNT(CASE WHEN status = 'processing' THEN 1 END) as processing_projects,
                    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_projects,
                    COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_projects,
                    COUNT(CASE WHEN created_at > NOW() - INTERVAL '24 hours' THEN 1 END) as projects_last_24h
                FROM projects
                WHERE deleted_at IS NULL
                """
            )
            
            # Job statistics
            job_stats = await self.db.query(
                """
                SELECT 
                    COUNT(*) as total_jobs,
                    COUNT(CASE WHEN status = 'queued' THEN 1 END) as queued_jobs,
                    COUNT(CASE WHEN status = 'processing' THEN 1 END) as processing_jobs,
                    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_jobs,
                    COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_jobs,
                    AVG(CASE 
                        WHEN status = 'completed' AND completed_at IS NOT NULL AND started_at IS NOT NULL
                        THEN EXTRACT(EPOCH FROM (completed_at - started_at))
                    END) as avg_processing_time
                FROM jobs
                WHERE created_at > NOW() - INTERVAL '7 days'
                """
            )
            
            # Credit statistics
            credit_stats = await self.db.query(
                """
                SELECT 
                    SUM(CASE WHEN type = 'deduction' THEN ABS(amount) ELSE 0 END) as total_credits_used,
                    SUM(CASE WHEN type = 'purchase' THEN amount ELSE 0 END) as total_credits_purchased,
                    COUNT(CASE WHEN type = 'purchase' THEN 1 END) as purchase_count,
                    SUM(CASE WHEN type = 'purchase' THEN payment_amount ELSE 0 END) as total_revenue
                FROM credit_transactions
                WHERE created_at > NOW() - INTERVAL '30 days'
                """
            )
            
            return {
                "users": user_stats[0] if user_stats else {},
                "projects": project_stats[0] if project_stats else {},
                "jobs": job_stats[0] if job_stats else {},
                "credits": credit_stats[0] if credit_stats else {},
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error fetching system stats: {str(e)}")
            raise
    
    async def search_users(
        self,
        query: str,
        limit: int = 20,
        offset: int = 0
    ) -> List[Dict]:
        """
        Search users by email or name
        
        Args:
            query: Search query
            limit: Number of results to return
            offset: Pagination offset
            
        Returns:
            List of matching users
        """
        try:
            users = await self.db.query(
                """
                SELECT 
                    id, email, first_name, last_name, tier, credits,
                    is_active, email_verified, created_at, last_login_at
                FROM users
                WHERE deleted_at IS NULL
                AND (
                    email ILIKE %s
                    OR first_name ILIKE %s
                    OR last_name ILIKE %s
                )
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
                """,
                (f"%{query}%", f"%{query}%", f"%{query}%", limit, offset)
            )
            
            return users
            
        except Exception as e:
            logger.error(f"Error searching users: {str(e)}")
            raise
    
    async def get_user_details(self, user_id: str) -> Dict:
        """
        Get detailed information about a user
        
        Args:
            user_id: User ID
            
        Returns:
            User details with related data
        """
        try:
            # Get user info
            users = await self.db.query(
                "SELECT * FROM users WHERE id = %s AND deleted_at IS NULL",
                (user_id,)
            )
            
            if not users:
                raise ValueError("User not found")
            
            user = users[0]
            
            # Get project count
            project_count = await self.db.query(
                "SELECT COUNT(*) as count FROM projects WHERE user_id = %s AND deleted_at IS NULL",
                (user_id,)
            )
            
            # Get completed project count
            completed_projects = await self.db.query(
                "SELECT COUNT(*) as count FROM projects WHERE user_id = %s AND status = 'completed' AND deleted_at IS NULL",
                (user_id,)
            )
            
            # Get credit usage
            credit_usage = await self.db.query(
                """
                SELECT 
                    SUM(CASE WHEN type = 'deduction' THEN ABS(amount) ELSE 0 END) as total_used,
                    SUM(CASE WHEN type = 'purchase' THEN amount ELSE 0 END) as total_purchased
                FROM credit_transactions
                WHERE user_id = %s
                """,
                (user_id,)
            )
            
            # Get recent activity
            recent_projects = await self.db.query(
                """
                SELECT id, title, status, created_at
                FROM projects
                WHERE user_id = %s AND deleted_at IS NULL
                ORDER BY created_at DESC
                LIMIT 5
                """,
                (user_id,)
            )
            
            return {
                "user": user,
                "statistics": {
                    "total_projects": project_count[0]["count"] if project_count else 0,
                    "completed_projects": completed_projects[0]["count"] if completed_projects else 0,
                    "credits_used": credit_usage[0]["total_used"] if credit_usage else 0,
                    "credits_purchased": credit_usage[0]["total_purchased"] if credit_usage else 0
                },
                "recent_projects": recent_projects
            }
            
        except Exception as e:
            logger.error(f"Error fetching user details: {str(e)}")
            raise
    
    async def suspend_user(self, user_id: str, reason: str) -> bool:
        """
        Suspend a user account
        
        Args:
            user_id: User ID
            reason: Reason for suspension
            
        Returns:
            True if successful
        """
        try:
            await self.db.update(
                "users",
                {"id": user_id},
                {"is_active": False}
            )
            
            # Log the action
            await self._log_admin_action(
                user_id=user_id,
                action="suspend_user",
                details={"reason": reason}
            )
            
            logger.info(f"User suspended: {user_id} - Reason: {reason}")
            return True
            
        except Exception as e:
            logger.error(f"Error suspending user: {str(e)}")
            raise
    
    async def reactivate_user(self, user_id: str) -> bool:
        """
        Reactivate a suspended user account
        
        Args:
            user_id: User ID
            
        Returns:
            True if successful
        """
        try:
            await self.db.update(
                "users",
                {"id": user_id},
                {"is_active": True}
            )
            
            await self._log_admin_action(
                user_id=user_id,
                action="reactivate_user",
                details={}
            )
            
            logger.info(f"User reactivated: {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error reactivating user: {str(e)}")
            raise
    
    async def grant_credits(
        self,
        user_id: str,
        amount: int,
        reason: str
    ) -> Dict:
        """
        Grant credits to a user (admin action)
        
        Args:
            user_id: User ID
            amount: Number of credits to grant
            reason: Reason for granting credits
            
        Returns:
            Transaction information
        """
        try:
            # Get current balance
            user = await self.db.query(
                "SELECT credits FROM users WHERE id = %s",
                (user_id,)
            )
            
            if not user:
                raise ValueError("User not found")
            
            current_balance = user[0]["credits"]
            new_balance = current_balance + amount
            
            # Update credits
            await self.db.update(
                "users",
                {"id": user_id},
                {"credits": new_balance}
            )
            
            # Record transaction
            transaction_data = {
                "user_id": user_id,
                "type": "grant",
                "amount": amount,
                "balance_before": current_balance,
                "balance_after": new_balance,
                "description": f"Admin grant: {reason}"
            }
            
            transaction_id = await self.db.insert(
                "credit_transactions",
                transaction_data
            )
            
            await self._log_admin_action(
                user_id=user_id,
                action="grant_credits",
                details={"amount": amount, "reason": reason}
            )
            
            logger.info(f"Credits granted: {amount} to user {user_id}")
            
            return {
                "transaction_id": transaction_id,
                "amount": amount,
                "balance_after": new_balance
            }
            
        except Exception as e:
            logger.error(f"Error granting credits: {str(e)}")
            raise
    
    async def get_failed_jobs(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict]:
        """
        Get list of failed jobs for investigation
        
        Args:
            limit: Number of jobs to return
            offset: Pagination offset
            
        Returns:
            List of failed jobs
        """
        try:
            jobs = await self.db.query(
                """
                SELECT 
                    j.*,
                    u.email as user_email,
                    p.title as project_title
                FROM jobs j
                JOIN users u ON j.user_id = u.id
                JOIN projects p ON j.project_id = p.id
                WHERE j.status = 'failed'
                ORDER BY j.failed_at DESC
                LIMIT %s OFFSET %s
                """,
                (limit, offset)
            )
            
            return jobs
            
        except Exception as e:
            logger.error(f"Error fetching failed jobs: {str(e)}")
            raise
    
    async def get_moderation_queue(
        self,
        limit: int = 20,
        offset: int = 0
    ) -> List[Dict]:
        """
        Get projects pending moderation
        
        Args:
            limit: Number of projects to return
            offset: Pagination offset
            
        Returns:
            List of projects for moderation
        """
        try:
            # Projects with potentially inappropriate content
            projects = await self.db.query(
                """
                SELECT 
                    p.*,
                    u.email as user_email,
                    u.tier as user_tier
                FROM projects p
                JOIN users u ON p.user_id = u.id
                WHERE p.status = 'draft'
                AND p.deleted_at IS NULL
                ORDER BY p.created_at DESC
                LIMIT %s OFFSET %s
                """,
                (limit, offset)
            )
            
            return projects
            
        except Exception as e:
            logger.error(f"Error fetching moderation queue: {str(e)}")
            raise
    
    async def approve_project(self, project_id: str) -> bool:
        """Approve a project from moderation queue"""
        try:
            await self.db.update(
                "projects",
                {"id": project_id},
                {"status": "queued"}  # Move to ready for processing
            )
            
            await self._log_admin_action(
                project_id=project_id,
                action="approve_project",
                details={}
            )
            
            logger.info(f"Project approved: {project_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error approving project: {str(e)}")
            raise
    
    async def reject_project(
        self,
        project_id: str,
        reason: str
    ) -> bool:
        """Reject a project from moderation queue"""
        try:
            await self.db.update(
                "projects",
                {"id": project_id},
                {"status": "failed"}
            )
            
            # Could also send notification to user here
            
            await self._log_admin_action(
                project_id=project_id,
                action="reject_project",
                details={"reason": reason}
            )
            
            logger.info(f"Project rejected: {project_id} - Reason: {reason}")
            return True
            
        except Exception as e:
            logger.error(f"Error rejecting project: {str(e)}")
            raise
    
    async def _log_admin_action(
        self,
        action: str,
        user_id: Optional[str] = None,
        project_id: Optional[str] = None,
        details: Optional[Dict] = None
    ) -> None:
        """Log administrative action for audit trail"""
        try:
            log_data = {
                "action": f"admin_{action}",
                "user_id": user_id,
                "entity_type": "project" if project_id else "user",
                "entity_id": project_id or user_id,
                "old_values": None,
                "new_values": details
            }
            
            await self.db.insert("audit_logs", log_data)
            
        except Exception as e:
            logger.error(f"Error logging admin action: {str(e)}")
            # Don't raise - logging failure shouldn't break the operation
