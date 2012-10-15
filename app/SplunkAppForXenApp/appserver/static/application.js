function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regexS = "[\\?&]" + name + "=([^&#]*)";
    var regex = new RegExp(regexS, 'gi');
    var results = regex.exec(window.location.search);
    if(results == null)
        return "";
    else
        return decodeURIComponent(results[1].replace(/\+/g, " "));
}

switch (Splunk.util.getCurrentView()) {
    
    case "xa_landing":
	
	if (Splunk.Module.NullModule) {
                Splunk.Module.NullModule = $.klass(Splunk.Module.NullModule, {
                    onContextChange: function() {
                        var context = this.getContext();
                        
                        var name = context.get("click.name");
                        var val = context.get("click.value");
                        var name2 = context.get("click.name2");
                        var val2 = context.get("click.value2");
			
                        if (name == "Farm Name") {
                            location.href=Splunk.util.make_url("app", Splunk.util.getCurrentApp(), "farm_status") + "?farmname=" + val;
                        }
			
			if (name == "Server") {
                            location.href=Splunk.util.make_url("app", Splunk.util.getCurrentApp(), "event_viewer") + "?servername=" + val + "&SourceName=" + val2;
                        }
                    },
                });
        }
	
    break;

    case "farm_status":
	
	$(document).ready(function() {
            var farmname = getParameterByName("farmname");
            
            if(farmname != "") {
                $('input[name="farm"]').val(farmname);
		$('input[name="farm"]').closest("form").submit();
            } else {
                $('input[name="farm"]').val("Search by Farm Name");
                $('input[name="farm"]').focus(function(){
                    if($(this).val() == "Search by Farm Name") {
                        $(this).val("");
                    }
                });
            }
        });
	
	if (Splunk.Module.NullModule) {
                Splunk.Module.NullModule = $.klass(Splunk.Module.NullModule, {
                    onContextChange: function() {
                        var context = this.getContext();
                        
                        var name = context.get("click.name");
                        var val = context.get("click.value");
                        var name2 = context.get("click.name2");
                        var val2 = context.get("click.value2");
			
                        if (name == "Server Name") {
                            location.href=Splunk.util.make_url("app", Splunk.util.getCurrentApp(), "server_status") + "?servername=" + val;
                        }
                    },
                });
        }
	
    break;

    case "server_status":
	
	$(document).ready(function() {
            var servername = getParameterByName("servername");
            
            if(servername != "") {
                $('input[name="server"]').val(servername);
		$('input[name="server"]').closest("form").submit();
            } else {
                $('input[name="server"]').val("Search by Server Name");
                $('input[name="server"]').focus(function(){
                    if($(this).val() == "Search by Server Name") {
                        $(this).val("");
                    }
                });
            }
        });
	
	if (Splunk.Module.NullModule) {
                Splunk.Module.NullModule = $.klass(Splunk.Module.NullModule, {
                    onContextChange: function() {
                        var context = this.getContext();
                        
                        var name = context.get("click.name");
                        var val = context.get("click.value");
                        var name2 = context.get("click.name2");
                        var val2 = context.get("click.value2");
			
                        if (name == "Server Name") {
                            location.href=Splunk.util.make_url("app", Splunk.util.getCurrentApp(), "server_status") + "?servername=" + val;
                        }
                    },
                });
        }
	
    break;
    
    case "event_viewer":
	
	$(document).ready(function() {
	    
	    var submitForm = false;
	    var servername = getParameterByName("servername");
	    var eventcode = getParameterByName("eventcode");
	    var sourcename = getParameterByName("sourcename");
	    var eventtype = getParameterByName("type");
            
            if(servername != "") {
                $('input[name="ServerName"]').val(servername);
		submitForm = true;
            }
	    
	    if(eventcode != "") {
                $('input[name="EventCode"]').val(eventcode);
		submitForm = true;
            }
	    
	    if(sourcename != "") {
                $('input[name="SourceName"]').val(sourcename);
		submitForm = true;
            }
	    
	    if(eventtype != "") {
                $('input[name="Type"]').val(eventtype);
		submitForm = true;
            }
	    
	    if(submitForm) {
		$("#SubmitButton_0_5_0").find('.splButton-primary').click();
	    }
	    
            
            $.getScript("/static/app/SplunkAppForXenApp/jquery-ui.min.js", function() {
                $('#dialog').dialog({
                    autoOpen: false,
                    width: 600,
                    buttons: {
                        Ok: function() {
                            $( this ).dialog( "close" );
                        }
                    }
                });
            });
	});
        
        Splunk.Module.SimpleResultsTable = $.klass(Splunk.Module.SimpleResultsTable, {
            renderResults: function($super,data) {
                $super(data);
                //$('td:nth-child(1),th:nth-child(1)', this.container).hide();
                $(".panel_row2_col").find('td:nth-child(1)', this.container).hide();
                $(".panel_row2_col").find('th:nth-child(1)', this.container).hide();
            }
        });
        
        if (Splunk.Module.NullModule) {
                Splunk.Module.NullModule = $.klass(Splunk.Module.NullModule, {
                    onContextChange: function() {
                        var val = this.getContext().get("click.value");
                        
			$('#dialog').html("<p>"+val+"</p>");
			$('#dialog').dialog('open');
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

    case "xa_userexp_wizard":
	$(document).ready(function() {
	    
	    $('input[name="user"]').focus();
	    
	    var timeDiv = $("#sTime").parent().parent().parent();
	    $(timeDiv).addClass("timeCell");
	    
	    var userDiv = $("#sUser").parent().parent().parent();
	    $(userDiv).addClass("userCell");
	    
	    var serverDiv = $("#sServer").parent().parent().parent();
	    $(serverDiv).addClass("serverCell");
	    
	    var selectText = "Type in a user name and press 'List Servers'";
	    
	    $("#SearchSelectLister_0_3_0_id option:first").text(selectText);
	    
	    $("#btnSubmit").click(function(){
		
		var username = $('input[name="user"]').val();
		var servername = $("#SearchSelectLister_0_3_0_id option:selected").text();
		
		if($.trim(username) == "") {
		    alert("Please enter a user name");
		    $('input[name="user"]').focus();
		} else if(servername == selectText) {
			alert(selectText);
		} else {
		    location.href=Splunk.util.make_url("app", Splunk.util.getCurrentApp(), "xa_user_experience") + "?username=" + username + "&hostname=" + servername;
		}
		
	    });
	});
	
    break;

    case "xa_user_experience":
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
