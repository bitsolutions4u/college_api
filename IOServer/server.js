const express = require('express');
const http = require('http');
const socketio = require('socket.io');
var request = require('request');

const PORT = process.env.IO_PORT || 5000
const DjanagoBaseURL = process.env.DJANGO_URL || "http://192.168.1.127:8000/"
var IO_SECRET = process.env.IO_SECRET || "NV4387G0VESRRN6STZ0VC4KN8JTQA0"

var ReqOptions = {
    headers: {
      'Content-Type': 'application/json',
      'ioAuthorization': IO_SECRET
    }
};

const app = express();
const server = http.createServer(app);
const io = socketio(server, {
    cors: {
      origin: '*',
    }
});

app.use(express.json());

app.use(function(req, res, next) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    res.setHeader('Access-Control-Allow-Credentials', true);
    next();
});


// event fired every time a new client connects:
io.on("connection", (socket) => {
    console.info(`Client connected [id= ${socket.id}]`);
  
    socket.on("disconnect", () => {
        console.info(`Client disconnected [id= ${socket.id}]`);
        // io.to(django_sid).emit("client_logout", { sid: socket.id}); // NEED API
        var options = {
            ...ReqOptions,
            json: { sid: socket.id}
        };
        
        request.post(DjanagoBaseURL+'system/io_logout/', options, function(error, response, body) {
            if (!error && response.statusCode == 200) {
              // Do something with the response data
              console.log(body);
        
            }
        });
        
    });





    socket.on("login", (data) => {
        console.log("client_login sid ",socket.id)
        console.log(data)

        data.sid = socket.id
        // io.to(django_sid).emit("client_login", data); // NEED API

        var options = {
            ...ReqOptions,
            json: data
        };
        
        request.post(DjanagoBaseURL+'system/io_login/', options, function(error, response, data) {
            if (!error && response.statusCode == 200) {
              // Do something with the response data
              console.log(data);
              socket.emit("login_feedback", data.payload);
            } else {
                console.log("Failed at io_login ", error, response, data);
  
            }
        });


    });




    socket.on("logout", () => {
        console.log("logout sid ",socket.id)

        // io.to(django_sid).emit("client_logout", { sid: socket.id}); // NEED API
        var options = {
            ...ReqOptions,
            json: { sid: socket.id}
        };
        
        request.post(DjanagoBaseURL+'system/io_logout/', options, function(error, response, body) {
            if (!error && response.statusCode == 200) {
              // Do something with the response data
              console.log(body);
        
            }
        });

    });


});


app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});


app.post('/send_notification', function(req, res) {
    var data = req.body;

    io.to(data.sid).emit("notification", data.payload);
  
    res.status(200).json({ success: true, },);
});

app.post('/update_maintenance_mode', function(req, res) {
    var data = req.body;
    io.emit("update_maintenance_mode", data.payload);
  
    res.status(200).json({ success: true, },);
});

app.post('/auto_reload', function(req, res) {
    var data = req.body;

    io.to(data.sid).emit("auto_reload", data.payload);
  
    res.status(200).json({ success: true, },);
});

server.listen(PORT, () => {
    console.log("Socketio server started on PORT : ",PORT)
});