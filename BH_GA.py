import numpy as np
import matplotlib.pyplot as plt

# Antenna parameters
WIDTH = 10
HEIGHT = 2
NUM_POINTS = 20

# Genetic algorithm parameters
POP_SIZE = 100
GEN_SIZE = 100
MUTATION_RATE = 0.1


def generate_population(population_size):
    return np.random.uniform(low=-1, high=1, size=(population_size, NUM_POINTS * 2))


def fitness(chromosome):
    x = chromosome.reshape((-1, 2))[:, 0]
    y = chromosome.reshape((-1, 2))[:, 1]
    z = np.zeros_like(x)
    for i in range(NUM_POINTS):
        r = np.sqrt((x - x[i])**2 + (y - y[i])**2)
        z += np.exp(-r**2)
    return np.max(z)


def blackhole_selection(population, fitness):
    global fitnesses 
    fitnesses = np.array([fitness(chromosome) for chromosome in population])
    sorted_indices = np.argsort(fitnesses)[::-1]
    population = population[sorted_indices]
    fitnesses = fitnesses[sorted_indices]
    num_holes = int(POP_SIZE / 2)
    holes = np.random.choice(np.arange(POP_SIZE), size=num_holes, replace=False)
    for hole in holes:
        # Get the blackhole
        blackhole = population[hole]

        # Calculate the distance of all particles to the blackhole
        distances = np.linalg.norm(population - blackhole, axis=1)

        # Sort particles by distance
        sorted_indices = np.argsort(distances)

        # Move particles towards the blackhole
        for i in range(1, POP_SIZE):
            # Calculate the new position of the particle
            old_position = population[sorted_indices[i]]
            new_position = old_position + np.random.uniform() * (blackhole - old_position)

            # If the new position is outside the search space, generate a random position
            if not np.all((-1 <= new_position) & (new_position <= 1)):
                new_position = np.random.uniform(low=-1, high=1, size=old_position.shape)

            # Update the population
            population[sorted_indices[i]] = new_position

    return population


def genetic_algorithm(population, fitness, num_generations, mutation_rate):
    global fitnesses
    for generation in range(num_generations):
        offspring = np.zeros_like(population)
        for i in range(POP_SIZE):
            # selection
            parent1 = np.random.choice(np.arange(POP_SIZE), p=fitnesses / np.sum(fitnesses))
            parent2 = np.random.choice(np.arange(POP_SIZE), p=fitnesses / np.sum(fitnesses))
            offspring[i] = (population[parent1] + population[parent2]) / 2
            if np.random.uniform() < mutation_rate:
                offspring[i] += np.random.normal(scale=0.1, size=offspring[i].shape)

        population = np.vstack((population, offspring))
        population = population[:POP_SIZE]

    fitnesses = np.array([fitness(chromosome) for chromosome in population])
    sorted_indices = np.argsort(fitnesses)[::-1]
    population = population[sorted_indices]
    return population[0]


# Generate initial population
population = generate_population(POP_SIZE) 

# Run blackhole selection and genetic algorithm
best_chromosome = None
best_fitness = -1
for i in range(GEN_SIZE):
    population = blackhole_selection(population, fitness)
    chromosome = genetic_algorithm(population, fitness, 1, MUTATION_RATE)
    chromosome_fitness = fitness
# Convert chromosome to coordinates
x = best_chromosome[::2]
y = best_chromosome[1::2]

# Plot antenna
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y, '-o', markersize=8, linewidth=2)
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_aspect('equal', adjustable='box')
ax.set_title(f'Fitness: {best_fitness:.3f}')
plt.show()
