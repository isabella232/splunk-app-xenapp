function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regexS = "[\\?&]" + name + "=([^&#]*)";
    var regex = new RegExp(regexS);
    var results = regex.exec(window.location.search);
    if(results == null)
        return "";
    else
        return decodeURIComponent(results[1].replace(/\+/g, " "));
}

switch (Splunk.util.getCurrentView()) {
    
    case "event_viewer":
        
        Splunk.Module.SimpleResultsTable = $.klass(Splunk.Module.SimpleResultsTable, {
            renderResults: function($super,data) {
                $super(data);
                //$('td:nth-child(1),th:nth-child(1)', this.container).hide();
                $(".panel_row3_col").find('td:nth-child(1)', this.container).hide();
                $(".panel_row3_col").find('th:nth-child(1)', this.container).hide();
            }
        });
        
        if (Splunk.Module.NullModule) {
                Splunk.Module.NullModule = $.klass(Splunk.Module.NullModule, {
                    onContextChange: function() {
                        var val = this.getContext().get("click.value");
                        
                        $('div#evtMsg').html(val);
                        
                    },
                });
            }
    
    break;

    case "xa_userexp_profiler":
	$(document).ready(function() {
	    
	    // Set up toggle drop down for ICA Performance
	    $(".panel_row3_col").find(".meta").html('<img id="imgICAPerf" src="/static/app/SplunkAppForXenApp/expand.png" />');
	    $(".panel_row4_col").attr("id", "pnlICAPerf");
	    $(".panel_row4_col").hide();
	    
	    $("#imgICAPerf").click(function() {
		    $(".panel_row4_col").slideToggle("blind",
			function () {
			    $("#imgICAPerf").attr("src", $("#pnlICAPerf").is(":visible") ? "/static/app/SplunkAppForXenApp/collapse.png" : "/static/app/SplunkAppForXenApp/expand.png");
			});

		});

	    // Set up toggle drop down for XenApp Host Performance
	    $(".panel_row5_col").find(".meta").html('<img id="imgHostPerf" src="/static/app/SplunkAppForXenApp/expand.png" />');
	    $(".panel_row6_col").attr("id", "pnlHostPerf");
	    $(".panel_row6_col").hide();
	    
	    $("#imgHostPerf").click(function() {
		    $(".panel_row6_col").slideToggle("blind",
			function () {
			    $("#imgHostPerf").attr("src", $("#pnlHostPerf").is(":visible") ? "/static/app/SplunkAppForXenApp/collapse.png" : "/static/app/SplunkAppForXenApp/expand.png");
			});

		});
	    
	    // Set up toggle drop down for Hypervisor Host Performance
	    $(".panel_row7_col").find(".meta").html('<img id="imgHypPerf" src="/static/app/SplunkAppForXenApp/expand.png" />');
	    $(".panel_row8_col").attr("id", "pnlHypPerf");
	    $(".panel_row8_col").hide();
	    
	    $("#imgHypPerf").click(function() {
		    $(".panel_row8_col").slideToggle("blind",
			function () {
			    $("#imgHypPerf").attr("src", $("#pnlHypPerf").is(":visible") ? "/static/app/SplunkAppForXenApp/collapse.png" : "/static/app/SplunkAppForXenApp/expand.png");
			});

		});
	});
	
    break;

    case "xa_userexp_profiler2":
	$(document).ready(function() {
	    
	    var hostname = getParameterByName("hostname");
	    var username = getParameterByName("username");
	    
	    if(hostname != "") {
                $('input[name="host"]').val(hostname);
	    }
	    
	    if(username != "") {
		$('input[name="user"]').val(username);
	    }
	    
	    if((username != "") && (hostname != "")) {
		$(".SubmitButton").find(".splButton-primary").click();
	    }
	    
	    $(".panel_row7_col").hide();
	    
	    // Set up toggle drop down for ICA Performance
	    $(".panel_row3_col").find(".meta").html('<img id="imgICAPerf" src="/static/app/SplunkAppForXenApp/expand.png" />');
	    $(".panel_row4_col").attr("id", "pnlICAPerf");
	    $(".panel_row4_col").hide();
	    
	    $("#imgICAPerf").click(function() {
		    $(".panel_row4_col").slideToggle("blind",
			function () {
			    $("#imgICAPerf").attr("src", $("#pnlICAPerf").is(":visible") ? "/static/app/SplunkAppForXenApp/collapse.png" : "/static/app/SplunkAppForXenApp/expand.png");
			});

		});

	    // Set up toggle drop down for XenApp Host Performance
	    $(".panel_row5_col").find(".meta").html('<img id="imgHostPerf" src="/static/app/SplunkAppForXenApp/expand.png" />');
	    $(".panel_row6_col").attr("id", "pnlHostPerf");
	    $(".panel_row6_col").hide();
	    
	    $("#imgHostPerf").click(function() {
		    $(".panel_row6_col").slideToggle("blind",
			function () {
			    $("#imgHostPerf").attr("src", $("#pnlHostPerf").is(":visible") ? "/static/app/SplunkAppForXenApp/collapse.png" : "/static/app/SplunkAppForXenApp/expand.png");
			});

		});
	    
	    // Set up toggle drop down for Hypervisor Host Performance
	    $(".panel_row7_col").find(".meta").html('<img id="imgHypPerf" src="/static/app/SplunkAppForXenApp/expand.png" />');
	    $(".panel_row8_col").attr("id", "pnlHypPerf");
	    $(".panel_row8_col").hide();
	    
	    $("#imgHypPerf").click(function() {
		    $(".panel_row8_col").slideToggle("blind",
			function () {
			    $("#imgHypPerf").attr("src", $("#pnlHypPerf").is(":visible") ? "/static/app/SplunkAppForXenApp/collapse.png" : "/static/app/SplunkAppForXenApp/expand.png");
			});

		});
	});
	
    break;
    
    case "xa_perf_overview":
        $(document).ready(function() {
            $(".panel_row3_col .TableView").hide();
            $(".panel_row5_col .TableView").hide();
            $(".panel_row7_col .TableView").hide();
            $(".SingleValueHolder span").mouseover(function() { $(".SingleValueHolder span").css("cursor","pointer") });
            $(".panel_row3_col .SingleValueHolder span").click(function() { $(".panel_row3_col .TableView").toggle() });
            $(".panel_row5_col .SingleValueHolder span").click(function() { $(".panel_row5_col .TableView").toggle() });
            $(".panel_row7_col .SingleValueHolder span").click(function() { $(".panel_row7_col .TableView").toggle() });
        });
    
    break;
}
