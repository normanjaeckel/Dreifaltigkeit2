from collections import OrderedDict


def parish_pages(request):
    """
    Context processor to add all parish pages to the context of all views.
    """
    pages = OrderedDict()
    pages['gruppen'] = 'Gruppen und Kreise'
    pages['jugend'] = 'Kinder und Jugend'
    pages['kirchenmusik'] = 'Kirchenmusik'
    pages['markusbote'] = 'Markusbote'
    pages['mitarbeiter-innen'] = 'Mitarbeiter/innen'
    pages['kirchenvorstand'] = 'Kirchenvorstand'
    pages['gebaeude'] = 'Gebäude'
    return {
        'pages': pages
    }
