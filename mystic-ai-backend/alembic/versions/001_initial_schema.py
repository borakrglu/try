"""Initial database schema

Revision ID: 001
Revises:
Create Date: 2026-01-12

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('birth_date', sa.DateTime(), nullable=True),
        sa.Column('zodiac_sign', sa.String(length=20), nullable=True),
        sa.Column('language', sa.Enum('ENGLISH', 'TURKISH', 'GERMAN', name='languageenum'), nullable=False),
        sa.Column('google_id', sa.String(), nullable=True),
        sa.Column('apple_id', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_google_id'), 'users', ['google_id'], unique=True)
    op.create_index(op.f('ix_users_apple_id'), 'users', ['apple_id'], unique=True)

    # Create readings table
    op.create_table(
        'readings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.Enum('COFFEE', 'TAROT', 'PALM', name='readingtype'), nullable=False),
        sa.Column('input_data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('ai_response', sa.Text(), nullable=False),
        sa.Column('symbols_detected', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.Column('feedback_text', sa.Text(), nullable=True),
        sa.Column('processing_time_ms', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_readings_id'), 'readings', ['id'], unique=False)
    op.create_index(op.f('ix_readings_user_id'), 'readings', ['user_id'], unique=False)
    op.create_index(op.f('ix_readings_type'), 'readings', ['type'], unique=False)
    op.create_index(op.f('ix_readings_created_at'), 'readings', ['created_at'], unique=False)

    # Create reading_images table
    op.create_table(
        'reading_images',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('reading_id', sa.Integer(), nullable=False),
        sa.Column('image_url', sa.String(), nullable=False),
        sa.Column('image_type', sa.String(length=50), nullable=True),
        sa.Column('file_size', sa.Integer(), nullable=True),
        sa.Column('width', sa.Integer(), nullable=True),
        sa.Column('height', sa.Integer(), nullable=True),
        sa.Column('annotated_url', sa.String(), nullable=True),
        sa.Column('uploaded_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['reading_id'], ['readings.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reading_images_id'), 'reading_images', ['id'], unique=False)
    op.create_index(op.f('ix_reading_images_reading_id'), 'reading_images', ['reading_id'], unique=False)

    # Create chat_messages table
    op.create_table(
        'chat_messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('persona', sa.Enum('SAGE', 'WITCH', 'ASTROLOGER', name='personatype'), nullable=False),
        sa.Column('role', sa.Enum('USER', 'ASSISTANT', 'SYSTEM', name='messagerole'), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('related_reading_id', sa.Integer(), nullable=True),
        sa.Column('response_time_ms', sa.Integer(), nullable=True),
        sa.Column('tokens_used', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['related_reading_id'], ['readings.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chat_messages_id'), 'chat_messages', ['id'], unique=False)
    op.create_index(op.f('ix_chat_messages_user_id'), 'chat_messages', ['user_id'], unique=False)
    op.create_index(op.f('ix_chat_messages_persona'), 'chat_messages', ['persona'], unique=False)
    op.create_index(op.f('ix_chat_messages_created_at'), 'chat_messages', ['created_at'], unique=False)

    # Create journal_entries table
    op.create_table(
        'journal_entries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('entry_type', sa.String(length=50), nullable=False),
        sa.Column('mood', sa.String(length=50), nullable=True),
        sa.Column('tags', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('sentiment_analysis', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('chakra_scores', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('generated_affirmation', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_journal_entries_id'), 'journal_entries', ['id'], unique=False)
    op.create_index(op.f('ix_journal_entries_user_id'), 'journal_entries', ['user_id'], unique=False)
    op.create_index(op.f('ix_journal_entries_created_at'), 'journal_entries', ['created_at'], unique=False)

    # Create subscriptions table
    op.create_table(
        'subscriptions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('tier', sa.Enum('FREE', 'WEEKLY', 'MONTHLY', 'ANNUAL', name='subscriptiontier'), nullable=False),
        sa.Column('status', sa.Enum('ACTIVE', 'EXPIRED', 'CANCELED', 'TRIAL', name='subscriptionstatus'), nullable=False),
        sa.Column('platform', sa.Enum('IOS', 'ANDROID', 'WEB', name='platformtype'), nullable=True),
        sa.Column('original_transaction_id', sa.String(), nullable=True),
        sa.Column('latest_receipt', sa.String(), nullable=True),
        sa.Column('product_id', sa.String(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('canceled_at', sa.DateTime(), nullable=True),
        sa.Column('trial_ends_at', sa.DateTime(), nullable=True),
        sa.Column('auto_renew', sa.Boolean(), nullable=False),
        sa.Column('readings_this_month', sa.Integer(), nullable=False),
        sa.Column('chat_messages_today', sa.Integer(), nullable=False),
        sa.Column('last_usage_reset', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_subscriptions_id'), 'subscriptions', ['id'], unique=False)
    op.create_index(op.f('ix_subscriptions_user_id'), 'subscriptions', ['user_id'], unique=True)
    op.create_index(op.f('ix_subscriptions_status'), 'subscriptions', ['status'], unique=False)
    op.create_index(op.f('ix_subscriptions_original_transaction_id'), 'subscriptions', ['original_transaction_id'], unique=True)

    # Create user_stats table
    op.create_table(
        'user_stats',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('karma_points', sa.Integer(), nullable=False),
        sa.Column('total_readings', sa.Integer(), nullable=False),
        sa.Column('coffee_readings', sa.Integer(), nullable=False),
        sa.Column('tarot_readings', sa.Integer(), nullable=False),
        sa.Column('palm_readings', sa.Integer(), nullable=False),
        sa.Column('chat_messages_sent', sa.Integer(), nullable=False),
        sa.Column('journal_entries', sa.Integer(), nullable=False),
        sa.Column('current_journal_streak', sa.Integer(), nullable=False),
        sa.Column('longest_journal_streak', sa.Integer(), nullable=False),
        sa.Column('last_journal_date', sa.DateTime(), nullable=True),
        sa.Column('badges', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('last_active', sa.DateTime(), nullable=False),
        sa.Column('daily_quests', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_user_stats_id'), 'user_stats', ['id'], unique=False)
    op.create_index(op.f('ix_user_stats_user_id'), 'user_stats', ['user_id'], unique=True)
    op.create_index(op.f('ix_user_stats_karma_points'), 'user_stats', ['karma_points'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('user_stats')
    op.drop_table('subscriptions')
    op.drop_table('journal_entries')
    op.drop_table('chat_messages')
    op.drop_table('reading_images')
    op.drop_table('readings')
    op.drop_table('users')

    # Drop enums
    sa.Enum(name='languageenum').drop(op.get_bind())
    sa.Enum(name='readingtype').drop(op.get_bind())
    sa.Enum(name='personatype').drop(op.get_bind())
    sa.Enum(name='messagerole').drop(op.get_bind())
    sa.Enum(name='subscriptiontier').drop(op.get_bind())
    sa.Enum(name='subscriptionstatus').drop(op.get_bind())
    sa.Enum(name='platformtype').drop(op.get_bind())
