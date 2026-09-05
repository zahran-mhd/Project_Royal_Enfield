class AlarmController:

    def __init__(self, alarm_repository):
        self.alarm_repository = alarm_repository

    def get_alarm_settings(self):

        return self.alarm_repository.get_all_alarms()

    def save_alarm_settings(self, alarm_settings):

        self.alarm_repository.update_alarm_settings(
            alarm_settings
        )

    def get_enabled_alarms(self):

        return self.alarm_repository.get_enabled_alarms()