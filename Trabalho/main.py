import PySimpleGUI as sg
import os
import pygame
import player
import sys
from Conexao import Conexao

conexaoBD = Conexao("localhost", "root", "mysql", "spotninho")

def resource_path(relative_path):
    """Obtém o caminho absoluto para o recurso, lidando com PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

GO_BACK_IMAGE_PATH = resource_path('Images/back.png')
GO_FORWARD_IMAGE_PATH = resource_path('Images/next.png')
PLAY_SONG_IMAGE_PATH = resource_path('Images/play_button.png')
PAUSE_SONG_IMAGE_PATH = resource_path('Images/pause.png')
DEFAULT_ALBUM_COVER_IMAGE_PATH = resource_path('Images/pilot.png')

class Musica:
    def __init__(self, nome, artista, imagem, endereco):
        self.nome = nome
        self.artista = artista
        self.imagem = imagem
        self.endereco = endereco

    def get_album_cover_path(self):
        return self.imagem or DEFAULT_ALBUM_COVER_IMAGE_PATH

posic = 0
Iniciar = None
musica_pausada = False
playlists_usuario = {}

def carregar_playlists(nome_usuario):
    global playlists_usuario
    playlists_usuario = conexaoBD.consultarComParametros(
        "SELECT id_playlist, nome_playlist FROM playlist WHERE id_usuario = (SELECT id_usuario FROM usuario WHERE nome = %s)", 
        (nome_usuario,)
    )
    return [playlist[1] for playlist in playlists_usuario]  # Retorna os nomes das playlists

def update_song_display(window, music):
    window['song_name'].update(music.nome)
    window['currently_playing'].update(f'Tocando: {music.nome} - {music.artista}')
    
    album_cover_path = music.get_album_cover_path()
    window['album_cover'].update(filename=album_cover_path)

def Play_music(posic_atual, playlist_selecionada):
    global Iniciar, musica_pausada

    if not playlist_selecionada or not (0 <= posic_atual < len(playlist_selecionada)):
        sg.popup("Índice fora dos limites da lista de músicas.")
        return

    music = playlist_selecionada[posic_atual]

    if Iniciar:
        Iniciar.parar()

    Iniciar = player.Player(music)
    Iniciar.start()
    musica_pausada = False

    update_song_display(window, music)

# Carregar playlists do usuário (substitua 'NOME_USUARIO' pelo nome real do usuário logado)
playlists = carregar_playlists("pablo")

# Se não houver playlists, mostrar uma mensagem apropriada
if playlists:
    playlist_dropdown = sg.Combo(playlists, default_value=playlists[0], key='playlist_selecionada')
else:
    sg.popup("Nenhuma playlist encontrada para este usuário.")
    sys.exit()

sg.theme('Reddit')

song_title_column = [
    [sg.Text(text='Pressione play...', justification='center', background_color='black', text_color='white', size=(200, 0), font=('Cooper Black', 14), key='song_name')]
]

player_info = [
    [sg.Text('SPOT-NINHO', background_color='black', text_color='white', font=('Tahoma', 7))]
]

currently_playing = [
    [sg.Text(background_color='black', size=(200, 0), text_color='white', font=('Cooper Black', 10), key='currently_playing')]
]

main = [
    [sg.Canvas(background_color='black', size=(480, 20), pad=None)],
    [sg.Column(layout=player_info, justification='c', element_justification='c', background_color='black')],
    [sg.Text('Escolha uma Playlist:', background_color='black', text_color='white', font=('Tahoma', 10))],
    [playlist_dropdown],
    [
        sg.Canvas(background_color='black', size=(40, 350), pad=None),
        sg.Image(filename=DEFAULT_ALBUM_COVER_IMAGE_PATH, size=(350, 350), pad=None, key='album_cover'),
        sg.Canvas(background_color='black', size=(40, 350), pad=None)
    ],
    [sg.Canvas(background_color='black', size=(480, 10), pad=None)],
    [sg.Column(song_title_column, background_color='black', justification='c', element_justification='c')],
    [sg.Text('_'*80, background_color='black', text_color='white')],
    [
        sg.Canvas(background_color='black', size=(99, 200), pad=(0, 0)),
        sg.Image(pad=(10, 0), filename=GO_BACK_IMAGE_PATH, enable_events=True, size=(35, 44), key='previous', background_color='black'),
        sg.Image(filename=PLAY_SONG_IMAGE_PATH, size=(64, 64), pad=(10, 0), enable_events=True, key='play', background_color='black'),
        sg.Image(filename=PAUSE_SONG_IMAGE_PATH, size=(58, 58), pad=(10, 0), enable_events=True, key='pause', background_color='black'),
        sg.Image(filename=GO_FORWARD_IMAGE_PATH, enable_events=True, size=(35, 44), pad=(10, 0), key='next', background_color='black'),
    ],
    [sg.Column(layout=currently_playing, justification='c', element_justification='c', background_color='black', pad=None)]
]

window = sg.Window('Spoti-Ninho', layout=main, size=(480, 730), background_color='black', finalize=True, grab_anywhere=True, resizable=False)

playlist_selecionada = None

while True:
    event, values = window.read(timeout=100)
    
    if event == sg.WIN_CLOSED:
        break
    
    elif event == 'play':
        if not playlist_selecionada or values['playlist_selecionada'] != playlist_selecionada:
            playlist_selecionada = values['playlist_selecionada']
            id_playlist = next((p[0] for p in playlists_usuario if p[1] == playlist_selecionada), None)
            if id_playlist:
                musicas_data = conexaoBD.consultarComParametros(
                    '''SELECT m.nome, m.artista, m.imagem, m.endereco FROM musicas m
                    INNER JOIN lista l ON m.id_musica = l.id_musica
                    WHERE l.id_playlist = %s''', 
                    (id_playlist,)
                )
                # Criação de objetos Musica a partir dos dados
                musicas = [Musica(nome, artista, imagem, endereco) for nome, artista, imagem, endereco in musicas_data]
            else:
                sg.popup("Playlist não encontrada.")
                musicas = []

        if musicas:
            Play_music(posic, musicas)
        else:
            sg.popup("Nenhuma música encontrada na playlist selecionada.")
    
    elif event == 'pause':
        if not musica_pausada:
            Iniciar.pausar()
            musica_pausada = True
        else:
            Iniciar.despausar()
            musica_pausada = False

    elif event == 'next':
        if musicas:
            posic = (posic + 1) % len(musicas)
            Play_music(posic, musicas)
        
    elif event == 'previous':
        if musicas:
            posic = (posic - 1) % len(musicas)
            Play_music(posic, musicas)

    if Iniciar and not musica_pausada and not pygame.mixer.music.get_busy():
        if musicas:
            posic = (posic + 1) % len(musicas)
            Play_music(posic, musicas)
        
window.close()
pygame.quit()