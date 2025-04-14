$(document).ready(function() {
    var socket = io("http://localhost:8086");

    socket.on("connect", function() {
        console.log("Conectado ao servidor WebSocket");
    });

    socket.on("message", function(data) {
        console.log("Mensagem recebida:", data);
        $("#chat-container").append($('<p class="sent">').text(data)); // Sua mensagem enviada

        // Simulando uma mensagem recebida
        $("#chat-container").append($('<p class="received">').text("Mensagem de outro usuário!"));

        $("#chat-container").scrollTop($("#chat-container")[0].scrollHeight); // Garante a rolagem para o final
    });

    $("#botao").on('click', function() {
        var usuario = $('#usuario').val();
        var mensagem = $('#mensagem').val();
        if (usuario && mensagem) {
            var mensagemCompleta = usuario + ": " + mensagem;
            $("#chat-container").append($('<p class="sent">').text(mensagemCompleta));
            $('#mensagem').val('');
            // socket.emit('message', usuario + ": " + mensagem); // Comente ou remova esta linha por enquanto
            $("#chat-container").scrollTop($("#chat-container")[0].scrollHeight);
        }
    });
    $("#mensagem").on('keypress', function(event) {
        if (event.key === "Enter") {
            var usuario = $('#usuario').val();
            var mensagem = $('#mensagem').val();
            if (usuario && mensagem) {
                socket.emit('message', usuario + ": " + mensagem);
                $('#mensagem').val('');
            }
        }
    });
});
