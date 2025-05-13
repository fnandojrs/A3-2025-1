from nicegui import ui
import mysql.connector
from mysql.connector import Error
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def conectar():
    return mysql.connector.connect(
        host='metro.proxy.rlwy.net',
        port=25858,
        user='root',
        password='bojFqQXsCRiLKyzbmgsPidyeQLJAVlsE',
        database='railway'
    )

@ui.page('/')
def login_page():
    ui.add_head_html('<link rel="stylesheet" href="/static/custom.css">')

    with ui.element('div').classes('login-container'):
        with ui.element('div').classes('login-box'):
            ui.label('Login').classes('text-2xl mb-4')

            email = ui.input('Email').props('outlined').classes('w-full')

            # Estado para saber se a senha está visível
            mostrar = {'ativo': False}
            senha_valor = {'texto': ''}

            # Função que renderiza o campo de senha
            def render_senha():
                senha_container.clear()

                with senha_container:
                    with ui.row().classes('items-center w-full'):
                        campo = ui.input('Senha', password=not mostrar['ativo']).props('outlined').classes('flex-grow')
                        campo.value = senha_valor['texto']

                        def on_change(e):
                            senha_valor['texto'] = e.value

                        campo.on('input', on_change)

                        icon = ui.icon('visibility_off' if mostrar['ativo'] else 'visibility').on(
                            'click', toggle_senha).classes('cursor-pointer')

                        return campo

            # Alterna visibilidade da senha
            def toggle_senha():
                mostrar['ativo'] = not mostrar['ativo']
                render_senha()

            # Container dinâmico da senha
            senha_container = ui.element('div')
            senha_input = render_senha()

            def login():
                try:
                    conn = conectar()
                    cursor = conn.cursor()

                    if email.value == '' or senha_valor['texto'] == '':
                        ui.notify('Preencha todos os campos')
                        return

                    cursor.execute('SELECT * FROM usuarios WHERE nome = %s AND senha = %s',
                                   (email.value, senha_valor['texto']))
                    usuario = cursor.fetchone()

                    if usuario:
                        ui.navigate.to('/cadastro_usuario')
                    else:
                        ui.notify('Login inválido')
                        email.value = ''
                        senha_valor['texto'] = ''
                        render_senha()
                except Error as e:
                    ui.notify(f'Erro no banco: {e}')
                finally:
                    if conn.is_connected():
                        cursor.close()
                        conn.close()

            ui.button('Entrar', on_click=login).classes('mt-4 w-full')
            ui.button('Cadastrar Usuario', on_click=lambda: ui.navigate.to('/cadastro_usuario')).classes('mt-2 w-full')

