$("document").ready(function () {
    $("#btn-toggle-create-room").click(function () {
        $(this).closest("div").find(".form-create-room").toggle();
        $(this).closest("div").find(".txt-room-name").val("");
    });

    $(".btn-create-room").click(function () {
        var roomName = $(this).closest("div").find(".txt-room-name").val();
        var dataAjaxTarget = $(this).attr("data-ajax-target");
        var self = $(this);
        $.ajax({
            url: dataAjaxTarget,
            type: 'POST',
            data: {
                name: roomName,
            },
            dataType: 'json',
            success: function (data) {
                self.closest("div").find(".txt-room-name").val("");
                htmlElement = "<div class='col-md-4 margin-bot-10 each-room border-left border-bottom border-top'>";
                htmlElement += data.a_link_start;
                htmlElement += "<p class='name-of-room-p'>" + data.name_room + "</p>";
                htmlElement += "<p class='time_created_of_room-p'>" + data.time_created + "</p>";
                htmlElement += "<p class='created_by_p'>" + data.created_by + "</p>";
                htmlElement += data.a_link_end;
                htmlElement += "</div>";

                self.closest("div.container").find(".contains-list-room").append(htmlElement);
            },
        });
    });

    $("#btn-exit-room").click(function () {
        var idRoom = $(this).attr("data-id-room");
        var dataAjaxTarget = $(this).attr("data-ajax-target");
        hostName = window.location.hostname;
        $.ajax({
            url: dataAjaxTarget,
            type: 'POST',
            data: {
                id: idRoom,
            },
            dataType: 'json',
            success: function (data) {
                if (data.is_valid) {
                    window.location.href = "http://" + hostName + ":8000/home/";
                }
            },
        });
    });
    var socket = io('http://localhost:4000');
    console.log(socket);
    socket.on('connect', function () {
        socket.on('message', function (message) {
            var currentUsername = $("#text-username").val();
            var data = message.split(" ");
            var reply = "";
            for (var i = 1; i < data.length; i++) {
                reply += data[i] + " ";
            }
            htmlElement = "<div class='row each-reply'>";
            if (data[0] == currentUsername) {
                htmlElement += "<b style='color: plum;'>Me</b> : " + reply + "";
            } else {
                htmlElement += "<b style='color: #5b80b2;'>" + data[0] + "</b> : " + reply + "";
            }
            htmlElement += "</div>";
            $(".div-contains-room-chat-reply>div").append(htmlElement);
        })

        $("#btn-send-reply").click(function () {
            var msg = $(this).closest(".contains-form-send").find("#txt-reply").val();
            var idRoom = $(this).attr("data-id-room");
            var idUser = $(this).attr("data-id-user");
            var roomReply = {
                'new_msg': msg,
                'idRoom': idRoom,
                'idUser': idUser,
                'csrf': $("input[name=csrfmiddlewaretoken]").val()
            }
            console.log(roomReply);

            socket.emit('send_reply', roomReply, function (data) {
                console.log(data);
            });
            $(this).closest(".contains-form-send").find("#txt-reply").val("");
        });
    });

});