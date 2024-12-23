from network.manager import train_network

train_network(num_players=5,
              num_generations=20,
              save_file='best_genome.pkl',
              checkpoint_file=None)
