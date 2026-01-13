"""Add notifications, webhooks, and admin features

Revision ID: 002
Revises: 001
Create Date: 2026-01-13

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new fields to users table for admin functionality
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('users', sa.Column('is_banned', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('users', sa.Column('ban_reason', sa.String(length=500), nullable=True))

    # Create indexes for new user fields
    op.create_index(op.f('ix_users_is_admin'), 'users', ['is_admin'], unique=False)
    op.create_index(op.f('ix_users_is_banned'), 'users', ['is_banned'], unique=False)

    # Add ASTROLOGY to ReadingType enum
    op.execute("ALTER TYPE readingtype ADD VALUE 'ASTROLOGY'")

    # Create webhooks table
    op.create_table(
        'webhooks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('event_type', sa.String(length=100), nullable=False),
        sa.Column('payload', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('processed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_webhooks_id'), 'webhooks', ['id'], unique=False)
    op.create_index(op.f('ix_webhooks_event_type'), 'webhooks', ['event_type'], unique=False)
    op.create_index(op.f('ix_webhooks_status'), 'webhooks', ['status'], unique=False)
    op.create_index(op.f('ix_webhooks_created_at'), 'webhooks', ['created_at'], unique=False)

    # Create notification_tokens table
    op.create_table(
        'notification_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(length=500), nullable=False),
        sa.Column('device_type', sa.Enum('IOS', 'ANDROID', 'WEB', name='devicetype'), nullable=False),
        sa.Column('device_id', sa.String(length=200), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('last_used_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_tokens_id'), 'notification_tokens', ['id'], unique=False)
    op.create_index(op.f('ix_notification_tokens_user_id'), 'notification_tokens', ['user_id'], unique=False)
    op.create_index(op.f('ix_notification_tokens_token'), 'notification_tokens', ['token'], unique=True)
    op.create_index(op.f('ix_notification_tokens_is_active'), 'notification_tokens', ['is_active'], unique=False)

    # Create notification_history table
    op.create_table(
        'notification_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('notification_type', sa.Enum(
            'DAILY_AFFIRMATION',
            'READING_REMINDER',
            'JOURNAL_REMINDER',
            'MOON_PHASE',
            'STREAK_MILESTONE',
            'NEW_FEATURE',
            'SUBSCRIPTION_EXPIRY',
            'CUSTOM',
            name='notificationtype'
        ), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('sent_at', sa.DateTime(), nullable=False),
        sa.Column('delivered_at', sa.DateTime(), nullable=True),
        sa.Column('opened_at', sa.DateTime(), nullable=True),
        sa.Column('delivery_status', sa.String(length=50), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_history_id'), 'notification_history', ['id'], unique=False)
    op.create_index(op.f('ix_notification_history_user_id'), 'notification_history', ['user_id'], unique=False)
    op.create_index(op.f('ix_notification_history_notification_type'), 'notification_history', ['notification_type'], unique=False)
    op.create_index(op.f('ix_notification_history_sent_at'), 'notification_history', ['sent_at'], unique=False)

    # Create notification_preferences table
    op.create_table(
        'notification_preferences',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('enabled', sa.Boolean(), nullable=False),
        sa.Column('daily_affirmation', sa.Boolean(), nullable=False),
        sa.Column('reading_reminder', sa.Boolean(), nullable=False),
        sa.Column('journal_reminder', sa.Boolean(), nullable=False),
        sa.Column('moon_phase', sa.Boolean(), nullable=False),
        sa.Column('streak_milestone', sa.Boolean(), nullable=False),
        sa.Column('new_feature', sa.Boolean(), nullable=False),
        sa.Column('subscription_expiry', sa.Boolean(), nullable=False),
        sa.Column('quiet_hours_enabled', sa.Boolean(), nullable=False),
        sa.Column('quiet_hours_start', sa.String(length=5), nullable=True),
        sa.Column('quiet_hours_end', sa.String(length=5), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_notification_preferences_id'), 'notification_preferences', ['id'], unique=False)
    op.create_index(op.f('ix_notification_preferences_user_id'), 'notification_preferences', ['user_id'], unique=True)


def downgrade() -> None:
    # Drop notification tables
    op.drop_table('notification_preferences')
    op.drop_table('notification_history')
    op.drop_table('notification_tokens')
    op.drop_table('webhooks')

    # Drop new enums
    sa.Enum(name='devicetype').drop(op.get_bind())
    sa.Enum(name='notificationtype').drop(op.get_bind())

    # Remove user columns
    op.drop_index(op.f('ix_users_is_banned'), table_name='users')
    op.drop_index(op.f('ix_users_is_admin'), table_name='users')
    op.drop_column('users', 'ban_reason')
    op.drop_column('users', 'is_banned')
    op.drop_column('users', 'is_admin')

    # Note: Cannot remove ASTROLOGY from ReadingType enum in PostgreSQL
    # Would require recreating the enum and updating all dependent tables
