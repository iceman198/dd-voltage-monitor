
const char MAIN_page[] PROGMEM = R"=====(
<!DOCTYPE HTML><html>
	<head>
		<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0">
		<title>Volage Monitor</title>
		<script type = "text/javascript">
			var ws;
			function socketConnect() {
				ws = new WebSocket("ws://192.168.4.1:8181");
				if ("WebSocket" in window) {
					ws.onopen = function() {
						// Web Socket is connected, send data using send()
						//ws.send("Message to send");
					};
					
					ws.onmessage = function (evt) { 
						var received_msg = evt.data;
						console.log("Message received: " + received_msg);
						if (received_msg.indexOf("V1") >= -1) {
							document.getElementById("voltageOne").innerHTML = received_msg;
						}
						if (received_msg.indexOf("V2") >= -1) {
							document.getElementById("voltageTwo").innerHTML = received_msg;
						}
						//alert("Message is received...");
					};
					
					ws.onclose = function() { 
						// websocket is closed.
						//alert("Connection is closed..."); 
					};
				} else {
					// The browser doesn't support WebSocket
					alert("WebSocket NOT supported by your Browser!");
				}
			}
			
			function socketDisconnect() {
				ws.close();
			}

			socketConnect();

			function socketSend() {
				ws.send('testing');
			}
		</script>
	</head>
	<body>
		<h1>Voltage Monitor</h1>
		<button onclick="socketConnect()">Connect</button>
		<button onclick="socketDisconnect()">Disconnect</button>
		<button onclick="socketSend()">Send test</button>
		<hr>
		<div id="voltageOne"></div>
		<hr>
		<div id="voltageTwo"></div>
	</body>
</html>
)=====";