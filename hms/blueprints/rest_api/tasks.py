from hms.app import create_celery_app
from config.settings import *
from hms.blueprints.rest_api.models.livyAPI import LivyAPI

# celery = create_celery_app()

#
# @celery.task
# def delete_livy_sessions():
#
#     sessions = LivyAPI.get_sessions_by_name(0, 100, SERVER_NAME)
#
#     print("Delete Delete Delete ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~?")
#     print("Delete Delete Delete ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~?")
#     print("Delete Delete Delete ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~?")
#     # LivyAPI.get_sessions_by_name(0, 100, SERVER_NAME)
#     # return LivyAPI.delete_session(2)
#
#
# @celery.task
# def create_livy_session():
#
#     session = LivyAPI.create_session()
#
#     LivyAPI.session_id = session.data.id
#
#     print("create create create create create ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~?")
#     print("create create create create create ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~?")
#     print("create create create create create ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~?")
#
#     return 'OK'
#
#
# @celery.task
# def create_livy_statements():
#     for pivot_table in LivyAPI.pivot_tables:
#         statement = LivyAPI.get_statements(pivot_table)
#         print(statement)
#     return 'OK'
#
#     print("create create create create create ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~?")
#     print("create create create create create ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~?")
#     print("create create create create create ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~?")


@celery.task
def test():
    LivyAPI.session_id = 11