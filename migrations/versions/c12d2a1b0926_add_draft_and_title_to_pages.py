"""Add draft and title to Pages

Revision ID: c12d2a1b0926
Revises: 2539d8b5082e
Create Date: 2017-12-02 18:20:02.820141

"""
from CTFd.models import db
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text, table, column

# revision identifiers, used by Alembic.
revision = 'c12d2a1b0926'
down_revision = '2539d8b5082e'
branch_labels = None
depends_on = None

pages_table = table('pages',
    column('id', db.Integer),
    column('route', db.String(80)),
    column('title', db.String(80)),
    column('draft', db.Boolean),
)


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    connection = op.get_bind()
    op.add_column('pages', sa.Column('auth_required', sa.Boolean(), nullable=True))
    op.add_column('pages', sa.Column('draft', sa.Boolean(), nullable=True))
    op.add_column('pages', sa.Column('title', sa.String(length=80), nullable=True))

    for page in connection.execute(pages_table.select()):
        if page.route == 'index':
            connection.execute(
                pages_table.update().where(
                    pages_table.c.id == page.id
                ).values(
                    title=None,
                    draft=False
                )
            )
        else:
            connection.execute(
                pages_table.update().where(
                    pages_table.c.id == page.id
                ).values(
                    title=page.route.title(),
                    draft=False
                )
            )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pages', 'auth_required')
    op.drop_column('pages', 'title')
    op.drop_column('pages', 'draft')
    # ### end Alembic commands ###
