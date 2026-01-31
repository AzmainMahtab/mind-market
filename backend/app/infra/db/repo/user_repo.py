from datetime import datetime, timezone
from typing import Optional, List, Tuple, Union, cast
from uuid import UUID
from sqlalchemy import CursorResult, select, func, update, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.user import User
from app.ports.user_ports import UserRepository
from app.infra.db.models import UserTable

class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_domain(self, row: UserTable) -> User:
        return User(
            id=row.id,
            uuid=row.uuid,
            user_name=row.user_name,
            email=row.email,
            phone=row.phone,
            password=row.hashed_password,
            user_role=row.user_role,
            user_status=row.user_status,
            created_at=row.created_at,
            updated_at=row.updated_at,
            deleted_at=row.deleted_at
        )

    async def create(self, user: User) -> User:
        db_user = UserTable(
            user_name=user.user_name,
            email=user.email,
            phone=user.phone,
            hashed_password=user.password,
            user_role=user.user_role,
            user_status=user.user_status,
            uuid=user.uuid
        )
        self.session.add(db_user)
        await self.session.flush()
        return self._to_domain(db_user)

    async def update(self, user: User) -> User:
        stmt = (
            update(UserTable)
            .where(UserTable.uuid == user.uuid)
            .values(
                user_name=user.user_name,
                email=user.email,
                phone=user.phone,
                user_role=user.user_role,
                user_status=user.user_status,
                updated_at=datetime.now(timezone.utc)
            )
            .returning(UserTable)
        )
        result = await self.session.execute(stmt)
        row = result.scalar_one()
        return self._to_domain(row)

    async def get_by_id_or_uuid(self, identifier: Union[int, UUID]) -> Optional[User]:
        filter_col = UserTable.id if isinstance(identifier, int) else UserTable.uuid
        query = select(UserTable).where(filter_col == identifier, UserTable.deleted_at == None)
        result = await self.session.execute(query)
        row = result.scalar_one_or_none()
        return self._to_domain(row) if row else None

    async def get_by_email(self, email: str) -> Optional[User]:
        query = select(UserTable).where(UserTable.email == email, UserTable.deleted_at == None)
        result = await self.session.execute(query)
        row = result.scalar_one_or_none()
        return self._to_domain(row) if row else None

    async def get_by_username(self, username: str) -> Optional[User]:
        query = select(UserTable).where(UserTable.user_name == username, UserTable.deleted_at == None)
        result = await self.session.execute(query)
        row = result.scalar_one_or_none()
        return self._to_domain(row) if row else None

    async def list_users(self, skip: int = 0, limit: int = 10, role=None, status=None) -> Tuple[List[User], int]:
        # Build filters
        filters = [UserTable.deleted_at == None]
        if role: filters.append(UserTable.user_role == role)
        if status: filters.append(UserTable.user_status == status)

        # Count Query
        count_query = select(func.count()).select_from(UserTable).where(*filters)
        total_count = (await self.session.execute(count_query)).scalar() or 0

        # Data Query
        data_query = select(UserTable).where(*filters).offset(skip).limit(limit).order_by(UserTable.id.desc())
        result = await self.session.execute(data_query)
        users = [self._to_domain(row) for row in result.scalars().all()]

        return users, total_count

    async def soft_delete(self, identifier: Union[int, UUID]) -> bool:
        filter_col = UserTable.id if isinstance(identifier, int) else UserTable.uuid
        stmt = (
            update(UserTable)
            .where(filter_col == identifier)
            .values(deleted_at=datetime.now(timezone.utc))
        )
        result = await self.session.execute(stmt)
        cursor_result = cast(CursorResult, result)

        return (cursor_result.rowcount or 0) > 0

    async def prune(self, identifier: Union[int, UUID]) -> bool:
        filter_col = UserTable.id if isinstance(identifier, int) else UserTable.uuid
        stmt = delete(UserTable).where(filter_col == identifier)
        result = await self.session.execute(stmt)
        cursor_result = cast(CursorResult, result)

        return (cursor_result.rowcount or 0) > 0

