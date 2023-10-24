import pygame, random

# Classe du joueur
class Joueur:
    def __init__(self, x, y, vitesse, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (180, 180))
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.temps_dernier_tir = 0
        self.delai_tir = 500  # Délai millisecondes entre les tirs
        self.largeur = 180  # hitbox
        self.hauteur = 180
        

    def afficher(self, fenetre):
        fenetre.blit(self.image, (self.x - 65, self.y))

    def tirer(self, projectiles):
        temps_actuel = pygame.time.get_ticks()
        if temps_actuel - self.temps_dernier_tir >= self.delai_tir:
            nouveau_projectile = Projectile(self.x, self.y, 2, "projectile.png")
            projectiles.append(nouveau_projectile)
            self.temps_dernier_tir = temps_actuel

# Classe de l'ennemi
class Ennemi:
    def __init__(self, x, y, vitesse, image_path, pv):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.temps_dernier_tir_enn = 0
        self.delai_tir = 500
        self.largeur = 100  # hitbox
        self.hauteur = 100
        self.pv = 100

    def afficher(self, fenetre):
        fenetre.blit(self.image, (self.x, self.y))

    def tire_auto(self, projectiles_enn):
        projectile_aleatoire = random.choice([Projectile_t1, Projectile_t2, Projectile_t3])
        nouveau_projectile = projectile_aleatoire(self.x + 16, self.y, 2, None)
        projectiles_enn.append(nouveau_projectile)

    def hit(self, quantite):
        self.pv -= quantite
    
    def est_detruit(self):
        return self.pv <= 0

# Classe du projectile
class Projectile:
    def __init__(self, x, y, vitesse, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.x = x
        self.y = y
        self.vitesse = vitesse

    def afficher(self, fenetre):
        fenetre.blit(self.image, (self.x, self.y))

class Projectile_t1(Projectile):
    def __init__(self, x, y, vitesse, image_path):
        super().__init__(x, y, vitesse, "projectile_t1.png")
        self.image = pygame.transform.scale(self.image, (40, 80))

class Projectile_t2(Projectile):
    def __init__(self, x, y, vitesse, image_path):
        super().__init__(x, y, vitesse, "projectile_t2.png")
        self.image = pygame.transform.scale(self.image, (40, 80))

class Projectile_t3(Projectile):
    def __init__(self, x, y, vitesse, image_path):
        super().__init__(x, y, vitesse, "projectile_t3.png")
        self.image = pygame.transform.scale(self.image, (40, 80))

class GameOver:
    def __init__(self, fenetre):
        self.fenetre = fenetre  
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render("Game Over", True, (255, 0, 0))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = fenetre.get_rect().center

    def afficher(self):
        self.fenetre.blit(self.text, self.text_rect)
        pygame.display.flip()

class Win:
    def __init__(self, fenetre):
        self.fenetre = fenetre  
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render("What's the color ? BLUE !", True, (0, 206, 235))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = fenetre.get_rect().center

    def afficher(self):
        self.fenetre.blit(self.text, self.text_rect)
        pygame.display.flip()