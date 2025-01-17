"""Create QuestionsAndAnswers Table

Revision ID: 574996f55190
Revises: 
Create Date: 2024-06-30 23:18:18.792913

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '574996f55190'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('QuestionsAndAnswers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question', sa.Text(), nullable=False),
    sa.Column('answer', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('QuestionsAndAnswers')
    # ### end Alembic commands ###
