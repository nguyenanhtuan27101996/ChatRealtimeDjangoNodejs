var http = require('http');
var server = http.createServer().listen(4000);
var io = require('socket.io').listen(server);
var cookie_reader = require('cookie');
var querystring = require('querystring');
var redis = require('redis');
var sub = redis.createClient();

//Subscribe to the Redis chat channel
sub.subscribe('chat');
io.set('authorization', function (data, accept) {
    if (data.headers.cookie) {
        data.cookie = cookie_reader.parse(data.headers.cookie);
        return accept(null, true);
    }
    return accept('error', false);
});
io.set('log level', 1);


io.sockets.on('connection', function(socket){
    //Grab message from Redis and send to client
    sub.on('message', function(channel, message){
        socket.send(message);
    });

	socket.on('send_reply', function(data){
	    var dataNeedSend = {
            user_id: data.idUser,
            id: data.idRoom,
            reply: data.new_msg,
        }
	    var values = querystring.stringify(dataNeedSend);
        console.log(values);
        console.log(dataNeedSend);

		console.log(data.new_msg + " - "+ data.idRoom + " - " + data.idUser);
		var options = {
			hostname: 'localhost',
			port: '8000',
			path: '/ajax/create_reply_of_room_chat/',
			method: 'POST',
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
				'Content-Length': values.length
			},

		};
		var buffer = "";
        var req = http.request(options, function(res){
            res.setEncoding('utf8');

            res.on('data', function (chunk) {
                buffer += chunk;
            });
            res.on('end', function () {
                console.log(buffer);
            });
        });
        req.write(values);
        req.end();
	});
});