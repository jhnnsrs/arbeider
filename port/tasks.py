from celery import shared_task

@shared_task
def provide(x, y):
    return x + y