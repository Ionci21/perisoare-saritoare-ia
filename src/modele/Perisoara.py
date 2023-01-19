import pygame
from src.utils.Utils import IMAGINE_PERISOARA


class Perisoara:
    imagine_perisoara = IMAGINE_PERISOARA

    def __init__(self, x, y):
        self.pozitie_x = x
        self.pozitie_y = y
        self.tick_count = 0
        self.viteza_perisoara = 0

    def jump(self):
        self.viteza_perisoara = -10.5
        self.tick_count = 0

    def move(self):
        self.tick_count += 1
        valoare_deplasare_pixeli = self.viteza_perisoara * self.tick_count + 1.5 * self.tick_count ** 2
        # dacă ne ducem mai jos de 16px setăm valoarea deplasării-ului la 16px ( pentru a nu coborî prea repede )
        valoare_deplasare_pixeli = 16 if valoare_deplasare_pixeli >= 16 else valoare_deplasare_pixeli - 2
        self.pozitie_y += valoare_deplasare_pixeli

    def draw(self, win):
        win.blit(self.imagine_perisoara, self.imagine_perisoara.get_rect(topleft=(self.pozitie_x, self.pozitie_y)).center)

    def get_mask(self):
        # folosit pentru a verifica dacă perișoara se lovește de sabie.. este o funcție predefinită în PyGame ca și un
        # „upgrade” versiunei clasice cu desenarea de CUBURI în jurul obiectelor ( pentru a verifica dacă cuburile
        # se ating )
        return pygame.mask.from_surface(self.imagine_perisoara)
