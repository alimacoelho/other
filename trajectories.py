import pyxel

class App:
    def __init__(self):
        pyxel.init(192, 108, title="Retângulos Animados (3x6)", fps=60)
        
        # Dimensões
        self.rect_largura = 10
        self.rect_altura = 7.5
        self.espacamento_x = 5
        self.espacamento_y = 5
        
        # Grid
        self.linhas = 3
        self.colunas = 6
        
        # Cores
        self.cores = [1, 2, 3, 4, 5, 6, 7, 8]
        
        # Animação
        self.y_bloco = - (self.linhas * (self.rect_altura + self.espacamento_y))  # Começa acima
        self.velocidade = 1.5
        self.estado = "DESCENDO"  # Pode ser: DESCENDO, SUBINDO, PARADO, CENTRALIZANDO
        self.tempo_parado = 0
        self.altura_total = self.linhas * (self.rect_altura + self.espacamento_y)
        
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.estado == "DESCENDO":
            self.y_bloco += self.velocidade
            
            # Verifica colisão com a parte inferior
            if self.y_bloco + self.altura_total >= pyxel.height:
                self.estado = "SUBINDO"
                
        elif self.estado == "SUBINDO":
            self.y_bloco -= self.velocidade
            
            # Verifica se chegou na posição central
            pos_central = (pyxel.height - self.altura_total) // 2
            if self.y_bloco <= pos_central:
                self.y_bloco = pos_central
                self.estado = "PARADO"
                self.tempo_parado = pyxel.frame_count
                
        elif self.estado == "PARADO":
            # Espera 5 segundos (300 frames)
            if pyxel.frame_count - self.tempo_parado > 300:
                self.estado = "DESCENDO"
                self.y_bloco = -self.altura_total  # Reinicia acima da tela

    def draw(self):
        pyxel.cls(0)
        
        # Desenha retângulos
        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                x = coluna * (self.rect_largura + self.espacamento_x) + (pyxel.width - (self.colunas * (self.rect_largura + self.espacamento_x))) // 2
                y = linha * (self.rect_altura + self.espacamento_y) + self.y_bloco
                cor = self.cores[(linha * self.colunas + coluna) % len(self.cores)]
                pyxel.rect(x, y, self.rect_largura, self.rect_altura, cor)
        
        # Mostra estado
        if self.estado == "PARADO":
            tempo_restante = 5 - (pyxel.frame_count - self.tempo_parado) // 60
            pyxel.text(5, 5, f"Recomeçando em: {max(0, tempo_restante)}s", 7)

App()
