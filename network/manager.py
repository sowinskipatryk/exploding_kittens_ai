import neat
import os
import pickle

from game_logic.players.neural_player import NeuralPlayer
from game_logic.game import Game


CONFIG_FILENAME = "neat_config.txt"


def load_network(genome_filename):
    if os.path.exists(genome_filename):
        with open(genome_filename, "rb") as f:
            genome = pickle.load(f)

        config_filename = os.path.join(os.path.dirname(__file__), CONFIG_FILENAME)
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             config_filename)

        net = neat.nn.FeedForwardNetwork.create(genome, config)
        return net
    else:
        raise FileNotFoundError('The genome file was not found! You need to learn network first or pick other player type than Neural')


def save_network(genome, save_file):
    with open(save_file, 'wb') as file:
        pickle.dump(genome, file)


def train_network(num_players, num_generations, save_file, checkpoint_file):
    def evaluation_function(genomes, config):
        for i in range(0, len(genomes), num_players):
            players = []
            for j in range(num_players):
                genome_id, genome = genomes[i + j]
                network = neat.nn.FeedForwardNetwork.create(genome, config)
                player = NeuralPlayer(f"Neural {j+1}", network=network)
                players.append(player)

            game = Game(players)
            stats = game.play()

            for j in range(num_players):
                genome_id, genome = genomes[i + j]
                if genome.fitness is None:
                    genome.fitness = 0

                genome.fitness += stats['players'][players[j].name]['turns_survived']
                if players[j].name is stats['winner']:
                    genome.fitness += 100
                print(f"Game {(i // num_players) + 1}, {players[j].name}, Genome {genome_id}, Fitness: {genome.fitness}")

    def run_neat():
        config_path = os.path.join(os.path.dirname(__file__), CONFIG_FILENAME)
        cnf = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                          neat.DefaultSpeciesSet, neat.DefaultStagnation,
                          config_path)

        if checkpoint_file:
            population = neat.Checkpointer.restore_checkpoint(checkpoint_file)
        else:
            population = neat.Population(cnf)

        population.add_reporter(neat.StdOutReporter(show_species_detail=True))
        stats = neat.StatisticsReporter()
        population.add_reporter(stats)
        population.add_reporter(neat.Checkpointer(generation_interval=1))

        winner = population.run(evaluation_function, num_generations)
        save_network(winner, save_file)

    run_neat()
