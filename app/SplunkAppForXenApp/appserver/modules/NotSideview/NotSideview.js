/**
 * Module:			NotSideview
 * Search Input:	¯\(°_o)/¯
 * Parameters:		????
 **/

Splunk.Module.NotSideview = $.klass(Splunk.Module, {

   
    initialize: function($super, container) {
        $super(container);
        // this.childEnforcement  = Splunk.Module.ALWAYS_REQUIRE;
        this.parentEnforcement = Splunk.Module.ALWAYS_REQUIRE;


        if (Splunk.util.normalizeBoolean(this.getParam("enableDebugOutput"))) {
            this.setUpDebuggingCrap();
        }
        this.clickDirection = "down";
        this.drilldownPrefix = 'click';
        this.viewTarget = this.getParam('to');
        this.hide(this.HIDDEN_MODULE_KEY);
        //alert('butts');

    },

    // addDrilldownIntention: function(search, click) {
    //     intention = {
    //         flags:["keepevents"],
    //         name:"addterm"
    //     }
    //     // Looks clunky but our drilldown spec requires we pass explicit nulls in 
    //     // spots where we have no values. 
    //     // We cant proceed naively cause JS likes to take [foo,bar]  and if foo is undefined you end up with [bar]
    //     // step 1.   load em up at explicit indices.
    //     var vals = intention.arg.vals;

    //     intention.arg.vals[0] = [];
    //     intention.arg.vals[0][0] = click.name;
    //     intention.arg.vals[0][1] = click.value;

    //     intention.arg.vals[1] = [];
    //     intention.arg.vals[1][0] = click.name2;
    //     intention.arg.vals[1][1] = click.value2;
        
    //     // step 1.   if we let the values be undefined, the json conversion will kill them
    //     // so we walk through and replace with explicit nulls
    //     // being VERY careful to not touch values like '0'  or '-1' cause JS weak typing 
    //     // would happily damage these.
    //     for (var i=0; i<intention.arg.vals.length; i++) {
    //         for (var j=0; j<intention.arg.vals[i].length; j++) {
    //             if (!intention.arg.vals[i][j] && ("" + intention.arg.vals[i][j] == "undefined")) {
    //                 intention.arg.vals[i][j] = null;
    //             }
    //         }
    //     }

    //     search.addIntention(intention);
    //     return search;
    // },

    setUpDebuggingCrap: function() {
        var moduleInstance = this;
        $("<input type='checkbox' checked=\"checked\"/>")
            .click(function() {
                if ($(this).prop('checked')) {
                    moduleInstance.debugContainer.show();
                    moduleInstance._propagationPulldown.show();
                } else {
                    moduleInstance.debugContainer.hide();
                    moduleInstance._propagationPulldown.hide();
                }
            }).appendTo(this.container);

        this.container.append("Show debug foo");

        this._propagationPulldown = $("<div>").text("drilldown clicks should propagate:")
            .append(
            $("<select>")
                .append($("<option value='up'>Up</option").text("Up (experimental)"))
                .append($("<option selected='selected' value='down'></option").text("Down"))
                .change(function() {
                    moduleInstance.clickDirection = $(this).val();
                })
            )
            .appendTo(this.container);
         this.debugContainer = $("<div>").appendTo(this.container);
    },

    outputDebugMessages: function() {
        if (!this.debugContainer) return;
        var context = this.getContext();
        var click = context.getAll(this.drilldownPrefix);
        var search  = context.get("search");

         //quick and dirty debugging output.
        var debugMsg = "<h3>Debugging the drilldown intention args</h3>";
        debugMsg += "search = " + search.toString() + "<br/>";
        for (name in click) {
            debugMsg += name + "=" + click[name] + "<br/>";
        }
        this.debugContainer.html(debugMsg);
    },

    applyKeysToContext: function(click, context) {
        if (click && (click.name || click.value || click.name2 || click.value2) ) {
            var search  = context.get("search");
            var thingToPass = this.getParam('thingToPass');
            search.abandonJob();
        
            if (click.name == "_time") {
                if (click.timeRange) {
                    // We no longer add the timerange. 
                    // The FlashChart / SimpleResultsTable will have done this already.
                    //search.setTimeRange(click.timeRange);
                    
                    // TODO THE INTENTION DOES NOT ACTUALLY USE THIS VALUE FOR ANYTHING, 
                    //      so it may be more confusing to send it than not
                    click.value = click.timeRange.getEarliestTimeTerms() + "-" + click.timeRange.getLatestTimeTerms();
                    if (click.name2 == "_time") click.value2 = click.value;

                } else {
                    this.logger.error("we appear to have a time click but we are missing the TimeRange instance");
                }
            }

			//var horse = this.getContext();
			//var pony = horse.get('search');
			//search.setBaseSearch(butt + "=" + click.value);
            //alert(search.getBaseSearch());
            //alert(JSON.stringify(search));
            var queryString = {};
            queryString[thingToPass] = click.rawValue
            //context.set("search", search);
            //alert(JSON.stringify(click));
            Splunk.util.redirect_to(['app', Splunk.util.getCurrentApp(), this.viewTarget].join('/'), queryString);
        } 
        return context;
    },

    getModifiedContext: function() {
        var context = this.getContext();
        this.outputDebugMessages();
        var click = context.getAll('click');
        
        //TODO - i think this clinches it. We need to turn getModifiedContext() into modifyContext(context)
        //       i pulled this out only because i need to apply the modifications to two different contexts...

        this.applyKeysToContext(click, context);
        return context;
    }
});