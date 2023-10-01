from django.test import TransactionTestCase


# The test not implement for time limit but i write some test in coin app
class CeleryTaskTestCase(TransactionTestCase):
    pass
    # TODO implement celery task test case with mock all foreign method call
