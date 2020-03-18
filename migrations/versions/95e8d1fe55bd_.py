"""empty message

Revision ID: 95e8d1fe55bd
Revises: 7a2763f0402c
Create Date: 2020-03-18 20:49:40.844321

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95e8d1fe55bd'
down_revision = '7a2763f0402c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('emplyee_master',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('employee_id', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_emplyee_master_employee_id'), 'emplyee_master', ['employee_id'], unique=True)
    op.create_table('super_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('emp_id', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_super_users_emp_id'), 'super_users', ['emp_id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_super_users_emp_id'), table_name='super_users')
    op.drop_table('super_users')
    op.drop_index(op.f('ix_emplyee_master_employee_id'), table_name='emplyee_master')
    op.drop_table('emplyee_master')
    # ### end Alembic commands ###