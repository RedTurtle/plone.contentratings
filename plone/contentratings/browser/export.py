# -*- coding: utf-8 -*-

import csv
from DateTime import DateTime
from Products.AdvancedQuery import Ge
from Products.Five.browser import BrowserView
from StringIO import StringIO
from zope.i18nmessageid import MessageFactory
from zope.i18n import translate

_ = MessageFactory('plone.contentratings')


class ContentRatingsExportControlPanel(ControlPanelForm):

    def __call__(self):
        query = Ge('average_rating', 0)
        brains = self.context.portal_catalog.evalAdvancedQuery(query)
        response = StringIO()
        writer = csv.writer(response, delimiter=';', quoting=csv.QUOTE_ALL)
        # header
        writer.writerow([translate(_(u"URL")), translate(_(u"Number of rates")), translate(_(u"Average rating"))])
        for brain in brains:
            writer.writerow([brain.getURL(), brain.number_of_ratings, brain.average_rating])
        value = response.getvalue()
        self.request.RESPONSE.setHeader('Content-Type', 'text/csv')
        self.request.RESPONSE.setHeader('Content-Disposition',
                                        'attachment;filename=ratings-export-%s.csv' % (DateTime().strftime("%Y%m%d-%H%M")))
        return value
