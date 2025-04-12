import flet as ft


class MensagemInstantaneaApp(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.texto_titulo = ft.Text("Mensagem Instantânea", style=ft.TextThemeStyle.HEADLINE_MEDIUM, color=ft.colors.WHITE)
        self.chat = ft.Column(expand=True, spacing=10)
        self.nome_usuario = ft.TextField(label="Escreva seu nome")
        self.campo_mensagem = ft.TextField(label="Digite uma mensagem", on_submit=self.enviar_mensagem, expand=True)
        self.botao_enviar_mensagem = ft.ElevatedButton("Enviar", on_click=self.enviar_mensagem)
        self.popup = ft.AlertDialog(
            open=False,
            modal=True,
            title=ft.Text("Bem vindo ao mensagem_instantanea"),
            content=self.nome_usuario,
            actions=[ft.ElevatedButton("Entrar", on_click=self.entrar_popup)],
        )
        self.botao_iniciar = ft.ElevatedButton("Iniciar chat", on_click=self.entrar_chat)
        self.logo = ft.Image(src="src/img/Logo.jpg", width=30, height=30) # Caminho correto para a logo

    def enviar_mensagem_tunel(self, mensagem):
        tipo = mensagem["tipo"]
        if tipo == "mensagem":
            texto_mensagem = mensagem["texto"]
            usuario_mensagem = mensagem["usuario"]
            self.chat.controls.append(
                ft.Container(
                    content=ft.Text(f"{usuario_mensagem}: {texto_mensagem}", color=ft.colors.BLACK),
                    bgcolor=ft.colors.WHITE,
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
                    color=ft.colors.ORANGE_500,
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
        if self.nome_usuario.value:
            self.page.pubsub.send_all({"usuario": self.nome_usuario.value, "tipo": "entrada"})
            self.page.add(ft.Column([
                ft.Expanded(self.chat),
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
        self.page.pubsub.subscribe(self.enviar_mensagem_tunel)
        return ft.Column(
            [
                ft.AppBar(
                    title=ft.Text("Mensagem Instantânea", color=ft.colors.WHITE),
                    bgcolor=ft.colors.RED_ACCENT_700,
                    leading=self.logo
                ),
                ft.Expanded(
                    ft.Container(
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
                            colors=[ft.colors.BLUE_GREY_800, ft.colors.BLUE_GREY_900],
                        )
                    )
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True
        )

def main(pagina: ft.Page):
    pagina.title = "Mensagem Instantânea"
    pagina.theme = ft.Theme(color_scheme=ft.ColorScheme(primary="#075E54"))
    pagina.bgcolor = ft.colors.TRANSPARENT
    app = MensagemInstantaneaApp()
    pagina.add(app)

ft.app(target=main, view=ft.WEB_BROWSER, port=8000)