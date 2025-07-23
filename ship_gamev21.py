import pyxel
import random
import math


class AssetManager:
    """
    Centraliza o carregamento e o fornecimento de todos os dados de configuração
    e "assets" do jogo, como definições de sprites, inimigos e armas.
    No futuro, também poderá gerenciar o carregamento de imagens e sons.
    """
    def __init__(self):
        # --- DADOS DO PLAYER (Movido de Player.ANIMATION_FRAMES) ---
        self.player_animation_data = {
            'neutral': (0, 0),
            'left': [
                (11, 0), (22, 0), (33, 0), (41, 0)
            ],
            'right': [
                (33, 12), (22, 12), (11, 12), (0, 12)
            ]
        }

        # --- DADOS DOS INIMIGOS (Movido de Enemy.ANIMATION_DATA e Enemy.GLOW_SPRITE_DATA) ---
        self.enemy_animation_data = {
            'green':  [(50, 0), (50, 7)],
            'orange': [(57, 0), (57, 7)],
            'red':    [(64, 0), (64, 7)],
            'purple': [(57, 14), (57, 21)],
            'yellow': [(57, 36), (57, 43)],
            'blue':   [(50, 14), (50, 21)]
        }
        
        self.enemy_glow_data = {
            'green': {
                'high':   {'size': (12, 12), 'frames': [(70, 0), (84, 0)]},
                'medium': {'size': (10, 10), 'frames': [(99, 1), (113, 1)]},
                'low':    {'size': (8, 8),   'frames': [(127, 2), (138, 2)]}
            },
            'yellow': {
                'high':   {'size': (12, 12), 'frames': [(70, 12), (84, 12)]},
                'medium': {'size': (10, 10), 'frames': [(99, 13), (113, 13)]},
                'low':    {'size': (8, 8),   'frames': [(127, 14), (138, 14)]}
            },
            'orange': {
                'high':   {'size': (12, 12), 'frames': [(70, 24), (84, 24)]},
                'medium': {'size': (10, 10), 'frames': [(99, 25), (113, 25)]},
                'low':    {'size': (8, 8),   'frames': [(127, 26), (138, 26)]}
            },
            'blue': {
                'high':   {'size': (12, 12), 'frames': [(70, 36), (84, 36)]},
                'medium': {'size': (10, 10), 'frames': [(99, 37), (113, 37)]},
                'low':    {'size': (8, 8),   'frames': [(127, 38), (138, 38)]}
            },
            'purple': {
                'high':   {'size': (12, 12), 'frames': [(70, 48), (84, 48)]},
                'medium': {'size': (10, 10), 'frames': [(99, 49), (113, 49)]},
                'low':    {'size': (8, 8),   'frames': [(127, 50), (138, 50)]}
            },
            'red': {
                'high':   {'size': (12, 12), 'frames': [(70, 60), (84, 60)]},
                'medium': {'size': (10, 10), 'frames': [(99, 61), (113, 61)]},
                'low':    {'size': (8, 8),   'frames': [(127, 62), (138, 62)]}
            }
        }
        
        # --- DEFINIÇÕES GERAIS DO JOGO (Movido de Game) ---
        self.enemy_definitions = {
            'red': {'color': 4, 'health': 4},
            'purple': {'color': 8, 'health': 4},
            'blue': {'color': 2, 'health': 4},
            'green': {'color': 3, 'health': 4},
            'yellow': {'color': 15, 'health': 4},
            'orange': {'color': 5, 'health': 4},
            'asteroid': {'color': 4, 'health': 5}
        }
        
        self.movement_patterns = {
            'alien_grid_formation': {
                'type': 'simple_down',
                'speed_range': (0.3, 0.3)
            },
            'alien_galaga_entry': {
                'type': 'galaga_entry',
                'speed_down': 0.7,
                'horizontal_speed': 1.0,
                'ascend_speed': 0.8,
                'sin_amplitude': 40,
                'sin_freq_scale': 0.09
            },
            'alien_side_entry_align': {
                'type': 'side_entry_align',
                'horizontal_speed': 1.5,
                'y_center': 75,
                'sin_amplitude': 55,
                'sin_frequency': 0.033
            },
            'asteroid_slow_drift': {
                'type': 'asteroid',
                'dx_range': (-0.2, 0.2), 'dy_range': (0.1, 0.3), 'angular_speed_range': (-0.02, 0.02)
            },
            'asteroid_fast_fall': {
                'type': 'asteroid',
                'dx_range': (-0.1, 0.1), 'dy_range': (0.8, 1.2), 'angular_speed_range': (-0.05, 0.05)
            }
        }

        self.bullet_properties = {
            'standard': {'weapon_type': 'projectile', 'damage': 1, 'cooldown': 10, 'color': 7, 
                         'num_shots': 1, 'speed': 4, 'angles_deg': [-90], 'spread_deg': 0, 
                         'size': {'width': 1, 'height': 3}, 'behavior': None},

            'red': {'weapon_type': 'laser', 'damage_per_frame': 2 / 60, 'cooldown': 0, 'color': 4},

            'green': {'weapon_type': 'projectile', 'damage': 2, 'cooldown': 15, 'color': 3, 
                       'num_shots': 2, 'speed': 1.062, 'angles_deg': [-110.55, -69.45], 'spread_deg': 0,
                        'size': {'width': 2, 'height': 2}, 'behavior': {'type': 'boomerang', 'turn_speed': 0.04}},
            
            'blue': {
                'weapon_type': 'projectile', 'damage': 0.6, 'cooldown': 14, 'color': 2, 
                'num_shots': 3, 'speed': 4.5, 'angles_deg': [-105, -90, -75], 'spread_deg': 0, 
                'size': {'width': 2, 'height': 2}, 'behavior': None
            },
            
            'purple': {
                'weapon_type': 'projectile', 'damage': 4, 'cooldown': 0, 'color': 8,
                'num_shots': 1, 'speed': 8, 'angles_deg': [-90], 'spread_deg': 0,
                'size': {'width': 3, 'height': 5}, 
                'behavior': {'piercing': True},
                'charge_time': 45
            },
            
            'yellow': {'weapon_type': 'projectile', 'damage': 0.5, 'cooldown': 5, 'color': 15, 
                       'num_shots': 1, 'speed': 6, 'angles_deg': [-90], 'spread_deg': 10, 
                       'size': {'width': 1, 'height': 2}, 'behavior': None},
            
            'orange': {'weapon_type': 'projectile', 'damage': 4, 'cooldown': 30, 'color': 5, 
                       'num_shots': 1, 'angles_deg': [-90], 'spread_deg': 0, 'size': {'width': 4, 'height': 4}, 
                       'speed': 0, 'behavior': {'type': 'homing', 'homing_distance': 30, 'turn_speed': 0.1, 
                        'max_speed': 0.5, 'acceleration': 0.02, 'initial_angle_deg': -90}}
        }

        self.asteroid_sizes = {
            'small': 6,
            'medium': 12,
            'large': 24
        }

    # --- MÉTODOS DE ACESSO (GETTERS) ---
    # Fornecem uma interface limpa para outras classes obterem os dados.

    def get_player_animation_data(self):
        return self.player_animation_data

    def get_enemy_animation_data(self):
        return self.enemy_animation_data

    def get_enemy_glow_data(self):
        return self.enemy_glow_data

    def get_enemy_definitions(self):
        return self.enemy_definitions

    def get_movement_patterns(self):
        return self.movement_patterns

    def get_bullet_properties(self):
        return self.bullet_properties
    def get_asteroid_sizes(self):
        return self.asteroid_sizes



class BaseState:
    """
    Classe base para todos os estados do jogo. Define a interface comum.
    """
    def __init__(self, game):
        self.game = game # Cada estado terá uma referência ao objeto principal do jogo.
        self.name = "base"

    def enter(self):
        """Código a ser executado ao entrar neste estado."""
        pass

    def exit(self):
        """Código a ser executado ao sair deste estado."""
        pass

    def update(self):
        """Lógica de atualização do estado."""
        pass

    def draw(self):
        """Lógica de desenho do estado."""
        pass

class StateManager:
    """
    Gerencia a pilha de estados do jogo e as transições entre eles.
    """
    def __init__(self, game):
        self.game = game
        self.states = {}
        self.active_state = None

    def add_state(self, state):
        """Adiciona um estado ao dicionário de estados disponíveis."""
        self.states[state.name] = state

    def change_state(self, name):
        """Muda o estado ativo do jogo."""
        if self.active_state:
            self.active_state.exit()
        
        if name in self.states:
            self.active_state = self.states[name]
            self.active_state.enter()
        else:
            print(f"Erro: Estado '{name}' não encontrado.")


class PlayingState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.name = "playing"

    def update(self):
        


        if pyxel.btnp(pyxel.KEY_P):
                self.game.state_manager.change_state("paused")
                return # Retorna imediatamente para não processar o resto do frame


        self.game._update_wave_spawner()


 # --- LÓGICA DO SCREEN SHAKE ---
        if self.game.shake_duration > 0:
            self.game.shake_offset_x = pyxel.rndi(-self.game.shake_intensity, self.game.shake_intensity)
            self.game.shake_offset_y = pyxel.rndi(-self.game.shake_intensity, self.game.shake_intensity)
            self.game.shake_duration -= 1
        else:
            self.game.shake_offset_x = 0
            self.game.shake_offset_y = 0
        # --- FIM DA LÓGICA DO SCREEN SHAKE ---

        
        self.game.game_time = pyxel.frame_count // self.game.game_fps 

        # Lógica de ativação/desativação do boost
        if pyxel.btnp(pyxel.KEY_C) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X):
            self.game.is_boosting = not self.game.is_boosting
            if self.game.is_boosting: 
                self.game.boost_timer = self.game.boost_duration 
            else: 
                self.game.player.speed = self.game.player_base_speed 
        
        # Gerenciamento do timer de boost
        if self.game.is_boosting:
            self.game.player.speed = self.game.player_boost_speed 
            self.game.boost_timer -= 1
            if self.game.boost_timer <= 0: 
                self.game.is_boosting = False
                self.game.player.speed = self.game.player_base_speed 
        else:
            self.game.player.speed = self.game.player_base_speed 

        self.game.player.update() 

        # Regeneração de Energia (Adicionado)
        self.game.energy_recharge_timer += 1
        if self.game.energy_recharge_timer >= self.game.energy_recharge_rate:
            if self.game.player_energy < self.game.player_max_energy:
                self.game.player_energy += 1
            self.game.energy_recharge_timer = 0

        # Atualiza todas as partículas de fundo (estrelas e asteroides de fundo)
        for p in self.game.background_particles: p.update()
        for p in self.game.midground_particles: p.update()
        for p in self.game.foreground_particles: p.update()

        # Geração de partículas de rastro para a nave do jogador
        if self.game.is_boosting:
            min_dy, max_dy, num_particles, c1, c2 = 1.0, 2.0, 6, 8, 2  
            flame_size = 2 if random.random() < 0.4 else 1 
        else:
            min_dy, max_dy, num_particles, c1, c2 = 0.5, 1.0, 2, 4, 5 
            flame_size = 1
        
        flame_color = c1 if pyxel.frame_count % 4 < 2 else c2 
        flame_dx_offset = 0.5 if pyxel.btn(pyxel.KEY_LEFT) else -0.5 if pyxel.btn(pyxel.KEY_RIGHT) else 0

        for _ in range(num_particles):
            flame_x = self.game.player.x + pyxel.rndf(3, self.game.player.width - 4) #tamanho da chama
            # A chama é gerada na parte inferior da nave, com um pequeno deslocamento aleatório
            flame_y = self.game.player.y + self.game.player.height-1
            dx = pyxel.rndf(-0.5, 0.5) + flame_dx_offset
            dy = pyxel.rndf(min_dy, max_dy) 
            self.game.flame_particles.append(FlameParticle(flame_x, flame_y, dx, dy, flame_color, pyxel.rndi(5,15), flame_size))

        for p in self.game.flame_particles:
            p.update()
        # Depois, filtramos a lista
        self.game.flame_particles[:] = [p for p in self.game.flame_particles if p.lifetime > 0]

                # --- LÓGICA DE DISPARO ---
        enemies_destroyed_this_frame = []
        
        current_bullet_type_name = self.game.bullet_type_keys[self.game.current_bullet_type_index]
        props = self.game.asset_manager.get_bullet_properties()[current_bullet_type_name]
        self.game.is_laser_active = False 
        self.game.laser_draw_end_y = 0 
        self.game.laser_spark_point = None
        
        self.game.player.is_charging = False
        self.game.player.is_fully_charged = False

        if current_bullet_type_name == 'red':
            if pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A):
            # ### LÓGICA ADICIONADA ###
            # Capturamos o retorno do método _fire_laser.
                killed_enemy = self.game._fire_laser(props)
        # Se um inimigo foi retornado (ou seja, foi derrotado),
        # adiciona-o à nossa lista central de destruição.
                if killed_enemy:
                    enemies_destroyed_this_frame.append(killed_enemy)
        elif current_bullet_type_name == 'purple':
            if pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A):
                self.game.is_charging_weapon = True
                self.game.player.is_charging = True
                if self.game.charge_timer < props['charge_time']:
                    self.game.charge_timer += 1
                if self.game.charge_timer >= props['charge_time']:
                    self.game.player.is_fully_charged = True
            elif (pyxel.btnr(pyxel.KEY_Z) or pyxel.btnr(pyxel.GAMEPAD1_BUTTON_A)) and self.game.is_charging_weapon:
                if self.game.charge_timer >= props['charge_time']:
                    self.game._fire_projectiles(props)
                self.game.is_charging_weapon = False
                self.game.charge_timer = 0
            else:
                self.game.is_charging_weapon = False
                self.game.charge_timer = 0
        # --- START REPLACEMENT HERE ---
        else: # This handles 'yellow' and any other projectile types that are not red/purple
            if pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A):
                # Simple cooldown check for regular projectiles
                is_ready_to_fire = (pyxel.frame_count - self.game.last_shot_frame[current_bullet_type_name] >= props['cooldown'])
                
                if is_ready_to_fire:
                    if self.game._fire_projectiles(props): # This will now always return True
                        self.game.last_shot_frame[current_bullet_type_name] = pyxel.frame_count

                                
        if pyxel.btnp(pyxel.KEY_X) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            self.game.current_bullet_type_index = (self.game.current_bullet_type_index + 1) % len(self.game.bullet_type_keys)
            self.game.yellow_burst_count = 0

        if pyxel.btnp(pyxel.KEY_V) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y):
            self.game.current_enemy_category = 'asteroids' if self.game.current_enemy_category == 'aliens' else 'aliens'
            # Limpa tudo para a transição
            self.game.enemies.clear()
            self.game.enemies_to_spawn.clear()
            # Reseta para a onda 1 da nova categoria e a prepara
            self.game.wave_number = 1
            self.game._setup_wave()
            self.game.game_state = 'playing'


        if pyxel.btnp(pyxel.KEY_G):
            self.game.glow_mode = (self.game.glow_mode + 1) % 5

        # Atualiza todos os inimigos
        for enemy in self.game.enemies: 
            new_bullet = enemy.update(self.game.player)
            if new_bullet:
                self.game.enemy_bullets.append(new_bullet)


        # Tecla 'C' para forçar a próxima onda.
        if pyxel.btnp(pyxel.KEY_C):
            self.game.enemies.clear()
            self.game.enemies_to_spawn.clear()
            self.game.wave_spawn_timer = self.game.wave_spawn_delay # Força a transição imediata

        # --- SEÇÃO DE COLISÃO DE BALAS E PROCESSAMENTO DE DESTRUIÇÃO ---
        bullets_to_keep = []
        
        
        for bullet in self.game.bullets:
            if bullet.state == 'seeking' and not bullet.target_enemy:
                closest_enemy, min_dist_sq = None, float('inf')
                for enemy in self.game.enemies:
                    if not isinstance(enemy, Asteroid): 
                        dist_sq = ((enemy.x + enemy.width / 2) - bullet.x)**2 + ((enemy.y + enemy.height / 2) - bullet.y)**2
                        if dist_sq < min_dist_sq:
                            min_dist_sq, closest_enemy = dist_sq, enemy
                if closest_enemy and min_dist_sq <= bullet.homing_distance_sq:
                    bullet.target_enemy, bullet.state = closest_enemy, 'homing'
            
            bullet.update() 
            
            bullet_should_be_removed = False
            for enemy in self.game.enemies:
                collided = False
                if isinstance(enemy, Asteroid):
                    # Para asteroides, usamos a verificação precisa de polígono.
                    # Pegamos o centro da bala como o ponto a ser verificado.
                    bullet_center_x = bullet.x + bullet.width / 2
                    bullet_center_y = bullet.y + bullet.height / 2
                    if self.game._is_point_in_polygon(bullet_center_x, bullet_center_y, enemy.get_rotated_vertices()):
                        collided = True
                else:
                    # Para inimigos normais (não rotacionados), o AABB é eficiente e correto.
                    if self.game._check_aabb_collision(bullet.x, bullet.y, bullet.width, bullet.height, enemy.x, enemy.y, enemy.width, enemy.height):
                        collided = True

                if collided:
                    # Gera faíscas de impacto toda vez que uma colisão é detectada.
                    self.game.create_hit_sparks(bullet.x, bullet.y, bullet.color)

                    if not bullet.behavior.get('piercing', False):
                        bullet_should_be_removed = True

                    damage_to_deal = bullet.damage
                    if bullet.type == enemy.type and bullet.type != 'standard':
                        damage_to_deal *= 2
                    if isinstance(enemy, Asteroid) and bullet.type == 'orange':
                        damage_to_deal *= 1.5

                    if enemy.take_damage(damage_to_deal): 
                        enemies_destroyed_this_frame.append(enemy) 
                        self.game.score += 1 
                    
                    if bullet_should_be_removed:
                        break 
            
            if bullet.y > -bullet.height and not bullet_should_be_removed:
                bullets_to_keep.append(bullet)
        
        self.game.bullets = bullets_to_keep 

        # --- Processa os inimigos destruídos e cria as explosões ---
        newly_destroyed_enemies = [e for e in self.game.enemies if e in enemies_destroyed_this_frame]
        new_fragments = []
        for enemy in newly_destroyed_enemies:
            if isinstance(enemy, Asteroid):
                # Primeiro, tentamos partir o asteroide e guardamos os fragmentos.
                fragments = enemy.shatter()
                
                # Agora, verificamos se ele realmente se partiu.
                if fragments:
                    # SE SIM (era grande/médio), usamos o novo efeito SUTIL de poeira.
                    self.game.create_shatter_effect(enemy)
                    # E adicionamos os novos fragmentos ao jogo.
                    new_fragments.extend(fragments)
                else:
                    # SE NÃO (era pequeno), usamos a explosão FINAL e intensa.
                    self.game.create_asteroid_debris_explosion(enemy)
            else:
                # Inimigos normais continuam usando a explosão de pixel debris.
                self.game.create_pixel_explosion(enemy)
        
        # Atualiza a lista de inimigos, removendo os destruídos e adicionando fragmentos
        self.game.enemies = [e for e in self.game.enemies if e not in newly_destroyed_enemies] + new_fragments

        enemy_bullets_to_keep = []
        for bullet in self.game.enemy_bullets:
            bullet.update()
            
            collided_with_player = False
            # Verifica a colisão apenas se o jogador estiver vivo e sem invencibilidade.
            if self.player.is_alive and self.player.invincibility_timer == 0:
                if self.game._check_aabb_collision(bullet.x, bullet.y, bullet.width, bullet.height,
                                            self.player.x, self.player.y, self.player.width, self.player.height):
                    
                    collided_with_player = True
                    self.player_hp -= 10 # Player toma 10 de dano
                    self.game.trigger_screen_shake(duration=15, intensity=2) # Ativa o shake
                    
                    # Cria faíscas no jogador quando atingido.
                    self.game.create_hit_sparks(self.game.player.x + self.game.player.width / 2, self.game.player.y + self.game.player.height / 2, bullet.color)

                    if self.game.player_hp <= 0:
                        self.game.player_lives -= 1
                        if self.game.player_lives <= 0:
                            self.game.player.is_alive = False
                            self.game.state_manager.change_state("game_over")
                        else:
                            self.game.player_hp = self.game.player_max_hp # Reseta HP ao perder uma vida
                            self.game.player.take_damage() # Ativa invencibilidade
                    else: # Se o HP ainda está acima de zero
                        self.game.player.take_damage() # Ativa a invencibilidade temporária.
            
            # Mantém a bala se ela não atingiu o jogador e ainda está na tela.
            if not collided_with_player and bullet.y < pyxel.height and bullet.y > -bullet.height:
                enemy_bullets_to_keep.append(bullet)
                
        self.game.enemy_bullets = enemy_bullets_to_keep

        # --- FIM DA SEÇÃO DE COLISÃO DE BALAS ---

        # Atualiza e remove partículas de explosão/detritos
        self.game.particles[:] = [p for p in self.game.particles if p.update()]

        # --- SEÇÃO DE COLISÃO JOGADOR-INIMIGO ---
        if self.game.player.is_alive and self.game.player.invincibility_timer == 0:
            enemies_collided_with_player = []
            
            # Define os vértices do retângulo do jogador uma vez
            px, py = self.game.player.x, self.game.player.y
            pw, ph = self.game.player.width, self.game.player.height
            player_vertices = [(px, py), (px + pw, py), (px + pw, py + ph), (px, py + ph)]

            for enemy in self.game.enemies:
                collided = False
                if isinstance(enemy, Asteroid):
                    # Para asteroides, usamos a colisão precisa de polígonos
                    asteroid_vertices = enemy.get_rotated_vertices()
                    if self.game._check_polygon_collision(player_vertices, asteroid_vertices):
                        collided = True
                else:
                    # Para inimigos normais, AABB é suficiente e mais rápido
                    if self.game._check_aabb_collision(px, py, pw, ph, enemy.x, enemy.y, enemy.width, enemy.height):
                        collided = True
                
                if collided:
                    enemies_collided_with_player.append(enemy)

            if enemies_collided_with_player:
                self.game.player_hp -= 25 # Dano de colisão direta (maior)
                self.game.trigger_screen_shake(duration=20, intensity=3) # Shake mais forte

                # Para cada inimigo que colidiu, cria sua respectiva explosão
                for enemy in enemies_collided_with_player:
                    if isinstance(enemy, Asteroid):
                        self.game.create_asteroid_debris_explosion(enemy)
                        self.game.score += 0.5 
                    else:
                        self.game.create_pixel_explosion(enemy)
                        self.game.score += 1 

                # Remove os inimigos que colidiram
                self.game.enemies = [e for e in self.game.enemies if e not in enemies_collided_with_player]
                
                if self.game.player_hp <= 0:
                    self.game.player_lives -= 1
                    if self.game.player_lives <= 0:
                        self.game.player.is_alive = False
                        self.game.state_manager.change_state("game_over")
                    else:
                        self.game.player_hp = self.game.player_max_hp
                        self.game.player.take_damage()
                else:
                    self.game.player.take_damage()        # --- FIM DA SEÇÃO DE COLISÃO JOGADOR-INIMIGO ---

        # Remove inimigos que saíram da tela ou foram destruídos
        self.game.enemies[:] = [e for e in self.game.enemies if e.health > 0 and e.y < pyxel.height and e.x < pyxel.width and e.x + e.width > 0]

        # Lógica de gerenciamento de ondas
        self.game._update_wave_spawner()

        # Atualiza e coleta power-ups
        powerups_to_keep = []
        for p in self.game.powerups:
            p.update()
            if self.game._check_aabb_collision(self.player.x, self.player.y, self.player.width, self.player.height, p.x, p.y, p.width, p.height):
                if p.type == 'boost':
                    self.game.is_boosting, self.game.boost_timer = True, self.game.boost_duration 
            elif p.y < pyxel.height: 
                powerups_to_keep.append(p)
        self.game.powerups = powerups_to_keep


        pass

    def draw(self):
        # A MAIORIA DO CÓDIGO DO Game.draw() VEM PARA CÁ.
                # Aplica o offset do shake ANTES de limpar a tela e desenhar o fundo
        pyxel.camera(self.game.shake_offset_x, self.game.shake_offset_y)

        pyxel.cls(0) # Fundo da tela: Preto (0)
        # 1. Desenha as camadas de fundo
        for p in self.game.background_particles: p.draw()
        for p in self.game.midground_particles: p.draw()
        for p in self.game.foreground_particles: p.draw()
        
        # 2. Desenha os objetos principais do jogo
        self.game.player.draw() 
        for e in self.game.enemies: e.draw(self.game.glow_mode) # Passa o modo de glow para os inimigos
        for p in self.game.powerups: p.draw()

        # 3. Desenha os efeitos e projéteis por cima dos objetos
        for p in self.game.flame_particles: p.draw()
        if self.game.is_laser_active: 
            laser_x = self.game.player.x + (self.game.player.width // 2)
            pyxel.line(laser_x, self.game.player.y, laser_x, self.game.laser_draw_end_y, 4) 
        for b in self.game.bullets: b.draw()
        for b in self.game.enemy_bullets: b.draw() # Desenha as balas dos inimigos.
        
        ### CORREÇÃO: A LINHA ABAIXO FOI MOVIDA PARA DEPOIS DE DESENHAR OS INIMIGOS ###
        # Agora as partículas de explosão são desenhadas por cima de tudo.
        for p in self.game.particles: p.draw() 

        # Reseta a câmera para desenhar elementos da UI que NÃO DEVEM tremer
        pyxel.camera(0, 0)

        # 4. Desenha a Interface do Usuário (HUD), que sempre fica na camada mais alta
        self.game.hud.draw()
        pass

# ADICIONE ESTA NOVA CLASSE
class PausedState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.name = "paused"

    def update(self):
        # Apenas verifica a tecla para despausar.
        if pyxel.btnp(pyxel.KEY_P):
            # Usa o StateManager para voltar ao estado de jogo.
            self.game.state_manager.change_state("playing")

    def draw(self):
        # Primeiro, desenha a tela do jogo como ela estava.
        self.game.playing_state.draw()
        
        # Depois, desenha a sobreposição de pausa por cima.
        pyxel.bltm(0, 0, 0, 0, 126, pyxel.width, pyxel.height, 0)
        text = "PAUSED"
        text_x = (pyxel.width - len(text) * 4) / 2
        pyxel.text(text_x, 60, text, 7)

# ADICIONE ESTA NOVA CLASSE
class GameOverState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.name = "game_over"

    def update(self):
        # Apenas verifica a tecla para reiniciar.
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
            self.game.restart_game()

    def draw(self):
        # Desenha a tela final do jogo.
        self.game.playing_state.draw()
        
        # Desenha a mensagem "GAME OVER" por cima.
        text = "GAME OVER"
        text_x = (pyxel.width - len(text) * 4) / 2
        pyxel.text(text_x, 50, text, 15)
        
        prompt = "PRESS SPACE TO RESTART"
        prompt_x = (pyxel.width - len(prompt) * 4) / 2
        if pyxel.frame_count % 30 < 20:
            pyxel.text(prompt_x, 60, prompt, 7)
    



class Player:
    # --- CONSTANTES DE ANIMAÇÃO ---
    # Velocidade da animação. Número de frames do jogo por quadro de animação.
    # Menor valor = animação mais rápida.
    ANIMATION_SPEED = 3

    # Dicionário com as coordenadas (u, v) de todos os frames da animação na folha de sprites.
    # Organizar os dados assim deixa o código mais limpo e fácil de entender.


    SPRITE_BANK = 0  # A "folha" ou Image Bank onde os sprites estão
    SPRITE_W = 9     # Largura (width) do sprite
    SPRITE_H = 9     # Altura (height) do sprite
    
    def __init__(self, x, y,asset_manager):
        self.x = x
        self.y = y
        self.asset_manager = asset_manager
        self.animation_data = self.asset_manager.get_player_animation_data()
        self.width = self.SPRITE_W 
        self.height = self.SPRITE_H 
        self.speed = 1 
        
        self.tilt_level = 0
        self.animation_timer = 0
        
        self.is_charging = False
        self.is_fully_charged = False

        # --- NOVAS VARIÁVEIS DE ESTADO ---
        self.is_alive = True
        # Timer para invencibilidade (120 frames = 2 segundos a 60fps)
        self.invincibility_timer = 0
        self.INVINCIBILITY_DURATION = 120

    def take_damage(self):
        """Ativa o estado de invencibilidade do jogador."""
        self.invincibility_timer = self.INVINCIBILITY_DURATION

    def update(self):
        # Decrementa o timer de invencibilidade se estiver ativo.
        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1

        # A lógica de movimento e animação só ocorre se o jogador estiver vivo.
        if not self.is_alive:
            return

        # --- LÓGICA DE MOVIMENTO ---
        # Mover para a esquerda
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.x = max(0, self.x - self.speed)
        # Mover para a direita
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.x = min(pyxel.width - self.width, self.x + self.speed)
        # Mover para cima
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            self.y = max(0, self.y - self.speed)
        # Mover para baixo
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            self.y = min(pyxel.height - self.height, self.y + self.speed)

        # --- LÓGICA DE ANIMAÇÃO DE INCLINAÇÃO ---
        
        # 1. Determinar o estado alvo da inclinação com base no input do jogador.
        target_tilt = 0
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            target_tilt = -4  # Alvo: inclinação máxima para a esquerda
        elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            target_tilt = 4   # Alvo: inclinação máxima para a direita

        # 2. Controlar o tempo da animação.
        self.animation_timer += 1
        if self.animation_timer >= self.ANIMATION_SPEED:
            self.animation_timer = 0
            
            # 3. Mover o nível de inclinação atual em direção ao alvo.
            if self.tilt_level < target_tilt:
                self.tilt_level += 1
            elif self.tilt_level > target_tilt:
                self.tilt_level -= 1

    def draw(self):
        # Se o jogador não estiver vivo, não desenha nada.
        if not self.is_alive:
            return
            
        ### CORREÇÃO: LÓGICA DE PISCAR ADICIONADA AQUI ###
        # Se o jogador estiver invencível, a nave pisca.
        if self.invincibility_timer > 0:
            # Em frames pares, pulamos o desenho para criar o efeito de piscar.
            if pyxel.frame_count % 2 == 0:
                return 

        # --- LÓGICA DE FEEDBACK VISUAL DE CARREGAMENTO (existente) ---
        center_x = self.x + self.width / 2 -1
        center_y = self.y + self.height / 2
        
        if self.is_fully_charged:
            pulse = math.sin(pyxel.frame_count * 0.4) * 1.5 
            radius = 7 + pulse
            color = 10 if pyxel.frame_count % 10 < 5 else 6
            pyxel.circb(center_x, center_y, radius, color)
        elif self.is_charging:
            pulse = math.sin(pyxel.frame_count * 0.3) 
            radius = 6 + pulse
            color = 10 if pyxel.frame_count % 12 < 6 else 9
            pyxel.circb(center_x, center_y, radius, color)

        # --- LÓGICA DE DESENHO DA NAVE (existente) ---
        u, v = self.animation_data['neutral'] 

        if self.tilt_level < 0:
            frame_index = abs(self.tilt_level) - 1
            u, v = self.animation_data['left'][frame_index]
        elif self.tilt_level > 0:
            frame_index = self.tilt_level - 1
            u, v = self.animation_data['right'][frame_index]

        pyxel.blt(self.x, self.y, self.SPRITE_BANK, u, v, self.SPRITE_W, self.SPRITE_H, 0)

class Bullet:
    def __init__(self, x, y, color, type, dx, dy, damage, height, width=1, 
             behavior=None, particle_list=None, owner='player'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color 
        self.type = type
        self.damage = damage
        
        # --- CORREÇÃO APLICADA AQUI ---
        # Armazena o dicionário de comportamento na instância da bala.
        # O 'or {}' garante que self.behavior seja sempre um dicionário, evitando erros.
        self.behavior = behavior or {}

        self.dx = dx
        self.dy = dy
        self.speed = math.hypot(dx, dy)
        self.angle = math.atan2(dy, dx)
        self.particle_list = particle_list
        self.owner = owner
    
 

        self.state = None
        self.target_enemy = None

        # A lógica agora usa o atributo da instância (self.behavior) que acabamos de salvar.
        if self.behavior:
            if self.behavior.get('type') == 'boomerang':
                self.state = 'straight'
                self.y_initial = self.y
                self.initial_dx = dx
                self.return_angle = math.atan2(-dy, -dx)
                self.return_dy = self.speed * math.sin(self.return_angle)
                turn_speed = self.behavior.get('turn_speed', 0.04)
                self.angular_velocity = turn_speed * -math.copysign(1, dx)
            
            elif self.behavior.get('type') == 'homing':
                self.state = 'launching'
                self.max_speed = self.behavior.get('max_speed', 0.5)
                self.acceleration = self.behavior.get('acceleration', 0.02)
                self.speed = 0
                self.dx = 0
                self.dy = 0
                self.angle = math.radians(self.behavior.get('initial_angle_deg', -90))
                self.homing_distance_sq = self.behavior.get('homing_distance', 30) ** 2
                self.homing_turn_speed = self.behavior.get('turn_speed', 0.1)

    def update(self):
        # Lógica de atualização para balas com comportamento 'boomerang'
        if self.state == 'straight':
            # Se a bala alcançou a distância de retorno, muda para 'curving'
            if abs(self.y - self.y_initial) >= 60:
                self.state = 'curving'
        elif self.state == 'curving':
            # Ajusta o ângulo da bala para iniciar a curva
            self.angle += self.angular_velocity
            # Se a bala começou a "voltar" o suficiente, muda para 'returning'
            if self.dy >= self.return_dy:
                self.state = 'returning'
                self.angle = self.return_angle # Trava o ângulo para o retorno direto
        
        # Lógica de atualização para balas com comportamento 'homing'
        elif self.state == 'launching':
            # Acelera a bala até a velocidade máxima
            self.speed = min(self.max_speed, self.speed + self.acceleration)
            # Quando atinge a velocidade máxima, muda para 'seeking' (procurando alvo)
            if self.speed >= self.max_speed:
                self.state = 'seeking'
        
        elif self.state == 'seeking' or self.state == 'lost_target':
            # O estado 'seeking' tem sua lógica de detecção de alvo no Game.update()
            # 'lost_target' significa que a bala perdeu o alvo e continua em linha reta
            pass

        elif self.state == 'homing':
            # Se há um inimigo alvo e ele ainda está vivo
            if self.target_enemy and self.target_enemy.health > 0:
                # Calcula o ângulo para o centro do inimigo alvo
                target_angle = math.atan2((self.target_enemy.y + self.target_enemy.height / 2) - self.y, 
                                          (self.target_enemy.x + self.target_enemy.width / 2) - self.x)
                # Calcula a diferença de ângulo, normalizando para o menor caminho
                angle_diff = (target_angle - self.angle + math.pi) % (2 * math.pi) - math.pi
                # Limita a quantidade de giro por frame
                turn_amount = max(-self.homing_turn_speed, min(self.homing_turn_speed, angle_diff))
                self.angle += turn_amount # Aplica o giro
            else:
                self.state = 'lost_target' # Se o alvo não existe ou está morto, a bala perde o alvo

        # Se a bala tem um estado de movimento especial, recalcula dx e dy
        if self.state is not None:
            self.dx = self.speed * math.cos(self.angle)
            self.dy = self.speed * math.sin(self.angle)

        # Geração de rastro de chama para balas do tipo 'orange' (míssil teleguiado)
        if self.type == 'orange' and self.state in ['launching', 'seeking', 'homing', 'lost_target']:
            for _ in range(2):
                rastro_color = 4 if pyxel.frame_count % 4 < 2 else 15 
                back_x = self.x - 1.5 * math.cos(self.angle)
                back_y = self.y - 1.5 * math.sin(self.angle)
                particle_dx = -self.dx * 1.2 + pyxel.rndf(-0.5, 0.5)
                particle_dy = -self.dy * 1.2 + pyxel.rndf(-0.5, 0.5)
                self.particle_list.append(FlameParticle(back_x, back_y, particle_dx, particle_dy, rastro_color, pyxel.rndi(6, 12)))

        # Atualiza a posição da bala
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        # Desenha a bala 'orange' como uma linha
        if self.type == 'orange' and self.state is not None:
            nose_x = self.x + 1.5 * math.cos(self.angle)
            nose_y = self.y + 1.5 * math.sin(self.angle)
            tail_x = self.x - 1.5 * math.cos(self.angle)
            tail_y = self.y - 1.5 * math.sin(self.angle)
            pyxel.line(tail_x, tail_y, nose_x, nose_y, self.color)
        # Desenha outras balas como retângulos simples
        else:
            pyxel.rect(self.x, self.y, self.width, self.height, self.color)


class ExplosionParticle:
    def __init__(self, x, y, dx, dy, color, lifetime):
        self.x = x
        self.y = y
        self.dx = dx 
        self.dy = dy 
        self.color = color
        self.lifetime = lifetime # Tempo de vida da partícula em frames

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1
        return self.lifetime > 0 # Retorna se a partícula ainda está viva

    def draw(self):
        pyxel.pset(self.x, self.y, self.color)


class PixelDebrisParticle:
    """Representa um único pixel que se desprende de um inimigo destruído."""
    def __init__(self, x, y, color, dx, dy, lifetime, friction=0.98):
        self.x = x
        self.y = y
        self.color = color
        self.dx = dx
        self.dy = dy
        self.lifetime = lifetime
        self.friction = friction # Fator de desaceleração (atrito do "espaço")

    def update(self):
        self.x += self.dx
        self.y += self.dy
        
        # Aplica o atrito para desacelerar a partícula
        self.dx *= self.friction
        self.dy *= self.friction
        
        self.lifetime -= 1
        return self.lifetime > 0

    def draw(self):
        pyxel.pset(self.x, self.y, self.color)


class Enemy:
    # --- CONSTANTES DE ANIMAÇÃO E SPRITE ---
    # Velocidade da animação. Número de frames do jogo por quadro de animação.
    ANIMATION_SPEED = 25 
    SPRITE_BANK = 0  # Folha de imagem onde os sprites estão
    SPRITE_W = 6     # Largura do sprite do inimigo
    SPRITE_H = 6     # Altura do sprite do inimigo

    # A matriz SPRITE_DATA foi removida.

    def __init__(self, x, y, type, color, health, movement_pattern, asset_manager, game_particles_list=None, **kwargs):

        self.x = x
        self.y = y
        self.type = type 
        self.color = color
        self.health = health
        self.game_particles_list = game_particles_list 
        self.asset_manager = asset_manager
        self.animation_data = self.asset_manager.get_enemy_animation_data()
        self.glow_sprite_data = self.asset_manager.get_enemy_glow_data()
        self.width = self.SPRITE_W 
        self.height = self.SPRITE_H
        self.movement_pattern = movement_pattern
        self.pattern_type = movement_pattern.get('type', 'simple_down')
        
        # Variáveis de estado
        self.state = 'spawning' # Estado inicial padrão
        self.state_timer = 0

        # Inicialização baseada no tipo de padrão
        if self.pattern_type == 'simple_down':
            speed_min, speed_max = movement_pattern.get('speed_range', (0.5, 0.5))
            self.speed = pyxel.rndf(speed_min, speed_max)
        
        elif self.pattern_type == 'galaga_entry':
            self.state = 'DESCENDING_SIN'
            self.y_start = y
            self.x = 64 - (self.width / 2) # Sempre começa no centro
            # Pega os parâmetros do dicionário de argumentos extras (**kwargs)
            self.final_x = kwargs.get('final_x')
            self.final_y = kwargs.get('final_y')
        
        elif self.pattern_type == 'side_entry_align':
            self.state = 'ENTERING_WAVE'
            self.direction = kwargs.get('direction', 1)
            if self.direction == 1: self.x = -self.width
            else: self.x = 128
            self.final_x = kwargs.get('final_x')
            self.final_y = kwargs.get('final_y')


        self.animation_frame_index = 0
        self.animation_timer = pyxel.rndi(0, self.ANIMATION_SPEED)
        self.shoot_cooldown = pyxel.rndi(120, 240) # Aumentado para ser menos caótico
        self.last_shot_frame = pyxel.frame_count

    def _update_simple_down(self):
        self.y += self.speed



    def shoot(self, player_x, player_y):
        """Cria e retorna uma bala direcionada à posição do jogador."""
        # Calcula o ângulo do centro do inimigo para o centro do jogador.
        enemy_center_x = self.x + self.width / 2
        enemy_center_y = self.y + self.height / 2
        player_center_x = player_x + Player.SPRITE_W / 2
        player_center_y = player_y + Player.SPRITE_H / 2
        
        angle = math.atan2(player_center_y - enemy_center_y, player_center_x - enemy_center_x)
        
        # Define as propriedades da bala.
        speed = 1.0 # Bala lenta
        color = 15 if pyxel.frame_count % 10 < 5 else 14 # Efeito de piscar amarelo
        size = 2
        
        # Calcula os vetores de movimento.
        dx = speed * math.cos(angle)
        dy = speed * math.sin(angle)
        
        # Cria a instância da bala, especificando que o 'owner' é 'enemy'.
        new_bullet = Bullet(enemy_center_x, enemy_center_y, color, 'enemy_shot', dx, dy, 1, size, size, owner='enemy')
        return new_bullet



    def _update_galaga_entry(self):
        pattern = self.movement_pattern
        if self.state == 'DESCENDING_SIN':
            sin_phase = (self.y - self.y_start) * pattern['sin_freq_scale']
            self.x = 64 + math.sin(sin_phase) * pattern['sin_amplitude'] - (self.width / 2)
            self.y += pattern['speed_down']
            
            if self.y >= self.final_y - 20: # Ponto de início da curva horizontal
                self.state = "MOVING_HORIZONTAL"

        elif self.state == "MOVING_HORIZONTAL":
            if self.x < self.final_x:
                self.x = min(self.x + pattern['horizontal_speed'], self.final_x)
            elif self.x > self.final_x:
                self.x = max(self.x - pattern['horizontal_speed'], self.final_x)
            
            if abs(self.x - self.final_x) < 1:
                self.x = self.final_x
                self.state = "ASCENDING"

        elif self.state == "ASCENDING":
            self.y -= pattern['ascend_speed']
            if self.y <= self.final_y:
                self.y = self.final_y
                self.state = "HALTED"

    def _update_side_entry_align(self):
        pattern = self.movement_pattern
        if self.state == 'ENTERING_WAVE':
            self.x += pattern['horizontal_speed'] * self.direction
            sin_phase = self.x * pattern['sin_frequency']
            self.y = pattern['y_center'] + math.sin(sin_phase) * pattern['sin_amplitude']

            # Condição de transição para alinhamento (ex: quando cruza o centro da tela)
            if (self.direction == 1 and self.x > 64) or \
            (self.direction == -1 and self.x < 64):
                self.state = 'ALIGNING'
        
        elif self.state == 'ALIGNING':
            # Interpolação suave para as posições finais
            target_dx = self.final_x - self.x
            target_dy = self.final_y - self.y
            self.x += target_dx * 0.05
            self.y += target_dy * 0.05

            if abs(target_dx) < 1 and abs(target_dy) < 1:
                self.x, self.y = self.final_x, self.final_y
                self.state = 'HALTED'

    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0 

    def update(self, player=None):
        # Roteador de movimento
        if self.pattern_type == 'simple_down':
            self._update_simple_down()
        elif self.pattern_type == 'galaga_entry':
            self._update_galaga_entry()
        elif self.pattern_type == 'side_entry_align':
            self._update_side_entry_align()

        # Animação do sprite (funciona para todos)
        self.animation_timer += 1
        if self.animation_timer >= self.ANIMATION_SPEED:
            self.animation_timer = 0
            self.animation_frame_index = 1 - self.animation_frame_index
        
        # Lógica de tiro (só atira quando parado)
        if self.state == 'HALTED' and self.type == 'yellow' and player:
            if pyxel.frame_count - self.last_shot_frame > self.shoot_cooldown:
                self.last_shot_frame = pyxel.frame_count
                return self.shoot(player.x, player.y)
        
        return None
            
    def draw(self, glow_mode=0):
        """
        Desenha o inimigo usando sprites de brilho com múltiplos tamanhos,
        mantendo a hitbox lógica de 6x6.
        """
        has_glow_sprites = self.type in self.glow_sprite_data
        
        if glow_mode == 0 or not has_glow_sprites:
            frames = self.animation_data[self.type]
            u, v = frames[self.animation_frame_index]
            pyxel.blt(self.x, self.y, self.SPRITE_BANK, u, v, self.SPRITE_W, self.SPRITE_H, 0)
            return

        # --- LÓGICA PARA 5 ESTADOS DE BRILHO ---
        
        # 1. Mapeia o glow_mode para o estado de brilho ('low', 'medium', 'high').
        if glow_mode == 1:
            glow_state_to_draw = 'low'
        elif glow_mode == 2:
            glow_state_to_draw = 'medium'
        elif glow_mode == 3:
            glow_state_to_draw = 'high'
        elif glow_mode == 4: # Modo Pulsante (alterna entre médio e alto)
            if pyxel.frame_count % 60 < 30:
                glow_state_to_draw = 'high'
            else:
                glow_state_to_draw = 'medium'
        
        # 2. Pega as propriedades do sprite de brilho correto.
        sprite_props = self.glow_sprite_data[self.type][glow_state_to_draw]
        glow_w, glow_h = sprite_props['size']
        u, v = sprite_props['frames'][self.animation_frame_index]

        # 3. Calcula o offset para centralizar.
        offset_x = (self.SPRITE_W - glow_w) / 2
        offset_y = (self.SPRITE_H - glow_h) / 2

        # 4. Calcula a posição final.
        draw_x = self.x + offset_x
        draw_y = self.y + offset_y

        # 5. Desenha o sprite de brilho.
        pyxel.blt(draw_x, draw_y, self.SPRITE_BANK, u, v, glow_w, glow_h, 0)



class Asteroid(Enemy):
    def __init__(self, x, y, size_type, movement_pattern, asset_manager, initial_dx=None, initial_dy=None, game_particles_list=None):
        asteroid_color = 4 
        self.size_type = size_type
        if self.size_type == 'small':
            self.base_size, asteroid_health, self.num_vertices, self.irregularity = 6, 2, pyxel.rndi(5, 7), 2.0
        elif self.size_type == 'medium':
            self.base_size, asteroid_health, self.num_vertices, self.irregularity = 12, 5, pyxel.rndi(7, 9), 3.5
        elif self.size_type == 'large':
            self.base_size, asteroid_health, self.num_vertices, self.irregularity = 24, 10, pyxel.rndi(9, 12), 5.0
        
        # Armazena o padrão para que os fragmentos (shatter) possam usá-lo também.
        self.movement_pattern = movement_pattern
        
        # Chama o construtor da classe base, passando o padrão de movimento.
        super().__init__(x, y, 'asteroid', asteroid_color, asteroid_health, movement_pattern, asset_manager, game_particles_list)
        # --- MUDANÇA PRINCIPAL: USA OS VALORES DO PADRÃO ---
        dx_min, dx_max = movement_pattern['dx_range']
        dy_min, dy_max = movement_pattern['dy_range']
        as_min, as_max = movement_pattern['angular_speed_range']

        self.dx = initial_dx if initial_dx is not None else pyxel.rndf(dx_min, dx_max)
        self.dy = initial_dy if initial_dy is not None else pyxel.rndf(dy_min, dy_max)
        self.angular_speed = pyxel.rndf(as_min, as_max)
        self.rotation = pyxel.rndf(0, math.pi * 2)

        self._generate_vertices()

    def _generate_vertices(self):
        # Lógica de geração de vértices similar à classe Asteroid
        self.vertices = []
        angle_step = (2 * math.pi) / self.num_vertices # Ângulo entre os vértices para um polígono regular
        
        for i in range(self.num_vertices):
            # Adiciona uma pequena aleatoriedade ao ângulo e ao raio para a irregularidade
            angle = i * angle_step + pyxel.rndf(-0.1, 0.1) 
            radius = self.base_size / 2 + pyxel.rndf(-self.irregularity, self.irregularity)
            vx = radius * math.cos(angle)
            vy = radius * math.sin(angle)
            self.vertices.append((vx, vy))

    def get_rotated_vertices(self):
        # Calcula os vértices do asteroide após a rotação atual
        center_x = self.x + self.base_size / 2
        center_y = self.y + self.base_size / 2
        rotated_vertices = []
        for vx, vy in self.vertices:
            x_rot = vx * math.cos(self.rotation) - vy * math.sin(self.rotation)
            y_rot = vx * math.sin(self.rotation) + vy * math.cos(self.rotation)
            rotated_vertices.append((center_x + x_rot, center_y + y_rot))
        return rotated_vertices

    def update(self, player=None):
        # Nao chamamos super().update() aqui para que os asteroides nao gerem particulas de brilho
        self.x += self.dx
        self.y += self.dy
        self.rotation += self.angular_speed # Atualiza o ângulo de rotação
            
    def draw(self, glow_mode=0):
        center_x = self.x + self.base_size / 2
        center_y = self.y + self.base_size / 2

        # Desenha o asteroide conectando seus vértices rotacionados
        for i in range(self.num_vertices):
            x1_rel, y1_rel = self.vertices[i]
            x2_rel, y2_rel = self.vertices[(i + 1) % self.num_vertices] # Conecta o último vértice ao primeiro

            # Aplica a rotação aos vértices
            x1_rot = x1_rel * math.cos(self.rotation) - y1_rel * math.sin(self.rotation)
            y1_rot = x1_rel * math.sin(self.rotation) + y1_rel * math.cos(self.rotation)
            x2_rot = x2_rel * math.cos(self.rotation) - y2_rel * math.sin(self.rotation)
            y2_rot = x2_rel * math.sin(self.rotation) + y2_rel * math.cos(self.rotation)
            
            # Converte para coordenadas absolutas na tela
            x1_abs = center_x + x1_rot
            y1_abs = center_y + y1_rot
            x2_abs = center_x + x2_rot
            y2_abs = center_y + y2_rot
            
            pyxel.line(x1_abs, y1_abs, x2_abs, y2_abs, self.color)

    def shatter(self):
        fragments = []
        center_x = self.x + self.base_size / 2
        center_y = self.y + self.base_size / 2

        # Lógica de fragmentação baseada no tamanho do asteroide
        if self.size_type == 'large':
            num_fragments = 2 
            fragment_size_type = 'medium'
        elif self.size_type == 'medium':
            num_fragments = 2 
            fragment_size_type = 'small'
        else: # Asteroides pequenos não fragmentam
            return fragments

        # Cria novos fragmentos com velocidades de espalhamento
        for i in range(num_fragments):
            angle = (i * (2 * math.pi / num_fragments)) + pyxel.rndf(-0.5, 0.5) 
            fragment_speed = pyxel.rndf(0.5, 1.0) / 2.0 
            frag_dx = (self.dx * 0.2 + fragment_speed * math.cos(angle)) # Adiciona um pouco do movimento original
            frag_dy = (self.dy * 0.2 + fragment_speed * math.sin(angle))
            offset_x = pyxel.rndf(-self.base_size / 8, self.base_size / 8) # Pequeno offset para posicionamento
            offset_y = pyxel.rndf(-self.base_size / 8, self.base_size / 8)
            fragments.append(Asteroid(center_x + offset_x, center_y + offset_y, fragment_size_type, self.movement_pattern, self.asset_manager, frag_dx, frag_dy, self.game_particles_list))
        return fragments



class BackgroundParticle:
    def __init__(self, x, y, speed, size, color):
        self.x = x
        self.y = y
        self.speed = speed 
        self.size = size
        self.color = color

    def update(self):
        self.y += self.speed
        # Se a partícula sair da tela, reposiciona no topo
        if self.y > pyxel.height:
            self.y = -self.size
            self.x = pyxel.rndi(0, pyxel.width - 1)

    def draw(self):
        if self.size == 1:
            pyxel.pset(self.x, self.y, self.color)
        else:
            pyxel.rect(self.x, self.y, self.size, self.size, self.color)

class BackgroundAsteroid:
    """
    Representa um asteroide visual de fundo. Não possui saúde nem colisão.
    Reutiliza a lógica de forma e rotação da classe Asteroid.
    """
    def __init__(self, x, y, size_type, speed, color):
        self.x = x
        self.y = y
        self.size_type = size_type
        self.speed = speed # Esta é a velocidade principal Y de rolagem
        self.color = color

        # Configurações de tamanho e forma baseadas no size_type
        if self.size_type == 'small':
            self.base_size = 6
            self.num_vertices = pyxel.rndi(5, 7)
            self.irregularity = 2.0
        elif self.size_type == 'medium':
            self.base_size = 12
            self.num_vertices = pyxel.rndi(7, 9)
            self.irregularity = 3.5
        elif self.size_type == 'large':
            self.base_size = 24
            self.num_vertices = pyxel.rndi(9, 12)
            self.irregularity = 5.0
        
        # Componentes de movimento lateral e rotação, proporcionais à velocidade principal para o efeito de profundidade
        self.dx = pyxel.rndf(-0.1, 0.1) * self.speed * 0.5 # Pequeno desvio lateral, ajustado
        self.dy_base = self.speed # Componente Y da velocidade (principalmente para baixo)
        self.angular_speed = pyxel.rndf(-0.02, 0.02) * self.speed * 0.5 # Velocidade de rotação, ajustada
        self.rotation = pyxel.rndf(0, math.pi * 2)

        self._generate_vertices()

    def _generate_vertices(self):
        # Lógica de geração de vértices similar à classe Asteroid
        self.vertices = []
        angle_step = (2 * math.pi) / self.num_vertices
        for i in range(self.num_vertices):
            angle = i * angle_step + pyxel.rndf(-0.1, 0.1)
            radius = self.base_size / 2 + pyxel.rndf(-self.irregularity, self.irregularity)
            vx = radius * math.cos(angle)
            vy = radius * math.sin(angle)
            self.vertices.append((vx, vy))

    def update(self):
        self.x += self.dx
        self.y += self.dy_base
        self.rotation += self.angular_speed

        # Reposiciona o asteroide no topo da tela quando sai por baixo
        if self.y > pyxel.height:
            self.y = -self.base_size
            self.x = pyxel.rndi(0, pyxel.width - self.base_size)
            # Reseta as propriedades de movimento e rotação para variar a aparência
            self.dx = pyxel.rndf(-0.1, 0.1) * self.speed * 0.5
            self.angular_speed = pyxel.rndf(-0.02, 0.02) * self.speed * 0.5
            self.rotation = pyxel.rndf(0, math.pi * 2)
            self._generate_vertices() # Gera uma nova forma para o asteroide

    def draw(self):
        center_x = self.x + self.base_size / 2
        center_y = self.y + self.base_size / 2

        # Desenha o asteroide conectando seus vértices rotacionados
        for i in range(self.num_vertices):
            x1_rel, y1_rel = self.vertices[i]
            x2_rel, y2_rel = self.vertices[(i + 1) % self.num_vertices] 
            
            x1_rot = x1_rel * math.cos(self.rotation) - y1_rel * math.sin(self.rotation)
            y1_rot = x1_rel * math.sin(self.rotation) + y1_rel * math.cos(self.rotation)
            x2_rot = x2_rel * math.cos(self.rotation) - y2_rel * math.sin(self.rotation)
            y2_rot = x2_rel * math.sin(self.rotation) + y2_rel * math.cos(self.rotation)
            
            x1_abs = center_x + x1_rot
            y1_abs = center_y + y1_rot
            x2_abs = center_x + x2_rot
            y2_abs = center_y + y2_rot
            
            pyxel.line(x1_abs, y1_abs, x2_abs, y2_abs, self.color)


class FlameParticle:
    
    def __init__(self, x, y, dx, dy, color, lifetime, size=1):
        self.x = x
        self.y = y
        self.dx = dx 
        self.dy = dy 
        self.color = color
        self.lifetime = lifetime
        self.size = size

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1
        return self.lifetime > 0

    def draw(self):
        if self.lifetime > 0:
            if self.size == 1:
                pyxel.pset(self.x, self.y, self.color)
            else:
                pyxel.rect(self.x, self.y, self.size, self.size, self.color)

class PowerUp:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.width = 6
        self.height = 6
        self.type = type
        self.color = 15 # Power-ups usam a cor Amarelo (15)

    def update(self):
        self.y += 0.5 

    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, self.color)

class HUD:
    """
    Classe dedicada para desenhar a Interface do Usuário (Heads-Up Display).
    Ela lê os dados do objeto 'game' para mostrar informações na tela.
    """
    def __init__(self, game):
        # Armazena uma referência ao objeto principal do jogo
        self.game = game

    def draw(self):
        # Usa a referência 'self.game' para acessar as propriedades do jogo
        pyxel.text(100, 1, f"T: {self.game.game_time:02}", 7) # Texto geral: Branco (7)
        pyxel.text(100, 9, f"SC: {self.game.score}", 7) # Texto geral: Branco (7)
        
 # --- BARRAS DE HP E ENERGIA ---
        self.draw_hp_bar()
        self.draw_energy_bar()
        
        # --- ATUALIZAÇÃO DA HUD: MOSTRAR ARMA ATIVA ---
        # Desenhar o fundo da circunferência com a cor das barras
        pyxel.circ(8, 8, 8, 1) # Cor 1 (cinza escuro) para o fundo do círculo

        # Desenhar a borda da circunferência no canto superior esquerdo
        pyxel.circb(8, 8, 8, 7) # Cor 7 (branco) para a borda
        
        # Indicar o poder ativo dentro do círculo (aqui, a arma ativa)
        current_bullet_name = self.game.bullet_type_keys[self.game.current_bullet_type_index].upper()
        # Pega a primeira letra do nome da arma para exibir no círculo
        display_char = current_bullet_name[0]
        
        # Usa a cor da bala definida em bullet_properties para a letra no círculo

        bullet_display_color = self.game.asset_manager.get_bullet_properties()[current_bullet_name.lower()]['color']
        
        # Ajusta a posição da letra no centro do círculo
        text_x = 9 - pyxel.FONT_WIDTH // 2 
        text_y = 9 - pyxel.FONT_HEIGHT // 2
        pyxel.text(text_x, text_y, display_char, bullet_display_color)


        # Linha "SHOT:" e nome da arma (mantida)
       # pyxel.text(1, 17, f"SHOT: {current_bullet_name}", bullet_display_color)

        pyxel.text(100, 25, f"E: {self.game.current_enemy_category.upper()}", 7) # Texto geral: Branco (7)

        # Mostra o tempo restante do boost
        if self.game.is_boosting:
            boost_seconds = self.game.boost_timer // self.game.game_fps
            pyxel.text(100, 33, f"B: {boost_seconds}", 5) # Texto de Boost no HUD: Laranja (5)

       

    def draw_hp_bar(self):
        bar_x = 15 # Deslocado para a direita para não colidir com o círculo da arma
        bar_y = 3
        bar_width = 80 # Largura ajustada
        bar_height = 5 # Altura ajustada

        pyxel.rect(bar_x, bar_y, bar_width, bar_height, 1) # Fundo (cinza escuro)

        if self.game.player_max_hp > 0:
            hp_ratio = self.game.player_hp / self.game.player_max_hp
        else:
            hp_ratio = 0 

        current_bar_width = int(bar_width * hp_ratio)
        pyxel.rect(bar_x, bar_y, current_bar_width, bar_height, 4) # Preenchimento (vermelho)
        pyxel.rectb(bar_x, bar_y, bar_width, bar_height, 7) # Borda (branco)

    def draw_energy_bar(self):
        bar_x =15 # Deslocado para a direita
        bar_y = 9 # Abaixo da barra de HP
        bar_width = 80 # Largura ajustada
        bar_height = 5 # Altura ajustada

        pyxel.rect(bar_x, bar_y, bar_width, bar_height, 1) # Fundo (cinza escuro)

        if self.game.player_max_energy > 0:
            energy_ratio = self.game.player_energy / self.game.player_max_energy
        else:
            energy_ratio = 0 

        current_bar_width = int(bar_width * energy_ratio)
        pyxel.rect(bar_x, bar_y, current_bar_width, bar_height, 2) # Preenchimento (azul claro/ciano)
        pyxel.rectb(bar_x, bar_y, bar_width, bar_height, 7) # Borda (branco)


class Game:
    def __init__(self):
        self.game_fps = 60 
        pyxel.init(128, 128, title="Space Game", fps=self.game_fps)
        pyxel.load("shipgame.pyxres")

        self.asset_manager = AssetManager()

        # --- CONFIGURAÇÃO DA PALETA DE CORES ---
        # Definindo as cores Pyxel de 0 a 15 de acordo com a paleta fornecida e os novos requisitos
        

                # Definições de inimigos ajustadas conforme as 6 cores
        


        pyxel.colors[0]  = 0x000000 # 0: Preto
        pyxel.colors[1]  = 0x999999 # 1: Cinza
        pyxel.colors[2]  = 0x00FFFF # 2: Ciano (agora definido como Branco)
        pyxel.colors[3]  = 0x00FF00 # 3: Verde
        pyxel.colors[4]  = 0xFF0000 # 4: Vermelho
        pyxel.colors[5]  = 0xFF7500 # 5: Laranja
        pyxel.colors[6]  = 0xCCCCCC # 6: Cinza Claro
        pyxel.colors[7]  = 0xFFFFFF # 7: Branco
        pyxel.colors[8]  = 0xFF00FF # 8: Magenta
        pyxel.colors[9]  = 0x800080 # 9: Roxo Claro
        pyxel.colors[10] = 0x4C004C # 10: Roxo Médio
        pyxel.colors[11] = 0x330033 # 11: Roxo escuro (Teal)
        pyxel.colors[12] = 0x804000 # 12: Marrom
        pyxel.colors[13] = 0x4C4C00 # 13: Amarelo Médio
        pyxel.colors[14] = 0x808000 # 14: Amarelo Claro
        pyxel.colors[15] = 0xFFFF00 # 15: Amarelo
        # --- FIM DA CONFIGURAÇÃO DA PALETA DE CORES ---

        self.player_hp = 100        # HP inicial do player
        self.player_max_hp = 100    # HP máximo inicial

        self.player_energy = 10     # Energia inicial do player (novo!)
        self.player_max_energy = 10 # Energia máxima (novo!)
        self.energy_recharge_timer = 0 # Timer para regeneração de energia (novo!)
        self.energy_recharge_rate = 30 # A cada 30 frames, 1 de energia é recarregado (novo!)

        self.player_lives = 3 # Mantido para Game Over final, mas HP é o principal agora.

        self.movement_pattern_keys = list(self.asset_manager.get_movement_patterns().keys())
# Índice para controlar qual padrão está selecionado.
        self.current_movement_pattern_index = 0

        self.player = Player(pyxel.width / 2 - (Player(0,0, self.asset_manager).width // 2), pyxel.height - 16, self.asset_manager)
        
        ### NOVO: CONTROLE DE ONDAS E SPAWN ###
        self.wave_number = 1
        self.wave_spawn_timer = 0
        self.wave_spawn_delay = 180 # 3 segundos de delay entre ondas
        self.enemy_spawn_timer = 0
        self.enemies_to_spawn = [] # Uma "fila" de inimigos a serem criados
        # Instancia a HUD (Heads-Up Display)
        self.hud = HUD(self)
        
        self.state_manager = StateManager(self)

        # Criamos instâncias de cada estado para que o jogo as conheça
        self.playing_state = PlayingState(self)
        self.paused_state = PausedState(self)
        self.game_over_state = GameOverState(self)

        # Adicionamos os estados ao gerenciador
        self.state_manager.add_state(self.playing_state)
        self.state_manager.add_state(self.paused_state)
        self.state_manager.add_state(self.game_over_state)

        # Definimos o estado inicial do jogo
        self.state_manager.change_state("playing")


        # Listas para gerenciar os objetos do jogo
        self.bullets = []
        self.particles = [] 
        self.enemies = []
        self.flame_particles = [] 
        self.powerups = []
        self.enemy_bullets = [] # Nova lista para as balas dos inimigos.
        # Estado do boost do jogador
        self.is_boosting = False
        self.boost_timer = 0
        self.boost_duration = 60 * 5 # 5 segundos de boost (60 frames/segundo * 5)
        self.player_base_speed = 1 
        self.player_boost_speed = 1.5 

        # Variáveis de jogo
        self.game_time = 0
        self.score = 0
        
        #self.wave_cleared_timer = 0
        #self.wave_cleared_delay = 60 * 1 # 1 segundo de atraso entre as ondas
        self.powerup_spawn_chance = 0.3 # Chance de um power-up aparecer
        self.glow_mode = 0
        
        
        # --- VARIÁVEIS DE SCREEN SHAKE ---
        self.shake_duration = 0  # Duração restante do shake
        self.shake_intensity = 0 # Intensidade do shake
        self.shake_offset_x = 0  # Deslocamento X da tela
        self.shake_offset_y = 0  # Deslocamento Y da tela






        # Tipos de inimigos alienígenas que serão gerados
        self.specific_enemy_types = ['red', 'purple', 'blue', 'green', 'yellow', 'orange'] 
        self.enemy_types_sequence = ['green', 'yellow', 'orange', 'blue', 'purple', 'red']
        self.current_enemy_type_index = 0
        self.asteroid_size_types = ['small', 'medium', 'large'] 
        self.current_enemy_category = 'aliens' 
        self.is_charging_weapon = False
        self.charge_timer = 0
        
        # Nomes dos tipos de bala para alternar - inclui os novos e a reorganização
        self.bullet_type_keys = list(self.asset_manager.get_bullet_properties().keys())
        self.current_bullet_type_index = 0 
        self.last_shot_frame = {bullet_type: 0 for bullet_type in self.bullet_type_keys} 
        self.is_laser_active = False 
        self.laser_draw_end_y = 0 
        self.laser_spark_point = None
        
        # Geração das partículas de fundo (estrelas e agora asteroides de fundo)
        self.background_particles = [] 
        self.midground_particles = [] 
        self.foreground_particles = [] 

        # Velocidades para as camadas de fundo (estrelas e asteroides de fundo usarão essas)
        self.bg_speed_distant = 0.1
        self.bg_speed_medium = 0.75
        self.bg_speed_close = 3.0

        # Partículas de fundo (estrelas)
        # Distantes: Roxo Escuro (11)
        # Médias: Roxo Médio (10)
        # Próximas: Cinza escuro (1)
        for _ in range(50): 
            x = pyxel.rndi(0, pyxel.width - 1)
            y = pyxel.rndi(0, pyxel.height - 1)
            self.background_particles.append(BackgroundParticle(x, y, self.bg_speed_distant, 1, 11)) 

        for _ in range(30): 
            x = pyxel.rndi(0, pyxel.width - 1)
            y = pyxel.rndi(0, pyxel.height - 1)
            self.midground_particles.append(BackgroundParticle(x, y, self.bg_speed_medium, 1, 10)) 

        for _ in range(10): 
            x = pyxel.rndi(0, pyxel.width - 1)
            y = pyxel.rndi(0, pyxel.height - 1)
            size = pyxel.rndi(1, 2)
            self.foreground_particles.append(BackgroundParticle(x, y, self.bg_speed_close, size, 1)) 

        # --- ADIÇÃO: Asteroides de Fundo ---
        # Asteroides de fundo distantes
        asteroid_sizes = self.asset_manager.get_asteroid_sizes() # Pega os dados aqui

        # Asteroides de fundo distantes
        for _ in range(5): 
            size = asteroid_sizes['large'] # Usa a variável local
            x = pyxel.rndi(0, pyxel.width - size)
            y = pyxel.rndi(0, pyxel.height - size)
            self.background_particles.append(BackgroundAsteroid(x, y, 'large', self.bg_speed_distant, 11))

        for _ in range(5):
            size = asteroid_sizes['medium'] # Usa a variável local
            x = pyxel.rndi(0, pyxel.width - size)
            y = pyxel.rndi(0, pyxel.height - size)
            self.midground_particles.append(BackgroundAsteroid(x, y, 'medium', self.bg_speed_medium, 10))

            
        
        #self.spawn_enemy_wave() 
        self._setup_wave()

        pyxel.run(self.update, self.draw) 

    
    def restart_game(self):
        """Reseta o jogo para seu estado inicial."""
        self.player_lives = 3
        self.player_hp = self.player_max_hp
        self.player_energy = self.player_max_energy
        self.score = 0
        self.state_manager.change_state("playing")
        
        self.player.x = pyxel.width / 2 - (self.player.width // 2)
        self.player.y = pyxel.height - 16
        self.player.is_alive = True
        self.player.invincibility_timer = 0
        
        self.bullets, self.particles, self.enemies, self.flame_particles, self.powerups, self.enemy_bullets = [], [], [], [], [], []
        
        self.current_enemy_category = 'aliens'
        
        # --- CORREÇÃO APLICADA AQUI ---
        self.wave_number = 1
        self._setup_wave()
        
        self.reset_screen_shake()

    def _setup_wave(self):
        """Prepara a lista de inimigos a serem gerados para a onda atual."""
        self.enemies_to_spawn = [] # Limpa a fila

        enemy_defs = self.asset_manager.get_enemy_definitions()
        movement_patterns = self.asset_manager.get_movement_patterns()
        
        if self.current_enemy_category == 'aliens':
            if self.wave_number == 1: # Formação de Grade (Inspirado na Fase 1)
                pattern = movement_patterns['alien_grid_formation']
                num_rows, num_cols, spacing_x, spacing_y = 3, 5, 16, 12
                num_enemy_types = len(self.specific_enemy_types)
                start_x = (128 - (num_cols * Enemy.SPRITE_W + (num_cols - 1) * spacing_x)) / 2
                start_y = -((num_rows * Enemy.SPRITE_H) + ((num_rows - 1) * spacing_y))
                for row in range(num_rows):
                    for col in range(num_cols):
                        enemy_random_index = pyxel.rndi(0, num_enemy_types-1)
                        enemy_type = self.specific_enemy_types[enemy_random_index]
                        enemy_def = enemy_defs[enemy_type]
                        x, y = start_x + col * (Enemy.SPRITE_W + spacing_x), start_y + row * (Enemy.SPRITE_H + spacing_y)
                        self.enemies_to_spawn.append({'x': x, 'y': y, 'type': enemy_type, 'def': enemy_def, 'pattern': pattern, 'delay': 0})

            elif self.wave_number == 2: # Entrada Galaga (Inspirado na Fase 2)
                pattern = self.asset_manager.get_movement_patterns()['alien_galaga_entry']
                num_enemies = 8
                final_positions = [(20 + i * 12, 40) for i in range(num_enemies)] # Posições finais em linha
                for i in range(num_enemies):
                    enemy_type = random.choice(self.specific_enemy_types)
                    enemy_def = enemy_defs[enemy_type]
                    kwargs = {'final_x': final_positions[i][0], 'final_y': final_positions[i][1]}
                    self.enemies_to_spawn.append({'x': 0, 'y': -10, 'type': enemy_type, 'def': enemy_def, 'pattern': pattern, 'delay': 30 * i, 'kwargs': kwargs})

            elif self.wave_number == 3: # Entrada Lateral (Inspirado na Fase 3)
                pattern = self.asset_manager.get_movement_patterns()['alien_side_entry_align']
                num_enemies = 10
                final_positions = [(20 + (i % 5) * 18, 20 + (i // 5) * 15) for i in range(num_enemies)] # Grid 2x5
                for i in range(num_enemies):
                    enemy_type = random.choice(self.specific_enemy_types)
                    enemy_def = enemy_defs[enemy_type]
                    direction = 1 if i % 2 == 0 else -1
                    kwargs = {'final_x': final_positions[i][0], 'final_y': final_positions[i][1], 'direction': direction}
                    self.enemies_to_spawn.append({'x': 0, 'y': 0, 'type': enemy_type, 'def': enemy_def, 'pattern': pattern, 'delay': 20 * i, 'kwargs': kwargs})
            
            else: # Se acabaram as ondas de aliens, reinicia o ciclo de ondas de aliens
                self.wave_number = 1
                self._setup_wave()

        elif self.current_enemy_category == 'asteroids':
            if self.wave_number == 1:
                wave_patterns = ['asteroid_slow_drift']
                num_asteroids = 5
            elif self.wave_number == 2:
                wave_patterns = ['asteroid_slow_drift', 'asteroid_fast_fall']
                num_asteroids = 8
            else: # Se acabaram as ondas de asteroides, reinicia o ciclo de ondas de asteroides
                self.wave_number = 1
                self._setup_wave()
                return # Retorna para evitar executar o código de spawn abaixo com valores antigos

            for _ in range(num_asteroids):
                pattern_name = random.choice(wave_patterns)
                movement_pattern = self.asset_manager.get_movement_patterns()[pattern_name]
                size_type = random.choice(['medium', 'large'])
                asteroid_size_ref = self.asset_manager.get_asteroid_sizes()[size_type]
                x, y = pyxel.rndi(0, pyxel.width - asteroid_size_ref), pyxel.rndi(-40, -20)
                self.enemies_to_spawn.append({'is_asteroid': True, 'x': x, 'y': y, 'size': size_type, 'pattern': movement_pattern, 'delay': pyxel.rndi(0, 60)})

    def _update_wave_spawner(self):
        """Verifica se é hora de gerar a próxima onda ou o próximo inimigo da fila."""
        if not self.enemies and not self.enemies_to_spawn: # Se a tela está limpa e a fila vazia
            self.wave_spawn_timer += 1
            if self.wave_spawn_timer > self.wave_spawn_delay:
                self.wave_number += 1
                self.wave_spawn_timer = 0
                self.enemy_spawn_timer = 0
                self._setup_wave()
        
        elif self.enemies_to_spawn:
            self.enemy_spawn_timer += 1
            # O primeiro inimigo da fila tem um delay, então verificamos contra ele
            if self.enemy_spawn_timer >= self.enemies_to_spawn[0]['delay']:
                enemy_data = self.enemies_to_spawn.pop(0)
                
                # Lógica para criar o tipo certo de objeto
                if enemy_data.get('is_asteroid'):
                    self.enemies.append(Asteroid(
                    x=enemy_data['x'], y=enemy_data['y'], 
                    size_type=enemy_data['size'],
                    movement_pattern=enemy_data['pattern'],
                    asset_manager=self.asset_manager
                    ))
                    
                else: # É um inimigo alienígena padrão
                    kwargs = enemy_data.get('kwargs', {})
                    self.enemies.append(Enemy(
                    x=enemy_data['x'], y=enemy_data['y'], type=enemy_data['type'], 
                    color=enemy_data['def']['color'], health=enemy_data['def']['health'], 
                    movement_pattern=enemy_data['pattern'], asset_manager=self.asset_manager, **kwargs
                    ))
                
                # Reseta o timer para o delay do próximo inimigo (se houver)
                if self.enemies_to_spawn:
                    self.enemy_spawn_timer = 0
    
    def spawn_test_enemy(self):
        """Limpa e gera um único inimigo de teste usando o padrão de movimento selecionado."""
        self.enemies.clear()
        self.enemy_bullets.clear()

        enemy_type = self.enemy_types_sequence[self.current_enemy_type_index]
        # CORREÇÃO: Busca e armazena os dados ANTES de usá-los
        enemy_data = self.asset_manager.get_enemy_definitions()[enemy_type]
        spawn_x, spawn_y = pyxel.width / 2 - Enemy.SPRITE_W / 2, 15

        # Pega o NOME do padrão atual usando o índice.
        pattern_name = self.movement_pattern_keys[self.current_movement_pattern_index]
        # Pega o DICIONÁRIO completo do padrão correspondente.
        movement_pattern = self.asset_manager.get_movement_patterns()[pattern_name]

        # Agora a criação do inimigo funciona, pois `enemy_data` existe
        new_enemy = Enemy(spawn_x, spawn_y, enemy_type, enemy_data['color'], enemy_data['health'], movement_pattern, self.asset_manager)        
        
        # Adiciona o inimigo único à lista.
        self.enemies.append(new_enemy)

    def spawn_powerup(self):
        powerup_x = pyxel.rndi(0, pyxel.width - PowerUp(0,0,'boost').width)
        powerup_y = -PowerUp(0,0,'boost').height - pyxel.rndi(10, 30)
        self.powerups.append(PowerUp(powerup_x, powerup_y, 'boost'))

    # Método auxiliar para detecção de colisão AABB (Axis-Aligned Bounding Box)
    def _check_aabb_collision(self, obj1_x, obj1_y, obj1_width, obj1_height, obj2_x, obj2_y, obj2_width, obj2_height):
        return (obj1_x < obj2_x + obj2_width and
                obj1_x + obj1_width > obj2_x and
                obj1_y < obj2_y + obj2_height and
                obj1_y + obj1_height > obj2_y)

    # Método auxiliar para detecção de intersecção de linha (usado para laser com asteroides)
    def _line_intersection(self, p1, p2, p3, p4):
        x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0: return None # Linhas são paralelas ou colineares
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
        # Verifica se os pontos de intersecção estão dentro dos segmentos de linha
        if 0 <= t <= 1 and 0 <= u <= 1:
            return x1 + t * (x2 - x1), y1 + t * (y2 - y1)
        return None
    

    def _is_point_in_polygon(self, point_x, point_y, polygon_vertices):
        """
        Verifica se um ponto está dentro de um polígono usando o algoritmo Ray Casting.
        Retorna True se o ponto estiver dentro, False caso contrário.
        """
        num_vertices = len(polygon_vertices)
        if num_vertices < 3:
            return False # Não é um polígono válido

        intersections = 0
        # O "raio" é um segmento de linha que vai do ponto até um ponto bem fora da tela à direita.
        ray_end_x = pyxel.width + 10 

        for i in range(num_vertices):
            p1 = polygon_vertices[i]
            # Garante que a última aresta conecte o último vértice ao primeiro.
            p2 = polygon_vertices[(i + 1) % num_vertices] 

            # Verifica se o nosso raio imaginário cruza esta aresta do polígono.
            if self._line_intersection((point_x, point_y), (ray_end_x, point_y), p1, p2):
                intersections += 1
        
        # Se o número de interseções for ímpar, o ponto está dentro.
        return intersections % 2 == 1


    def _check_polygon_collision(self, poly1_vertices, poly2_vertices):
        """
        Verifica a colisão entre dois polígonos convexos.
        Retorna True se houver colisão, False caso contrário.
        """
        # Etapa 1: Verificar se alguma aresta do Polígono 1 cruza com alguma do Polígono 2
        for i in range(len(poly1_vertices)):
            p1 = poly1_vertices[i]
            p2 = poly1_vertices[(i + 1) % len(poly1_vertices)] # Aresta do Polígono 1

            for j in range(len(poly2_vertices)):
                p3 = poly2_vertices[j]
                p4 = poly2_vertices[(j + 1) % len(poly2_vertices)] # Aresta do Polígono 2

                if self._line_intersection(p1, p2, p3, p4):
                    return True # Encontrou uma interseção de arestas

        # Etapa 2: Se não houver cruzamento de arestas, verificar se um polígono está dentro do outro.
        # Basta testar um único ponto de cada polígono.
        if self._is_point_in_polygon(poly1_vertices[0][0], poly1_vertices[0][1], poly2_vertices):
            return True
        
        if self._is_point_in_polygon(poly2_vertices[0][0], poly2_vertices[0][1], poly1_vertices):
            return True

        return False



    def create_pixel_explosion(self, enemy):
            """
            Cria uma explosão de "detritos de pixel" baseada no sprite atual do inimigo.
            Este método lê cada pixel do sprite do inimigo diretamente da folha de sprites (Image Bank)
            e cria uma partícula para cada um, simulando um efeito de despedaçamento.
            """
            # Obtém a lista de frames de animação para o tipo específico do inimigo.
            frames = enemy.animation_data[enemy.type]
            
            # Pega as coordenadas (u, v) do frame de animação que estava sendo exibido no momento da destruição.
            # Isso garante que a explosão corresponda visualmente ao inimigo.
            u, v = frames[enemy.animation_frame_index]
            
            # Itera sobre cada pixel dentro da área do sprite (largura x altura).
            for y_offset in range(enemy.height):
                for x_offset in range(enemy.width):
                    
                    # --- CORREÇÃO APLICADA AQUI ---
                    # Usamos `pyxel.image(banco).pget(x, y)` para obter a cor do pixel diretamente da
                    # folha de sprites (Image Bank), em vez de `pyxel.pget(x, y)` que lê da tela.
                    # `enemy.SPRITE_BANK` nos dá o número do banco de imagem correto (neste caso, 0).
                    pixel_color = pyxel.images[enemy.SPRITE_BANK].pget(u + x_offset, v + y_offset)                    
                    # A cor 0 é a cor de transparência padrão do Pyxel.
                    # Só criamos partículas para pixels que são visíveis (cor diferente de 0).
                    if pixel_color != 0:
                        # Gera uma velocidade aleatória (dx, dy) para a partícula, para que ela se espalhe.
                        dx = pyxel.rndf(-1.5, 1.5)
                        dy = pyxel.rndf(-1.5, 1.5)
                        
                        # Define um tempo de vida aleatório para a partícula.
                        lifetime = pyxel.rndi(20, 40)
                        
                        # Cria a instância da partícula de detrito de pixel.
                        particle = PixelDebrisParticle(
                            enemy.x + x_offset,   # Posição inicial X no mundo do jogo.
                            enemy.y + y_offset,   # Posição inicial Y no mundo do jogo.
                            pixel_color,          # A cor que lemos do sprite.
                            dx, dy,               # A velocidade de espalhamento.
                            lifetime              # O tempo que a partícula ficará na tela.
                        )
                        # Adiciona a nova partícula à lista de partículas do jogo para ser atualizada e desenhada.
                        self.particles.append(particle)

    def create_shatter_effect(self, asteroid):
        """
        Cria um efeito de "poeira" mais sutil para quando um asteroide se parte,
        em vez de uma explosão completa.
        """
        # Gera uma quantidade menor de partículas para um efeito mais contido.
        num_particles = int((asteroid.width * asteroid.height) / 20)
        for _ in range(num_particles):
            # Gera uma posição aleatória dentro da caixa delimitadora do asteroide.
            px = asteroid.x + pyxel.rndf(0, asteroid.width)
            py = asteroid.y + pyxel.rndf(0, asteroid.height)

            # Usa velocidades menores para simular poeira em vez de uma explosão.
            dx = pyxel.rndf(-0.8, 0.8)
            dy = pyxel.rndf(-0.8, 0.8)
            lifetime = pyxel.rndi(15, 30)
            self.particles.append(PixelDebrisParticle(px, py, asteroid.color, dx, dy, lifetime))


    def create_hit_sparks(self, x, y, color):
        """
        Cria um pequeno efeito de faíscas no ponto de impacto de um projétil.
        Usado para feedback visual quando um tiro atinge um inimigo.
        """
        # Gera um pequeno número de partículas (2 a 3) para o efeito.
        for _ in range(pyxel.rndi(2, 3)):
            # Define uma velocidade de espalhamento alta e aleatória.
            dx = pyxel.rndf(-2, 2)
            dy = pyxel.rndf(-2, 2)
            
            # Define um tempo de vida muito curto (entre 4 e 8 frames).
            lifetime = pyxel.rndi(4, 8)
            
            # Cria a partícula de explosão, que aqui serve como uma faísca.
            spark = ExplosionParticle(x, y, dx, dy, color, lifetime)
            
            # Adiciona a faísca à lista principal de partículas do jogo.
            self.particles.append(spark)                  

    def create_asteroid_debris_explosion(self, asteroid):
        """
        Cria uma explosão de detritos que corresponde à forma do asteroide.
        Combina partículas no contorno e no interior para um efeito mais preciso.
        """
        # Pega os vértices já rotacionados do asteroide.
        rotated_vertices = asteroid.get_rotated_vertices()
        
        # ### 1. GERAÇÃO DE PARTÍCULAS DE CONTORNO ###
        # Itera sobre cada aresta do polígono (de um vértice ao próximo).
        for i in range(len(rotated_vertices)):
            p1 = rotated_vertices[i]
            p2 = rotated_vertices[(i + 1) % len(rotated_vertices)] # Garante que o último vértice se conecte ao primeiro.
            
            # Calcula o comprimento da aresta para determinar quantas partículas gerar.
            edge_length = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
            # Gera aproximadamente 1 partícula a cada 2 pixels de comprimento da aresta.
            num_particles_on_edge = max(1, int(edge_length / 2))

            for j in range(num_particles_on_edge):
                # Interpola a posição ao longo da aresta para posicionar a partícula.
                # j / num_particles_on_edge nos dá uma fração de 0.0 a 1.0.
                t = j / num_particles_on_edge
                px = p1[0] + t * (p2[0] - p1[0])
                py = p1[1] + t * (p2[1] - p1[1])
                
                # Cria a partícula de detrito.
                dx = pyxel.rndf(-1.5, 1.5)
                dy = pyxel.rndf(-1.5, 1.5)
                lifetime = pyxel.rndi(25, 45)
                self.particles.append(PixelDebrisParticle(px, py, asteroid.color, dx, dy, lifetime))

        # ### 2. GERAÇÃO DE PARTÍCULAS DE PREENCHIMENTO ###
        # Calcula o número de partículas internas com base na área aproximada do asteroide.
        num_interior_particles = int((asteroid.width * asteroid.height) / 4)
        for _ in range(num_interior_particles):
            # Gera uma posição aleatória dentro da caixa delimitadora do asteroide.
            px = asteroid.x + pyxel.rndf(0, asteroid.width)
            py = asteroid.y + pyxel.rndf(0, asteroid.height)

            # Cria a partícula de detrito.
            dx = pyxel.rndf(-1.0, 1.0) # Velocidade um pouco menor para o interior.
            dy = pyxel.rndf(-1.0, 1.0)
            lifetime = pyxel.rndi(20, 40)
            self.particles.append(PixelDebrisParticle(px, py, asteroid.color, dx, dy, lifetime))

    def trigger_screen_shake(self, duration, intensity):
        """Ativa o efeito de screen shake."""
        self.shake_duration = duration
        self.shake_intensity = intensity

    def reset_screen_shake(self):
        """Reseta o screen shake para zero."""
        self.shake_duration = 0
        self.shake_intensity = 0
        self.shake_offset_x = 0
        self.shake_offset_y = 0
    
    def update(self):
        self.state_manager.active_state.update()


        
    # Método para disparar o laser (arma 'red')
    def _fire_laser(self, props):
        """
        Calcula e aplica o dano do laser.
        Retorna o objeto do inimigo se ele for derrotado, ou None caso contrário.
        """
        self.is_laser_active = True
        laser_x = self.player.x + (self.player.width // 2)
        closest_impact_y, closest_target, final_spark_point = 0, None, None

        for enemy in self.enemies:
            if enemy.y + enemy.height > self.player.y: continue
            impact_y_cand, impact_x_cand = -1, -1

            if isinstance(enemy, Asteroid):
                verts = enemy.get_rotated_vertices()
                best_y = -1
                for i in range(enemy.num_vertices):
                    intersect = self._line_intersection((laser_x, self.player.y), (laser_x, 0), verts[i], verts[(i + 1) % enemy.num_vertices])
                    if intersect and intersect[1] > best_y:
                        best_y = intersect[1]
                if best_y != -1: impact_y_cand, impact_x_cand = best_y, laser_x
            elif laser_x >= enemy.x and laser_x <= enemy.x + enemy.width:
                impact_y_cand, impact_x_cand = enemy.y + enemy.height, laser_x

            if impact_y_cand > closest_impact_y:
                closest_impact_y, closest_target, final_spark_point = impact_y_cand, enemy, (impact_x_cand, impact_y_cand)

        if closest_target:
            damage_to_deal = props['damage_per_frame']
            if closest_target.type == 'red':
                damage_to_deal *= 2

            # ### MUDANÇA PRINCIPAL ###
            # Verificamos se o dano do laser derrotou o inimigo.
            if closest_target.take_damage(damage_to_deal):
                self.score += 1
                self.laser_draw_end_y, self.laser_spark_point = closest_impact_y, final_spark_point
                # Se o inimigo foi derrotado, nós o RETORNAMOS para que o método update() saiba.
                return closest_target
            
            # Se o inimigo foi atingido mas NÃO foi derrotado, apenas criamos as faíscas.
            self.laser_draw_end_y, self.laser_spark_point = closest_impact_y, final_spark_point
            spark_color = 4 if pyxel.frame_count % 4 < 2 else 5
            self.particles.append(ExplosionParticle(final_spark_point[0] + pyxel.rndf(-2, 2), final_spark_point[1] + pyxel.rndf(-2, 2), pyxel.rndf(-1, 1), pyxel.rndf(-1, 1), spark_color, pyxel.rndi(5, 10)))
        else:
            self.laser_draw_end_y, self.laser_spark_point = 0, None
        
        # ### MUDANÇA DE LÓGICA ###
        # Se a função chegar até aqui, significa que ou nenhum inimigo foi atingido,
        # ou o inimigo atingido não morreu. Em ambos os casos, retornamos None.
        return None
    

    # Método para disparar projéteis
    def _fire_projectiles(self, props):
        """
        Fires projectiles based on the given properties.
        Always returns True as there's no complex burst logic here.
        """
        size, behavior = props['size'], props.get('behavior')
        player_center_x = self.player.x + (self.player.width // 2) - (size['width'] // 2) 
        bullet_y = self.player.y - 3 - (size['height'] - 1) 

        # Fire the projectiles
        for i in range(props['num_shots']):
            angle = math.radians(props['angles_deg'][i]) + pyxel.rndf(-math.radians(props['spread_deg'])/2, math.radians(props['spread_deg'])/2)
            dx, dy = props['speed'] * math.cos(angle), props['speed'] * math.sin(angle) 
            self.bullets.append(Bullet(player_center_x, bullet_y, props['color'], self.bullet_type_keys[self.current_bullet_type_index], dx, dy, props['damage'], size['height'], size['width'], behavior, self.flame_particles))
        
        # Since there's no burst logic, always return True to indicate a shot was fired
        # and allow the main cooldown in update() to be applied.
        return True
    


    def draw(self):

        self.state_manager.active_state.draw()



if __name__ == "__main__":
    Game()
