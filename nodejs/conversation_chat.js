var http = require('http');
var server = http.createServer().listen(4001);
var io = require('socket.io').listen(server);
var cookie_reader = require('cookie');
var querystring = require('querystring');
var redis = require('redis');
var sub1 = redis.createClient();

//Subscribe to the Redis chat channel
sub1.subscribe('conversation_chat');

io.set('authorization', function (data, accept) {
    if (data.headers.cookie) {
        data.cookie = cookie_reader.parse(data.headers.cookie);
        return accept(null, true);
    }
    return accept('error', false);
});
io.set('log level', 1);

io.sockets.on('connection', function(socket){

	sub1.on('message', function(channel, message){
        socket.send(message);

    });
	socket.on('send_conversation_reply', function(data){
	    var dataNeedSend = {
            request_user_id: data.requestUserId,
            page_user_id: data.pageUserId,
            reply: data.new_msg,
        }
	    var values = querystring.stringify(dataNeedSend);


		var options = {
			hostname: 'localhost',
			port: '8000',
			path: '/ajax/create_conversation_reply/',
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