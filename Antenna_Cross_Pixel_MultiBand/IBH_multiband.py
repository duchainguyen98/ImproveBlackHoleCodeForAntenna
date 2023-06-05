"""
Authors:
"""
"Thuật toán BH với số pixel của Antenna là ngẫu nhiên"
import math, random
import numpy as np

import Antenna_cross_pixel_multiband as Antenna

class Star:

    def __init__(self, location):
        self.location = location
        self.get_fitval()

    def get_fitval(self):
        antenna=Antenna.Anten(self.location)
        S11= antenna.run()
        self.fitval = S11
        if (np.any(np.less_equal(S11,-15)) or np.all(np.less_equal(S11,-10))):
            save_value=str(self.location)
            file_save = open("C:\DATA\Master\Python_Code\ImproveBlackHoleCodeForAntenna\Antenna_Cross_Pixel_MultiBand\Value_S11.txt", "a")
            # Ghi data vao cuoi file
            Value_fitval="\n Value_fitval " + str(S11) + "\n---------------------------------------------------------\n"
            file_save.write(save_value)
            file_save.write(Value_fitval)
            file_save.close()
        # S11=np.random.randint (1, 10)
        # return S11
    def is_absorbed(self, R):
        distance = self.fitval
        for i in range(len(distance)):
            if (distance[i] > R[i]):
                return True
        return False


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
        best_star = self.stars[0]
        for i in range(1, len(self.stars)):
            if np.all(np.less_equal(self.stars[i].fitval,best_star.fitval)):
                best_star = self.stars[i]
        return best_star
    #Tính toán bán kính chân trời sự kiện (Điều kiện giữ hay loại bỏ cá thể)
    def calculate_radius_event_horizon(self):
        all_stars_fitval = [0,0,0]
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
        new_star_location=star.location
        for i in range(number_index_mutation):
            new_star_location[cut_pointx[i],cut_pointy[i]]=1-new_star_location[cut_pointx[i],cut_pointy[i]]
        # return star with higher fitness value
        new_star=Star(new_star_location)
        return new_star
    
    #Thực hiện lai ghép  các cá thể ngôi sao
    def crossover(self):
        # get two random stars
        mid = (len(self.stars_not_is_absorbed) - 1) // 2
        a = np.random.randint(0, mid)
        b = np.random.randint(mid + 1, len(self.stars_not_is_absorbed) - 1)

        star1 = self.stars_not_is_absorbed[a]
        star2 = self.stars_not_is_absorbed[b]

        # # split points
        # cut_pointx = np.random.randint(1, self.pixel_max_x-2)
        # cut_pointy = np.random.randint(1, self.pixel_max_y-2)
        # star1_cut_point = star1.location[:cut_pointx,:cut_pointy]
        # star2_cut_point = star2.location[:cut_pointx,:cut_pointy]
        # # do crossover
        # child1_location = star2.location
        # child1_location[:cut_pointx,:cut_pointy]=star1_cut_point
        # child2_location= star1.location
        # child2_location[:cut_pointx,:cut_pointy]=star2_cut_point
        child1_boolean=np.logical_and(star1.location, star2.location)
        child2_boolean=np.logical_or(star1.location, star2.location)

        child1_location=child1_boolean.astype(int)
        child2_location=child2_boolean.astype(int)

        child1=Star(child1_location)
        child2=Star(child2_location)
        # return star with higher fitness value
        return child1 if child2.fitval > child1.fitval else child2
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
                star = new_star
            else:
                new_star = None
                new_star=self.mutation(star)
                star = new_star
            if (np.all(np.less_equal(star.fitval,best_star.fitval))):
                best_star = star
            elif(np.all(np.less_equal(star.fitval,-10)) and (self.count==1)):
                best_star = star
                self.count=0
                print("All less than -10")
        return best_star

    def run(self):
        print("Run IBH")
        self.generate_initial()
        best_star_value = self.get_best_star()
        self.count=1
        print("Run loop")
        for i in range(self.max_iter):
            R = self.calculate_radius_event_horizon()
            evolution_rate = self.get_evolution_rate(i + 1)
            
            # Inner Loop Thực hiện so sánh với chân trời sự kiện và cập nhật các ngôi sao mới
            best_star = self.move_each_star(R, evolution_rate, best_star_value)
            best_star_value = best_star
            print("best_star + "+str(i)+" "+str(best_star_value.location))
            print("best_value + "+str(i)+" "+ str(best_star_value.fitval))

            file_save = open("C:\DATA\Master\Python_Code\ImproveBlackHoleCodeForAntenna\Antenna_Cross_Pixel_MultiBand\IBH_value.txt", "a")
            # Ghi data vao cuoi file
            Value_fitval="\n Value_fitval " + str(best_star_value.fitval) + "\n---------------------------------------------------------\n"
            file_save.write(str(best_star_value.location))
            file_save.write(Value_fitval)
            file_save.close()
        best_last_star_location = Star(best_star_value.location)
        best_last_star=Antenna.Anten(best_last_star_location)
        best_last_star.run_antenna()

        return best_star_value
