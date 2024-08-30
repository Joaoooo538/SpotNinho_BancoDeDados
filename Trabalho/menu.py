from Conexao import Conexao
import os

conexaoBD = Conexao("localhost", "root", "mysql", "spotninho")

def cadastrar_usuario():
    print("\n----- CADASTRAR USUÁRIO -----")
    
    nome = input("\nInsira um nome de usuário: ")
    email = input("Insira um email válido: ")
    senha = input("Insira uma senha válida: ")
    
    # Verifica se o email ou nome já estão cadastrados
    usuario_existente = conexaoBD.consultarComParametros(
        "SELECT * FROM usuario WHERE email = %s OR nome = %s", 
        (email, nome)
    )
    
    if not usuario_existente:
        if email.endswith("@gmail.com"):
            conexaoBD.manipularComParametros(
                "INSERT INTO usuario (nome, senha, email) VALUES (%s, %s, %s)",
                (nome, senha, email)
            )
            print("USUÁRIO CADASTRADO!")
        else:
            print("EMAIL INVÁLIDO.")
    else:
        print("NOME OU EMAIL DE USUÁRIO JÁ EXISTENTE.")
    os.system("PAUSE")

def remover_usuario():
    print("\n----- REMOVER USUÁRIO -----")
    
    email = input("Insira o email do usuário que deseja remover: ")
    usuario_existente = conexaoBD.consultarComParametros("SELECT * FROM usuario WHERE email = %s", (email,))
    
    if usuario_existente:
        conexaoBD.manipularComParametros("DELETE FROM usuario WHERE email = %s", (email,))
        print("USUÁRIO REMOVIDO!")
    else:
        print("USUÁRIO NÃO ENCONTRADO.")
    os.system("PAUSE")

def entrar():
    print("\n----- ENTRAR -----")
    
    nome = input("Insira seu nome de usuário: ")
    senha = input("Insira sua senha: ")
    
    consulta = conexaoBD.consultarComParametros("SELECT * FROM usuario WHERE nome = %s AND senha = %s", (nome, senha))
    
    if consulta:
        print(f"LOGIN BEM-SUCEDIDO. BEM-VINDO, {nome}!")
        menu_usuario(nome)
    else:
        print("NOME DE USUÁRIO OU SENHA INVÁLIDOS.")
    os.system("PAUSE")

def menu_usuario(nome_usuario):
    while True:
        print(f'''\nMENU USUÁRIO - {nome_usuario}:
        
[1] - CRIAR PLAYLIST.
[2] - VER PLAYLISTS.
[3] - VER HISTÓRICO.
[4] - SAIR.
''')
        
        escolha = input("Insira uma opção: ")
        
        if escolha == "1":
            criar_playlist(nome_usuario)
        
        elif escolha == "2":
            ver_playlists(nome_usuario)
        
        elif escolha == "3":
            ver_historico(nome_usuario)
        
        elif escolha == "4":
            break
        
        else:
            print("Opção inválida. Tente novamente.")
            os.system("PAUSE")

def criar_playlist(nome_usuario):
    print("\n----- CRIAR PLAYLIST -----")
    
    nome_playlist = input("Nome da playlist: ")
    
    # Recuperar id do usuário
    id_usuario = conexaoBD.consultarComParametros("SELECT id_usuario FROM usuario WHERE nome = %s", (nome_usuario,))[0][0]
    
    # Inserir nova playlist
    conexaoBD.manipularComParametros(
        "INSERT INTO playlist (nome_playlist, id_usuario) VALUES (%s, %s)",
        (nome_playlist, id_usuario)
    )
    
    # Recuperar ID da nova playlist
    id_playlist = conexaoBD.consultarComParametros(
        "SELECT id_playlist FROM playlist WHERE nome_playlist = %s AND id_usuario = %s ORDER BY id_playlist DESC LIMIT 1", 
        (nome_playlist, id_usuario)
    )[0][0]
    
    # Adicionar músicas à playlist
    while True:
        musicas_disponiveis = conexaoBD.consultar("SELECT id_musica, nome, artista FROM musicas")
        
        print("\nMúsicas disponíveis:")
        for musica in musicas_disponiveis:
            print(f"[{musica[0]}] - {musica[1]} ({musica[2]})")
        
        escolha_musica = input("Escolha o ID da música para adicionar à playlist (ou '0' para finalizar): ")
        
        if escolha_musica == "0":
            break
        else:
            conexaoBD.manipularComParametros(
                "INSERT INTO lista (id_playlist, id_musica) VALUES (%s, %s)",
                (id_playlist, escolha_musica)
            )
    
    print("PLAYLIST CRIADA COM SUCESSO!")
    os.system("PAUSE")

def ver_playlists(nome_usuario):
    print("\n----- VER PLAYLISTS -----")
    
    id_usuario = conexaoBD.consultarComParametros("SELECT id_usuario FROM usuario WHERE nome = %s", (nome_usuario,))[0][0]
    playlists = conexaoBD.consultarComParametros("SELECT id_playlist, nome_playlist FROM playlist WHERE id_usuario = %s", (id_usuario,))
    
    if playlists:
        for playlist in playlists:
            print(f"[{playlist[0]}] - {playlist[1]}")
        
        id_playlist = input("\nInsira o ID da playlist para visualizar as músicas (ou '0' para voltar): ")
        
        if id_playlist != "0":
            musicas = conexaoBD.consultarComParametros(
                '''SELECT m.nome, m.artista FROM musicas m 
                INNER JOIN lista l ON m.id_musica = l.id_musica 
                WHERE l.id_playlist = %s''', (id_playlist,)
            )
            
            if musicas:
                print("\nMúsicas na playlist:")
                for musica in musicas:
                    print(f"{musica[0]} - {musica[1]}")
            else:
                print("Nenhuma música encontrada na playlist.")
    else:
        print("Nenhuma playlist encontrada.")
    os.system("PAUSE")

def ver_historico(nome_usuario):
    print("\n----- VER HISTÓRICO -----")

    print("HISTÓRICO DE REPRODUÇÃO NÃO IMPLEMENTADO.")
    os.system("PAUSE")

# Menu Principal
while True:
    print('''MENU SPOT-NINHO:
          
[1] - CADASTRAR USUÁRIO.
[2] - REMOVER USUÁRIO.
[3] - ENTRAR.
[0] - SAIR.
''')

    escolha = input("Insira uma opção: ")

    if escolha == "1":
        cadastrar_usuario()

    elif escolha == "2":
        remover_usuario()

    elif escolha == "3":
        entrar()

    elif escolha == "0":
        break

    else:
        print("Opção inválida. Tente novamente.")
        os.system("PAUSE")