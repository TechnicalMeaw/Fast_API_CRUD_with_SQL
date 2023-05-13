"""add primary key and foreigh keys to products table

Revision ID: 71b02049e8f1
Revises: 345c77468a2c
Create Date: 2023-05-04 13:46:18.425292

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71b02049e8f1'
down_revision = '345c77468a2c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('products', 
                  sa.Column('owner_id', sa.Integer(), nullable=False))

    op.create_foreign_key('products_users_fk', source_table='products', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('products_users_fk', 'products')
    op.drop_column('products', 'id')
