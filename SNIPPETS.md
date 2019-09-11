# Snippets

## Import monthly texts

    import csv
    from dreifaltigkeit.models import MonthlyText
    f = open('texts.csv')
    r = list(csv.reader(f))
    for i in r:
        MonthlyText.objects.create(month=i[0], text=i[1], verse=i[2])
