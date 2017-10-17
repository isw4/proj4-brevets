//obtains the scriptroot string from the meta html tag
var SCRIPT_ROOT = $("#script-root").data("scriptroot");
var TIME_CALC_URL = SCRIPT_ROOT + "/_calc_times";

// Pass calctimes a <td> element containing the data for a control.
// It extracts the distance and calls the server to get times to
// fill in open and close times in a human-readable format.
// (If we want to also keep the ISO-formatted times, we'll need to
// stash them in hidden fields.) 
function calc_times(control) {
  var km = control.find("input[name='km']").val();
  var brev_dist  = $("#brevet_dist_km").val();
  var timezone   = moment.tz.guess();      // As a string. See moment.tz docs
  var begin_date = $("#begin_date").val(); // In YYYY/MM/DD
  var begin_time = $("#begin_time").val(); // In HH:mm
  var start_time = moment.tz(begin_date + " " + begin_time, timezone).format()
  console.log(start_time)

  var open_time_field = control.find("input[name='open']");
  var close_time_field = control.find("input[name='close']");

  $.getJSON(TIME_CALC_URL, { km: km, brev_dist: brev_dist, start_time: start_time }, 
    // response handler
    function(data) {
      var times = data.result;
      console.log("Got a response");
      console.log("Response.open = "  + times.open);
      console.log("Response.close = " + times.close);
      open_time_field.val( moment(times.open).format("ddd M/D/Y H:mm"));
      close_time_field.val( moment(times.close).format("ddd M/D/Y H:mm"));
    } // end of handler function
  );// End of getJSON
}

$(document).ready(function(){
// Do the following when the page is finished loading

  $('input[name="miles"]').change(function() {
    // If the input is in miles, converts to km first
    var miles = parseFloat($(this).val());
    var km = (1.609344 * miles).toFixed(1) ;
    console.log("Converted " + miles + " miles to " + km + " kilometers");
    var control_entry = $(this).parents(".control")
    var target = control_entry.find("input[name='km']");
    target.val( km );

    // Then calculate times for this entry
    calc_times(control_entry);
  });

  $('input[name="km"]').change(function() {
    // If the input is in km, convert to miles first
    var km = parseFloat($(this).val());
    var miles = (0.621371 * km).toFixed(1) ;
    console.log("Converted " + km + " km to " + miles + " miles");
    var control_entry = $(this).parents(".control")
    var target = control_entry.find("input[name='miles']");
    target.val( miles );

    // Then calculate times for this entry
    calc_times(control_entry);
  });

});   // end of what we do on document ready