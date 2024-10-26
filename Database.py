from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData, select, extract, desc, update, Boolean, \
    delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
import pandas as pd
from pathlib import Path
from cons import workers, foremen, managers, operator_workers, user_pass
import streamlit as st

# Database setup
db_path = Path(__file__).parent / "data/sakht_dashboard.db"
engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)
metadata = MetaData()

# Define the table structure
sakht_table = Table(
    'sakht', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('task_date', String),  # تاریخ به فرمت میلادی
    Column('person_name', String),
    Column('unit', String),
    Column('shift', String),
    Column('operation', String),
    Column('machine', String),
    Column('product', String),
    Column('work_type', String),
    Column('project_code', String),
    Column('task_description', String),
    Column('date', String),  # تاریخ به فرمت شمسی
    Column('operation_duration', String),  # به صورت HH:MM
    Column('announced_duration', String),  # به صورت HH:MM
    Column('done_duration', String),  # به صورت HH:MM
    Column('task_approve', Boolean, unique=False, default=False)
)

stoppage_table = Table(
    'stoppage', metadata,
    Column('stpg_id', Integer, primary_key=True, autoincrement=True),
    Column('stpg_date', String),  # تاریخ به فرمت میلادی
    Column('person_name', String),
    Column('machine', String),
    Column('reason', String),
    Column('stpg_description', String),
    Column('date', String),  # تاریخ به فرمت شمسی
    Column('stoppage_duration', String),  # به صورت HH:MM
    Column('stoppage_approve', Boolean, unique=False, default=False)
)

users_table = Table(
    'users', metadata,
    Column('user_id', Integer, primary_key=True, autoincrement=True, unique=True),
    Column('date', String),
    Column('person_name', String),
    Column('username', String, unique=True),
    Column('password', String),
)

# Create tables if they do not exist
metadata.create_all(engine)


# Context manager for handling sessions
@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise e
    finally:
        session.close()


def fetch_tasks(username, is_foreman=False):
    print("*******" + username)
    staff_list = operator_workers.get(username)

    # بازگرداندن لیست کارکرد همه
    if username in managers:
        with get_session() as session:
            fetch_query = select(sakht_table).where(sakht_table.c.task_approve == 0).order_by(
                desc(sakht_table.c.task_date))
            return pd.read_sql(fetch_query, con=engine)

    elif username in foremen:
        if is_foreman == True:
            # بازگرداندن لیست کارکرد کارگران هر سرشیفت
            with get_session() as session:
                fetch_query = select(sakht_table).where(sakht_table.c.person_name.in_(staff_list))
                return pd.read_sql(fetch_query, con=engine)
        else:
            #  بازگرداندن لیست کارکرد سرشیفت ها
            with get_session() as session:
                fetch_query = select(sakht_table).where(
                    sakht_table.c.person_name == user_pass.get(username)[0]).order_by(desc(sakht_table.c.task_date))
                return pd.read_sql(fetch_query, con=engine)
    elif username in workers:
        with get_session() as session:
            fetch_query = select(sakht_table).where(
                sakht_table.c.person_name == user_pass.get(username)[0]).order_by(desc(sakht_table.c.task_date))
            return pd.read_sql(fetch_query, con=engine)
    else:
        # Return an empty DataFrame or handle the case where no staff is found
        return pd.DataFrame()


def insert_task(task_data):
    with get_session() as session:
        insert_query = sakht_table.insert().values(**task_data)
        session.execute(insert_query)


def update_tasks(df, original_df):
    """Update tasks in the database and delete removed rows."""
    # Find deleted rows by comparing the original DataFrame and the edited DataFrame
    deleted_rows = original_df[~original_df['id'].isin(df['id'])]

    with get_session() as session:
        # Delete removed rows from the database
        for index, row in deleted_rows.iterrows():
            delete_query = delete(sakht_table).where(sakht_table.c.id == row['id'])
            session.execute(delete_query)

        # Update existing rows
        for index, row in df.iterrows():
            update_query = (
                update(sakht_table)
                .where(sakht_table.c.id == row['id'])  # Assuming 'id' is the primary key
                .values(
                    task_date=row['task_date'],
                    person_name=row['person_name'],
                    unit=row['unit'],
                    shift=row['shift'],
                    operation=row['operation'],
                    machine=row['machine'],
                    product=row['product'],
                    work_type=row['work_type'],
                    project_code=row['project_code'],
                    date=row['date'],
                    operation_duration=row['operation_duration'],
                    announced_duration=row['announced_duration'],
                    done_duration=row['done_duration'],
                    task_approve=row['task_approve']
                )
            )
            session.execute(update_query)


def fetch_stoppages(username):
    # بازگرداندن لیست توقفات همه
    if username in managers:
        with (get_session() as session):
            fetch_query = select(stoppage_table).where(stoppage_table.c.stoppage_approve == 0
                                                       ).order_by(desc(stoppage_table.c.stpg_date))
            return pd.read_sql(fetch_query, con=engine)
    elif username in foremen:
        # بازگرداندن لیست توقفات سرشیفت ها
        with get_session() as session:
            fetch_query = select(stoppage_table).where(stoppage_table.c.person_name == user_pass.get(username)[0])
            return pd.read_sql(fetch_query, con=engine)
    else:
        # Return an empty DataFrame or handle the case where no staff is found
        return pd.DataFrame()


def insert_stoppage(stpg_data):
    with get_session() as session:
        insert_query = stoppage_table.insert().values(**stpg_data)
        session.execute(insert_query)


def update_stoppages(df, original_df):
    """Update tasks in the database and delete removed rows."""
    # Find deleted rows by comparing the original DataFrame and the edited DataFrame
    deleted_rows = original_df[~original_df['stpg_id'].isin(df['stpg_id'])]

    with get_session() as session:
        # Delete removed rows from the database
        for index, row in deleted_rows.iterrows():
            delete_query = delete(stoppage_table).where(stoppage_table.c.stpg_id == row['stpg_id'])
            session.execute(delete_query)

        # Update existing rows
        for index, row in df.iterrows():
            update_query = (
                update(stoppage_table)
                .where(stoppage_table.c.stpg_id == row['stpg_id'])  # Assuming 'id' is the primary key
                .values(
                    stpg_date=row['stpg_date'],
                    person_name=row['person_name'],
                    machine=row['machine'],
                    reason=row['reason'],
                    date=row['date'],
                    stoppage_duration=row['stoppage_duration'],
                    stoppage_approve=row['stoppage_approve'],

                )
            )
            session.execute(update_query)


def fetch_tasks_by_month(month):
    with get_session() as session:
        # ساخت کوئری پایه بدون فیلتر ماه
        fetch_query = select(
            sakht_table.c.person_name,
            sakht_table.c.unit,
            sakht_table.c.shift,
            sakht_table.c.operation,
            sakht_table.c.machine,
            sakht_table.c.product,
            sakht_table.c.work_type,
            sakht_table.c.project_code,
            sakht_table.c.date,
            sakht_table.c.operation_duration,
            sakht_table.c.announced_duration,
            sakht_table.c.done_duration,
            sakht_table.c.task_description,
        )

        # اعمال فیلتر ماه در صورت غیر صفر بودن
        if month != 0:
            fetch_query = fetch_query.where(extract('month', sakht_table.c.date) == month)

        fetch_query = fetch_query.order_by(desc(sakht_table.c.date))

        df = pd.read_sql(fetch_query, con=engine)
        df.rename(columns={
            'person_name': 'نام فرد',
            'unit': 'واحد',
            'shift': 'شیفت',
            'operation': 'عملیات',
            'machine': 'ماشین',
            'product': 'محصول',
            'work_type': 'نوع کار',
            'project_code': 'کد پروژه',
            'date': 'تاریخ',
            'operation_duration': 'مدت عملیات',
            'announced_duration': 'مدت زمان اعلام شده',
            'done_duration': 'مدت زمان انجام شده',
            'task_description': 'توضیحات',
        }, inplace=True)

        return df



def fetch_stoppages_by_month(month):
    with get_session() as session:
        # ساخت کوئری پایه بدون فیلتر ماه
        fetch_query = select(
            stoppage_table.c.person_name,
            stoppage_table.c.machine,
            stoppage_table.c.reason,
            stoppage_table.c.date,
            stoppage_table.c.stoppage_duration,
            stoppage_table.c.stpg_description
        )

        # اعمال فیلتر ماه در صورت غیر صفر بودن
        if month != 0:
            fetch_query = fetch_query.where(extract('month', stoppage_table.c.date) == month)

        fetch_query = fetch_query.order_by(desc(stoppage_table.c.date))

        df = pd.read_sql(fetch_query, con=engine)
        df.rename(columns={
            'person_name': 'نام فرد',
            'machine': 'ماشین',
            'reason': 'علت توقف',
            'date': 'تاریخ',
            'stoppage_duration': 'مدت توقف',
            'stpg_description': 'توضیحات'
        }, inplace=True)

        return df
