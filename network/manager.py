import neat
import os
import pickle

from network.adapter import NetworkAdapter
from game_logic.players.neural_player import NeuralPlayer
from game_logic.game import Game

CONFIG_FILENAME = "neat_config.txt"
GENOME_FILENAME = 'best_genome'
GENOME_EXTENSION = '.pkl'
NUM_GENERATIONS = 20


def load_network(players_num):
    genome_fullname = GENOME_FILENAME + str(players_num) + GENOME_EXTENSION
    if os.path.exists(genome_fullname):
        with open(genome_fullname, "rb") as f:
            genome = pickle.load(f)

        config_filename = CONFIG_FILENAME
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             config_filename)

        net = neat.nn.FeedForwardNetwork.create(genome, config)
        return net
    else:
        raise FileNotFoundError('The genome file was not found! You need to learn network first or pick other player type than Neural')


def teach_network(players_num):
    def eval_genomes(genomes, config):
        for i in range(0, len(genomes), players_num):
            networks = []
            for j in range(players_num):
                genome_id, genome = genomes[i + j]
                networks.append(neat.nn.FeedForwardNetwork.create(genome, config))

            players = [NeuralPlayer(idx, network=network, adapter=NetworkAdapter(players_num)) for idx, network in enumerate(networks)]
            game = Game(players)
            stats = game.play()

            for j in range(4):
                genome_id, genome = genomes[i + j]
                genome.fitness = stats['score'][j]
                print(f"Game {i // players_num}, Player {j}, Genome {genome_id}, Fitness: {genome.fitness}")

    def run_neat():
        config_path = os.path.join(os.path.dirname(__file__), CONFIG_FILENAME)
        cnf = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                          neat.DefaultSpeciesSet, neat.DefaultStagnation,
                          config_path)

        # population = neat.Checkpointer.restore_checkpoint('neat-checkpoint-3')
        population = neat.Population(cnf)

        population.add_reporter(neat.StdOutReporter(show_species_detail=True))
        stats = neat.StatisticsReporter()
        population.add_reporter(stats)
        population.add_reporter(neat.Checkpointer(generation_interval=1))

        winner = population.run(eval_genomes, NUM_GENERATIONS)
        save_network(winner, players_num)

    run_neat()


def save_network(genome, players_num):
    genome_fullname = GENOME_FILENAME + str(players_num) + GENOME_EXTENSION
    with open(genome_fullname, 'wb') as file:
        pickle.dump(genome, file)
