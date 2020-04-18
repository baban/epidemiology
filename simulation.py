# -*- coding: utf-8 -*-

b = 2.5/14 # 感染率: 一人の人間が感染させる人数。2週間で2.5人で仮定
g = 1.0/14 # 2週間すると感染率を失う。それまでに一定の割合で抗体を得る（簡単のため

# 無免疫者
def suspectiable_delta():
  return b * suspectiable_rate * infected_rate

# 発症中の人
def infected_delta():
  return b * suspectiable_rate * infected_rate - g * infected_rate

# 回復者
def recoverd_delta():
  return g * infected_rate

print "start..."

# 日本の人口
population = 1.2*100000000
# 感染者の初期値
inflected_first = 100.0

# 国内に発生したウィルス所持者の初期値
infected_rate = inflected_first/population
# 無感染者の割合
suspectiable_rate = 1.0 - infected_rate
# 回復者
recovered_rate = 0.0

width = 30
suspectiable_list = [0] * width
infected_list = [0] * width
recovered_list = [0] * width
for i in list(range(width)):
    suspectiable_list[i] = suspectiable_delta()
    recovered_list[i] = recoverd_delta()
    infected_list[i] = suspectiable_list[i] - recovered_list[i]
    print "day:" + str(i+1)
    print "新規感染者:" + str(suspectiable_list[i]*population)
    print "抗体を得た人:" + str(recovered_list[i]*population)
    print "追加の感染者数:" + str(infected_list[i]*population)
    suspectiable_rate += suspectiable_list[i]
    infected_rate += infected_list[i]
    recovered_rate += recovered_list[i]
