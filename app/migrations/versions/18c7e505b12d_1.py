"""1

Revision ID: 18c7e505b12d
Revises: 472632c4f1fb
Create Date: 2024-10-08 16:02:43.154887

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '18c7e505b12d'
down_revision: Union[str, None] = '472632c4f1fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
