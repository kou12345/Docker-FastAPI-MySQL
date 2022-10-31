from lib2to3.pgen2.token import OP
from typing import List, Optional, Tuple

import models.task as task_model
import schemas.task as task_schema
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession


async def get_tasks_with_done(db: AsyncSession) -> List[Tuple[int, str, bool]]:
    result: Result = await (
        db.execute(
            select(
                task_model.Task.id,
                task_model.Task.title,
                task_model.Done.id.isnot(None).label("done"),  # type: ignore
            ).outerjoin(task_model.Done)
        )
    )
    return result.all()  # type: ignore


async def get_task(db: AsyncSession, task_id: int) -> Optional[task_model.Task]:
    result: Result = await db.execute(
        select(task_model.Task).filter(task_model.Task.id == task_id)
    )
    task: Optional[Tuple[task_model.Task]] = result.first()  # type: ignore
    return task[0] if task is not None else None  # 要素が一つであってもtupleで返されるので1つ目の要素を取り出す


"""
引数としてスキーマ task_create: task_schema.TaskCreate を受け取る。
これをDBモデルである task_model.Task に変換する
DBにコミットする
DB上のデータを元にTaskインスタンス task を更新する
（この場合、作成したレコードの id を取得する）
作成したDBモデルを返却する
"""


async def crete_task(
    db: AsyncSession, task_create: task_schema.TaskCreate
) -> task_model.Task:
    task = task_model.Task(**task_create.dict())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def update_task(
    db: AsyncSession, task_create: task_schema.TaskCreate, original: task_model.Task
) -> task_model.Task:  # type: ignore
    original.title = task_create.title  # type: ignore
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original


async def delete_task(db: AsyncSession, original: task_model.Task) -> None:
    await db.delete(original)
    await db.commit()
