"""create products table

Revision ID: 8ef7ead9a5a1
Revises: 
Create Date: 2023-05-04 11:07:11.139934

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ef7ead9a5a1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('products', 
                    sa.Column('name', sa.String(), nullable=False), 
                    sa.Column('price', sa.Integer(), nullable=False),
                    sa.Column('inventory', sa.Integer(), nullable=False, server_default=sa.text('0')), 
                    sa.Column('is_sale', sa.Boolean(), nullable=False, server_default=sa.text('FALSE')),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),
                    sa.Column('id', sa.Integer(), nullable=False,),

                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('products')
