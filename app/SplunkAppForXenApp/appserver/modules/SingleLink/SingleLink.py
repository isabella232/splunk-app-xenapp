import cherrypy, datetime
import controllers.module as module
import splunk, splunk.search, splunk.util, splunk.entity
import lib.util as util
import lib.i18n as i18n
import logging

logger = logging.getLogger('splunk.module.SingleLink')

# define standard time field name        
TIME_FIELD = '_time'

class SingleLink(module.ModuleHandler):
    
    def generateResults(self, host_app, client_app, sid, entity_name='results', url=None, urlParams=None, linkTextField=None, target='_self', beforeLabel=None, afterLabel=None, afterElement=None, show_preview=True):
    
        # assert input
        if not sid:
            raise Exception('SingleLink.generateResults - sid not passed!')
        
        job = splunk.search.JobLite(sid)
        
        job.setFetchOption(output_time_format=i18n.ISO8609_MICROTIME)
            
        if linkTextField:
            field_list = [linkTextField]
            job.setFetchOption(f=field_list)
            
        if splunk.util.normalizeBoolean(show_preview) and entity_name == 'results':
            entity_name = 'results_preview'
            
        rs = job.getResults(entity_name, 0, 1)
        
        if rs == None:
            return _('Invalid Job')
            
        value = None
        
        if rs and len(rs.results()) > 0:
            
            if not linkTextField: # Default to the first returned field
                fieldNames = [x for x in rs.fieldOrder() if (not x.startswith('_') or x == TIME_FIELD)]
                if len(fieldNames) > 0:
                    linkTextField = fieldNames[0]
            
            if linkTextField:  # Get Value of requested field
                rf = rs.results()[0].get(linkTextField)
                if rf: 
                    value = rf[0].value

            if(urlParams):
            
                # TODO: change this to a list for better functionality
                if urlParams.startswith("?"):
                    url = url + urlParams
                else:
                    url = url + "?" + urlParams
            
                if "[linkTextField]" in url:  # replace [linkTextField] with the field value
                    url = url.replace("[linkTextField]", value)
                
                urlVal = '<a href="%s" target="%s">%s</a>' % (url, target, value)
        
            if(beforeLabel):
                urlVal = beforeLabel + " " + urlVal
            
            if(afterLabel):
                urlVal = urlVal + " " + afterLabel

            if value != None:
                return urlVal
            
        return _('')