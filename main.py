import neat
from src.modele.Perisoara import Perisoara
from src.modele.Sabie import Sabie
from src.utils.Utils import *


def draw_window(fereastra, perisoare, sabii, scor, generatie, perisoare_vii):
    pygame.display.set_caption('Perisoare Zburatoare')
    fereastra.blit(IMAGINE_FUNDAL, (0, 0))
    for sabie in sabii:
        sabie.draw(fereastra)
    for perisoara in perisoare:
        perisoara.draw(fereastra)
    text = STAT_FONT.render("Score: " + str(scor), True, (255, 255, 255))
    fereastra.blit(text, (WIDTH - 10 - text.get_width(), 10))
    text = STAT_FONT.render("Gen: " + str(generatie), True, (255, 255, 255))
    fereastra.blit(text, (10, 10))
    text = STAT_FONT.render("Alive: " + str(perisoare_vii), True, (255, 255, 255))
    fereastra.blit(text, (10, 50))
    pygame.display.update()


# functia de fitness ( folosita pentru a deduce care perisoara s-a descurcat cel mai bine, perisoarele alese vor fi
# folosite mai apoi la crearea unei noi generatii de perisoare... )
def eval_genomes(genomes, config):
    # noinspection PyGlobalUndefined
    global GEN, ALIVE
    GEN += 1
    lista_retele_neuronale = []
    lista_genomi = []
    lista_perisoare = []
    # luăm fiecare genom, îi atribuim o rețea neuronală și o Perișoară, genomului îi setăm o valoare fitness de început
    # de 0
    for _, genom_curent in genomes:
        retea_neuronala = neat.nn.FeedForwardNetwork.create(genom_curent, config)
        lista_retele_neuronale.append(retea_neuronala)
        lista_perisoare.append(Perisoara(230, 350))
        genom_curent.fitness = 0
        lista_genomi.append(genom_curent)
    lista_sabii = [Sabie(600)]
    # generăm o fereastră cu dimensiunea WIDTH și HEIGHT ( setate în Utils.py )
    fereastra_joc = pygame.display.set_mode((WIDTH, HEIGHT))
    # folosit pentru a seta numărul de cadre pe secundă
    ceas = pygame.time.Clock()
    # scorul de început al populației curente
    scor_populatie = 0
    while True:
        # 30 FPS
        ceas.tick(30)
        # dacă utilizatorul apasă pe X ieșim din joc
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        index_sabie = 0
        if len(lista_perisoare) > 0:
            if len(lista_sabii) > 1:
                if lista_perisoare[0].pozitie_x > lista_sabii[0].pozitie_x + lista_sabii[0].SABIE_SUS.get_width():
                    index_sabie = 1
        else:
            break
        for index_perisoara, perisoara in enumerate(lista_perisoare):
            perisoara.move()
            # de fiecare dată când mișcăm perișoara valoarea fitness a acesteia va crește
            lista_genomi[index_perisoara].fitness += 0.1
            # ca și informații pentru Layer-ul de INPUT îi vom trimite 3 inputuri, poziția y a perișoarei, distanța
            # dintre perișoară și sabia de sus și distanța dintre perișoară și sabia de jos
            valoare_layer_output = lista_retele_neuronale[index_perisoara].activate(
                (perisoara.pozitie_y, abs(perisoara.pozitie_y - lista_sabii[index_sabie].inaltime),
                 abs(perisoara.pozitie_y - lista_sabii[index_sabie].pozitie_sabie_jos)))
            # dacă valoara returnată de către layer-ul de OUTPUT este mai mică de 0.5 ( după aplicarea funcției de
            # activare ) perișoara va sări!
            if valoare_layer_output[0] > 0.5:
                perisoara.jump()
        a_trecut_de_sabie = False
        lista_perisoare_pentru_sters = []
        for sabie in lista_sabii:
            for index_perisoara, perisoara in enumerate(lista_perisoare):
                # dacă perișoara s-a lovit de una dintre săbii o vom scoate din cele 3 liste
                if sabie.collide(perisoara):
                    lista_genomi[index_perisoara].fitness -= 1
                    lista_perisoare.pop(index_perisoara)
                    lista_retele_neuronale.pop(index_perisoara)
                    lista_genomi.pop(index_perisoara)
                if not sabie.passed and sabie.pozitie_x < perisoara.pozitie_x:
                    sabie.passed = True
                    a_trecut_de_sabie = True
            if sabie.pozitie_x + sabie.SABIE_SUS.get_width() < 0:
                lista_perisoare_pentru_sters.append(sabie)
            sabie.move()
        # dacă perișoara trece cu succes de săbii vom crește fitness-ul și scorul
        if a_trecut_de_sabie:
            scor_populatie += 1
            # incurajez genomes sa se duca prin gap astfel capatand mai mult fitness
            for genom_curent in lista_genomi:
                genom_curent.fitness += 1
            lista_sabii.append(Sabie(600))
        for perisoara_de_sters in lista_perisoare_pentru_sters:
            lista_sabii.remove(perisoara_de_sters)
        for index_perisoara, perisoara in enumerate(lista_perisoare):
            # unii genomes "sareau" incontinuu asa ca am facut sa moara cand ajunge si sus
            if perisoara.pozitie_y + perisoara.imagine_perisoara.get_height() >= 730 or perisoara.pozitie_y < 0:
                lista_perisoare.pop(index_perisoara)
                lista_retele_neuronale.pop(index_perisoara)
                lista_genomi.pop(index_perisoara)
        draw_window(fereastra_joc, lista_perisoare, lista_sabii, scor_populatie, GEN, len(lista_perisoare))


# noinspection PyShadowingNames
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)
    populatia_actuala = neat.Population(config)
    populatia_actuala.run(eval_genomes, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)
