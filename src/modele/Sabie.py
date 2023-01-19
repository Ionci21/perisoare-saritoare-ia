import pygame
import random
from src.utils.Utils import IMAGINE_SABIE


class Sabie:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.pozitie_x = x
        self.inaltime = 0
        self.pozitie_sabie_sus = 0
        self.pozitie_sabie_jos = 0
        self.SABIE_SUS = pygame.transform.flip(IMAGINE_SABIE, False, True)
        self.SABIE_JOS = IMAGINE_SABIE
        self.passed = False
        self.set_height()

    def set_height(self):
        self.inaltime = random.randrange(50, 450)
        self.pozitie_sabie_sus = self.inaltime - self.SABIE_SUS.get_height()
        self.pozitie_sabie_jos = self.inaltime + self.GAP

    def move(self):
        self.pozitie_x -= self.VEL

    def draw(self, win):
        win.blit(self.SABIE_SUS, (self.pozitie_x, self.pozitie_sabie_sus))
        win.blit(self.SABIE_JOS, (self.pozitie_x, self.pozitie_sabie_jos))

    def collide(self, obiect_perisoara):
        masca_pixeli_perisoara = obiect_perisoara.get_mask()
        masca_sabie_sus = pygame.mask.from_surface(self.SABIE_SUS)
        masca_sabie_jos = pygame.mask.from_surface(self.SABIE_JOS)
        offset_sabie_sus = (self.pozitie_x - obiect_perisoara.pozitie_x, self.pozitie_sabie_sus - round(obiect_perisoara.pozitie_y))
        offset_sabie_jos = (self.pozitie_x - obiect_perisoara.pozitie_x, self.pozitie_sabie_jos - round(obiect_perisoara.pozitie_y))
        punct_coliziune_sus = masca_pixeli_perisoara.overlap(masca_sabie_sus, offset_sabie_sus)
        punct_coliziune_jos = masca_pixeli_perisoara.overlap(masca_sabie_jos, offset_sabie_jos)
        return True if punct_coliziune_sus or punct_coliziune_jos else False
