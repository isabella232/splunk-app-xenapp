Splunk.Module.SingleLink = $.klass(Splunk.Module.DispatchingModule, {
    
    initialize: function($super, container) {
        $super(container);
        
        this._url = this._params['url'];
        this._urlParams = this._params['urlParams'];
        this._target = this._params['target'];
        this._afterElement = this._params['afterElement'];
        this._afterElementHTML = $(this._params['afterElement']).html();
        this._beforeLabel = this._params['beforeLabel'];
        this._afterLabel = this._params['afterLabel'];
        this._result_element = $('.SingleLinkHolder', container);
        this.entity_name = 'results';
        this._doAfter = false;
        
        this.logger = Splunk.Logger.getLogger("SingleLink.js");
    },

    onContextChange: function(evt) {
        this._doAfter = false;
        this.getResults();
    },
    
    onJobProgress: function(evt) {
        this.getResults();
    },

    onJobDone: function(evt) {
        this._doAfter = true;
        this.logger.debug('SINGLELINK - onjobdone');
        this.getResults();
    },

    getResultParams: function($super) {
        var params = $super();
        var context = this.getContext();
        var search  = context.get("search");
        var sid     = search.job.getSearchId();
        
        if (!sid) {
            this.logger.error(this.moduleType, "Assertion Failed. getResultParams was called, but searchId is missing from my job.")
        }
        
        params.sid = sid;
        params.linkTextField = this._params['linkTextField'];
        params.entity_name = this.entity_name;
        params.url = this._url;
        params.urlParams = this._urlParams;
        params.target = this._target;
        params.afterElement = this._afterElement;
        params.beforeLabel = this._beforeLabel;
        params.afterLabel = this._afterLabel;

        return params;
    },
    
    renderResults: function($super, result) {
        
        if(this._afterElement){
            
            if(this._doAfter){
                $(this._afterElement).after($(this._result_element).html(result));
            }
            
        } else {
            alert("no after" + result);
            $(this._result_element).html(result);
        }
    },
});