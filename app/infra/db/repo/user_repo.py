from datetime import datetime, timezone
from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy import  select, func, update, delete 
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.user import User, UserRole, UserStatus
from app.ports.user_ports import UserRepository
from app.infra.db.models import UserTable

class AlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_domain(self, user_row: UserTable) -> User:
        return User(
            id=user_row.id,
            user_name=user_row.user_name,
            email=user_row.email,
            phone=user_row.phone,
            password=user_row.hashed_password,
            user_status=user_row.user_status,
            user_role=user_row.user_role,
            uuid=user_row.uuid,
            created_at=user_row.created_at,
            updated_at=user_row.updated_at,
            deleted_at=user_row.deleted_at
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

    async def get_by_id_or_uuid(self, id: UUID) -> Optional[User]:
        query = select(UserTable).where(UserTable.uuid == id, UserTable.deleted_at == None)
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

    async def list_users(
        self, 
        skip: int = 0, 
        limit: int = 10, 
        role: Optional[UserRole] = None, 
        status: Optional[UserStatus] = None
    ) -> Tuple[List[User], int]:
        filters = [UserTable.deleted_at == None]
        if role: filters.append(UserTable.user_role == role)
        if status: filters.append(UserTable.user_status == status)

        count_query = select(func.count()).select_from(UserTable).where(*filters)
        total_count = (await self.session.execute(count_query)).scalar() or 0

        data_query = select(UserTable).where(*filters).offset(skip).limit(limit).order_by(UserTable.id.desc())
        result = await self.session.execute(data_query)
        users = [self._to_domain(row) for row in result.scalars().all()]

        return users, total_count

    async def soft_delete(self, id: UUID) -> bool:
        query = (
            update(UserTable)
            .where(UserTable.uuid == id)
            .values(deleted_at=datetime.now(timezone.utc))
        )
        result = await self.session.execute(query)
        return (getattr(result, "rowcount", 0)) > 0

    async def prune(self, id: UUID) -> bool:
        query = delete(UserTable).where(UserTable.uuid == id)
        result = await self.session.execute(query)
        return (getattr(result, "rowcount", 0)) > 0
