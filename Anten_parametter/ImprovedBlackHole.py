"""
Authors:
"""

import math, random
import numpy as np

import Antenna


class Star:

    def __init__(self, location):
        self.location = location
        self.get_fitval()

    def get_fitval(self):
        antenna=Antenna.Anten(self.location)
        S11= antenna.run()
        self.fitval = S11
        if (np.all(np.less_equal(S11,-12)) or np.any(np.less_equal(S11,-20))):
            save_value=str(self.location)
            file_save = open("C:\DATA\Master\Python_Code\ImproveBlackHoleCodeForAntenna\Anten_parametter\Value_S11.txt", "a")
            # Ghi data vao cuoi file
            Value_fitval="\n Value_fitval " + str(S11) + "\n---------------------------------------------------------\n"
            file_save.write(save_value)
            file_save.write(Value_fitval)
            file_save.close()
    def update_location(self, best_star):                                                                        
        for i in range(len(self.location)):
            Random = random.random()
            # self.location[i] = self.location[i] + Random * (best_star.location[i] - self.location[i])
            self.location[i]=round((self.location[i] + Random * (best_star.location[i] - self.location[i])),3)

        self.get_fitval()
        
    def is_absorbed(self, R, best_star):
        distance = self.fitval
        for i in range(len(distance)):
            if (distance[i] > R[i]):
                return True
        return False

class ImprovedBlackHole:

    def __init__(self, num_stars, min_values_location, max_values_location, max_iter):
        self.num_stars = num_stars
        self.min_values_location = min_values_location
        self.max_values_location = max_values_location
        self.max_iter = max_iter

    def generate_initial(self):
        self.stars = []
        for i in range(self.num_stars):
            location = []
            for j in range(len(self.min_values_location)):
                R = random.random()
                change=float(self.min_values_location[j] + R * (self.max_values_location[j] - self.min_values_location[j]))
                if(j==2):
                    self.max_values_location[len(self.min_values_location) - 1]=change
                round_change=round(change,3)
                location.append(round_change)
            self.stars.append(Star(location))
    def get_best_star(self):
        best_star = self.stars[0]
        for i in range(1, len(self.stars)):
            if np.all(np.less_equal(self.stars[i].fitval,best_star.fitval)):
                best_star = self.stars[i]
            elif(np.all(np.less_equal(self.stars[i].fitval,-15)) and (self.count==1)):
                best_star = self.stars[i]
                self.count=0
                print("All less than -10")
        return best_star

    def move_each_star(self, best_star):
        for star in self.stars:
            star.update_location(best_star)

            if (np.all(np.less_equal(star.fitval,best_star.fitval))):
                best_star = star
            elif(np.all(np.less_equal(star.fitval,-15)) and (self.count==1)):
                best_star = star
                self.count=0
                print("All less than -15")
        return best_star

    def calculate_radius_event_horizon(self):
        all_stars_fitval =[0,0,0]
        for i in range(len(self.stars)):
            all_stars_fitval =np.add(all_stars_fitval,self.stars[i].fitval)
        R = np.divide(all_stars_fitval,len(self.stars))
        return R

    def get_evolution_rate(self, iter):
        if (round(iter / self.max_iter, 1) * 10) % 2 == 0:
            return 0.5
        return 0.5

    def crossover(self):
        # get two random stars
        mid = (len(self.stars) - 1) // 2
        a = random.randint(0, mid)
        b = random.randint(mid + 1, len(self.stars) - 1)

        star1 = self.stars[a]
        star2 = self.stars[b]

        # split points
        s1 = random.randint(0, len(self.min_values_location) - 2)
        s2 = random.randint(0, len(self.min_values_location) - 2)

        if s1 > s2:
            s1, s2 = s2, s1

        # do crossover
        for i in range(s1, s2 + 1):
            star1.location[i], star2.location[i] = star2.location[i], star1.location[i]
            if(i==2):
                star1.location[len(self.min_values_location) - 1], star2.location[len(self.min_values_location) - 1] \
                    = star2.location[len(self.min_values_location) - 1], star1.location[len(self.min_values_location) - 1]
        child1=Star(star1.location)
        child2=Star(star2.location)
        # return star with higher fitness value
        return child1 if child1.fitval > child2.fitval else child2

    def generate_random_star(self):
        location = []
        for j in range(len(self.min_values_location)):
            Rand = random.random()
            change_random_star=float(self.min_values_location[j] + Rand * (self.max_values_location[j] - self.min_values_location[j]))
            if(j==2):
                    self.max_values_location[len(self.min_values_location) - 1]=change_random_star
            round_random_star = round(change_random_star,3)
            location.append(round_random_star)
        new_star = Star(location)
        return new_star

    def absorb_and_update(self, R, E, best_star):
        for star in self.stars:

            # if the star is in event horizon's radius
            if star.is_absorbed(R, best_star):
                new_star = None

                # improvement: there's a chance to crossover
                if random.random() <= E:
                    # crossover
                    new_star = self.crossover()
                else:
                    # generate new random star
                    new_star = self.generate_random_star()

                star = new_star

            if (np.all(np.less_equal(star.fitval,best_star.fitval))):
                best_star = star
            elif(np.all(np.less_equal(star.fitval,-15)) and (self.count==1)):
                best_star = star
                self.count=0
                print("All less than -10")
        return best_star

    def run(self):
        print("Run IBH")

        self.generate_initial()
        self.count=1

        best_star_value = self.get_best_star()
        print("best_star0",best_star_value.location)
        print("best_star0",best_star_value.fitval)
        for i in range(self.max_iter):
            best_star1 = self.move_each_star(best_star_value)

            R = self.calculate_radius_event_horizon()
            evolution_rate = self.get_evolution_rate(i + 1)

            # Inner Loop 2
            best_star2 = self.absorb_and_update(R, evolution_rate, best_star1)
            best_star_value = best_star2
            print("best_star + "+str(i)+" "+str(best_star_value.location))
            print("best_value + "+str(i)+" "+ str(best_star_value.fitval))
        return best_star_value


# example uses 2 features (location) [Two Dimensional-Space example]
# the space's dimension is defined by the length of min_values_loc and max_values_loc array


# Result
# print("Improved Black Hole Algorithm: Maximum Optimization")
# print("Max Location: %s" % (max_values_loc))
# print("Best Star Location: %s" % (best_star.location))
# print("Best Star Fitness Value: %.2f" % (best_star.get_fitval()))

# Error
# error = [(max_values_loc[i] - best_star.location[i]) for i in range(len(best_star.location))]
# print("Error Distance per Feature: %s" % (error))