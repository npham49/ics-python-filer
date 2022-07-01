#Brian Pham
#V00936214

import sys
import re
import datetime
from datetime import time

class eventone:
    """
    a class for 1 event.
    """
    def __init__(self, startDate, endTime,location,summary,repEnd):
        """
        properties:
        startDate: start date time in datetime
        endTime: end time in datetime time
        location: a string containing the location
        summary: a string containing the summary of the event
        repEnd: a datetime value that will only be added if the event repeats
        """
        self.startDate = startDate
        self.endTime = endTime
        self.location = location
        self.summary = summary
        self.repEnd = repEnd

class process_cal:
    """
    a class that will read a .ics file and allow for outputing events based on dates.
    """
    def __init__(self, filename):
        """
        class constructor that construct the process_cal class with the properties needed.
        will read through all the lines in file and create an array of eventone with repetitions and sorted.
        saved to class property process_cal.eventlist
        input (str): filename
        """
        file_handle=open(filename,'r')
        lines=file_handle.readlines()
        events = []
        for line in lines:
            if re.search("BEGIN:VEVENT",line):
                event ={}
            if re.search("DTSTART",line):
                startDate =datetime.datetime(int(re.split("T",re.split(':',line)[1])[0][:-4]),int(re.split("T",re.split(':',line)[1])[0][4:-2]),int(re.split("T",re.split(':',line)[1])[0][6:]),int(re.split("T",re.split(':',line)[1])[1][:-5]),int(re.split("T",re.split(':',line)[1])[1][2:-3]))
            if re.search("DTEND",line):
                endTime =time(int(re.split("T",re.split(':',line)[1])[1][:-5]),int(re.split("T",re.split(':',line)[1])[1][2:-3]))
                event["endTime"]=endTime
            if re.search("LOCATION",line):
                location =re.split(':',line)[1].strip()
                event['location']=location
            if re.search("SUMMARY",line):
                summary =re.split(':',line)[1].strip()
                event['summary']=summary
            if re.search("RRULE",line):
                if re.search("FREQ=WEEKLY",line):
                    for element in re.split(';',line):
                        if re.search("UNTIL",element):
                            repEndDate=datetime.datetime(int(re.split('T',re.split('=',element)[1])[0][:-4]),int(re.split('T',re.split('=',element)[1])[0][4:-2]),int(re.split('T',re.split('=',element)[1])[0][6:]),int(re.split('T',re.split('=',element)[1])[1][:-4]),int(re.split('T',re.split('=',element)[1])[1][2:-2]))
                            event['repEnd']=repEndDate
            # if end of event is reached then save event to the array, if event is repeating then runs repeats
            if re.search("END:VEVENT",line):
                if 'repEnd' in event:
                    events=process_cal.repeats(self,events,event,startDate)
                elif 'repEnd' not in event:
                    events.append(eventone(startDate,event['endTime'],event['location'],event['summary'],None))
        events = process_cal.sort(self,events)
        self.eventlist = events

    def repeats (self,events,event,startDate):
        """
        a function to add repeating events to the list until the repetition end date and return the list.
        input: 
            self
            events (list[eventone]): list of events
            event (eventone): the event to be repeated
            startDate (datetime):the datetime of the first repetition
        output:
            events (list[eventone]): list of events with all the repeated events
        """
        tevent=event
        #put a new event with the date in the back of the array until the repetition end
        while startDate<event['repEnd']:
            events.append(eventone(startDate,tevent['endTime'],tevent['location'],tevent['summary'],event['repEnd']))
            startDate = startDate+datetime.timedelta(7)
        return events
        
    def sort (self,events):
        """
        a function to sort events in the list using bubble sort with 
        each event's startDate as comparison and return the list.
        input: 
            self
            events (list[eventone]): list of events
        output:
            events (list[eventone]): list of sorted events by datetime order
        """
        n = len(events)
        #loop through events with 2 pointers comparing front back back then put the latest event last in array
        for i in range(n-1):
            for j in range(0, n-i-1):
                if events[j].startDate > events[j + 1].startDate :
                    events[j], events[j + 1] = events[j + 1], events[j]

        return events

    def get_events_for_day(self,lfdate):
        """
        a function that loops through array to check for the date 
        then return a string with the day and events if found, if not return None
        input: 
            self: the current process_cal object
            lfdate (datetime): the date to be looked up
        output:
            rtstr (str): the events in lfdate's date in srting form if it exist
                         None if no events
        """
        rtstr = ""
        eventin = False
        for event in self.eventlist:
            if event.startDate.date() == lfdate.date():
                #print out the date line and separator if it is in the date provided
                if not eventin:
                    rtstr=rtstr+ lfdate.strftime("%B %d, %Y (%a)") + "\n"
                    for b in range(len(lfdate.strftime("%B %d, %Y (%a)"))):
                        rtstr += '-'
                    rtstr += '\n'
                    eventin = True
                #code for handling converting 24-hour to 12-hour with the space before 1-9
                if (event.startDate.hour<10 and event.startDate.hour>0) or (event.startDate.hour<22 and event.startDate.hour>12):
                    stime=' '+event.startDate.strftime("%-I:%M %p")
                else:
                    stime=event.startDate.strftime("%-I:%M %p")
                if (event.endTime.hour<10 and event.endTime.hour>0) or (event.endTime.hour<22 and event.endTime.hour>12):
                    etime=' '+event.endTime.strftime("%-I:%M %p")
                else:
                    etime=event.endTime.strftime("%-I:%M %p")
                rtstr = rtstr + "%s to %s: %s {{%s}}" %(stime,etime,event.summary,event.location) + '\n'
        #decider for returning None or a date with what is in it
        if eventin:
            return rtstr.rstrip("\n")
        return None