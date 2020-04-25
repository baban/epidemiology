# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# 1日をm等分して細かいシミュレーションをする
m = 7
# 感染率bと回復率gは以下のurlから取得
# https://www.fttsus.jp/covinfo/numerical-simulation/
b = 0.488 / m # 感染率: 一人の人間が感染させる人数。
g = 0.0455 / m
term = 365 # 期間。1年間
width = term * m # 計算期間

# 日本の人口
population = 126100000
# 感染者の初期値
inflected_first = 10000.0

suspectiable_delta_list = [0] * width
infected_delta_list = [0] * width
recovered_delta_list = [0] * width

suspectiable_list = [0] * width
infected_list = [0] * width
recovered_list = [0] * width

# 感染後、発症して感染力を持つまでの期間
tau = 6

# 無免疫者
def suspectiable_delta(t):
  i = t - tau
  if i < 0:
    i = 0
  return b * suspectiable_list[i] * infected_list[i]

# 発症中の人
def infected_delta(t):
  return suspectiable_delta(t) - recoverd_delta(t)

# 回復者
def recoverd_delta(t):
  return g * infected_rate

print("start...")

# 国内に発生したウィルス所持者の初期値
infected_rate = inflected_first/population
# 無感染者の割合
suspectiable_rate = 1.0 - infected_rate
# 回復者
recovered_rate = 0.0

for i in list(range(width)):
  suspectiable_delta_list[i] = suspectiable_delta(i)
  recovered_delta_list[i] = recoverd_delta(i)
  infected_delta_list[i] = suspectiable_delta_list[i] - recovered_delta_list[i]
  # print("day:" + str(i+1))
  # print("新規感染者:" + str(suspectiable_delta_list[i] * population))
  # print("抗体を得た人:" + str(recovered_delta_list[i] * population))
  # print("追加の感染者数:" + str(infected_delta_list[i] * population))
  suspectiable_rate -= suspectiable_delta_list[i]
  infected_rate += infected_delta_list[i]
  recovered_rate += recovered_delta_list[i]
  suspectiable_list[i] = suspectiable_rate
  infected_list[i] = infected_rate
  recovered_list[i] = recovered_rate

# 日にちをn分割したものを元に戻す
plot_suspectiable_list = [0] * term
for i in list(range(width)):
  plot_suspectiable_list[int(i/m)] += int(suspectiable_delta_list[i]*population)

for i in list(range(term)):
  print("day:" + str(i+1))
  print("新規感染者:" + str(plot_suspectiable_list[i]))

print("caliculated...")

plt.title('daily new infected peple')
plt.bar(range(term), plot_suspectiable_list)
plt.show()
#plt.savefig('figure.png')
