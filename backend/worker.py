from __future__ import annotations

import os
import time

from backend.workers.async_jobs import _use_redis_queue, job_db, process_job


def run_polling_worker() -> None:
    print("consultslt worker started in polling mode")
    while True:
        pending = list(job_db()["jobs"].find({"status": "pending"}).sort("created_at", 1).limit(50))
        for job in pending:
            process_job(str(job.get("id") or job.get("_id")))
        time.sleep(float(os.environ.get("WORKER_POLL_INTERVAL_SECONDS", "1.0")))


def main() -> None:
    if _use_redis_queue():
        from redis import Redis  # type: ignore
        from rq import Connection, Worker  # type: ignore

        connection = Redis.from_url(os.environ["REDIS_URL"])
        with Connection(connection):
            worker = Worker(["consultslt-jobs"])
            worker.work(with_scheduler=True)
        return

    run_polling_worker()


if __name__ == "__main__":
    main()

