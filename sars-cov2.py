# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

Nan = np.nan

# 1日をm等分して細かいシミュレーションをする
m = 1
# 感染率bと回復率gは以下のurlから取得
# https://www.fttsus.jp/covinfo/numerical-simulation/
b = 0.488 / m # 感染率: 一人の人間が感染させる人数。
g = 0.0455 / m
term = 365 # 期間。1年間
width = term * m # 計算期間

# 日本の人口
population = 126100000.0
# 感染者の初期値
inflected_first = 36.0

# 14日分の前日の感染者のデータを持っていて、それを利用する
start = 14

# 感染後、発症して感染力を持つまでの期間
tau = 14 * m

first_inflected_data = [219, 228, 242, 260, 279, 315, 347, 403, 437, 480, 508, 567, 620, 676]
first_inflected_delta_list = [19,  9, 14, 18, 19, 36, 32, 56, 34, 43, 28, 59, 53, 56]
first_suspectiable_delta_list = [19,  9, 14, 18, 19, 36, 32, 56, 34, 43, 28, 59, 53, 56]

infected_list = first_inflected_data + [0] * (width - start)
suspectiable_list = list(map(lambda x: population - x, infected_list))
recovered_list = [0] * width

infected_delta_list = first_inflected_delta_list + [0] * (width - start)
suspectiable_delta_list = list(map(lambda x: -1 * x, infected_delta_list))
recovered_delta_list = [0] * width

# 無免疫者
def suspectiable_delta(t, diff):
  i = t - diff
  return b * suspectiable_list[i] * infected_list[i] / population

# 発症中の人
def infected_delta(t):
  return suspectiable_delta(t, tau) - recoverd_delta(t)

# 回復者
def recoverd_delta(t):
  return g * infected_list[t]

print("start...")

# 国内に発生したウィルス所持者の初期値
infected_count = infected_list[start]
# 無感染者の割合
suspectiable_count = population - infected_count
# 回復者
recovered_count = 36.0

for i in list(range(start, width)):
  infected_count = infected_list[i - 1]
  suspectiable_count = suspectiable_list[i - 1]
  recovered_count = recovered_list[i - 1]
  infected_delta_list[i] = infected_delta(i - 1)
  suspectiable_delta_list[i] = suspectiable_delta(i - 1, 0)
  recovered_delta_list[i] = recoverd_delta(i - 1)
  print("day:" + str(i+1))
  print("新規感染者:" + str(suspectiable_delta_list[i]))
  print("抗体を得た人:" + str(recovered_delta_list[i]))
  print("追加の感染者数:" + str(infected_delta_list[i]))
  infected_count += infected_delta_list[i]
  suspectiable_count -= suspectiable_delta_list[i]
  recovered_count += recovered_delta_list[i]
  infected_list[i] = infected_count
  suspectiable_list[i] = suspectiable_count
  recovered_list[i] = recovered_count

# 日にちをn分割したものを元に戻す
plot_list = [0] * term
for i in list(range(width)):
  plot_list[int(i/m)] += int(infected_list[i])

for i in list(range(term)):
  print("day:" + str(i+1))
  print("感染者:" + str(plot_list[i]))

print("caliculated...")

#print("死亡者: " + str(int(recovered_count * 0.36 / 100)))

plt.title('infected peple')
plt.bar(range(term), plot_list)
plt.show()
#plt.savefig('figure.png')
