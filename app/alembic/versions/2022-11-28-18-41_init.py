"""init

Revision ID: 648fedf0f215
Revises: 
Create Date: 2022-11-28 18:41:02.460753

"""
import sqlalchemy as sa
import sqlmodel  # added
from alembic import op

# revision identifiers, used by Alembic.
revision = "648fedf0f215"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "Domain",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("domain_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),  # type: ignore
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("modified_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_Domain_domain_name"), "Domain", ["domain_name"], unique=True)
    op.create_table(
        "ThirdPartyCred",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("provider", sqlmodel.sql.sqltypes.AutoString(), nullable=False),  # type: ignore
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),  # type: ignore
        sa.Column("mobile", sqlmodel.sql.sqltypes.AutoString(), nullable=True),  # type: ignore
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=False),  # type: ignore
        sa.Column("password", sqlmodel.sql.sqltypes.AutoString(), nullable=False),  # type: ignore
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("modified_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("provider"),
    )
    op.create_table(
        "Credential",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("domain_id", sa.Integer(), nullable=False),
        sa.Column("username", sqlmodel.sql.sqltypes.AutoString(), nullable=True),  # type: ignore
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=True),  # type: ignore
        sa.Column("mobile", sqlmodel.sql.sqltypes.AutoString(), nullable=True),  # type: ignore
        sa.Column("password", sqlmodel.sql.sqltypes.AutoString(), nullable=True),  # type: ignore
        sa.Column("pin", sa.Integer(), nullable=True),
        sa.Column("third_party_cred_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("modified_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["domain_id"],
            ["Domain.id"],
        ),
        sa.ForeignKeyConstraint(
            ["third_party_cred_id"],
            ["ThirdPartyCred.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_Credential_email"), "Credential", ["email"], unique=False)
    op.create_index(op.f("ix_Credential_username"), "Credential", ["username"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_Credential_username"), table_name="Credential")
    op.drop_index(op.f("ix_Credential_email"), table_name="Credential")
    op.drop_table("Credential")
    op.drop_table("ThirdPartyCred")
    op.drop_index(op.f("ix_Domain_domain_name"), table_name="Domain")
    op.drop_table("Domain")
    # ### end Alembic commands ###
