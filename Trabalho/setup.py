from Conexao import Conexao

conexaoBD = Conexao("localhost", "root", "mysql", "")

conexaoBD.manipular("DROP DATABASE IF EXISTS spotninho")

conexaoBD.manipular("CREATE DATABASE spotninho")

conexaoBD.manipular("USE spotninho")

conexaoBD.manipular('''
    CREATE TABLE spotninho.usuario(
    id_usuario INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
    );
''')

conexaoBD.manipular('''
    CREATE TABLE spotninho.playlist(
        id_playlist INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        nome_playlist VARCHAR(255) NOT NULL,
        id_usuario INT NOT NULL,
        CONSTRAINT fk_idUsuario FOREIGN KEY(id_usuario) REFERENCES usuario(id_usuario)
    );
''')

conexaoBD.manipular('''
    CREATE TABLE spotninho.musicas(
        id_musica INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        duracao INT NOT NULL,
        artista VARCHAR(255) NOT NULL,
        genero VARCHAR(255) NOT NULL,
        imagem VARCHAR(255) NOT NULL,
        endereco VARCHAR(255) NOT NULL
    );
''')

conexaoBD.manipular('''
    CREATE TABLE spotninho.lista(
        id_lista INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        id_playlist INT NOT NULL,
        id_musica INT NOT NULL,
        CONSTRAINT fk_idplaylist FOREIGN KEY(id_playlist) REFERENCES playlist(id_playlist),
        CONSTRAINT fk_idmusica FOREIGN KEY(id_musica) REFERENCES musicas(id_musica)
    );
''')

conexaoBD.manipular('''
    INSERT INTO spotninho.musicas(artista, nome, genero, duracao, endereco, imagem) VALUES
    ("Maneskin", "Beggin", "Rock", 149, "rep_musicas/Beggin.mp3", "Images/Beggin.png"),
    ("Natanzinho", "Anjo Azul", "Sertanejo", 143, "rep_musicas/anjo.mp3", "Images/anjo.png"),
    ("Marília Mendonça (cover)", "Troco de calçada", "Sertanejo", 154, "rep_musicas/mm.mp3", "Images/MM.png"),
    ("Link Park", "In The End", "Eletrônica", 167, "rep_musicas/link_park.mp3", "Images/link.png"),
    ("Ikimono-gakari", "Blue Bird", "Anime", 250, "rep_musicas/Blue Bird.mp3", "Images/bluebird.png"),
    ("Delacruz", "Sunshine", "Hip Hop", 230, "rep_musicas/delacruz.mp3", "Images/sunshine (1).png"),
    ("Aaron Smith", "Dancin", "Internacional", 232, "rep_musicas/dj jefinho.mp3", "Images/dancin.png"),
    ("Legião Urbana", "Eduardo e Mônica", "Pop", 232, "rep_musicas/edem.mp3", "Images/images (1).png"),
    ("Maíara e Maraisa", "Medo bobo", "Sertanejo", 232, "rep_musicas/medo.mp3", "Images/medo.png"),
    ("Miranda Cosgrove", "Tema Icarly", "Pop", 232, "rep_musicas/icarly.mp3", "Images/icarly.png");
''')
