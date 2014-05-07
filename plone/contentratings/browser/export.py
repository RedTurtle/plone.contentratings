# -*- coding: utf-8 -*-

import csv
from DateTime import DateTime
from Products.AdvancedQuery import Ge
from Products.Five.browser import BrowserView
from StringIO import StringIO
from zope.i18nmessageid import MessageFactory
from zope.i18n import translate

_ = MessageFactory('plone.contentratings')


class ContentRatingsExportView(BrowserView):

    def __call__(self):
        query = Ge('average_rating', 0)
	brains = self.context.portal_catalog.evalAdvancedQuery(query, (('average_rating','desc'), 'number_of_ratings',))
        response = StringIO()
        writer = csv.writer(response, delimiter=';', quoting=csv.QUOTE_ALL)
        # header
        writer.writerow([translate(_(u"URL"), context=self.request), translate(_(u"Number of rates"), context=self.request), translate(_(u"Average rating"), context=self.request)])
	for brain in brains:
            if int(brain.number_of_ratings)>0:
                writer.writerow([brain.getURL(), int(brain.number_of_ratings), brain.average_rating])
        value = response.getvalue()
        self.request.RESPONSE.setHeader('Content-Type', 'text/csv')
        self.request.RESPONSE.setHeader('Content-Disposition',
                                        'attachment;filename=ratings-export-%s.csv' % (DateTime().strftime("%Y%m%d-%H%M")))
        return value
