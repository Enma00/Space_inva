import pygame, random
from classes import *


pygame.init()

# Paramètres de la fenêtre
largeur, hauteur = 1280, 800
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Space Invaders")

# Couleurs
blanc = (255, 255, 255)
noir = (0, 0, 0)
rouge = (255, 0, 0)

# Création des instances
joueur = Joueur(largeur // 2 - 32, hauteur - 180, 5, "joueur.png")
ennemi = Ennemi(largeur - 64, 100, 1, "ennemi.png", 150)
projectiles = []
projectiles_enn = []

# Variable 
jeu_termine = False
victoire = False

# Création de l'objet GameOver, Win
game_over = GameOver(fenetre)
win = Win(fenetre)
en_cours = False
menu = True
message = False

def afficher_texte(texte, x, y, taille_police, couleur):
    police = pygame.font.Font(None, taille_police)
    texte_surface = police.render(texte, True, couleur)
    texte_rect = texte_surface.get_rect()
    texte_rect.center = (x, y)
    fenetre.blit(texte_surface, texte_rect)

def reinitialiser_jeu():
    global jeu_termine, victoire, message
    jeu_termine = False
    victoire = False
    message = False
    joueur.x = largeur // 2 - 32
    joueur.y = hauteur - 180

# timer tir automatique 
TIMER_EVENT_1 = pygame.USEREVENT + 1
def generer_delai_tir():
    return random.randint(500, 1500)
temps_avant_prochain_tir = generer_delai_tir()
pygame.time.set_timer(TIMER_EVENT_1, temps_avant_prochain_tir)
temps_debut_partie = 0

# timer win/loose
TIMER_EVENT_2 = pygame.USEREVENT + 2
pygame.time.set_timer(TIMER_EVENT_2, 3000 )

while menu :
    afficher_texte(f'Appuyez sur espace pour jouer', largeur // 2, (hauteur // 2) + 30, 40,  blanc)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu = False
        elif keys[pygame.K_SPACE]:
            en_cours = True
            temps_debut_partie = pygame.time.get_ticks()
    pygame.display.update()
    # Boucle 
    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
                menu = False
            elif event.type == TIMER_EVENT_1:
                ennemi.tire_auto(projectiles_enn)
                temps_avant_prochain_tir = generer_delai_tir() 
                pygame.time.set_timer(TIMER_EVENT_1, temps_avant_prochain_tir)
        if  not jeu_termine and not victoire:
            # Gestion des contrôles du joueur
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[ord("q")]:
                joueur.x -= joueur.vitesse
            if keys[pygame.K_RIGHT] or keys[ord("d")]:
                joueur.x += joueur.vitesse
            if keys[pygame.K_SPACE]:
                joueur.tirer(projectiles)

            # Déplacement du joueur
            joueur.x = max(0, min(largeur - 64, joueur.x))

            # Gestion des ennemis
            ennemi.x += ennemi.vitesse
            if ennemi.x <= 0:
                ennemi.x = 0
                ennemi.vitesse = 1
            elif ennemi.x >= largeur - 64:
                ennemi.x = largeur - 64
                ennemi.vitesse = -1

            # Déplacement des projectiles et gestion de la collision
            for projectile in projectiles:
                projectile.y -= projectile.vitesse
                if (
                    ennemi.x < projectile.x < ennemi.x + 64 and ennemi.y < projectile.y < ennemi.y + 64):
                    projectiles.remove(projectile)
                    ennemi.hit(7)
                    print(ennemi.pv)
                if ennemi.est_detruit():
                    victoire = True

            for projectile in projectiles_enn:
                projectile.y += projectile.vitesse
                if (
                    joueur.x - 65 < projectile.x < joueur.x + 64 and joueur.y < projectile.y < joueur.y + 64):
                    jeu_termine = True

            # Effacement de l'écran
            fenetre.fill(noir)

            # Affichage de la barre de vie
            barre_vie_largeur = 200  # Largeur de la barre de vie
            barre_vie_hauteur = 20   # Hauteur de la barre de vie
            barre_vie_x = (largeur - barre_vie_largeur) // 2
            barre_vie_y = 10
            pygame.draw.rect(fenetre, rouge, (barre_vie_x, barre_vie_y, barre_vie_largeur, barre_vie_hauteur))
            pygame.draw.rect(fenetre, blanc, (barre_vie_x, barre_vie_y, barre_vie_largeur, barre_vie_hauteur))

            # Calcul de la longueur de la barre de vie en fonction des PV actuels
            pv_max = 100
            longueur_barre = (barre_vie_largeur * ennemi.pv) / pv_max
            pygame.draw.rect(fenetre, rouge, (barre_vie_x, barre_vie_y, longueur_barre, barre_vie_hauteur)) 

            # Affichage du nombre de PV restants
            texte_pv = f"{max(ennemi.pv, 0)} / {pv_max}"  # Création du texte 
            texte_x = barre_vie_x + barre_vie_largeur // 2
            texte_y = barre_vie_y + barre_vie_hauteur // 2
            afficher_texte(texte_pv, texte_x, texte_y, 20, noir)

            # Timer 
            temps_ecoule = 0
            temps_actuel = pygame.time.get_ticks()
            temps_ecoule = temps_actuel - temps_debut_partie
            x_temps = largeur // 2 
            afficher_texte(f"Temps : {temps_ecoule // 1000} secondes", x_temps, 45, 24, blanc)      

            # Affichage des éléments
            joueur.afficher(fenetre)
            ennemi.afficher(fenetre)
            for projectile in projectiles:
                projectile.afficher(fenetre)
            for projectile in projectiles_enn:
                if isinstance(projectile, Projectile_t1):
                    projectile.afficher(fenetre)
                elif isinstance(projectile, Projectile_t2):
                    projectile.afficher(fenetre)
                elif isinstance(projectile, Projectile_t3):
                    projectile.afficher(fenetre)

            # Rafraîchissement de l'écran        
            pygame.display.update()
        else:
        
        # "Game Over"
            if jeu_termine:
                message = True
                if message:
                    game_over.afficher()
                if event.type == TIMER_EVENT_2:
                    reinitialiser_jeu()
                    en_cours = False

            if victoire:
                message = True
                if message: 
                    win.afficher()
                if event.type == TIMER_EVENT_2:
                    reinitialiser_jeu()
                    en_cours = False

# Fermeture 
pygame.quit()