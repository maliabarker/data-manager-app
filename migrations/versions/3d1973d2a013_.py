"""empty message

Revision ID: 3d1973d2a013
Revises: fa49f5047ebb
Create Date: 2022-07-12 11:27:51.247668

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d1973d2a013'
down_revision = 'fa49f5047ebb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('dataset')
    op.drop_table('downloaded_datasets')
    op.drop_table('favorited_datasets')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorited_datasets',
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('dataset_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['dataset_id'], ['dataset.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('downloaded_datasets',
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('dataset_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['dataset_id'], ['dataset.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('dataset',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=240), nullable=True),
    sa.Column('photo', sa.TEXT(), nullable=True),
    sa.Column('dataset_file', sa.TEXT(), nullable=True),
    sa.Column('description', sa.VARCHAR(length=240), nullable=True),
    sa.Column('download_count', sa.INTEGER(), nullable=True),
    sa.Column('created_by_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=80), nullable=False),
    sa.Column('profile_picture', sa.TEXT(), nullable=True),
    sa.Column('password', sa.VARCHAR(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###
