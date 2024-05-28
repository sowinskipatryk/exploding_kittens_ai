import neat
import os
import pickle

from game import Game


def eval_genomes(genomes, config):
    genomes_num = len(genomes)
    genomes_per_team = genomes_num // 2
    for i in range(genomes_per_team):
        _, team1_genome = genomes[i]
        print(round(i / genomes_per_team * 100), end=" ")
        team1_genome.fitness = 0
        for j in range(genomes_per_team, genomes_num):
            _, team2_genome = genomes[j]
            team2_genome.fitness = 0 if team2_genome.fitness is None else team2_genome.fitness

            team1_net = neat.nn.FeedForwardNetwork.create(team1_genome, config)
            team2_net = neat.nn.FeedForwardNetwork.create(team2_genome, config)

            game = Game(players_num, net1=team1_net, net2=team2_net)

            game_score = game.play_game()

            if game_score >= 0:
                team1_genome.fitness += 100
                team2_genome.fitness -= 100
            else:
                team1_genome.fitness -= 100
                team2_genome.fitness += 100

            if team1_genome.fitness > best_team1_fitness:
                best_team1_genome = team1_genome
                best_team1_fitness = team1_genome.fitness
            if team2_genome.fitness > best_team2_fitness:
                best_team2_genome = team2_genome
                best_team2_fitness = team2_genome.fitness

    save_best_genome(best_genome, 'best_genome.pkl')


def save_best_genome(best_genome, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(best_genome, file)


def run_neat():
    cnf = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                      neat.DefaultSpeciesSet, neat.DefaultStagnation,
                      config_path)

    # population = neat.Checkpointer.restore_checkpoint('')
    population = neat.Population(cnf)

    population.add_reporter(neat.StdOutReporter(show_species_detail=True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(generation_interval=1))

    population.run(eval_genomes, num_generations)


players_num = 5
num_generations = 100
config_path = os.path.join(os.path.dirname(__file__), 'config.txt')
