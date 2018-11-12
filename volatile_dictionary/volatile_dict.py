from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler


class NonvolatileTypeError(TypeError):
    _ERROR_MESSAGE = 'The key "{}" does not represent a volatile set.'

    def __init__(self, key):
        super().__init__(self, self._ERROR_MESSAGE.format(key))


def is_key_time_tuple(el):
    return isinstance(el, tuple) and (len(el) == 2) and isinstance(el[1], int)


class VolatileDictionary(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self._scheduler = BackgroundScheduler()
        self._scheduler.start()

        self._evaporation_jobs = {}

    def is_set_volatile(self, key):
        return key in self._evaporation_jobs

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

    def _evaporate(self, key):
        super().__delitem__(key)
        del self._evaporation_jobs[key]

    def cancel_volatility(self, key):
        if not self.is_set_volatile(key):
            raise NonvolatileTypeError(key)
        self._scheduler.remove_job(self._evaporation_jobs[key])

    def get_set_lifetime(self, key):
        if not self.is_set_volatile(key):
            raise NonvolatileTypeError(key)

        job_id = self._evaporation_jobs[key]
        job = self._scheduler.get_job(job_id)
        job_date = job.trigger.run_date
        return (job_date - datetime.now(job_date.tzinfo)).total_seconds()

    def volatile_keys(self):
        return [key for key in self if self.is_set_volatile(key)]

    def nonvolatile_keys(self):
        return [key for key in self if not self.is_set_volatile(key)]

    def volatile_values(self):
        return [self[key] for key in self.volatile_keys()]

    def nonvolatile_values(self):
        return [self[key] for key in self.nonvolatile_keys()]

    def volatile_items(self):
        return [(key, self[key]) for key in self.volatile_keys()]

    def nonvolatile_items(self):
        return [(key, self[key]) for key in self.nonvolatile_keys()]

    def __str__(self):
        volatile_keys = self.volatile_keys()
        non_volatile_keys = self.nonvolatile_keys()

        string = ''
        if len(volatile_keys) > 0:
            string += 'Volatile sets:\n'
            for key in volatile_keys:
                t = self.get_set_lifetime(key)
                string += '\t{}: {} [{}s]\n'.format(key, self[key], t)
            string += '\n'
        if len(non_volatile_keys) > 0:
            string += 'Nonvolatile sets:\n'
            for key in non_volatile_keys:
                string += '\t{}: {}\n'.format(key, self[key])
        return string
