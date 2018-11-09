from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler


def is_key_time_tuple(el):
    return isinstance(el, tuple) and (len(el) == 2) and isinstance(el[1], int)


class VolatileDictionary(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self._scheduler = BackgroundScheduler()
        self._scheduler.start()

        self._evaporation_jobs = {}

    def __setitem__(self, key, value, t=None):
        if is_key_time_tuple(key):
            key, t = key
        super().__setitem__(key, value)
        if t is not None:
            self._schedule_evaporation(key, t)

    def __delitem__(self, key):
        if key in self._evaporation_jobs:
            self.cancel_volatility(key)

        super().__delitem__(key)

    def _schedule_evaporation(self, key, t):
        date = datetime.now() + timedelta(seconds = t)
        job = self._scheduler.add_job(
            self._evaporate, 'date', run_date = date, args=(key,))
        self._evaporation_jobs[key] = job.id

    def cancel_volatility(self, key):
        self._scheduler.remove_job(self._evaporation_jobs[key])

    def _evaporate(self, key):
        super().__delitem__(key)
        del self._evaporation_jobs[key]

    def get_set_life_time(self, key):
        if key not in self._evaporation_jobs:
            raise TypeError('This set is not volatile')

        job_id = self._evaporation_jobs[key]
        job = self._scheduler.get_job(job_id)
        job_date = job.trigger.run_date
        return (job_date - datetime.now(job_date.tzinfo)).total_seconds()

    def volatile_keys(self):
        return [key for key in self if key in self._evaporation_jobs]

    def nonvolatile_keys(self):
        return [key for key in self if key not in self._evaporation_jobs]

    def volatile_values(self):
        return [self[key] for key in self.volatile_keys()]

    def nonvolatile_values(self):
        return [self[key] for key in self.nonvolatile_keys()]
