"""create users table

Revision ID: 345c77468a2c
Revises: 8ef7ead9a5a1
Create Date: 2023-05-04 12:01:08.082106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '345c77468a2c'
down_revision = '8ef7ead9a5a1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column('id', sa.Integer(), nullable=False), 
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False), 
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
                    
                    sa.UniqueConstraint('email'),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    pass
