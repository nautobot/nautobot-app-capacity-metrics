"""This script contains an example of a job about users."""

import time

from nautobot.core.celery import register_jobs
from nautobot.extras.jobs import BooleanVar, IntegerVar, Job


class TestJob(Job):
    """Job to test metrics with."""

    sleep = IntegerVar(description="How long this job should sleep.")
    fail = BooleanVar(description="Whether this job should fail.")

    def run(self, sleep, fail):
        """Run the job."""
        self.logger.warning(f"Sleeping {sleep} seconds.")
        time.sleep(sleep)
        if fail:
            raise ValueError("I am supposed to fail!")


register_jobs(TestJob)
