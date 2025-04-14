import flet as ft

class MensagemInstantaneaApp(ft.Control):
    def __init__(self):
        super().__init__()
        self.texto_titulo = ft.Text("Mensagem Instantânea", style=ft.TextThemeStyle.HEADLINE_MEDIUM, color=ft.Colors.WHITE)
        self.chat = ft.Column(expand=True, spacing=10)
        self.nome_usuario = ft.TextField(label="Escreva seu nome", autofocus=True)
        self.campo_mensagem = ft.TextField(label="Digite uma mensagem", on_submit=self.enviar_mensagem, expand=True)
        self.botao_enviar_mensagem = ft.ElevatedButton("Enviar", on_click=self.enviar_mensagem)
        self.popup = ft.AlertDialog(
            open=False,
            modal=True,
            title=ft.Text("Bem-vindo ao Mensagem Instantânea"),
            content=self.nome_usuario,
            actions=[ft.ElevatedButton("Entrar", on_click=self.entrar_popup)],
        )
        self.botao_iniciar = ft.ElevatedButton("Iniciar chat", on_click=self.entrar_chat)
        self.logo = ft.Image(src="src/img/Logo.jpg", width=30, height=30)

    def _get_control_name(self):
        return "mensageminstantanea"

    def enviar_mensagem_tunel(self, mensagem):
        tipo = mensagem["tipo"]
        if tipo == "mensagem":
            texto_mensagem = mensagem["texto"]
            usuario_mensagem = mensagem["usuario"]
            self.chat.controls.append(
                ft.Container(
                    content=ft.Text(f"{usuario_mensagem}: {texto_mensagem}", color=ft.Colors.BLACK),
                    bgcolor=ft.Colors.WHITE,
                    padding=10,
                    border_radius=10,
                    margin=ft.margin.only(left=10, right=10, top=5, bottom=5),
                    alignment=ft.alignment.center_left
                )
            )
        else:
            usuario_mensagem = mensagem["usuario"]
            self.chat.controls.append(
                ft.Text(
                    f"{usuario_mensagem} entrou no chat",
                    size=12,
                    italic=True,
                    color=ft.Colors.ORANGE_500,
                    text_align=ft.TextAlign.CENTER
                )
            )
        self.update()

    def enviar_mensagem(self, evento):
        if self.campo_mensagem.value:
            self.page.pubsub.send_all({"texto": self.campo_mensagem.value, "usuario": self.nome_usuario.value,
                                       "tipo": "mensagem"})
            self.campo_mensagem.value = ""
            self.update()

    def entrar_popup(self, evento):
        print("Função entrar_popup foi chamada!")
        print(f"Nome do usuário: {self.nome_usuario.value}")
        if self.nome_usuario.value:
            self.page.pubsub.send_all({"usuario": self.nome_usuario.value, "tipo": "entrada"})
            self.page.add(ft.Column([
            ft.Column([self.chat], expand=True),
            ft.Row([self.campo_mensagem, self.botao_enviar_mensagem], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ]))
        self.popup.open = False
        self.page.remove(self.botao_iniciar)
        self.page.remove(self.texto_titulo)
        self.update()

    def entrar_chat(self, evento):
        self.page.dialog = self.popup
        self.popup.open = True
        self.update()

    def build(self):
        return ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            self.logo,
                            ft.Text("Mensagem Instantânea", color=ft.Colors.WHITE, size=20),
                        ],
                        alignment=ft.MainAxisAlignment.START
                    ),
                    bgcolor=ft.Colors.RED_ACCENT_700,
                    padding=10
                ),
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        [
                            self.texto_titulo,
                            self.botao_iniciar,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_center,
                        end=ft.alignment.bottom_center,
                        colors=[ft.Colors.BLUE_GREY_800, ft.Colors.BLUE_GREY_900],
                    )
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True
        )


def main(pagina: ft.Page):
    pagina.title = "Mensagem Instantânea"
    pagina.theme = ft.Theme(color_scheme=ft.ColorScheme(primary="#075E54"))
    pagina.bgcolor = ft.Colors.TRANSPARENT
    app = MensagemInstantaneaApp()
    app.page = pagina  # Atribuir a página ao app
    pagina.add(app.build())
   # pagina.pubsub.subscribe(app.enviar_mensagem_tunel)  # Mover para cá


ft.app(target=main, view=ft.WEB_BROWSER, port=8086)