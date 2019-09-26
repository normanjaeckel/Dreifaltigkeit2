# Snippets

## Import monthly texts

    import csv
    from dreifaltigkeit.models import MonthlyText
    f = open('texts.csv')
    r = list(csv.reader(f))
    for i in r:
        MonthlyText.objects.create(month=i[0], text=i[1], verse=i[2])


## Import services

    import csv, datetime
    from dreifaltigkeit.models import Event
    f = open('services.csv')
    r = list(csv.reader(f))
    for i in r:
        Event.objects.create(type='service', title=i[0], place=i[1], content=i[2], begin=datetime.datetime.fromisoformat(i[3]), for_kids=bool(int(i[4])))
