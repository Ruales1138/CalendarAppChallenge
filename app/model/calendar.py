from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import ClassVar

from app.services.util import generate_unique_id, date_lower_than_today_error, event_not_found_error, \
    reminder_not_found_error, slot_not_available_error


# TODO: Implement Reminder class here
@dataclass
class Reminder:
    EMAIL = "email"
    SYSTEM = "system"

    def __init__(self, date_time: datetime, type: str = EMAIL):
        self.date_time: datetime = date_time
        self.type: str = type

    def __str__(self) -> str:
        return f"Reminder on {self.date_time} of type {self.type}"


# TODO: Implement Event class here
@dataclass
class Event:
    def __init__(self, title: str, description: str, date_: date, start_at: time, end_at: time, id: str = None):
        self.title: str = title
        self.description: str = description
        self.date_: date = date_
        self.start_at: time = start_at
        self.end_at: time = end_at
        self.reminders: list[Reminder] = []
        self.id: str = generate_unique_id()

    def add_reminder(self, date_time: datetime, reminder_type: str = Reminder.EMAIL):
        reminder = Reminder(date_time=date_time, type=reminder_type)
        self.reminders.append(reminder)

    def delete_reminder(self, reminder_index: int):
        if 0 <= reminder_index < len(self.reminders):
            del self.reminders[reminder_index]
        else:
            reminder_not_found_error()

    def __str__(self) -> str:
        return f'ID: {self.id} Event title: {self.title} Description: {self.description} Time: {self.start_at} - {self.end_at}'


# TODO: Implement Day class here
class Day:
    def __init__(self, date_: date):
        self.date_: date = date_
        self.slots: dict[time, str | None] = {}

    def _init_slots(self):
        pass

    def add_event(self, event_id: str, start_at: time, end_at: time):
        current_time = start_at
        while current_time < end_at:
            if self.slots.get(current_time) is not None:
                slot_not_available_error()
                return
            current_time = self._increment_time(current_time)

        current_time = start_at
        while current_time < end_at:
            self.slots[current_time] = event_id
            current_time = self._increment_time(current_time)

    def delete_event(self, event_id: str):
        deleted = False
        for slot, saved_id in self.slots.items():
            if saved_id == event_id:
                self.slots[slot] = None
                deleted = True
        if not deleted:
            event_not_found_error()

    def update_event(self, event_id: str, start_at: time, end_at: time):
        for slot in self.slots:
            if self.slots[slot] == event_id:
                self.slots[slot] = None

        for slot in self.slots:
            if start_at <= slot < end_at:
                if self.slots[slot]:
                    slot_not_available_error()
                else:
                    self.slots[slot] = event_id

    def _increment_time(self, t: time) -> time:
        new_minute = t.minute + 15
        new_hour = t.hour
        if new_minute == 60:
            new_minute = 0
            new_hour += 1
        return time(new_hour, new_minute)

# TODO: Implement Calendar class here
