from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.redis import RedisJobStore  # 需要安装redis
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
import datetime
import asyncio

default_redis_job_store = RedisJobStore(
    db=2,
    jobs_key="apschedulers.default_jobs",
    run_times_key="apschedulers.default_run_times",
    host="2.82.16.95",
    port=31010,
    password="ub0NEn9Oc8gQoism"
)

first_executor = AsyncIOExecutor()

init_scheduler_options = {
    "jobstores": {
        # first 为 jobstore的名字，在创建Job时直接直接此名字即可
        "default": default_redis_job_store
    },
    "executors": {
        # first 为 executor 的名字，在创建Job时直接直接此名字，执行时则会使用此executor执行
        "first": first_executor
    },
    # 创建job时的默认参数
    "job_defaults": {
        'coalesce': False,  # 是否合并执行
        'max_instances': 1  # 最大实例数
    }
}


scheduler = AsyncIOScheduler(**init_scheduler_options)
scheduler.start()


def job_execute(event):
    print(
        "job执行job:\ncode => {}\njob.id => {}\njobstore=>{}".format(
            event.code,
            event.job_id,
            event.jobstore
        )
    )


scheduler.add_listener(job_execute, EVENT_JOB_EXECUTED)


def interval_func(message):
    print("现在时间： {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    print("我是普通函数")
    print(message)


async def async_func(message):
    print("现在时间： {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    print("我是协程")
    print(message)
    print("delete job")
    # scheduler.remove_job("interval_func_test", 'default')
    print("remove success")


if scheduler.get_job("interval_func_test", "default"):
    # 存在的话，先删除
    scheduler.remove_job("interval_func_test", "default")

scheduler.add_job(interval_func, "interval",
                  args=["我是10s执行一次，存放在jobstore default, executor default"],
                  seconds=10,
                  id="interval_func_test",
                  jobstore="default",
                  executor="default",
                  start_date=datetime.datetime.now(),
                  end_date=datetime.datetime.now() + datetime.timedelta(seconds=240))


trigger = IntervalTrigger(seconds=5)

if scheduler.get_job("interval_func_test_2", "default"):
    # 存在的话，先删除
    scheduler.remove_job("interval_func_test_2", "default")


scheduler.add_job(async_func, trigger, args=["我是每隔5s执行一次，存放在jobstore second, executor = default"],
                  id="interval_func_test_2",
                  jobstore="default",
                  executor="default")

def add():
    for i in range(0, 10):
        if scheduler.get_job("interval_func_num_%d" % i, "default"):
            pass
        else:
            scheduler.add_job(async_func, trigger, args=["我是每隔5s执行一次，存放在 jobstore second, executor = default num%d" % i],
                              id="interval_func_num_%d" % i,
                              jobstore="default",
                              executor="default")

add()
print("启动: {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
asyncio.get_event_loop().run_forever()
