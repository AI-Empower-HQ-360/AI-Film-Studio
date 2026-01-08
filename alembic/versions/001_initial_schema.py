"""Initial database schema

Revision ID: 001
Revises: 
Create Date: 2025-12-31

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create initial database schema"""
    
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.Enum('CREATOR', 'ADMIN', name='userrole'), nullable=False),
        sa.Column('credits', sa.Integer(), nullable=False),
        sa.Column('plan_type', sa.Enum('FREE', 'STANDARD', 'PRO', 'ENTERPRISE', name='plantype'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    
    # Create projects table
    op.create_table(
        'projects',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('script', sa.Text(), nullable=True),
        sa.Column('images', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('voice', sa.Enum('MALE', 'FEMALE', 'NEUTRAL', name='voiceoption'), nullable=True),
        sa.Column('duration', sa.Integer(), nullable=True),
        sa.Column('music', sa.String(length=255), nullable=True),
        sa.Column('status', sa.Enum('PENDING', 'PROCESSING', 'COMPLETE', 'FAILED', name='projectstatus'), nullable=False),
        sa.Column('video_url', sa.String(length=500), nullable=True),
        sa.Column('subtitles_url', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_projects_id'), 'projects', ['id'], unique=False)
    op.create_index(op.f('ix_projects_user_id'), 'projects', ['user_id'], unique=False)
    
    # Create credits table
    op.create_table(
        'credits',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('plan_type', sa.Enum('FREE', 'STANDARD', 'PRO', 'ENTERPRISE', name='plantype'), nullable=False),
        sa.Column('credits_balance', sa.Integer(), nullable=False),
        sa.Column('subscription_start', sa.DateTime(timezone=True), nullable=True),
        sa.Column('subscription_end', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_credits_id'), 'credits', ['id'], unique=False)
    op.create_index(op.f('ix_credits_user_id'), 'credits', ['user_id'], unique=False)
    
    # Create credit_transactions table
    op.create_table(
        'credit_transactions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('transaction_type', sa.Enum('DEDUCTION', 'PURCHASE', 'GRANT', 'REFUND', name='transactiontype'), nullable=False),
        sa.Column('amount', sa.Integer(), nullable=False),
        sa.Column('balance_after', sa.Integer(), nullable=False),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_credit_transactions_id'), 'credit_transactions', ['id'], unique=False)
    op.create_index(op.f('ix_credit_transactions_user_id'), 'credit_transactions', ['user_id'], unique=False)
    
    # Create subscription_plans table
    op.create_table(
        'subscription_plans',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('plan_type', sa.Enum('FREE', 'STANDARD', 'PRO', 'ENTERPRISE', name='plantype'), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('credits_per_month', sa.Integer(), nullable=False),
        sa.Column('credits_per_minute', sa.Integer(), nullable=False),
        sa.Column('max_video_length', sa.Integer(), nullable=False),
        sa.Column('features', sa.String(length=1000), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('plan_type')
    )
    op.create_index(op.f('ix_subscription_plans_id'), 'subscription_plans', ['id'], unique=False)
    
    # Create youtube_integrations table
    op.create_table(
        'youtube_integrations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('channel_id', sa.String(length=255), nullable=True),
        sa.Column('video_id', sa.String(length=255), nullable=True),
        sa.Column('playlist_id', sa.String(length=255), nullable=True),
        sa.Column('upload_status', sa.Enum('PENDING', 'PROCESSING', 'COMPLETE', 'FAILED', name='uploadstatus'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_youtube_integrations_id'), 'youtube_integrations', ['id'], unique=False)
    op.create_index(op.f('ix_youtube_integrations_user_id'), 'youtube_integrations', ['user_id'], unique=False)
    op.create_index(op.f('ix_youtube_integrations_project_id'), 'youtube_integrations', ['project_id'], unique=False)
    
    # Create logs table
    op.create_table(
        'logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('action', sa.String(length=255), nullable=False),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_logs_id'), 'logs', ['id'], unique=False)
    op.create_index(op.f('ix_logs_user_id'), 'logs', ['user_id'], unique=False)
    op.create_index(op.f('ix_logs_project_id'), 'logs', ['project_id'], unique=False)
    op.create_index(op.f('ix_logs_timestamp'), 'logs', ['timestamp'], unique=False)


def downgrade() -> None:
    """Drop all tables"""
    op.drop_index(op.f('ix_logs_timestamp'), table_name='logs')
    op.drop_index(op.f('ix_logs_project_id'), table_name='logs')
    op.drop_index(op.f('ix_logs_user_id'), table_name='logs')
    op.drop_index(op.f('ix_logs_id'), table_name='logs')
    op.drop_table('logs')
    
    op.drop_index(op.f('ix_youtube_integrations_project_id'), table_name='youtube_integrations')
    op.drop_index(op.f('ix_youtube_integrations_user_id'), table_name='youtube_integrations')
    op.drop_index(op.f('ix_youtube_integrations_id'), table_name='youtube_integrations')
    op.drop_table('youtube_integrations')
    
    op.drop_index(op.f('ix_subscription_plans_id'), table_name='subscription_plans')
    op.drop_table('subscription_plans')
    
    op.drop_index(op.f('ix_credit_transactions_user_id'), table_name='credit_transactions')
    op.drop_index(op.f('ix_credit_transactions_id'), table_name='credit_transactions')
    op.drop_table('credit_transactions')
    
    op.drop_index(op.f('ix_credits_user_id'), table_name='credits')
    op.drop_index(op.f('ix_credits_id'), table_name='credits')
    op.drop_table('credits')
    
    op.drop_index(op.f('ix_projects_user_id'), table_name='projects')
    op.drop_index(op.f('ix_projects_id'), table_name='projects')
    op.drop_table('projects')
    
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    
    # Drop enums
    sa.Enum(name='uploadstatus').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='projectstatus').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='voiceoption').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='transactiontype').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='plantype').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='userrole').drop(op.get_bind(), checkfirst=True)
