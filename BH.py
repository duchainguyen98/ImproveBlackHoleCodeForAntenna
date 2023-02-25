import random
import math
import numpy as np

# Định nghĩa hàm mục tiêu f(x)
def f(x):
    # Tính toán tổng lực cảm nhận được bởi anten
    # Dựa trên các tọa độ, độ rộng và độ cao của pixel
    # Trong trường hợp này, ta sẽ trả về giá trị ngẫu nhiên
    # Để làm ví dụ
    return sum([random.random() for i in range(len(x))])

# Khởi tạo các tham số
n = 10
alpha = 0.1
max_iter = 100

# Khởi tạo các giá trị ngẫu nhiên cho tọa độ, độ rộng và độ cao của pixel
x = np.random.randint(0, n, size=n)
y = np.random.randint(0, n, size=n)
w = [random.random() for i in range(n)]
h = [random.random() for i in range(n)]

print(x)

# Tính toán giá trị hàm mục tiêu cho bộ giá trị pixel hiện tại
best_x = x.copy()
best_y = y.copy()
best_w = w.copy()
best_h = h.copy()
best_f = f([x[i] + w[i] / 2 for i in range(n)] + [y[i] + h[i] / 2 for i in range(n)])
print("best_x "+str(best_x))

# Lặp lại các bước từ 3 đến 7
for iter in range(3):
    # Khởi tạo một điểm đen ngẫu nhiên trong không gian tìm kiếm
    bh_x = random.random()
    bh_y = random.random()

    # Tính toán khoảng cách của tất cả các pixel đến điểm đen
    distances = [math.sqrt((bh_x - x[i])**2 + (bh_y - y[i])**2) for i in range(n)]
    print("distances "+str(distances ))
    # Sắp xếp các pixel theo khoảng cách tăng dần đến điểm đen
    sorted_indices = sorted(range(n), key=lambda k: distances[k])
    print("sorted_indices "+str(sorted_indices ))

    # Cập nhật giá trị tọa độ của các pixel
    for i in sorted_indices:
        x[i] = x[i] + alpha * (bh_x - x[i])
        y[i] = y[i] + alpha * (bh_y - y[i])

    # Kiểm tra xem giá trị mới có cải thiện hơn giá trị cũ hay không
    new_f = f([x[i] + w[i] / 2 for i in range(n)] + [y[i] + h[i] / 2 for i in range(n)])
    if new_f < best_f:
        best_x = x.copy()
        best_y = y.copy()
        best_w = w.copy()
        best_h = h.copy()
        best_f = new_f

# In ra kết quả tối ưu hoá
print("Best position:", [(best_x[i], best_y[i], best_w[i], best_h[i]) for i in range(n)])
print("Best value:", best_f)