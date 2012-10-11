/**
 * Module:			ListView
 * Search Input:
 * 		Single row from the msad-dc-health information
 * Display:
 * 		Table with the server status
 * Parameters:
 * 		firebug		true/false		Determines if the debug output is generated.
 */
Splunk.Module.ListView = $.klass(Splunk.Module.DispatchingModule, {

	/**
	 * Entry point for the module.  Initialization routine
	 */
	initialize:			function($super, container) {
		$super(container);
		this._container = container;
		
		$(".listRow").mouseover(function() {$(".listRow").addClass(mouseOverHighlight)} );
		$(".listRow").mouseout(function() {$(".listRow").removeClass(mouseOverHighlight)} );
		
	},
	
	/**
	 * Event Handler for context changes
	 */
	onContextChange: 	function(evt) { this.getResults(); },
	
	/**
	 * Event Handler for job completion
	 */
	onJobDone: 			function(evt) { this.getResults(); },

	/**
	 * Reset the UI
	 */
	resetUI:			function() { $('#ListViewWrapper', this._container).empty(); },
	
	/**
     * Returns json encoded copies of the fields defined in the
     * view config. These are passed to the list endpoints and
     * used to generate the proper list of data.
     *
     * @return {Array} array of json encoded strings.
     */
	getFields: function(paramName) {
        var output = [];
        if (this.getParam(paramName)) {
            $.each(this.getParam(paramName), function(i, field){
                output.push(JSON.stringify(field));
            });
        }
        return output;
    },

	/**
	 * Insert parameters into the request to the back-end
	 */
	getResultParams: function($super) {
		var params = $super();
		var context = this.getContext();
		var search = context.get("search");
		
		// Search ID
		var sid = search.job.getSearchId();
		if (!sid) {
			console.error("ListView::dispatch - Assertion (SearchId) in getResultParams");
		}
		params.sid = sid;
		
		// Post Processing
		if (search.getPostProcess())
			params.postprocess = search.getPostProcess();
		
		return params;
	},

	/**
	* Eats aforementioned {Array} and makes each string within it an object
	*
	* @return [Array] of Javascript objects
	*/
	objectify: function(jsonArray) {
		var objects = [];
		for (var i = 0 ; i < jsonArray.length ; i++ ) {
			objects.push(eval(jsonArray[i]));
		}
		return objects
	},
	
	renderResults: function($super, jsonResponse) {
		if (this.firebug) console.debug("ListView:: Entering renderResults: %s", jsonResponse);
		this.results = JSON.parse(jsonResponse);
		if (this.firebug) console.debug("ListView:: Rendering Results %o", this.results);
		
		// Internal to rendering functions
		var makeRow = function(col1,col2) { return '<tr><td class="col1"><span class="listRow">' + col1 + '</span></td><td class="col2"><span class="listRow">' + col2 + '</span></td></tr>'; };
		var makeUrl = function(url,val)   { return '<a href="' + url + val + '">' + val + '</a>'; };
		var makeLnk = function(url,val)	  { return '<a href="' + url + '">' + val + '</a>'; };
		var divider = function()          { return '<tr class="divider"><td colspan="2">&nbsp;</td></tr>'; };
		var makeImg = function(img)		  { return '<span class="icon image' + img + '"/>'; };
		
		// Get the list of fields (as JSON strings) from the xml
		var jsonFields = this.getFields('fieldList');
		
		// Parse this JSON real quick
		var fields = this.objectify(jsonFields);
		
		// Get search results
		var row  = this.results[0];
				
		// Start the rendering in a collecting variable
		var html = '<table class="ListView_Table"><tbody>';
		
		// This is it
		for (var i = 0 ; i < fields.length ; i++) {
			// var listItems = row[fields[i]].split(';');
			if (row[fields[i]] /*&& listItems.length == 1*/) {
				if (row[fields[i]].toLowerCase() == 'False'.toLowerCase() || row[fields[i]].toLowerCase() == 'True'.toLowerCase() || row[fields[i]].toLowerCase() == 'On'.toLowerCase() || row[fields[i]].toLowerCase() == 'Off'.toLowerCase()) {
					html += makeRow(fields[i] + ':' , makeImg(row[fields[i]]));
				} else {
					html += makeRow(fields[i] + ':' , row[fields[i]]);
				}
			// } else if (row[fields[i]] && listItems.length > 1) {
			// 	html += '<tr><td class="col1">' + fields[i] + ':' + '</td><td class="col2"><table class="subList">';
			// 	for (var j = 0 ; j < listItems.length ; j++) {
			// 		html += '<tr><td>' + listItems[j] + '</td></tr>';
			// 	}
			// 	html += '</table></td>';
			} else {
				html += makeRow(fields[i] + ':' , 'N/A');
			}
		}
		html += '</tbody></table>';
		$('#ListViewWrapper', this._container).html(html);
		$(".listRow").mouseover(function() {$(".listRow").addClass(mouseOverHighlight)} );
		$(".listRow").mouseout(function() {$(".listRow").removeClass(mouseOverHighlight)} );
	}
});
