$(document).ready(function () {
    $("#btn-open-message").click(function () {
        $(".conversation-chat-box").fadeToggle();
    });


    var socket = io('http://localhost:4001');
    console.log(socket);
    socket.on('connect', function () {
        socket.on('message', function (message) {
            console.log(message);
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
            $(".div-contains-conversation-reply>div").append(htmlElement);
        });

        $("#btn-send-reply").click(function () {
            var msg = $("#txt-reply").val();
            var requestUserId = $(this).attr("data-request-user");
            var pageUserId = $(this).attr("data-page-user");
            var conversationReply = {
                'new_msg': msg,
                'requestUserId': requestUserId,
                'pageUserId': pageUserId,
                'csrf': $("input[name=csrfmiddlewaretoken]").val()
            }
            socket.emit('send_conversation_reply', conversationReply, function (data) {
                console.log(data);
            });
            $("#txt-reply").val("");
        });
    });


});