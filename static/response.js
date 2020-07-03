let map;
let markersArray = [];

$(document).ready(function() {
  $("#myButton2").hide();
  $("#myButton3").hide();
  $("#myButton4").hide();
  $("#myButton5").hide();
  $("#myButton1").click(function() {
    $("#myButton1").before('<input type="text" id="stop_address1" name="stop_address1" value="" placeholder="Enter Stop 1 Address"  style="width: 100%" required>');
    $("#myButton1").before('<br/>');

    $(this).hide();
    $("#myButton2").show();
  });
});

$(document).ready(function() {
  $("#myButton2").click(function() {
    $("#myButton2").before('<input type="text" id="stop_address2" name="stop_address2" value="" placeholder="Enter Stop 2 Address" style="width: 100%" required>');
    $("#myButton2").before('<br/>');

    $(this).hide();
      $("#myButton3").show();
  });
});

$(document).ready(function() {
  $("#myButton3").click(function() {
    $("#myButton3").before('<input type="text" id="stop_address3" name="stop_address3" value="" placeholder="Enter Stop 3 Address" style="width: 100%" required>');
    $("#myButton3").before('<br/>');

    $(this).hide();
      $("#myButton4").show();
  });
});

$(document).ready(function() {
  $("#myButton4").click(function() {
    $("#myButton4").before('<input type="text" id="stop_address4" name="stop_address4" value="" placeholder="Enter Stop 4 Address" style="width: 100%" required>');
    $("#myButton4").before('<br/>');

    $(this).hide();
      $("#myButton5").show();
  });
});

$(document).ready(function() {
  $("#myButton5").click(function() {
    $("#myButton5").before('<input type="text" id="stop_address5" name="stop_address5" value="" placeholder="Enter Stop 5 Address" style="width: 100%" required>');
    $("#myButton5").before('<br/>');
    $(this).hide();
    $("addstop").hide();

  });
});

$('#myform1').submit(function (e) {
    var data;

    data = new FormData();
    data.append('file', $('#file')[0].files[0]);

    $.ajax({
        url: 'http://127.0.0.1:5000',
        data: data,
        processData: false,
        type: 'POST',

        // This will override the content type header,
        // regardless of whether content is actually sent.
        // Defaults to 'application/x-www-form-urlencoded'
        contentType: 'multipart/form-data',

        //Before 1.5.1 you had to do this:
        beforeSend: function (x) {
            if (x && x.overrideMimeType) {
                x.overrideMimeType("multipart/form-data");
            }
        },
        // Now you should be able to do this:
        mimeType: 'multipart/form-data',    //Property added in 1.5.1

        success: function (data) {
            alert(data);
        }
    });

    e.preventDefault();
});





function myMap()
    {
        myLatLng = {lat: 17.5438, lng: 78.5700}
        var mapProp=
            {
                center:new google.maps.LatLng(17.5438,78.5700),
                zoom:12,
            };
        map = new google.maps.Map(document.getElementById("googleMap"),mapProp);
        var marker = new google.maps.Marker({
            position: myLatLng,
            map: map,
            title: "Drag Me",
            draggable: true
        });

        google.maps.event.addListener(map, 'click', function(event) {
        console.log(event);
        placeMarker(event.latLng);
});

}
function placeMarker(location) {
    var marker = new google.maps.Marker({
        position: location,
        map: map,
        draggable: true
    });

    markersArray.push(marker);
}

$(document).ready(function(){
$("#addButton").bind("click",AddTables);
function AddTables(e)
    {
        if($("#tbl tr[addedrow='yes']").length<7)
        {
        $("#tbl").append("<tr addedrow='yes'><td>First Name</td><td><input type='text'/></td></tr><tr><td>Last Name</td><td><input type='text'/></td></tr>");
        }
    }

});
