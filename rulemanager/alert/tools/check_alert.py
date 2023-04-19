from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from rulemanager import settings


def job_execute(event):
    print(
        "job执行job:\ncode => {}\njob.id => {}\njobstore=>{}".format(
            event.code,
            event.job_id,
            event.jobstore,
        )
    )


default_redis_job_store = RedisJobStore(
    db=2,
    jobs_key="apschedulers.default_jobs",
    run_times_key="apschedulers.default_run_times",
    host=settings.ap_redis_host,
    port=settings.ap_redis_port,
    password=settings.ap_redis_password
)
# self.scheduler = ()
init_scheduler_options = {
    "jobstores": {
        # first 为 jobstore的名字，在创建Job时直接直接此名字即可
        "default": default_redis_job_store
    },
    "executors": {
        # first 为 executor 的名字，在创建Job时直接直接此名字，执行时则会使用此executor执行
        # "first": self.executor,
        "default": ThreadPoolExecutor(1),
        'thread_pool': ThreadPoolExecutor(200),
        'process_pool': ProcessPoolExecutor(10)
    },
    # 创建job时的默认参数
    "job_defaults": {
        'coalesce': True,  # 是否合并执行
        'max_instances': 5,  # 最大实例数
        'misfire_grace_time': 60
    }
}
scheduler = BackgroundScheduler(**init_scheduler_options)
scheduler.add_listener(job_execute, EVENT_JOB_EXECUTED)


class Scheduler(object):
    def __init__(self):
        pass

    def start(self):
        scheduler.start()

    def delete(self):
        job_list = scheduler.get_jobs("default")
        for i in job_list:
            scheduler.remove_job(i.id, jobstore="default")








