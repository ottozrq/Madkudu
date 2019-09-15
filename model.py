from mongoengine import *
import datetime
import json


class Page(EmbeddedDocument):
    name = StringField()
    visit_time = DateTimeField()


class User(Document):
    user_id = StringField(unique=True)
    records = ListField(EmbeddedDocumentField("Page"))

    def insert_record(self, name, visit_time):
        page = Page(name=name, visit_time=visit_time)
        self.records.append(page)

    def get_result(self):
        res = {
            'user_id': self.user_id,
            'number_pages_viewed_the_last_7_days': 0,
            'time_spent_on_site_last_7_days': 0,
            'number_of_days_active_last_7_days': 0,
            'most_viewed_page_last_7_days': ''
        }
        today = datetime.datetime.today()
        one_week_before = today - datetime.timedelta(days=7)
        records = [r for r in self.records if r.visit_time > one_week_before]
        active_days = []
        page_viewed = {}
        for record in records:
            res['time_spent_on_site_last_7_days'] += 1
            day = record.visit_time.date()
            name = record.name
            if day not in active_days:
                active_days.append(day)
            if name in page_viewed:
                page_viewed[name] += 1
            else:
                page_viewed[name] = 1
        max_viewed_page = ''
        for key in page_viewed:
            if max_viewed_page == '':
                max_viewed_page = key
            res['number_pages_viewed_the_last_7_days'] += 1
            if page_viewed[key] > page_viewed[max_viewed_page]:
                max_viewed_page = key
        res['most_viewed_page_last_7_days'] = max_viewed_page
        res['number_of_days_active_last_7_days'] = len(active_days)
        return res

