import typing

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import select, update, delete
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import func

from . import base


class DataBase:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(DataBase, cls).__new__(cls)
        return cls.__instance

    def __init__(self, link: str, echo=False) -> None:
        if not hasattr(self, 'session'):
            self.session = Session(create_engine(link, echo=echo))

    def add(self, table: base.Table, conflicts: typing.Iterable[str] = None, **kwargs) -> None:
        """
            Adds a new record to the table.

            :param table: Table model.
            :param conflicts: List of columns that use a unique constraint.
        """

        if not isinstance(conflicts, (list, tuple, base.NoneType)):
            conflicts = (conflicts, )

        sql = insert(table).values(**kwargs)
        sql = sql.on_conflict_do_nothing(index_elements=conflicts)

        self.session.execute(sql)
        self.session.commit()

    def get_data(self,
                 table: base.Table, *,
                 order_by: typing.Iterable = None,
                 conditions: typing.Iterable = None,
                 columns: base.Columns = None,
                 default: base.Default = None,
                 offset: base.Integer = None,
                 **kwargs) -> typing.Union[base.Table, base.Default, base.Columns]:
        """
            Get record from database.

            :param table: Table model.
            :param conditions: condition for getting a record.
            :param default: The default value to be returned if there is no record.
        """

        if not isinstance(conditions, (list, tuple, base.NoneType)):
            conditions = (conditions, )
        if not isinstance(order_by, (list, tuple, base.NoneType)):
            order_by = (order_by, )
        if not isinstance(columns, (list, tuple, base.NoneType)):
            columns = (columns, )

        if columns:
            sql = select(columns).select_from(table)
        else:
            sql = select(table)

        if order_by is not None:
            sql = sql.order_by(*order_by)
        if conditions is not None:
            sql = sql.filter(*conditions)
        if offset is not None:
            sql = sql.offset(offset)
        if kwargs:
            sql = sql.filter_by(**kwargs)

        result = self.session.execute(sql)

        if columns is not None and len(columns) > 1:
            return result.all()
        return result.scalars().first() or default

    def get_all_data(self,
                     tables: base.Table, *,
                     order_by: typing.Iterable = None,
                     conditions: typing.Iterable = None,
                     distinct: typing.Iterable = None,
                     columns: base.Columns = None,
                     default: base.Default = None,
                     limit: base.Integer = None,
                     group_by: typing.Iterable = None,
                     is_get_all: bool = False,
                     **kwargs) -> typing.Union[typing.List[base.Table], base.Default, base.Columns]:
        """
            Get records from database.

            :param table: Table model.
            :param conditions: Condition for getting a record.
            :param order_by: Sorts entries by. Accepts either asc or desc.
            :param distinct: Used to get unique record. Takes column.
            :param default: The default value to be returned if there is no record. Default list.
        """

        if not isinstance(conditions, (list, tuple, base.NoneType)):
            conditions = (conditions, )
        if not isinstance(order_by, (list, tuple, base.NoneType)):
            order_by = (order_by, )
        if not isinstance(distinct, (list, tuple, base.NoneType)):
            distinct = (distinct, )
        if not isinstance(columns, (list, tuple, base.NoneType)):
            columns = (columns, )
        if not isinstance(group_by, (list, tuple, base.NoneType)):
            group_by = (group_by, )
        if not isinstance(tables, (list, tuple)):
            tables = (tables, )

        if columns:
            sql = select(columns).select_from(*tables)
        else:
            sql = select(*tables)

        if order_by is not None:
            sql = sql.order_by(*order_by)
        if conditions is not None:
            sql = sql.filter(*conditions)
        if distinct is not None:
            sql = sql.distinct(*distinct)
        if limit is not None:
            sql = sql.limit(limit)
        if group_by is not None:
            sql = sql.group_by(*group_by)
        if kwargs:
            sql = sql.filter_by(**kwargs)

        result = self.session.execute(sql)

        if columns is not None and len(columns) > 1 or is_get_all:
            return result.all()
        return result.scalars().all() or default or []

    def counter(self,
                table: base.Table, *,
                conditions: typing.Iterable = None,
                default: base.Default = None,
                **kwargs) -> typing.Union[int, base.Default]:
        """
            Counts the number of records.

            :param table: Table model.
        """

        if not isinstance(conditions, (list, tuple, base.NoneType)):
            conditions = (conditions, )

        sql = select(func.count('*')).select_from(table)

        if conditions is not None:
            sql = sql.filter(*conditions)
        if kwargs:
            sql = sql.filter_by(**kwargs)

        result = self.session.execute(sql)
        return result.scalar() or default or 0

    def update_by_id(self, table: base.Table, _id: int, **kwargs) -> None:
        """
            Updates records by id.

            :param table: Table model.
            :param id: Record Id.
        """

        self.session.execute(update(table).where(table.id == _id).values(kwargs))
        self.session.commit()

    def update(self, table: base.Table, conditions: typing.Iterable = None, **kwargs) -> None:
        """
            Updates records by conditions.

            :param table: Table model.
            :param conditions: Conditions.
        """

        if not isinstance(conditions, (list, tuple, base.NoneType)):
            conditions = (conditions, )

        sql = update(table).values(kwargs)

        if conditions is not None:
            sql = sql.where(*conditions)

        self.session.execute(sql)
        self.session.commit()

    def delete(self, table: base.Table, **kwargs) -> None:
        """
            Removes a record from a table.

            :param table: Table model.
        """

        self.session.execute(delete(table).filter_by(**kwargs))
        self.session.commit()
