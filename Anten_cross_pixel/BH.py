"""
Authors:
"""
"Thuật toán BH với số pixel của Antenna là ngẫu nhiên"
import math, random
import numpy as np

import Anten_cross_pixel as Antenna

class Star:

    def __init__(self, location):
        self.location = location
        self.fitval = self.get_fitval()

    def get_fitval(self):
        fitval_sum = 0
        antenna=Antenna.Anten(self.location)
        S11= antenna.run()
        # S=[S11[0]]
        return S11[0]
        # S11=np.random.randint (1, 10)
        # return S11
    def is_absorbed(self, R):
        distance = self.fitval
        return True if (distance > R) else False


class ImprovedBlackHole:
    #Hàm khởi tạo lớp
    def __init__(self, num_stars, pixel_max_x, pixel_max_y, max_iter):
        self.num_stars = num_stars
        self.pixel_max_x = pixel_max_x
        self.pixel_max_y = pixel_max_y
        self.max_iter = max_iter
    #Khoi tao quan the ban dau
    def generate_initial(self):
        self.stars = []
        for i in range(self.num_stars):
            location = np.random.randint (2, size = (self.pixel_max_x,self.pixel_max_y))
            self.stars.append(Star(location))
    #Tim giá trị tốt nhất 
    def get_best_star(self):
        for i in range(1, len(self.stars)):
            if self.stars[i].fitval < self.best_star.fitval:
                self.best_star = self.stars[i]
        return self.best_star
    #Tính toán bán kính chân trời sự kiện (Điều kiện giữ hay loại bỏ cá thể)
    def calculate_radius_event_horizon(self):
        all_stars_fitval = 0
        for i in range(len(self.stars)):
            all_stars_fitval =np.add(all_stars_fitval,self.stars[i].fitval)
        R = np.divide(all_stars_fitval,len(self.stars))
        return R
    #Tỉ lệ thực hiện việc đột biến ngẫu nhiên
    def get_evolution_rate(self, iter):
        # if (round(iter / self.max_iter, 1) * 10) % 2 == 0:
        #     return 0.75
        return 0.5
    #Thực hiện  đột biến các cá thể ngôi sao
    def mutation(self,star):

        number_index_mutation= np.random.randint(1, self.pixel_max_x//2)

        # split points
        cut_pointx = np.random.randint(self.pixel_max_x-1, size=(number_index_mutation))
        cut_pointy = np.random.randint(self.pixel_max_y-1, size=(number_index_mutation))
        new_star=star
        for i in range(number_index_mutation):
            new_star.location[cut_pointx[i],cut_pointy[i]]=1-new_star.location[cut_pointx[i],cut_pointy[i]]
        # return star with higher fitness value
        return new_star
    
    #Thực hiện lai ghép  các cá thể ngôi sao
    def crossover(self):
        # get two random stars
        mid = (len(self.stars_not_is_absorbed) - 1) // 2
        a = np.random.randint(0, mid)
        b = np.random.randint(mid + 1, len(self.stars_not_is_absorbed) - 1)

        star1 = self.stars_not_is_absorbed[a]
        star2 = self.stars_not_is_absorbed[b]

        # split points
        cut_pointx = np.random.randint(1, self.pixel_max_x-2)
        cut_pointy = np.random.randint(1, self.pixel_max_y-2)
        star1_cut_point = star1.location[:cut_pointx,:cut_pointy]
        star2_cut_point = star2.location[:cut_pointx,:cut_pointy]

        # do crossover
        child1 = star2
        child1.location[:cut_pointx,:cut_pointy]=star1_cut_point
        child2= star1
        child2.location[:cut_pointx,:cut_pointy]=star2_cut_point

        # return star with higher fitness value
        return child1 if child1.fitval > child2.fitval else child2
    #Thực hiện tạo ngôi sao ngẫu nhiên
    def generate_random_star(self):
        location = []
        location = np.random.randint (2, size = (self.pixel_max_x,self.pixel_max_y))
        new_star = Star(location)
        return new_star
    #So sánh và Thực hiện di chuyển các ngôi sao theo một hàm cụ thể
    def move_each_star(self, R, E, best_star):
        self.stars_not_is_absorbed = []
        for star in self.stars:
            if not star.is_absorbed(R):
                self.stars_not_is_absorbed.append(star)

        for star in self.stars:
            # if the star is in event horizon's radius
            if star.is_absorbed(R):
                new_star = None

                # improvement: there's a chance to crossover
                if random.random() <= E and (len(self.stars_not_is_absorbed) >= 4):
                    # crossover
                    new_star = self.crossover()
                else:
                    # generate new random star
                    new_star = self.generate_random_star()
                star.location = new_star.location
                star.fitval = new_star.fitval
            else:
                new_star = None
                new_star=self.mutation(star)
                star.location = new_star.location
                star.fitval = new_star.fitval
        self.get_best_star()
        return self.best_star

    def run(self):
        self.generate_initial()
        self.best_star=self.stars[0]
        self.best_star = self.get_best_star()
        print("Run IBH")
        for i in range(self.max_iter):
            R = self.calculate_radius_event_horizon()
            evolution_rate = self.get_evolution_rate(i + 1)
            # Inner Loop Thực hiện so sánh với chân trời sự kiện và cập nhật các ngôi sao mới
            self.best_star = self.move_each_star(R, evolution_rate, self.best_star)
            print("best_star + "+str(i)+" "+str(self.best_star.location))
            print("best_value + "+str(i)+" "+ str(self.best_star.fitval))
        return self.best_star


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