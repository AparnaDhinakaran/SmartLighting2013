class Util:
    def make_unix_timestamp(date_string, time_string):
        """This command converts string format of date into unix timstamps."""
        format = '%Y %m %d %H %M %S'
        return time.mktime(time.strptime(date_string + " " + time_string, format))
