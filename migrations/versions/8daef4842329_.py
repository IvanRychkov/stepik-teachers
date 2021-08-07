"""empty message

Revision ID: 8daef4842329
Revises: 
Create Date: 2021-08-07 06:15:56.031581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8daef4842329'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('goals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('ru_name', sa.String(), nullable=True),
    sa.Column('emoji', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('ru_name')
    )
    op.create_table('teachers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('about', sa.String(), nullable=True),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('picture', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('free', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('weekdays',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('short_name', sa.VARCHAR(length=3), nullable=True),
    sa.Column('ru_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('ru_name'),
    sa.UniqueConstraint('short_name')
    )
    op.create_table('bookings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('day_short_name', sa.VARCHAR(length=3), nullable=True),
    sa.Column('time', sa.Time(), nullable=True),
    sa.ForeignKeyConstraint(['day_short_name'], ['weekdays.short_name'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('goal_id', sa.Integer(), nullable=True),
    sa.Column('time', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['goal_id'], ['goals.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teachers_goals',
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('goal_name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['goal_name'], ['goals.name'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('teachers_goals')
    op.drop_table('requests')
    op.drop_table('bookings')
    op.drop_table('weekdays')
    op.drop_table('teachers')
    op.drop_table('goals')
    # ### end Alembic commands ###
