import logging
from zope.app.component.hooks import setSite
from zope.component import getSiteManager
from plone.contentratings.browser.interfaces import ICategoryContainer
from Products.CMFCore.utils import getToolByName

logger = logging.getLogger('plone.contentratings')


def uninstallVarious(context):
    """Remove all persistent configuration from the site manager"""
    if context.readDataFile('ratings-uninstall.txt') is None:
        return
    site = context.getSite()
    setSite(site)
    sm = getSiteManager(site)
    cat_manager = ICategoryContainer(site)
    for cat in cat_manager._get_local_categories():
        cat_manager.remove(cat)

# form : http://maurits.vanrees.org/weblog/archive/2009/12/catalog
def addKeyToCatalog(portal):
    '''Takes portal_catalog and adds a key to it
@param portal: context providing portal_catalog
'''

    catalog = getToolByName(portal, 'portal_catalog')
    indexes = catalog.indexes()
    # Specify the indexes you want, with ('index_name', 'index_type')

    indexables = []

    WANTED_INDEXES = (('average_rating', 'FieldIndex'),
                      ('rating_users', 'KeywordIndex'),
                      ('number_of_ratings', 'FieldIndex'),
                      )

    for name, meta_type in WANTED_INDEXES:
        if name not in indexes:
            catalog.addIndex(name, meta_type)
            indexables.append(name)
            logger.info("Added %s for field %s.", meta_type, name)
#    if len(indexables) > 0:
#        logger.info("Indexing new index: %s.", ', '.join(indexables))
#        catalog.manage_reindexIndex(ids=indexables)


def setupVarious(context):
    if context.readDataFile('plone.contentratings_various.txt') is None:
        return
    portal = context.getSite()
    addKeyToCatalog(portal)
