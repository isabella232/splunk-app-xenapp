/*
 * Load the jquery.dataTables.js file from static if it isn't already loaded
 */
function loadStaticFile(filename) {
	if (filename.indexOf('.js') > 0) { //if filename is a external JavaScript file
		var fileref=document.createElement('script');
		fileref.setAttribute("type","text/javascript");
		fileref.setAttribute("src", '/static/app/SplunkAppForXenDesktop/' + filename);
	}
	else if (filename.indexOf('.css') > 0) { //if filename is an external CSS file
		var fileref=document.createElement("link");
		fileref.setAttribute("rel", "stylesheet");
		fileref.setAttribute("type", "text/css");
		fileref.setAttribute("href", '/static/app/SplunkAppForXenDesktop/' + filename);
	}
	if (typeof fileref != "undefined")
		document.getElementsByTagName("head")[0].appendChild(fileref);
}

var filesNeeded = [ 'jquery.dataTables.min.js', 'jquery.dataTables.css' ];
for (var i = 0 ; i < filesNeeded.length ; i++) {
	loadStaticFile(filesNeeded[i]);
}

/*
 * The TableView Module
 */
Splunk.Module.TableView = $.klass(Splunk.Module.DispatchingModule, {

	/**
	 * Initialize the Module
	 */
	initialize: function($super, container) {
		$super(container);

		this._container = container;
		this._titleField = this.getParam("titleField");
		this._fieldList = this.getParam('fieldList');
		this._drilldownPrefix = this.getParam('drilldownPrefix');
		this.firebug = this.parseBoolean(this.getParam('firebug'), false);
		//this.printObject(this._fieldList);
		//alert(this.grabKeys(this._fieldList));
	},



	parseBoolean: function(o,d) {
		if (o !== null) {
			if (typeof o === "boolean")
				return o;
			if (typeof o === "string")
				switch (o.toLowerCase()) {
				case "1": case "t": case "true": case "enable": case "enabled": case "on":
					return true;
				case "0": case "f": case "false": case "disable": case "disabled": case "off":
					return false;
				}
		}
		return d;
	},
	
	/**
	 * Called when a downstream module requests updated context
	 */
	//getModifiedContext: function(context) {
	//	var context = context || this.getContext();
	//
	//	// For the fields in the row that is clicked, specify the $click.field$ values
	//	for (var fld in this._selection) {
	//		var ctxVar = this._drilldownPrefix + '.' + fld;
	//		context.set(ctxVar, this._selection[fld]);
	//	}
	//
	//	return context;
	//},

	isReadyForContextPush: function($super) {
		if (!this._selection) {
			return Splunk.Module.CANCEL;
		}
		return $super();
	},
	
    pushContextToChildren: function($super, explicitContext) {
        this.withEachDescendant(function(module) {
            module.dispatchAlreadyInProgress = false;
        });
        return $super(explicitContext);
    },
    
	/* Context Change Event Handler */
	onContextChange: function(evt) {
		this.getResults();
	},

	/* Jon in flight Event Handler */
	onJobProgress: function(evt) {
		this.getResults();
	},

	/* Job Completed Event Handler */
	onJobDone: function(evt) {
		this.getResults();
	},

	/* Reset the UI */
	resetUI: function() {
		$('#TableView', this._container).empty();
	},

	/* 
	 * Set the Parameters needed for this search to return.  We don't need
	 * need anything since the search returns JSON to us and we alert when
	 * it comes back with the wrong thing.
	 */
	getResultParams: function($super) {
		var params = $super();
		var context = this.getContext();

		var search  = context.get("search");
		var sid     = search.job.getSearchId();
		if (!sid) {
			console.error("TableView::getResultParams - Assertion Failed. getResultParams was called, but searchId is missing from my job.");
			this.logger.error(this.moduleType, "Assertion Failed. getResultParams was called, but searchId is missing from my job.")
		}
		params.sid = sid;

		// Handle post-processing
		var postprocess = search.getPostProcess();
		if (postprocess)
			params.postprocess = postprocess;
		return params;
	},
	
	// Grabs only the key from an object and sticks in an array. Used to grab just the fieldList param names from the xml, ignoring their null values.
	grabKeys: function(object) {
		grabbedKeys = [];
		for (var key in object) {
			grabbedKeys.push(object[key]);
		}
		return grabbedKeys;
	},

	/**
	 * Construct a Results Table object based on the rows received from the backend
	 */
	buildResultsTable: function() {
		this.tables = {};
		this.tableTitles = [];
		
		if (this.firebug) console.debug("Constructing Results Table Information");
		for (var i = 0 ; i < this.results.length ; i++) {
			if (this.firebug) console.debug("TitleField = %s.  Processing %o", this._titleField, this.results[i]);
			var title = this.results[i][this._titleField];
			if (!this.tables[title]) {
				this.tables[title] = [];
				this.tableTitles.push(title);
			}
			this.tables[title].push(this.results[i]);
		}
		if (this.firebug) {
			console.debug("Results Table Information: %o", this.tables);
			console.debug("Results Table List: %o", this.tableTitles);
		}
	},

	/**
	 * Renders a single table based on the data in the array of objects
	 */
	renderTable: function(data) {
		var html = '<table class="MSADTopology_DataTable">';
		var fields = this.grabKeys(this._fieldList);
		
		// Append the Headers
		html += '<thead><tr>';
		for (var i = 0 ; i < fields.length ; i++) {
			html += '<th>' + fields[i] + '</th>'
		}
		html += '</tr></thead>';
		
		// Handle the body of the table
		html += '<tbody>';
		for (var i = 0 ; i < data.length ; i++) {
			var row = data[i];
			html += '<tr>';
			for (var j = 0 ; j < fields.length ; j++) {	
				if (row[fields[j]].split(',').length > 1) {
					html += '<td class="center"><table class="subList">';
					for (var k = 0 ; k < row[fields[j]].split(',').length ; k++) {
						html += '<tr><td>' + row[fields[j]].split(',')[k] + '</td></tr>';
					}
					html += '</table></td>';
				} else if (row[fields[j]] == 'True' || row[fields[j]] == 'False') {
					html += '<td class="center truefalse"><div class="image' + row[fields[j]] + '">&nbsp;</div></td>';
				} else {
				html += '<td class="center"><span class="class">' + row[fields[j]] + '</span></td>';
				}
			}
			// End of Row
			html += '</tr>';
		}
		html += '</tbody>';
		
		// Finish off the table and return
		html += '</table>';
		//alert(data[2]['Processe(s)'].split(',')[0]);
		return html;
	},
	
	/**
	 * Render the results of the search
	 */
	renderResults: function($super, searchResults) {
		if (searchResults.length == 0) {
			if (this.firebug) console.debug("TableView::renderResults: No search response yet");
			return;
		}
				
		// Parse the JSON results
		if (this.firebug) console.debug("TableView::renderResults: %s", searchResults);
		this.results = JSON.parse(searchResults);
		if (this.firebug) console.debug("TableView::renderResults: %o", this.results);

		// Build the results table
		this.buildResultsTable();
		
		// Reset the UI First
		this.resetUI();
		
		// For each table that we are going to render:
		//		1. Render a title
		//		2. Render the table for that title
		for (var i = 0 ; i < this.tableTitles.length ; i++) {
			var table = this.renderTable(this.tables[this.tableTitles[i]]);
			
			$('#TableView', this._container).append(table);
		}
		
		// Create the data table
		$('#TableView > .MSADTopology_DataTable', this._container).dataTable({
			'oLanguage':	{
							'oPaginate':	{
											'sPrevious': "",
											'sNext': ""
											}
							}
		});
	}
});

